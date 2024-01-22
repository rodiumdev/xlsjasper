def is_empty(structure):
    return not structure


def charecter_range(start_column, end_column):
    return list(map(chr, range(ord(start_column), ord(end_column) + 1)))
