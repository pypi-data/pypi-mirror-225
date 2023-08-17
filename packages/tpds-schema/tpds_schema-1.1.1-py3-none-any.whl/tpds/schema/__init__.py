import os

# This import is required in order to use the datamodels properly as
# it adds additional validators to the pydantic system
import xsdata_pydantic.bindings  # noqa F401


def get_ecc204_ta010_xsd_path():
    return os.path.join(
        os.path.dirname(__file__), "data", "cryptoauth", "ECC204_TA010_Config_1.1.xsd"
    )


def get_ta100_xsd_path():
    return os.path.join(os.path.dirname(__file__), "data", "trustanchor", "TA100_Config_1.1.xsd")


__all__ = ["get_ecc204_ta010_xsd_path", "get_ta100_xsd_path"]
