def is_empty(dictionary):
    return len(dictionary) == 0


def print_to_file(output_path, data):
    with open(output_path, "w") as file_writer:
        print(data, file=file_writer)
