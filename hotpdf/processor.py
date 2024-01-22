import html
import logging
import os
import re
import subprocess
import tempfile
from enum import Enum


class Result(Enum):
    LOADED = 0
    LOCKED = 1
    WRONG_PASSWORD = 2
    UNKNOWN_ERROR = 3


def generate_xml_file(file_path: str, password: str, first_page: int, last_page: int) -> str:
    """Generate XML notation of PDF File.

    Args:
        file_path (str): The path to the PDF file.
        password (str): The password to use to unlock the file
        first_page (int): The first page to extract.
        last_page (int): The last page to extract.
    Raises:
        PermissionError: If the password is missing or wrong
    Returns:
        str: XML File Path
    """
    temp_file_name = tempfile.NamedTemporaryFile(delete=False).name

    result = call_ghostscript(file_path, temp_file_name, password, first_page, last_page)

    handle_gs_result(result)

    clean_xlm(temp_file_name)

    return temp_file_name


def call_ghostscript(file_path: str, temp_file_name: str, password: str, first_page: int, last_page: int) -> Result:
    ghostscript = "gs" if os.name != "nt" else "gswin64c"
    command_line_args = [ghostscript, "-dNOPAUSE", "-dBATCH", "-dSAFER", "-dTextFormat=1", "-sDEVICE=txtwrite"]

    if password:
        command_line_args.append(f'-sPDFPassword="{password}"')
    if first_page:
        command_line_args.append(f"-dFirstPage={first_page}")
    if last_page:
        command_line_args.append(f"-dLastPage={last_page}")

    command_line_args.extend([f'-sOutputFile="{temp_file_name}"', f'"{file_path}"'])
    gs_call = " ".join(command_line_args)

    try:
        output = subprocess.check_output(gs_call, shell=ghostscript == "gs", stderr=subprocess.STDOUT).decode(
            errors="ignore"
        )
        status = validate_gs_output(output)
    except subprocess.CalledProcessError as err:
        status = Result.UNKNOWN_ERROR
        logging.error(err)

    return status


def clean_xlm(temporary_xml_file_name: str) -> None:
    """
    Clean the raw xlm file generated by ghostscript
    Apply changes directly to the temporaryfile.

    Args:
        temporary_xml_file_name (str): the temporary file outputted b
    """
    with open(temporary_xml_file_name, "r+", encoding="utf-8") as f:
        raw_xml = f.read()
        raw_xml = re.sub(r"(&#x[0-9]+;)", "", raw_xml)
        raw_xml = re.sub(r"(&quot;)", "'", raw_xml)
        raw_xml = html.unescape(raw_xml)
        raw_xml = re.sub(
            r"[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]", "", raw_xml
        )  # Remove invalid XML chars
        raw_xml = raw_xml.replace("&", "&amp;")
        raw_xml = re.sub(r"<(?!/?[a-zA-Z])", "&lt;", raw_xml)
        raw_xml = '<?xml version="1.0" encoding="UTF-8"?><pages>' + raw_xml + "</pages>"
        f.seek(0)
        f.write(raw_xml)
        f.truncate()


def validate_gs_output(output: str) -> Result:
    if "This file requires a password for access" in output:
        return Result.LOCKED
    if "Password did not work" in output:
        return Result.WRONG_PASSWORD
    if "Page" in output:
        return Result.LOADED
    return Result.UNKNOWN_ERROR


def handle_gs_result(status: Result) -> None:
    if status == Result.LOADED:
        logging.info("GS: PARSING COMPLETE")
        return

    if status == Result.WRONG_PASSWORD:
        logging.error("GS: WRONG PASSWORD")
        raise PermissionError("Wrong password")

    if status == Result.LOCKED:
        logging.error("GS: FILE IS ENCRYPTED. PROVIDE A PASSWORD")
        raise PermissionError("File is encrypted. You need a password")

    if status == Result.UNKNOWN_ERROR:
        logging.error("GS: UNKNOWN ERROR")
        raise RuntimeError("Unknown error in processing")
