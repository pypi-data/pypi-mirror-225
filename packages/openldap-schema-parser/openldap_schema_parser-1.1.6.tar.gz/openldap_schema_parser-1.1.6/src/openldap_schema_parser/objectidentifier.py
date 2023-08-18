from typing import Union


class ObjectIdentifier:
    """ObjectIdentifier情報を保持するクラス

    :param str key: ObjectIdentifierの名前
    :param str oid: ObjectIdentifierのOID
    """

    def __init__(self, key: str = "", oid: str = ""):
        self.key = key
        self.oid = oid

    def __repr__(self):
        args = [
            f"key={repr(self.key)}",
            f"oid={repr(self.oid)}",
        ]
        return f"ObjectIdentifier({', '.join(args)})"

    def get_oid(self, suffix: Union[str, int] = None) -> str:
        """実際のOIDを取得する

        ObjectIdentifierにsuffixを与えた場合の実際のOIDを返します。

        >>> oid = ObjectIdentifier("testOID", "1.2.3")
        >>> oid.get_oid(4)
        1.2.3.4
        >>> oid.get_oid(5)
        1.2.3.5
        >>> oid.get_oid()
        1.2.3

        :param Union[str, int] suffix: suffixの値を指定。Noneの場合は自身のOIDをそのまま返す
        :return str: suffixを与えた場合の実際のOID
        """
        if suffix is None:
            return self.oid
        return f"{self.oid}.{suffix}"

    def pprint_str(self, width: int = 80, tabsize: int = 8, **kwargs) -> str:
        return f"objectIdentifier {self.key}\t{self.oid}".expandtabs(tabsize=tabsize)
