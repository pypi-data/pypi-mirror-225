""" openldap-schema-parser

OpenLDAP schemaファイルを構文解析するモジュール
schema-parserというコマンドラインツールも提供する
"""
__name__ = "openldap-schema-parser"
import pkg_resources

__version__ = pkg_resources.get_distribution(__name__).version
