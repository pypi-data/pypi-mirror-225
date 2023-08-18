import enum


class PythonVersion(enum.Enum):
    PYTHON_3_8 = "3.8"
    PYTHON_3_9 = "3.9"
    PYTHON_3_10 = "3.10"
    PYTHON_3_11 = "3.11"


class Hardware(enum.Enum):
    CPU = "CPU"
    GPU = "GPU"
    A10 = "A10"
    TURING_4000 = "TURING_4000"
    TURING_5000 = "TURING_5000"
    AMPERE_A4000 = "AMPERE_A4000"
    AMPERE_A5000 = "AMPERE_A5000"
    AMPERE_A6000 = "AMPERE_A6000"
    AMPERE_A100 = "AMPERE_A100"
