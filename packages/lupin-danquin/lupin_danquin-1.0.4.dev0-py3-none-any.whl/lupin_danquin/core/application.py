from typing import Any, Dict, List
from xml.dom import minidom

from .global_variable import GlobalVariable
from .program import Program
from .line_ended import LINE_ENDED


def get_program_list(
    program_path,
    application_name,
    exclude=["UT.pgx", "start.pgx", "stop.pgx", "test.pgx"],
) -> List[Program]:
    file_path = program_path + "/" + application_name + ".pjx"
    doc = minidom.parse(file_path)
    progs = doc.getElementsByTagName("Program")
    return_progs = []
    for prog in progs:
        name = prog.getAttribute("file")
        should_exclude = False
        for e in exclude:
            if e in name:
                should_exclude = True
        if not should_exclude:
            return_progs.append(Program(program_path, name))
    return return_progs


def get_dependencies(program_path, application_name, exclude=["Logger"]) -> List[str]:
    file_path = program_path + "/" + application_name + ".pjx"
    doc = minidom.parse(file_path)
    deps = doc.getElementsByTagName("Library")
    return_deps = []
    for dep in deps:
        name = dep.getAttribute("alias")
        should_exclude = False
        for e in exclude:
            if e in name:
                should_exclude = True
        if not should_exclude:
            return_deps.append(name)
    return return_deps


def get_type_dependencies(
    program_path, application_name, exclude=["Logger"]
) -> List[str]:
    file_path = program_path + "/" + application_name + ".pjx"
    doc = minidom.parse(file_path)
    deps = doc.getElementsByTagName("Type")
    return_deps = []
    for dep in deps:
        name = dep.getAttribute("name")
        should_exclude = False
        for e in exclude:
            if e in name:
                should_exclude = True
        if not should_exclude:
            return_deps.append(name)
    return return_deps


def get_global_variables(
    program_path, application_name, exclude=["UT"]
) -> List[GlobalVariable]:
    file_path = program_path + "/" + application_name + ".dtx"
    doc = minidom.parse(file_path)
    vars = doc.getElementsByTagName("Data")
    return_vars = []
    for var in vars:
        name = var.getAttribute("name")
        should_exclude = False
        for e in exclude:
            if e in name:
                should_exclude = True
        if not should_exclude:
            xsi = var.getAttribute("xsi:type")
            access = var.getAttribute("access")
            type_ = var.getAttribute("type")
            size = var.getAttribute("size")
            return_vars.append(
                GlobalVariable(name, access, type_, xsi, size, file_path)
            )
    return return_vars


def get_application_description(program_path) -> str:
    file_path = program_path + "/README.md"
    lines = []
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Missing documentation file " + file_path)
    return LINE_ENDED.join(lines)


class Application:
    def __init__(self, program_path: str, application_name: str):
        self.application_name = application_name
        self.dependencies = get_dependencies(program_path, application_name)
        self.type_dependencies = get_type_dependencies(program_path, application_name)
        self.program_list = get_program_list(program_path, application_name)
        self.global_variables = get_global_variables(program_path, application_name)
        self.application_description = get_application_description(program_path)

    def check_coding_rules(self) -> List[str]:
        result = []
        for p in self.program_list:
            result += p.check_coding_rules()
        for gv in self.global_variables:
            result += gv.check_coding_rules()
        return result

    def get_all_information_from_app(self) -> Dict[str, Any]:
        """Return all information from the application in a dict for the documentation generation"""
        all_information = {
            "name": self.application_name,
            "description": self.application_description,
            "dependencies": self.dependencies,
            "type_dependencies": self.type_dependencies,
            "global_variables": self.global_variables,
            "private_program_list": [p for p in self.program_list if not p.public],
            "public_program_list": [p for p in self.program_list if p.public],
        }
        return all_information
