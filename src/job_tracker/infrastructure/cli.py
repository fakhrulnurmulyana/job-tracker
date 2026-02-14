def silent_input(
        text_input: str, 
        *, 
        normalize: bool = True
) -> str:
    """
    Prompt user input and remove the prompt line from the console.

    This function captures user input and immediately clears the
    previous console line using ANSI escape sequences. Optionally,
    the returned value can be normalized by stripping whitespace
    and converting it to lowercase.

    Args:
        text_input (str): Prompt text displayed to the user.
        normalize (bool, optional): Whether to strip whitespace and
            convert the input to lowercase. Defaults to True.

    Returns:
        str: User input, optionally normalized.
    """
    value = input(text_input)
    print("\033[A\033[K", end="")
    return value.strip().lower() if normalize else value