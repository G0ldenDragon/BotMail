import os


def language_selector(sentence: dict[str, str]):
    return sentence[os.getenv("LANGUAGE")]