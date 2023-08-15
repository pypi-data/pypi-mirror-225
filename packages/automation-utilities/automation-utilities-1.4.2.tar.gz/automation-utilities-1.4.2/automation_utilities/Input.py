def int_input(prompt: str, default: int = 1) -> int:
    try:
        return int(input(prompt))
    except ValueError:
        return default
