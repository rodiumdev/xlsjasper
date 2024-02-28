import unicodedata
import re


def is_empty(structure):
    return not structure


def charecter_range(start_column, end_column):
    return list(map(chr, range(ord(start_column), ord(end_column) + 1)))


def header_text(text):
    return normalize_whitespace(text.lower().capitalize())


def normalize_whitespace(text):
    return " ".join(text.strip().split())


def print_to_file(output_path, data):
    with open(output_path, "w") as file_writer:
        print(data, file=file_writer)


def append_to_file(output_path, data):
    with open(output_path, "a") as file_writer:
        print("\n" + data + "\n", file=file_writer)


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def clean_brackets(variable):
    return re.sub(r"\([^)]*\)|\([^)]*", "", variable)


def to_variable(variable):
    variable = re.sub(r"\([^)]*\)|\([^)]*", "", variable).replace("_", " ").replace("-", "").strip().split(" ")
    capitalized_words = [word.capitalize() for word in variable[1:]]
    return remove_accents(variable[0].lower() + "".join(capitalized_words))


def to_class(variable):
    variable = re.sub(r"\([^)]*\)|\([^)]*", "", variable).replace("_", " ").replace("-", "").strip().split(" ")
    capitalized_words = [word.capitalize() for word in variable[1:]]
    return remove_accents(variable[0].capitalize() + "".join(capitalized_words))
