from typing import List

from .rules import OTHER_TYPES, TYPE_RULES


class LocalVariable:
    def __init__(
        self, name: str, type_data: str, xsi: str, size: str, context: str = ""
    ):
        self.name = name
        self.type_data = type_data
        self.xsi = xsi
        self.size = size
        self.context = context

    def check_coding_rules(self) -> List:
        result = []
        if not self.name.startswith("l_"):
            result += [
                f"Local variable {self.name} should begin by 'l_'. {self.context}"
            ]

        if self.type_data in TYPE_RULES.keys():
            rule = TYPE_RULES.get(self.type_data)
            if not self.name.startswith("l_" + rule):
                result += [
                    f"Local variable {self.name} of type {self.type_data} should begin by 'l_{rule}'. {self.context}"
                ]
        else:
            if not self.name.startswith("l_" + OTHER_TYPES):
                result += [
                    f"Local variable {self.name} of type CUSTOM should begin by 'l_{OTHER_TYPES}'. {self.context}"
                ]

        return result
