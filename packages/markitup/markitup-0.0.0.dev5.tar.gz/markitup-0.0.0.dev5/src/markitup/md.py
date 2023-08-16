

def code_block(content: str, lang: str = "") -> str:
    """
    Code block in markdown format.

    Parameters
    ----------
    content : str
        The code to be included in the code block.
    lang : str, optional
        The language of the code, e.g. 'python', 'json', 'bash', 'html'.

    Returns
    -------
    str
        The code block in markdown format.
    """
    return f"\n```{lang}\n{content}\n```\n"
