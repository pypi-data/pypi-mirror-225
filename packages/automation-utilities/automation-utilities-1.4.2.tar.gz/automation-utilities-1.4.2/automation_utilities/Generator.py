import random
import string
from names import get_first_name


def generate_email(domain: str, name: str = get_first_name(), username_length: int = random.randint(10, 15)):
    return f'{name}{"".join(random.choice(string.digits) for _ in range(username_length - len(name)))}@{domain}'


def generate_password(length: int = random.randint(10, 20)):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
