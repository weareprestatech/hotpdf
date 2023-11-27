import os
import tempfile
import subprocess
import html
import re


def generate_xml_file(file_path: str) -> str:
    """
    Generates XML notation of PDF File.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: XML File Path
    """
    ghostscript = "gs" if os.name != "nt" else "gswin64"
    temporary_xml_file = tempfile.NamedTemporaryFile(delete=False)
    command_line_args = " ".join(
        [
            ghostscript,
            "-dNOPAUSE",
            "-dBATCH",
            "-dSAFER",
            "-sDEVICE=txtwrite",
            "-dTextFormat=0",
            f'-sOutputFile="{temporary_xml_file.name}"',
            "-f",
            f'"{file_path}"',
        ]
    )
    _ = subprocess.check_output(command_line_args, shell=ghostscript == "gs")
    with open(temporary_xml_file.name, "r+") as f:
        raw_xml = f.read()
        raw_xml = re.sub(r"(&#x[0-9]+;)", "", raw_xml)
        raw_xml = re.sub(r"(&quot;)", "'", raw_xml)
        raw_xml = html.unescape(raw_xml)
        raw_xml = html.escape(raw_xml)
        raw_xml = '<?xml version="1.0" encoding="UTF-8"?><pages>' + raw_xml + "</pages>"
        f.seek(0)
        f.write(raw_xml)
        f.truncate()
    return temporary_xml_file.name
