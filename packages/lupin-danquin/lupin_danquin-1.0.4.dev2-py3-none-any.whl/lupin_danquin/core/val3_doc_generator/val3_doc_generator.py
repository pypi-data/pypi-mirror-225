from typing import Any, Dict, List
import codecs
import os

from jinja2 import (
    Environment,
    PackageLoader,
    select_autoescape,
    Template,
    TemplateNotFound,
    TemplateError,
    TemplateRuntimeError,
)

from lupin_danquin.core.application import Application
from lupin_danquin.core.tools.utils import (
    die,
    find_usrapp_dir,
    info,
    split_path_and_app_name,
)


class Val3Documentation:
    def __init__(self):
        self.user_app_dir = find_usrapp_dir()

    def _get_informations_from_applications(
        self, application_names: List
    ) -> List[Dict[str, Any]]:
        """Get all informations from applications"""

        apps_information = []
        base_program_path = self.user_app_dir + os.sep
        for application_name in application_names:
            program_path, application_name = split_path_and_app_name(
                base_program_path, application_name
            )
            if not os.path.isdir(program_path):
                die(msg=f"Application '{application_name}' not found")
            info(msg=f"Get informations from '{application_name}'")
            apps_information.append(
                Application(
                    program_path, application_name
                ).get_all_information_from_app()
            )
        return apps_information

    def _get_local_template(self) -> Template:
        try:
            # Create jinja2 environment
            env = Environment(
                loader=PackageLoader("lupin_danquin", "templates"),
                autoescape=select_autoescape(),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            # Charge template
            template = env.get_template("val3_documentation_md.j2")
            return template
        except TemplateNotFound:
            die(
                msg="Template 'lupin_danquin/templates/val3_documentation_md.j2 not found"
            )

    def generate_markdown(
        self, applications_list: List, begining_of_file, end_of_file
    ) -> None:
        """Generate the documentation"""
        context = {
            "beginning_of_file": begining_of_file,
            "end_of_file": end_of_file,
            "applications": self._get_informations_from_applications(applications_list),
        }

        template = self._get_local_template()
        try:
            content = template.render(context)
        except (TemplateError, TemplateRuntimeError) as e:
            die(msg=f"Error rendering Jinja2 template: {e}")

        with codecs.open("./val3_documentation.md", "w", encoding="utf-8") as f:
            f.write(content)
        info(msg="val3_documentation.md generated")
