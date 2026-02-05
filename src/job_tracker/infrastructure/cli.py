def silent_input(text_input: str, *, normalize: bool = True) -> str:
    value = input(text_input)
    print("\033[A\033[K", end="")
    return value.strip().lower() if normalize else value