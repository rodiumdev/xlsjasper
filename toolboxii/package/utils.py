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
