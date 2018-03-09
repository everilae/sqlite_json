from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.mysql.json import JSONIndexType, JSONPathType
from sqlalchemy.engine import CreateEnginePlugin

from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql import sqltypes
from sqlalchemy.sql.operators import json_getitem_op, json_path_getitem_op

__all__ = [
    "JSON",
    "JsonPlugin"
]

_json_serializer = None
_json_deserializer = None


class JSON(sqltypes.JSON):

    class Comparator(sqltypes.JSON.Comparator):

        def _setup_getitem(self, index):
            operator, index, _ = super()._setup_getitem(index)
            # https://www.sqlite.org/json1.html#jex
            # "the SQL datatype of the result is NULL for a JSON null, INTEGER
            # or REAL for a JSON numeric value, an INTEGER zero for a JSON false
            # value, an INTEGER one for a JSON true value, the dequoted text for
            # a JSON string value, and a text representation for JSON object and
            # array values. If there are multiple path arguments (P1, P2, and so
            # forth) then this routine returns SQLite text which is a
            # well-formed JSON array holding the various values."
            return operator, index, sqltypes.NullType()

    comparator_factory = Comparator


@compiles(JSON, "sqlite")
@compiles(sqltypes.JSON, "sqlite")
def compile_json_type(element, compiler, **kw):
    return "JSON"


@compiles(BinaryExpression, "sqlite")
def compile_binary(binary, compiler, override_operator=None, **kw):
    operator = override_operator or binary.operator

    if operator is json_getitem_op:
        return visit_json_getitem_op_binary(
            compiler, binary, operator, override_operator=override_operator,
            **kw)

    if operator is json_path_getitem_op:
        return visit_json_path_getitem_op_binary(
            compiler, binary, operator, override_operator=override_operator,
            **kw)

    return compiler.process(binary, override_operator=override_operator, **kw)


def visit_json_getitem_op_binary(compiler, binary, operator, **kw):
    return "JSON_EXTRACT(%s, %s)" % (
        compiler.process(binary.left),
        compiler.process(binary.right))


def visit_json_path_getitem_op_binary(compiler, binary, operator, **kw):
    return "JSON_EXTRACT(%s, %s)" % (
        compiler.process(binary.left),
        compiler.process(binary.right))


def monkeypatch_dialect(dialect):
    if not hasattr(dialect, "_json_serializer"):
        dialect._json_serializer = _json_serializer

    if not hasattr(dialect, "_json_deserializer"):
        dialect._json_deserializer = _json_deserializer

    if sqltypes.JSON not in dialect.colspecs:
        dialect.colspecs = dialect.colspecs.copy()
        dialect.colspecs[sqltypes.JSON] = JSON
        dialect.colspecs[sqltypes.JSON.JSONIndexType] = JSONIndexType
        dialect.colspecs[sqltypes.JSON.JSONPathType] = JSONPathType

    if "json" not in dialect.ischema_names:
        dialect.ischema_names = dialect.ischema_names.copy()
        dialect.ischema_names["json"] = JSON


class JsonPlugin(CreateEnginePlugin):

    def engine_created(self, engine):
        monkeypatch_dialect(engine.dialect)
