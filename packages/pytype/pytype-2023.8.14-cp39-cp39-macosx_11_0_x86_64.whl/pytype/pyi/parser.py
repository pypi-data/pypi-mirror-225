"""Parse a pyi file using typed_ast."""

import ast as astlib
import dataclasses
import hashlib
import io
import keyword
import re
import sys
import tokenize
from typing import Any, List, Optional, Tuple, Union

from pytype.ast import debug
from pytype.pyi import classdef
from pytype.pyi import conditions
from pytype.pyi import definitions
from pytype.pyi import evaluator
from pytype.pyi import function
from pytype.pyi import modules
from pytype.pyi import types
from pytype.pyi import visitor
from pytype.pytd import pep484
from pytype.pytd import pytd
from pytype.pytd import pytd_utils
from pytype.pytd import visitors
from pytype.pytd.codegen import decorate

# reexport as parser.ParseError
ParseError = types.ParseError

_UNKNOWN_IMPORT = "__unknown_import__"

#------------------------------------------------------
# imports


def _tuple_of_import(alias: astlib.alias) -> Union[str, Tuple[str, str]]:
  """Convert a typedast import into one that add_import expects."""
  if alias.asname is None:
    return alias.name
  return alias.name, alias.asname


def _import_from_module(module: Optional[str], level: int) -> str:
  """Convert a typedast import's 'from' into one that add_import expects."""
  if module is None:
    return {1: "__PACKAGE__", 2: "__PARENT__"}[level]
  prefix = "." * level
  return prefix + module


def _keyword_to_parseable_name(kw):
  return f"__KW_{kw}__"


def _parseable_name_to_real_name(name):
  m = re.fullmatch(r"__KW_(?P<keyword>.+)__", name)
  return m.group("keyword") if m else name


#------------------------------------------------------
# typevars


@dataclasses.dataclass
class _TypeVariable:
  """Internal representation of type variables."""

  name: str
  bound: Optional[str]
  constraints: List[Any]

  @classmethod
  def from_call(cls, node: astlib.Call):
    """Construct a _TypeVar from an ast.Call node."""
    name, *constraints = node.args
    bound = None
    # 'bound' is the only keyword argument we currently use.
    # TODO(rechen): We should enforce the PEP 484 guideline that
    # len(constraints) != 1. However, this guideline is currently violated
    # in typeshed (see https://github.com/python/typeshed/pull/806).
    kws = {x.arg for x in node.keywords}
    extra = kws - {"bound", "covariant", "contravariant"}
    if extra:
      raise ParseError(f"Unrecognized keyword(s): {', '.join(extra)}")
    for kw in node.keywords:
      if kw.arg == "bound":
        bound = kw.value
    return cls(name, bound, constraints)


@dataclasses.dataclass
class _TypeVar(_TypeVariable):
  """Internal representation of TypeVar."""


@dataclasses.dataclass
class _ParamSpec(_TypeVariable):
  """Internal representation of ParamSpec."""


#------------------------------------------------------
# pytd utils

#------------------------------------------------------
# Main tree visitor and generator code


def _attribute_to_name(node: astlib.Attribute) -> astlib.Name:
  """Recursively convert Attributes to Names."""
  val = node.value
  if isinstance(val, astlib.Name):
    prefix = val.id
  elif isinstance(val, astlib.Attribute):
    prefix = _attribute_to_name(val).id
  elif isinstance(val, (pytd.NamedType, pytd.Module)):
    prefix = val.name
  else:
    msg = f"Unexpected attribute access on {val!r} [{type(val)}]"
    raise ParseError(msg)
  return astlib.Name(f"{prefix}.{node.attr}")


class AnnotationVisitor(visitor.BaseVisitor):
  """Converts typed_ast annotations to pytd."""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Exclude defaults because they may contain strings
    # which should not be interpreted as annotations
    self._node_children[self._ast.arguments] = [
        field
        for field in self._ast.arguments._fields
        if field not in ("kw_defaults", "defaults")
    ]

  def show(self, node):
    print(debug.dump(node, astlib, include_attributes=False))

  def convert_late_annotation(self, annotation):
    try:
      # Late annotations may need to be parsed into an AST first
      if annotation.isalpha():
        return self.defs.new_type(annotation)
      a = astlib.parse(annotation)
      # Unwrap the module the parser puts around the source string
      typ = a.body[0].value  # pytype: disable=attribute-error
      return self.visit(typ)
    except ParseError as e:
      # Clear out position information since it is relative to the typecomment
      e.clear_position()
      raise e

  def convert_metadata(self, node):
    ret = MetadataVisitor().visit(node)
    return ret if ret is not None else node

  def visit_Pyval(self, node):
    # Handle a types.Pyval node (converted from a literal constant).
    # We do not handle the mixed case
    #   x: List['int']
    # since we need to not convert subscripts for typing.Literal, i.e.
    #   x: Literal['int']
    # pyi files do not require quoting forward references anyway, so we keep the
    # code simple here and just handle the basic case of a fully quoted type.
    if node.type == "str" and not self.subscripted:
      return self.convert_late_annotation(node.value)

  def visit_Tuple(self, node):
    return tuple(node.elts)

  def visit_List(self, node):
    return list(node.elts)

  def visit_Name(self, node):
    if self.subscripted and (node is self.subscripted[-1]):
      # This is needed because
      #   Foo[X]
      # parses to
      #   Subscript(Name(id = Foo), Name(id = X))
      # so we see visit_Name(Foo) before visit_Subscript(Foo[X]).
      # If Foo resolves to a generic type we want to know if it is being passed
      # params in this context (in which case we simply resolve the type here,
      # and create a new type when we get the param list in visit_Subscript) or
      # if it is just being used as a bare Foo, in which case we need to create
      # the new type Foo[Any] below.
      return self.defs.resolve_type(node.id)
    else:
      return self.defs.new_type(node.id)

  def _convert_getattr(self, node):
    # The protobuf pyi generator outputs getattr(X, 'attr') when 'attr' is a
    # Python keyword.
    if node.func.name != "getattr" or len(node.args) != 2:
      return None
    obj, attr = node.args
    if (not isinstance(obj, pytd.NamedType) or
        not isinstance(attr, types.Pyval) or attr.type != "str"):
      return None
    return pytd.NamedType(f"{obj.name}.{attr.value}")

  def visit_Call(self, node):
    ret = self._convert_getattr(node)
    if ret:
      return ret
    raise ParseError("Constructors and function calls in type annotations "
                     "are not supported.")

  def _get_subscript_params(self, node):
    if sys.version_info >= (3, 9):
      return node.slice
    else:
      return node.slice.value

  def _set_subscript_params(self, node, new_val):
    if sys.version_info >= (3, 9):
      node.slice = new_val
    else:
      node.slice.value = new_val

  def _convert_typing_annotated(self, node):
    typ, *args = self._get_subscript_params(node).elts
    typ = self.visit(typ)
    params = (self.convert_metadata(x) for x in args)
    self._set_subscript_params(node, (typ,) + tuple(params))

  def enter_Subscript(self, node):
    if isinstance(node.value, astlib.Attribute):
      node.value = _attribute_to_name(node.value).id
    if self.defs.matches_type(getattr(node.value, "id", ""),
                              "typing.Annotated"):
      self._convert_typing_annotated(node)
    self.subscripted.append(node.value)

  def visit_Subscript(self, node):
    params = self._get_subscript_params(node)
    if type(params) is not tuple:  # pylint: disable=unidiomatic-typecheck
      params = (params,)
    try:
      return self.defs.new_type(node.value, params)
    except definitions.StringParseError:
      params = tuple(self.convert_late_annotation(p.value)
                     if isinstance(p, types.Pyval) and p.type == "str" else p
                     for p in params)
      return self.defs.new_type(node.value, params)

  def leave_Subscript(self, node):
    self.subscripted.pop()

  def visit_Attribute(self, node):
    annotation = _attribute_to_name(node).id
    return self.defs.new_type(annotation)

  def visit_BinOp(self, node):
    if self.subscripted:
      last = self.subscripted[-1]
      if isinstance(last, astlib.Name):
        last_id = last.id
      elif isinstance(last, str):
        last_id = last
      else:
        last_id = ""
      if self.defs.matches_type(last_id, "typing.Literal"):
        raise ParseError("Expressions are not allowed in typing.Literal.")
    if isinstance(node.op, astlib.BitOr):
      return self.defs.new_type("typing.Union", [node.left, node.right])
    else:
      raise ParseError(f"Unexpected operator {node.op}")

  def visit_BoolOp(self, node):
    if isinstance(node.op, astlib.Or):
      raise ParseError("Deprecated syntax `x or y`; use `Union[x, y]` instead")
    else:
      raise ParseError(f"Unexpected operator {node.op}")


class MetadataVisitor(visitor.BaseVisitor):
  """Converts typing.Annotated metadata."""

  def visit_Call(self, node):
    posargs = tuple(evaluator.literal_eval(x) for x in node.args)
    kwargs = {x.arg: evaluator.literal_eval(x.value) for x in node.keywords}
    return (node.func.id, posargs, kwargs)

  def visit_Dict(self, node):
    return evaluator.literal_eval(node)


def _flatten_splices(body: List[Any]) -> List[Any]:
  """Flatten a list with nested Splices."""
  if not any(isinstance(x, Splice) for x in body):
    return body
  out = []
  for x in body:
    if isinstance(x, Splice):
      # This technically needn't be recursive because of how we build Splices
      # but better not to have the class assume that.
      out.extend(_flatten_splices(x.body))
    else:
      out.append(x)
  return out


class Splice:
  """Splice a list into a node body."""

  def __init__(self, body):
    self.body = _flatten_splices(body)

  def __str__(self):
    return "Splice(\n" + ",\n  ".join([str(x) for x in self.body]) + "\n)"

  def __repr__(self):
    return str(self)


def _is_valid_default(val):
  return (not val or types.is_any(val) or isinstance(val, types.Pyval) or
          val.name == "None")


class _GeneratePytdVisitor(visitor.BaseVisitor):
  """Converts a typed_ast tree to a pytd tree."""

  def __init__(self, src, filename, module_name, options):
    defs = definitions.Definitions(modules.Module(filename, module_name))
    super().__init__(defs=defs, filename=filename)
    self.src_code = src
    self.module_name = module_name
    self.options = options
    self.level = 0
    self.in_function = False  # pyi will not have nested defs
    self.annotation_visitor = AnnotationVisitor(defs=defs, filename=filename)
    self.class_stack = []

  def show(self, node):
    print(debug.dump(node, astlib, include_attributes=True))

  def convert_node(self, node):
    # Converting a node via a visitor will convert the subnodes, but if the
    # argument node itself needs conversion, we need to use the pattern
    #   node = annotation_visitor.visit(node)
    # However, the AnnotationVisitor returns None if it does not trigger on the
    # root node it is passed, so call it via this method instead.
    if isinstance(node, types.Pyval) and node.type != "str":
      raise ParseError(f"Unexpected literal: {node.value!r}")
    ret = self.annotation_visitor.visit(node)
    return ret if ret is not None else node

  def convert_node_annotations(self, node):
    """Transform type annotations to pytd."""
    if getattr(node, "annotation", None):
      node.annotation = self.convert_node(node.annotation)
    elif getattr(node, "type_comment", None):
      node.type_comment = self.annotation_visitor.convert_late_annotation(
          node.type_comment)

  def resolve_name(self, name):
    """Resolve an alias or create a NamedType."""
    return self.defs.type_map.get(name) or pytd.NamedType(name)

  def visit_Module(self, node):
    node.body = _flatten_splices(node.body)
    return self.defs.build_type_decl_unit(node.body)

  def visit_Pass(self, node):
    return self.defs.ELLIPSIS

  def visit_Expr(self, node):
    # Handle some special cases of expressions that can occur in class and
    # module bodies.
    if node.value == self.defs.ELLIPSIS:
      # class x: ...
      return node.value
    elif types.Pyval.is_str(node.value):
      # docstrings
      return Splice([])

  def enter_arg(self, node):
    self.convert_node_annotations(node)

  def visit_arg(self, node):
    self.convert_node_annotations(node)

  def _get_name(self, node):
    if isinstance(node, astlib.Name):
      return node.id
    elif isinstance(node, astlib.Attribute):
      return f"{node.value.id}.{node.attr}"
    else:
      raise ParseError(f"Unexpected node type in get_name: {node}")

  def _preprocess_decorator_list(self, node):
    decorators = []
    for d in node.decorator_list:
      if isinstance(d, (astlib.Name, astlib.Attribute)):
        decorators.append(self._get_name(d))
      elif isinstance(d, astlib.Call):
        decorators.append(self._get_name(d.func))
      else:
        raise ParseError(f"Unexpected decorator: {d}")
    node.decorator_list = decorators

  def _preprocess_function(self, node):
    node.args = self.convert_node(node.args)
    node.returns = self.convert_node(node.returns)
    self._preprocess_decorator_list(node)
    node.body = _flatten_splices(node.body)

  def visit_FunctionDef(self, node):
    self._preprocess_function(node)
    return function.NameAndSig.from_function(node, False)

  def visit_AsyncFunctionDef(self, node):
    self._preprocess_function(node)
    return function.NameAndSig.from_function(node, True)

  def _read_str_list(self, name, value):
    if not (isinstance(value, (astlib.List, astlib.Tuple)) and
            all(types.Pyval.is_str(x) for x in value.elts)):
      raise ParseError(f"{name} must be a list of strings")
    return tuple(x.value for x in value.elts)

  def new_alias_or_constant(self, name, value):
    """Build an alias or constant."""
    # This is here rather than in _Definitions because we need to build a
    # constant or alias from a partially converted typed_ast subtree.
    if name == "__slots__":
      return types.SlotDecl(self._read_str_list(name, value))
    elif isinstance(value, types.Pyval):
      return pytd.Constant(name, value.to_pytd())
    elif isinstance(value, types.Ellipsis):
      return pytd.Constant(name, pytd.AnythingType())
    elif isinstance(value, pytd.NamedType):
      res = self.defs.resolve_type(value.name)
      return pytd.Alias(name, res)
    elif isinstance(value, (astlib.List, astlib.Tuple)):
      if name == "__all__":
        self.defs.all = self._read_str_list(name, value)
        return Splice([])
      else:
        # Silently discard the literal value, just preserve the collection type
        typ = "list" if isinstance(value, astlib.List) else "tuple"
        return pytd.Constant(name, pytd.NamedType(typ))
    elif isinstance(value, astlib.Name):
      value = self.defs.resolve_type(value.id)
      return pytd.Alias(name, value)
    else:
      # TODO(mdemello): add a case for TypeVar()
      # Convert any complex type aliases
      value = self.convert_node(value)
      return pytd.Alias(name, value)

  def enter_AnnAssign(self, node):
    self.convert_node_annotations(node)

  def visit_AnnAssign(self, node):
    self.convert_node_annotations(node)
    name = _parseable_name_to_real_name(node.target.id)
    typ = node.annotation
    if isinstance(node.value, types.Pyval):
      val = node.value
    else:
      val = self.convert_node(node.value)
    is_alias = False
    if name == "__match_args__" and isinstance(val, tuple):
      typ = pytd.NamedType("tuple")
      val = None
    elif typ.name:
      if self.defs.matches_type(typ.name, "typing.Final"):
        if isinstance(node.value, types.Pyval):
          # to_pytd_literal raises an exception if the value is a float, but
          # checking upfront allows us to generate a nicer error message.
          if isinstance(node.value.value, float):
            raise ParseError(
                f"Default value for {name}: Final can only be '...' or a legal "
                f"Literal parameter, got {val}")
          else:
            typ = node.value.to_pytd_literal()
            val = None
        elif isinstance(val, pytd.NamedType):
          typ = pytd.Literal(val)
          val = None
      elif self.defs.matches_type(typ.name, "typing.TypeAlias"):
        typ = val
        val = None
        is_alias = True
      elif (self.module_name == "typing_extensions" and
            typ.name == "_SpecialForm"):
        def type_of(n):
          return pytd.GenericType(
              pytd.NamedType("builtins.type"), (pytd.NamedType(n),))
        # We convert known special forms to their corresponding types and
        # otherwise treat them as unknown types.
        if name in {"Final", "Protocol", "Self", "TypeGuard"}:
          typ = type_of(f"typing.{name}")
        elif name == "LiteralString":
          typ = type_of("builtins.str")
        else:
          typ = pytd.AnythingType()
    if not _is_valid_default(val):
      raise ParseError(
          f"Default value for {name}: {typ.name} can only be '...' or a "
          f"literal constant, got {val}")
    if is_alias:
      assert not val
      ret = pytd.Alias(name, typ)
    else:
      ret = pytd.Constant(name, typ, val)
    if self.level == 0:
      self.defs.add_alias_or_constant(ret)
    return ret

  def visit_AugAssign(self, node):
    name = node.target.id
    if name == "__all__":
      # Ignore other assignments
      self.defs.all += self._read_str_list(name, node.value)
    return Splice([])

  def _assign(self, node, target, value):
    name = target.id

    # Record and erase TypeVar and ParamSpec definitions.
    if isinstance(value, _TypeVar):
      self.defs.add_type_var(name, value)
      return Splice([])
    elif isinstance(value, _ParamSpec):
      self.defs.add_param_spec(name, value)
      return Splice([])

    if node.type_comment:
      # TODO(mdemello): can pyi files have aliases with typecomments?
      ret = pytd.Constant(name, node.type_comment)
    else:
      ret = self.new_alias_or_constant(name, value)

    if self.in_function:
      # Should never happen, but this keeps pytype happy.
      if isinstance(ret, types.SlotDecl):
        raise ParseError("Cannot change the type of __slots__")
      return function.Mutator(name, ret.type)

    if self.level == 0 and not isinstance(ret, Splice):
      self.defs.add_alias_or_constant(ret)
    return ret

  def visit_Assign(self, node):
    self.convert_node_annotations(node)
    out = []
    value = node.value
    is_unknown_import = getattr(value, "name", None) == _UNKNOWN_IMPORT
    for target in node.targets:
      if isinstance(target, astlib.Tuple):
        count = len(target.elts)
        if not (isinstance(value, astlib.Tuple) and count == len(value.elts)):
          msg = f"Cannot unpack {count} values for multiple assignment"
          raise ParseError(msg)
        for k, v in zip(target.elts, value.elts):
          out.append(self._assign(node, k, v))
      elif is_unknown_import:
        constant = pytd.Constant(target.id, pytd.AnythingType())
        self.defs.add_alias_or_constant(constant)
        out.append(constant)
      else:
        out.append(self._assign(node, target, value))
    return Splice(out)

  def visit_ClassDef(self, node):
    full_class_name = ".".join(self.class_stack)
    self.defs.type_map[full_class_name] = pytd.NamedType(full_class_name)

    # Convert decorators to named types
    self._preprocess_decorator_list(node)
    decorators = classdef.get_decorators(
        node.decorator_list, self.defs.type_map)

    self.annotation_visitor.visit(node.bases)
    self.annotation_visitor.visit(node.keywords)
    defs = _flatten_splices(node.body)
    return self.defs.build_class(
        full_class_name, node.bases, node.keywords, decorators, defs)

  def enter_If(self, node):
    # Evaluate the test and preemptively remove the invalid branch so we don't
    # waste time traversing it.
    node.test = conditions.evaluate(node.test, self.options)
    if not isinstance(node.test, bool):
      raise ParseError("Unexpected if statement " + debug.dump(node, astlib))

    if node.test:
      node.orelse = []
    else:
      node.body = []

  def visit_If(self, node):
    if not isinstance(node.test, bool):
      raise ParseError("Unexpected if statement " + debug.dump(node, astlib))

    if node.test:
      return Splice(node.body)
    else:
      return Splice(node.orelse)

  def visit_Import(self, node):
    if self.level > 0:
      raise ParseError("Import statements need to be at module level")
    imports = [_tuple_of_import(x) for x in node.names]
    self.defs.add_import(None, imports)
    return Splice([])

  def visit_ImportFrom(self, node):
    if self.level > 0:
      raise ParseError("Import statements need to be at module level")
    imports = [_tuple_of_import(x) for x in node.names]
    module = _import_from_module(node.module, node.level)
    self.defs.add_import(module, imports)
    return Splice([])

  def _convert_newtype_args(self, node: astlib.Call):
    if len(node.args) != 2:
      msg = "Wrong args: expected NewType(name, [(field, type), ...])"
      raise ParseError(msg)
    name, typ = node.args
    typ = self.convert_node(typ)
    node.args = [name.s, typ]

  def _convert_typing_namedtuple_args(self, node: astlib.Call):
    # TODO(mdemello): handle NamedTuple("X", a=int, b=str, ...)
    if len(node.args) != 2:
      msg = "Wrong args: expected NamedTuple(name, [(field, type), ...])"
      raise ParseError(msg)
    name, fields = node.args
    fields = self.convert_node(fields)
    fields = [(types.string_value(n), t) for (n, t) in fields]
    node.args = [name.s, fields]

  def _convert_collections_namedtuple_args(self, node: astlib.Call):
    if len(node.args) != 2:
      msg = "Wrong args: expected namedtuple(name, [field, ...])"
      raise ParseError(msg)
    name, fields = node.args
    fields = self.convert_node(fields)
    fields = [(types.string_value(n), pytd.AnythingType()) for n in fields]
    node.args = [name.s, fields]  # pytype: disable=attribute-error

  def _convert_typevar_args(self, node):
    self.annotation_visitor.visit(node.keywords)
    if not node.args:
      raise ParseError("Missing arguments to TypeVar")
    name, *rest = node.args
    if not isinstance(name, astlib.Str):
      raise ParseError("Bad arguments to TypeVar")
    node.args = [name.s] + [self.convert_node(x) for x in rest]
    # Special-case late types in bound since typeshed uses it.
    for kw in node.keywords:
      if kw.arg == "bound":
        if isinstance(kw.value, types.Pyval):
          val = types.string_value(kw.value, context="TypeVar bound")
          kw.value = self.annotation_visitor.convert_late_annotation(val)

  def _convert_paramspec_args(self, node):
    return self._convert_typevar_args(node)

  def _convert_typed_dict_args(self, node: astlib.Call):
    msg = "Wrong args: expected TypedDict(name, {field: type, ...})"
    if len(node.args) != 2:
      raise ParseError(msg)
    name, fields = node.args
    if not (isinstance(name, astlib.Str) and isinstance(fields, astlib.Dict)):
      raise ParseError(msg)
    name_value = name.s
    fields_value = {}
    for k, v in zip(fields.keys, fields.values):
      if (hasattr(astlib, "Constant") and isinstance(k, astlib.Constant) and
          isinstance(k.value, str)):
        k_value = k.value
      else:
        raise ParseError(msg)
      v_pytd = self.convert_node(v)
      if not isinstance(v_pytd, pytd.Type):
        raise ParseError(msg)
      fields_value[k_value] = v_pytd
    node.args = [name_value, fields_value]

  def enter_Call(self, node):
    # Some function arguments need to be converted from strings to types when
    # entering the node, rather than bottom-up when they would already have been
    # converted to types.Pyval.
    # We also convert some literal string nodes that are not meant to be types
    # (e.g. the first arg to TypeVar()) to their bare values since we are
    # passing them to internal functions directly in visit_Call.
    if isinstance(node.func, astlib.Attribute):
      node.func = _attribute_to_name(node.func)
    if self.defs.matches_type(node.func.id, "typing.TypeVar"):
      self._convert_typevar_args(node)
    elif self.defs.matches_type(node.func.id, "typing.ParamSpec"):
      self._convert_paramspec_args(node)
    elif self.defs.matches_type(node.func.id, "typing.NamedTuple"):
      self._convert_typing_namedtuple_args(node)
    elif self.defs.matches_type(node.func.id, "collections.namedtuple"):
      self._convert_collections_namedtuple_args(node)
    elif self.defs.matches_type(node.func.id, "typing.TypedDict"):
      self._convert_typed_dict_args(node)
    elif self.defs.matches_type(node.func.id, "typing.NewType"):
      return self._convert_newtype_args(node)

  def visit_Call(self, node):
    if self.defs.matches_type(node.func.id, "typing.TypeVar"):
      if self.level > 0:
        raise ParseError("TypeVars need to be defined at module level")
      return _TypeVar.from_call(node)
    elif self.defs.matches_type(node.func.id, "typing.ParamSpec"):
      return _ParamSpec.from_call(node)
    elif self.defs.matches_type(
        node.func.id, ("typing.NamedTuple", "collections.namedtuple")):
      return self.defs.new_named_tuple(*node.args)
    elif self.defs.matches_type(node.func.id, "typing.TypedDict"):
      return self.defs.new_typed_dict(*node.args, node.keywords)
    elif self.defs.matches_type(node.func.id, "typing.NewType"):
      return self.defs.new_new_type(*node.args)
    elif self.defs.matches_type(node.func.id, "importlib.import_module"):
      return pytd.NamedType(_UNKNOWN_IMPORT)
    # Convert all other calls to NamedTypes; for example:
    # * typing.pyi uses things like
    #     List = _Alias()
    # * pytd extensions allow both
    #     raise Exception
    #   and
    #     raise Exception()
    return pytd.NamedType(node.func.id)

  def visit_Raise(self, node):
    ret = self.convert_node(node.exc)
    return types.Raise(ret)

  # Track nesting level

  def enter_FunctionDef(self, node):
    self.level += 1
    self.in_function = True

  def leave_FunctionDef(self, node):
    self.level -= 1
    self.in_function = False

  def enter_AsyncFunctionDef(self, node):
    self.enter_FunctionDef(node)

  def leave_AsyncFunctionDef(self, node):
    self.leave_FunctionDef(node)

  def enter_ClassDef(self, node):
    self.level += 1
    self.class_stack.append(_parseable_name_to_real_name(node.name))

  def leave_ClassDef(self, node):
    self.level -= 1
    self.class_stack.pop()


def post_process_ast(ast, src, name=None):
  """Post-process the parsed AST."""
  ast = definitions.finalize_ast(ast)
  ast = ast.Visit(pep484.ConvertTypingToNative(name))

  if name:
    ast = ast.Replace(name=name)
    ast = ast.Visit(visitors.AddNamePrefix())
  else:
    # If there's no unique name, hash the sourcecode.
    ast = ast.Replace(name=hashlib.md5(src.encode("utf-8")).hexdigest())
  ast = ast.Visit(visitors.StripExternalNamePrefix())

  # Now that we have resolved external names, validate any class decorators that
  # do code generation. (We will generate the class lazily, but we should check
  # for errors at parse time so they can be reported early.)
  try:
    ast = ast.Visit(decorate.ValidateDecoratedClassVisitor())
  except TypeError as e:
    # Convert errors into ParseError. Unfortunately we no longer have location
    # information if an error is raised during transformation of a class node.
    raise ParseError.from_exc(e)

  return ast


def _fix_src(src: str) -> str:
  """Attempts to fix syntax errors in the source code."""
  # TODO(b/294445640): This is a hacky workaround to deal with invalid stubs
  # produced by the protobuf pyi generator.
  try:
    tokens = list(tokenize.generate_tokens(io.StringIO(src).readline))
  except SyntaxError:
    return src
  num_tokens = len(tokens)

  def _is_classname(i):
    return i and tokens[i-1].string == "class"

  def _is_varname(i):
    if i and tokens[i-1].string.strip():  # not proceeded by whitespace
      return False
    return i < num_tokens - 1 and tokens[i+1].type == tokenize.OP

  lines = src.splitlines()
  for i, token in enumerate(tokens):
    if (not keyword.iskeyword(token.string) or
        not _is_classname(i) and not _is_varname(i)):
      continue
    start_line, start_col = token.start
    end_line, end_col = token.end
    if start_line != end_line:
      continue
    line = lines[start_line-1]
    new_line = (line[:start_col] + _keyword_to_parseable_name(token.string) +
                line[end_col:])
    lines[start_line-1] = new_line
  return "\n".join(lines)


def _parse(src: str, feature_version: int, filename: str = ""):
  """Call the typed_ast parser with the appropriate feature version."""
  kwargs = {"feature_version": feature_version}
  if sys.version_info >= (3, 8):
    kwargs["type_comments"] = True
  try:
    ast_root_node = astlib.parse(src, filename, **kwargs)
  except SyntaxError as e:
    # We only attempt to fix the source code if a syntax error is encountered
    # because (1) this way, if the fixing fails, the error details will
    # correctly reflect the original source, and (2) fixing is unnecessary most
    # of the time, so always running it would be inefficient.
    fixed_src = _fix_src(src)
    try:
      ast_root_node = astlib.parse(fixed_src, filename, **kwargs)
    except SyntaxError:
      raise ParseError(
          e.msg, line=e.lineno, filename=filename, column=e.offset, text=e.text
      ) from e
  return ast_root_node


def _feature_version(python_version: Tuple[int, ...]) -> int:
  """Get the python feature version for the parser."""
  if len(python_version) == 1:
    return sys.version_info.minor
  else:
    return python_version[1]


# Options that will be copied from pytype.config.Options.
_TOPLEVEL_PYI_OPTIONS = (
    "platform",
    "python_version",
    "strict_primitive_comparisons",
)


@dataclasses.dataclass
class PyiOptions:
  """Pyi parsing options."""

  python_version: Tuple[int, int] = sys.version_info[:2]
  platform: str = sys.platform
  strict_primitive_comparisons: bool = True

  @classmethod
  def from_toplevel_options(cls, toplevel_options):
    kwargs = {}
    for k in _TOPLEVEL_PYI_OPTIONS:
      kwargs[k] = getattr(toplevel_options, k)
    return cls(**kwargs)


def parse_string(
    src: str,
    name: Optional[str] = None,
    filename: Optional[str] = None,
    options: Optional[PyiOptions] = None,
):
  return parse_pyi(src, filename=filename, module_name=name, options=options)


def parse_pyi(
    src: str,
    filename: Optional[str],
    module_name: str,
    options: Optional[PyiOptions] = None,
) -> pytd.TypeDeclUnit:
  """Parse a pyi string."""
  filename = filename or ""
  options = options or PyiOptions()
  feature_version = _feature_version(options.python_version)
  root = _parse(src, feature_version, filename)
  gen_pytd = _GeneratePytdVisitor(src, filename, module_name, options)
  root = gen_pytd.visit(root)
  root = post_process_ast(root, src, module_name)
  return root


def parse_pyi_debug(
    src: str,
    filename: str,
    module_name: str,
    options: Optional[PyiOptions] = None,
) -> Tuple[pytd.TypeDeclUnit, _GeneratePytdVisitor]:
  """Debug version of parse_pyi."""
  options = options or PyiOptions()
  feature_version = _feature_version(options.python_version)
  root = _parse(src, feature_version, filename)
  print(debug.dump(root, astlib, include_attributes=False))
  gen_pytd = _GeneratePytdVisitor(src, filename, module_name, options)
  root = gen_pytd.visit(root)
  print("---transformed parse tree--------------------")
  print(root)
  root = post_process_ast(root, src, module_name)
  print("---post-processed---------------------")
  print(root)
  print("------------------------")
  print(gen_pytd.defs.type_map)
  print(gen_pytd.defs.module_path_map)
  return root, gen_pytd


def canonical_pyi(pyi, multiline_args=False, options=None):
  """Rewrite a pyi in canonical form."""
  ast = parse_string(pyi, options=options)
  ast = ast.Visit(visitors.ClassTypeToNamedType())
  ast = ast.Visit(visitors.CanonicalOrderingVisitor())
  ast.Visit(visitors.VerifyVisitor())
  return pytd_utils.Print(ast, multiline_args)
