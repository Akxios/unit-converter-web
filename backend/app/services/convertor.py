def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    Преобразуем температуру в разные величины
    """

    if from_unit == to_unit:
        return value

    if from_unit == "c" and to_unit == "f":
        return value * (9 / 5) + 32
    if from_unit == "c" and to_unit == "k":
        return value + 273.15
    if from_unit == "f" and to_unit == "c":
        return (value - 32) * (5 / 9)
    if from_unit == "f" and to_unit == "k":
        return (5 / 9) * (value - 32) + 273.15
    if from_unit == "k" and to_unit == "c":
        return value - 273.15
    if from_unit == "k" and to_unit == "f":
        return (9 / 5) * (value - 273.15) + 32

    raise ValueError("Unsupported temperature unit")


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """
    Преобразуем вес в разные величины
    """

    if from_unit == to_unit:
        return value

    units = {"mg": 0.000001, "g": 0.001, "kg": 1.0, "oz": 0.02835, "lb": 0.45359237}

    if from_unit not in units:
        raise ValueError("Unsupported weight unit")

    if to_unit not in units:
        raise ValueError("Unsupported weight unit")

    return value * units[from_unit] / units[to_unit]


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """
    Преобразуем длину в разные величины
    """

    if from_unit == to_unit:
        return value

    units = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1,
        "km": 1000,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.344,
    }

    if from_unit not in units:
        raise ValueError("Unsupported length unit")

    if to_unit not in units:
        raise ValueError("Unsupported length unit")

    return value * units[from_unit] / units[to_unit]
