from typing import Optional

from dotenv import load_dotenv, find_dotenv
import typer

from lupin_danquin.core.tools.utils import (
    configure_logging,
    convert_application_name_to_list,
    read_file,
)

from lupin_danquin.core.coding_rules_validator.coging_rules_validator import (
    CodingRulesValidator,
)
from lupin_danquin.core.val3_doc_generator.val3_doc_generator import Val3Documentation
from lupin_danquin import __version__


load_dotenv(find_dotenv(usecwd=True))

cli = typer.Typer()
configure_logging()


@cli.command(help="Print version")
def version():
    print(f"Version: {__version__}")


@cli.command()
def valdocs(
    application_names: str = typer.Argument(
        ...,
        help="Name of applications to be documented. Ex: 'app1,app2,subfolders/app3'",
        envvar="VAL3_APPLICATIONS",
    ),
    beginning_file_path: Optional[str] = typer.Option(
        None,
        "--beginning-file-path",
        "-b",
        help="Path to the file containing the beginning content of the documentation",
        envvar="VAL3_BEGINNING_FILE_PATH",
    ),
    end_file_path: Optional[str] = typer.Option(
        None,
        "--end-file-path",
        "-e",
        help="Path to the file containing the end content of the documentation",
        envvar="VAL3_END_FILE_PATH",
    ),
):
    """
    Generate documentation from VAL3 applications in usrapp directory or its sub-folders.
    You can specify the applications to be documented in the 'danq valdocs' command
    or by setting the VAL3_APPLICATIONS, VAL3_BEGINNING_FILE_PATH and VAL3_END_FILE_PATH environment variable.
    :param application_names: Name of applications to be documented. Ex: app1,app2,subfolders/app3
    :type application_names: str
    :param beginning_file_path: Path to the file containing the beginning content of the documentation
    :type beginning_file_path: str
    :param end_file_path: Path to the file containing the end content of the documentation
    :type end_file_path: str
    :example: danq valdocs "App1,App2,subfolders/app3" --beginning-file-path "beginning.txt" --end-file-path "end.txt"
    or danq valdocs "App1,App2,subfolders/app3," -b "beginning.txt" -e "end.txt"
    """
    applications_list = convert_application_name_to_list(application_names)

    if not beginning_file_path:
        begining_of_file = ""
    else:
        begining_of_file = read_file(beginning_file_path)
    if not end_file_path:
        end_of_file = ""
    else:
        end_of_file = read_file(end_file_path)

    Val3Documentation().generate_markdown(
        applications_list, begining_of_file, end_of_file
    )


@cli.command()
def check_coding_rules(
    application_names: str = typer.Argument(
        ...,
        help="Name of applications to be check. Ex: 'app1,app2,subfolders/app3'",
        envvar="VAL3_APPLICATIONS",
    )
):
    """
    Check coding rules
    """

    applications_list = convert_application_name_to_list(application_names)

    check_coding_rules = CodingRulesValidator(applications_list)
    check_coding_rules.validate()
