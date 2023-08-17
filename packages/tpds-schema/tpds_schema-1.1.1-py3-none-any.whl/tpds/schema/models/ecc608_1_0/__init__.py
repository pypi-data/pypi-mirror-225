from .ecc608_config_1_0 import Ecc608Config


class Ecc608AConfig(Ecc608Config):
    class Meta:
        name = "ATECC608A"


class Ecc608BConfig(Ecc608Config):
    class Meta:
        name = "ATECC608B"


__all__ = ["Ecc608Config", "Ecc608AConfig", "Ecc608BConfig"]
