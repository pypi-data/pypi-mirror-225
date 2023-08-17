from goofis_ardihikaru.enums.language import Language


def reformat_name(name: str, about: str, lang: str) -> str:
    # do nothing if this logic below got triggered
    if about is None or len(about) < 0 or len(name) < 0:
        return name
    if lang != Language.INDONESIA.value:
        return name

    # splits DOT first
    about_arr = about.split(".")
    about = about_arr[0]

    # starts converting value
    about_short = about[0:120]  # gets first 120 chars
    if "merupakan" in about_short:
        about_arr = about_short.split("merupakan")
        name = about_arr[0]

    elif "adalah" in about[0:120]:
        about_arr = about_short.split("adalah")
        name = about_arr[0]

    if "adalah" in name:
        about_arr = about_short.split("adalah")
        name = about_arr[0]

    # makes it shorter further
    if "atau" in name:
        about_arr = about_short.split("atau")
        name = about_arr[0]

    # makes it shorter further
    if "disingkat" in about_short:
        about_arr = about_short.split("disingkat")
        name = about_arr[0]

    # remove dots if exists
    name_arr = name.split(".")
    name = name_arr[0]

    name = name.replace("Perusahaan Perseroan ", "")

    return name.strip()
