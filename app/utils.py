import random
import string

ALPHA_NUM = string.ascii_uppercase + string.ascii_lowercase + string.digits


def generate_name() -> str:
    return "".join(random.choices(ALPHA_NUM, k=20))
