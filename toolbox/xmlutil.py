from pathlib import Path

XML_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/assets/templates/"


def template_to_string(template):
    return Path(XML_PATH + template).read_text()
