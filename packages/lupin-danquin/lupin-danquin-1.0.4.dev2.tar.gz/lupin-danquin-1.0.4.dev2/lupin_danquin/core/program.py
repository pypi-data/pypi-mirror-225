from typing import List
from xml.dom import minidom

from .parameter import Parameter
from .local_variable import LocalVariable


def get_parameters(program_path: str, program_file: str) -> List[Parameter]:
    file_path = program_path + "/" + program_file
    doc = minidom.parse(file_path)
    params = doc.getElementsByTagName("Parameter")
    returned_params = []
    for param in params:
        returned_params.append(
            Parameter(
                param.getAttribute("name"),
                param.getAttribute("type"),
                param.getAttribute("xsi:type"),
                param.getAttribute("use"),
                file_path,
            )
        )
    return returned_params


def get_program_description(program_path: str, program_file: str) -> str:
    file_path = program_path + "/" + program_file
    input_txt = []
    with open(file_path, "r") as f_input:
        input_txt = f_input.readlines()
    comment_txt = r"//"
    doc = ""
    start_doc = False
    for line in input_txt:
        if start_doc:
            if comment_txt in line:
                doc += line.split(comment_txt)[-1]
            else:
                break
        # first code line
        if "<Code><![CDATA[begin" in line:
            start_doc = True
        # last code line
        if "end]]></Code>" in line:
            break
    if len(doc) == 0:
        print("Missing description for program " + file_path)
    return doc


def get_code(program_path: str, program_file: str) -> str:
    file_path = program_path + "/" + program_file
    input_txt = ""
    with open(file_path, "r") as f_input:
        input_txt = f_input.read()
    return input_txt.split("<Code><![CDATA[begin")[-1].split("end]]></Code>")[0]


def is_public(program_path: str, program_file: str) -> bool:
    file_path = program_path + "/" + program_file
    doc = minidom.parse(file_path)
    prog = doc.getElementsByTagName("Program")
    for p in prog:
        return p.getAttribute("access") == "public"
    return False


def get_local_variables(program_path: str, program_file: str) -> List[LocalVariable]:
    file_path = program_path + "/" + program_file
    doc = minidom.parse(file_path)
    vars = doc.getElementsByTagName("Local")
    returned_vars = []
    for var in vars:
        returned_vars.append(
            LocalVariable(
                var.getAttribute("name"),
                var.getAttribute("type"),
                var.getAttribute("xsi:type"),
                var.getAttribute("size"),
                file_path,
            )
        )
    return returned_vars


def get_program_signature(program_name: str, parameters: List[Parameter]) -> str:
    return (
        program_name.removesuffix(".pgx")
        + "("
        + ", ".join(
            [
                param.type_data
                + ("& " if (param.use == "reference") else " ")
                + param.name
                for param in parameters
            ]
        )
        + ")"
    )


class Program:
    def __init__(self, program_path: str, program_name: str):
        self.program_path = program_path
        self.program_name = program_name
        self.param_list = get_parameters(program_path, program_name)
        self.variable_list = get_local_variables(program_path, program_name)
        self.description = get_program_description(program_path, program_name)
        self.signature = get_program_signature(program_name, self.param_list)
        self.public = is_public(program_path, program_name)
        self.code = get_code(program_path, program_name)
        self.check_has_unused_parameter()
        self.check_has_unused_variable()

    def check_coding_rules(self) -> List[str]:
        return self.check_has_unused_parameter() + self.check_has_unused_variable()

    def check_has_unused_parameter(self) -> List[str]:
        result = []
        for param in self.param_list:
            if param.name not in self.code:
                result += [
                    f"Unused parameter {param.name} in program {self.program_path}/{self.program_name}"
                ]
            result += param.check_coding_rules()
        return result

    def check_has_unused_variable(self) -> List[str]:
        result = []
        for var in self.variable_list:
            if var.name not in self.code:
                result += [
                    f"Unused local variable {var.name} in program {self.program_path}/{self.program_name}"
                ]
        return result
