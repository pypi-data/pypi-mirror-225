from goofis_ardihikaru.enums.language import Language


def reformat_name(name: str, about: str, lang: str) -> str:
    # do nothing if this logic below got triggered
    if about is None or len(about) < 0 or len(name) < 0:
        return name
    if lang != Language.INDONESIA.value:
        return name

    # starts converting value
    about_short = about[0:120]  # gets first 120 chars
    if "merupakan" in about_short:
        about_arr = about_short.split("merupakan")
        name = about_arr[0]

    elif "adalah" in about_short:
        about_arr = about_short.split("adalah")
        name = about_arr[0]

    return name.strip()
