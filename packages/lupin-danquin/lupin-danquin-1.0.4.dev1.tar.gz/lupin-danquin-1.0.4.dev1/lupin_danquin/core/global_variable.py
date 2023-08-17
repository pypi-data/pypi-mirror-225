from typing import List

from .rules import OTHER_TYPES, TYPE_RULES


class GlobalVariable:
    def __init__(
        self,
        name: str,
        access: str,
        type_data: str,
        xsi: str,
        size: str,
        context: str = "",
    ):
        self.name = name
        self.type_data = type_data
        self.xsi = xsi
        self.size = size
        self.access = access
        self.context = context

    def check_coding_rules(self) -> List:
        result = []
        if self.access == "private" and not self.name.startswith("_"):
            result += [
                f"Global private variable {self.name} should begin by '_'. {self.context}"
            ]
        if self.access != "private" and self.name.startswith("_"):
            result += [
                f"Global public variable {self.name} should not begin by '_'. {self.context}"
            ]

        name = self.name[1:] if self.name.startswith("_") else self.name
        if self.type_data in TYPE_RULES.keys():
            rule = TYPE_RULES.get(self.type_data)
            if not name.startswith(rule):
                result += [
                    (
                        f"Global variable {self.name} of type {self.type_data} should begin by "
                        f"'{'_' if self.access == 'private' else ''}{rule}'. {self.context}"
                    )
                ]
        else:
            if not name.startswith(OTHER_TYPES):
                result += [
                    (
                        f"Global variable {self.name} of type CUSTOM should begin by "
                        f"'{'_' if self.access == 'private' else ''}{OTHER_TYPES}'. {self.context}"
                    )
                ]
        return result
