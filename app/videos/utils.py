from app import utils


def parse_file_extension(file_name: str):
    file_name = file_name.split(".")
    if len(file_name) <= 1:
        return ""

    return f".{file_name[-1]}"


def generate_file_path(file_name: str):
    file_extension = parse_file_extension(file_name)
    generated_file_name = utils.generate_name()

    return f"media/{generated_file_name}{file_extension}"
