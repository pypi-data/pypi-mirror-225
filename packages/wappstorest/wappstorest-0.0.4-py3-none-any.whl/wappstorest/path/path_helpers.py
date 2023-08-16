

class Wrapper:
    __path__: str

    def __init__(self, name, parent):
        self.__path__ = 'this_' + '.'.join(
            f"{parent}.{name}".split('.')[1:]
        )

    def value_converter(self, value) -> str:
        """
        TODO: Check for datetime, Enum and the likes & costume convert.
        """
        return str(value)

    def __lt__(self, other) -> str:
        """
        less then
        """
        return (
            f"{self.__path__}"
            f"<"
            f"{self.value_converter(other)}"
        )

    def __le__(self, other) -> str:
        """
        less then equel to
        """
        return (
            f"{self.__path__}"
            f"<="
            f"{self.value_converter(other)}"
        )

    def __eq__(self, other) -> str:
        """
        equel to
        """
        return (
            f"{self.__path__}"
            f"=="
            f"{self.value_converter(other)}"
        )

    def __ne__(self, other) -> str:
        """not equel to"""
        return (
            f"{self.__path__}"
            f"!="
            f"{self.value_converter(other)}"
        )

    def __gt__(self, other) -> str:
        """
        greater then
        """
        return (
            f"{self.__path__}"
            f">"
            f"{self.value_converter(other)}"
        )

    def __ge__(self, other) -> str:
        """
        greater then equel to
        """
        return (
            f"{self.__path__}"
            f">="
            f"{self.value_converter(other)}"
        )

    def __invert__(self) -> str:
        """
        """
        return (
            f"~"
            f"{self.__path__}"
        )

    # def __getattr__(self, name):
    #     # https://stackoverflow.com/questions/14512620/is-there-any-way-to-override-the-double-underscore-magic-methods-of-arbitrary
    #     return getattr(self.wrapped, name)
