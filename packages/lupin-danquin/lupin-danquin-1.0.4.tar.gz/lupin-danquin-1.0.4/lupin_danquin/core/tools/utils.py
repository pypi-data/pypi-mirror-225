from typing import List
import codecs
import logging
import os
import re
import sys


def configure_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )


def die(msg: str) -> None:
    logging.error(msg)
    sys.exit(1)


def info(msg: str) -> None:
    logging.info(msg)


def warn(msg: str) -> None:
    logging.warning(msg)


def update_version():
    """get version from setup.cfg file and
    update __version__ in lupin_danquin.__init__.py
    """
    with open("setup.cfg", "r", encoding="utf-8") as f:
        setup_cfg = f.read()
    _version = re.search(
        r"(^version = )(\d{1,2}\.\d{1,2}\.\d{1,2})(\.[a-z]{1,})?(\d{1,2})?",
        setup_cfg,
        re.MULTILINE,
    )
    version = ""
    for group in _version.group(2, 3, 4):
        if group is not None:
            version = version + str(group)
    content = f'__version__ = "{version}"\n'

    with open("lupin_danquin/__init__.py", "w", encoding="utf-8") as outfile:
        outfile.write(content)
    return version


def convert_application_name_to_list(application_name: str) -> List:
    """Convert application name to list.
    Args:
        application_name (str): The name of the application.
    Returns:
        list: The list of the application name.
    """
    return [app.strip() for app in application_name.split(",") if app.strip()]


def read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        die(msg=f"File '{file_path}' does not exist.")
    info(msg=f"Get informations from {file_path}")
    with codecs.open(file_path, encoding="utf-8") as f:
        result = f.read()
    return result


def find_usrapp_dir() -> str:
    """Find the usrapp directory"""
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        if "usrapp" in dirnames:
            return os.path.join(dirpath, "usrapp")
    die(msg="'usrapp' directory not found")


def split_path_and_app_name(base_program_path: str, application_name: str) -> tuple:
    application_name_parts = application_name.split("/")
    if len(application_name_parts) > 1:
        application_name = application_name_parts[-1]
    new_base_program_path = os.path.join(base_program_path, *application_name_parts)

    return new_base_program_path, application_name
