from pathlib import Path

from openldap_schema_parser.attribute import ATTRIBUTE_USAGE
from openldap_schema_parser.objectclass import STRUCTURAL_TYPE
from openldap_schema_parser.schema import (
    Attribute,
    ObjectClass,
    ObjectIdentifier,
    Schema,
)
from openldap_schema_parser.schema_parser import Lark_StandAlone, Transformer


class SchemaTransformer(Transformer):
    """構文解析用Transformerクラス

    schemaファイルをSchemクラスに変換するためのTransformerクラス
    """

    def __init__(self, name):
        self._schema = Schema(name)

    def start(self, token):
        return self._schema

    def schema(self, token):
        if isinstance(token[0], ObjectIdentifier):
            self._schema.objectidentifier_list.append(token[0])
        elif isinstance(token[0], Attribute):
            self._schema.attribute_list.append(token[0])
        elif isinstance(token[0], ObjectClass):
            self._schema.objectclass_list.append(token[0])
        return self._schema

    def attributetype(self, token):
        data = {"oid": token[1]}
        for t in token:
            if isinstance(t, dict):
                data.update(t)
        return Attribute(**data)

    def attributetype_state(self, token):
        return token[0]

    def objectclass(self, token):
        data = {"oid": token[1]}
        for t in token:
            if isinstance(t, dict):
                data.update(t)
        return ObjectClass(**data)

    def objectclass_state(self, token):
        return token[0]

    def objectidentifier(self, token):
        return ObjectIdentifier(str(token[0]), str(token[1]))

    def ldapsyntax(self, token):
        data = {"oid": token[1]}
        for t in token:
            if isinstance(t, dict):
                data.update(t)
        return None

    def ldapsyntax_state(self, token):
        return token[0]

    def name(self, token):
        return {"name": token[0]}

    def desc(self, token):
        return {"description": token[0]}

    def OBSOLETE(self, token):
        return {"obsolete": True}

    def attributetype_sup(self, token):
        return {"sup": token[0]}

    def objectclass_sup(self, token):
        return {"sup": token[0]}

    def equality(self, token):
        return {"equality": token[0]}

    def ordering(self, token):
        return {"ordering": token[0]}

    def substr(self, token):
        return {"substr": token[0]}

    def syntax(self, token):
        return {"syntax": token[0]}

    def single_value(self, token):
        return {"single_value": True}

    def collective(self, token):
        return {"collective": True}

    def no_user_modification(self, token):
        return {"no_user_modification": True}

    def usage(self, token):
        return {"usage": token[0]}

    def ATTRIBUTE_USAGE(self, token):
        if token == "userApplications":
            return ATTRIBUTE_USAGE.USER_APPLICATIONS
        elif token == "directoryOperation":
            return ATTRIBUTE_USAGE.DIRECTORY_OPERATION
        elif token == "distributedOperation":
            return ATTRIBUTE_USAGE.DISTRIBUTED_OPERATION
        elif token == "dSAOperation":
            return ATTRIBUTE_USAGE.DSA_OPERATION

    def user_attr(self, token):
        return {token[0]: token[1]}

    def USER_KEY(self, token):
        return token.strip()

    def structural(self, token):
        return {"structural_type": token[0]}

    def ABSTRACT(self, token):
        return STRUCTURAL_TYPE.ABSTRACT

    def STRUCTURAL(self, token):
        return STRUCTURAL_TYPE.STRUCTURAL

    def AUXILIARY(self, token):
        return STRUCTURAL_TYPE.AUXILIARY

    def must(self, token):
        return {"must": token[0]}

    def may(self, token):
        return {"may": token[0]}

    def oids(self, token):
        if len(token) > 1:
            return token[1]
        return [token[0]]

    def oidlist(self, token):
        return token

    def qdescrs(self, token):
        if len(token) > 1:
            return token[1]
        return token[0]

    def qdescrlist(self, token):
        return token

    def MACROOID(self, token):
        return token.strip()

    def NOIDLEN(self, token):
        return token.strip()

    def WOID(self, token):
        return token.strip()

    def DQSTRING(self, token):
        return token.strip().strip("'")

    def QDESCR(self, token):
        return token.strip("'")


def parse(target_file: str) -> Schema:
    """schema形式のファイルをパースします

    OpenLDAP schema形式のファイル構文解析し、Schemaクラスとして返します。

    :param str target_file: パースするshcemaファイルのパスを指定します
    :return: schemaファイルを構文解析した結果をSchemaクラスとして返します。
    :rtype: openldap_schema_parser.Schema
    :raises SchemaParseError: target_fileのパースに失敗
    """
    target_path = Path(target_file)
    text = ""
    with target_path.open() as fd:
        text = fd.read()
    return parse_str(text, target_path.stem)


def parse_str(text: str, name: str = "parsed") -> Schema:
    """schema形式の文字列をパースします

    OpenLDAP schema形式のテキストを構文解析し、Schemaクラスとして返します。

    :param str text: パースするshcema形式の文字列を指定します。
    :param str name: Schemaの名前を指定します。
    :return: schemaファイルを構文解析した結果をSchemaクラスとして返します。
    :rtype: openldap_schema_parser.Schema
    :raises SchemaParseError: target_fileのパースに失敗
    """
    parser = Lark_StandAlone(transformer=SchemaTransformer(name))
    result = parser.parse(text)
    return result
