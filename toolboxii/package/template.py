import os
from pathlib import Path
from package import config


XML_PATH = config.XML_PATH
JAVA_PATH = config.JAVA_PATH
TMP_PATH = config.TMP_PATH


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
