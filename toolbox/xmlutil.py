from pathlib import Path

xml_path = "C:/Programming/scripts_queries/scripts/jasper/assets/templates/"


def template_to_string(template):
    return Path(xml_path + template).read_text()
