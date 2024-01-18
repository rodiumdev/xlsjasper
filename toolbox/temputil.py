import os
from pathlib import Path

XML_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/assets/templates/jasper/"
JAVA_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/assets/templates/java/"
TMP_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/temp/java/tmp.java"


def template_to_string(template):
    return Path(XML_PATH + template).read_text()


def java_template_to_string(template):
    return Path(JAVA_PATH + template).read_text()


def tmp_template_to_string():
    text = ""
    if os.path.exists(TMP_PATH):
        text = Path(TMP_PATH).read_text()
        os.remove(TMP_PATH)
    return text
