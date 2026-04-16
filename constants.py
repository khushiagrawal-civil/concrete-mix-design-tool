# IS 456 Durability
DURABILITY = {
    "mild": {"max_wc": 0.55, "min_cement": 300},
    "moderate": {"max_wc": 0.50, "min_cement": 300},
    "severe": {"max_wc": 0.45, "min_cement": 320},
    "very_severe": {"max_wc": 0.45, "min_cement": 340},
    "extreme": {"max_wc": 0.40, "min_cement": 360},
}

# Minimum grade requirement (IS 456)
MIN_GRADE = {
    "mild": 20,
    "moderate": 25,
    "severe": 30,
    "very_severe": 35,
    "extreme": 40
}

# IS 10262 Standard deviation
STD_DEV = {
    "M20": 4.0,
    "M25": 4.0,
    "M30": 5.0
}

# IS 10262 X values
X_VALUES = {
    "M20": 5.5,
    "M25": 5.5,
    "M30": 6.5
}

# Water content (kg/m³)
WATER_CONTENT = {
    10: 208,
    20: 186,
    40: 165
}

CA_VOLUME = {
    10: {
        "Zone I": 0.48,
        "Zone II": 0.50,
        "Zone III": 0.52,
        "Zone IV": 0.54
    },
    20: {
        "Zone I": 0.60,
        "Zone II": 0.62,
        "Zone III": 0.64,
        "Zone IV": 0.66
    },
    40: {
        "Zone I": 0.69,
        "Zone II": 0.71,
        "Zone III": 0.72,
        "Zone IV": 0.73
    }
}

# Air content
AIR_CONTENT = {
    10: 0.015,
    20: 0.01,
    40: 0.008
}

# max cement
MAX_CEMENT = 450