from typing import List
import os

from lupin_danquin.core.application import Application
from lupin_danquin.core.tools.utils import (
    die,
    find_usrapp_dir,
    info,
    warn,
    split_path_and_app_name,
)


class CodingRulesValidator:
    def __init__(self, application_names: List):
        self.application_names = application_names
        self.user_app_dir = find_usrapp_dir()

    def _check_coding_rules(self):
        """Check coding rules for all applications"""
        result = []
        base_program_path = self.user_app_dir + os.sep
        for application_name in self.application_names:
            program_path, application_name = split_path_and_app_name(
                base_program_path, application_name
            )
            if not os.path.isdir(program_path):
                die(msg=f"Application '{application_name}' not found")
            app = Application(program_path, application_name)
            info(msg=f"Check coding rules for '{application_name}'")
            result += app.check_coding_rules()
        return result

    def validate(self):
        """Validate coding rules"""
        result = self._check_coding_rules()
        if len(result) > 0:
            info(msg=f"{len(result)} errors found while checking coding rules")
            for error in result:
                warn(msg=error)
            die(msg="Coding rules not respected")
        else:
            info(msg="No error found while checking coding rules")
