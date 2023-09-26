import re
import unicodedata
from PIL import ImageFont


def is_empty(dictionary):
    return len(dictionary) == 0


def print_to_file(output_path, data):
    with open(output_path, "w") as file_writer:
        print(data, file=file_writer)


def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    return int(font.getlength(text))


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def to_java_variable(variable):
    variable = re.sub(r"\([^)]*\)", "", variable).replace("_", "").replace("-", "").strip().split(" ")
    capitalized_words = [word.capitalize() for word in variable[1:]]
    return remove_accents(variable[0].lower() + "".join(capitalized_words))
