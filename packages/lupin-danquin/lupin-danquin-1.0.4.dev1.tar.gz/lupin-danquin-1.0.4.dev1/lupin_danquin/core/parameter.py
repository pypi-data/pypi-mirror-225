from typing import List

from .rules import OTHER_TYPES, TYPE_RULES


class Parameter:
    def __init__(
        self, name: str, type_data: str, xsi: str, use: str, context: str = ""
    ):
        self.name = name
        self.type_data = type_data
        self.xsi = xsi
        self.use = use
        if len(use) == 0:
            self.use = "value"
        self.context = context

    def check_coding_rules(self) -> List:
        result = []
        if not self.name.startswith("x_"):
            result += [f"Parameter {self.name} should begin by 'x_'.  {self.context}"]
        if (
            self.use != "value"
            and self.xsi == "element"
            and not self.name.endswith("Out")
        ):
            result += [
                f"Output parameter {self.name} should ends by 'Out'. {self.context}"
            ]

        if self.type_data in TYPE_RULES.keys():
            rule = TYPE_RULES.get(self.type_data)
            if not self.name.startswith("x_" + rule):
                result += [
                    f"Parameter {self.name} of type {self.type_data} should begin by 'x_{rule}'. {self.context}"
                ]
        else:
            if not self.name.startswith("x_" + OTHER_TYPES):
                result += [
                    f"Parameter {self.name} of type CUSTOM should begin by 'x_{OTHER_TYPES}'. {self.context}"
                ]
        return result
