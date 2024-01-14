import html
import os
import re
import subprocess
import tempfile


def generate_xml_file(file_path: str, first_page: int, last_page: int) -> str:
    """
    Generates XML notation of PDF File.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: XML File Path
    """
    ghostscript = "gs" if os.name != "nt" else "gswin64c"
    temporary_xml_file = tempfile.NamedTemporaryFile(delete=False)
    command_line_args = " ".join([
        ghostscript,
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-sDEVICE=txtwrite",
        "-dTextFormat=1",
        f"-dFirstPage={first_page}" if first_page else "",
        f"-dLastPage={last_page}" if last_page else "",
        f'-sOutputFile="{temporary_xml_file.name}"',
        "-f",
        f'"{file_path}"',
    ])
    _ = subprocess.check_output(command_line_args, shell=ghostscript == "gs")
    with open(temporary_xml_file.name, "r+", encoding="utf-8") as f:
        raw_xml = f.read()
        raw_xml = re.sub(r"(&#x[0-9]+;)", "", raw_xml)
        raw_xml = re.sub(r"(&quot;)", "'", raw_xml)
        raw_xml = html.unescape(raw_xml)
        raw_xml = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]", "", raw_xml)  # Remove invalid XML chars
        raw_xml = raw_xml.replace("&", "&amp;")
        raw_xml = re.sub(r"<(?!/?[a-zA-Z])", "&lt;", raw_xml)
        raw_xml = '<?xml version="1.0" encoding="UTF-8"?><pages>' + raw_xml + "</pages>"
        f.seek(0)
        f.write(raw_xml)
        f.truncate()
    return temporary_xml_file.name
