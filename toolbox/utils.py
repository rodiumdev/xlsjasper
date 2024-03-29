import re
import os
import unicodedata

from PIL import ImageFont


def is_empty(dictionary):
    return len(dictionary) == 0


def print_to_file(output_path, data):
    with open(output_path, "w") as file_writer:
        print(data, file=file_writer)


def append_to_file(output_path, data):
    with open(output_path, "a") as file_writer:
        print("\n" + data + "\n", file=file_writer)


def del_file(tmp_path):
    os.remove(tmp_path)


def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    return int(font.getlength(text))


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def to_java_variable(variable):
    variable = re.sub(r"\([^)]*\)|\([^)]*", "", variable).replace("_", "").replace("-", "").strip().split(" ")
    capitalized_words = [word.capitalize() for word in variable[1:]]
    return remove_accents(variable[0].lower() + "".join(capitalized_words))


def to_java_variable_cap(variable):
    variable = re.sub(r"\([^)]*\)|\([^)]*", "", variable).replace("_", " ").replace("-", "").strip().split(" ")
    capitalized_words = [word.capitalize() for word in variable[1:]]
    return remove_accents(variable[0].lower() + "".join(capitalized_words))


def to_java_object(variable):
    variable = re.sub(r"\([^)]*\)|\([^)]*", "", variable).replace("_", " ").replace("-", "").strip().split(" ")
    capitalized_words = [word.capitalize() for word in variable[1:]]
    return remove_accents(variable[0].lower() + "".join(capitalized_words))


def to_java_class(variable):
    variable = re.sub(r"\([^)]*\)|\([^)]*", "", variable).replace("_", " ").replace("-", "").strip().split(" ")
    capitalized_words = [word.capitalize() for word in variable[1:]]
    return remove_accents(variable[0].capitalize() + "".join(capitalized_words))
