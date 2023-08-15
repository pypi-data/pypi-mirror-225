def format_bytes(size: int) -> dict:
    """
    Nicely format a file size in bytes (int) with an appropriate suffix
    which will output a dict with separate value and suffix key/ value pairs.
    """
    # 2**10 = 1024
    power = 2 ** 10
    n = 0
    power_labels = {0: "", 1: "k", 2: "m", 3: "g", 4: "t"}

    while size > power:
        size /= power
        n += 1

    return {
        "value": size,
        "suffix": power_labels[n] + "b",
    }
