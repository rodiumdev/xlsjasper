from PIL import ImageFont


def is_empty(dictionary):
    return len(dictionary) == 0


def print_to_file(output_path, data):
    with open(output_path, "w") as file_writer:
        print(data, file=file_writer)


def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    return int(font.getlength(text))
