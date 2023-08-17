from dataclasses import field
from enum import Enum
from pydantic.dataclasses import dataclass
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDateTime, XmlDuration

__NAMESPACE__ = "https://www.microchip.com/schema/ECC204_TA010_Config_1.1"


class AsymmetricSecretBinaryEncodingEnum(Enum):
    HEX = "Hex"
    BASE64 = "Base64"
    PEM = "PEM"


class BooleanType(Enum):
    """
    Boolean enumeration.
    """
    TRUE = "True"
    FALSE = "False"


class ByteOrderType(Enum):
    BIG = "Big"
    LITTLE = "Little"


class ChipModeCmosEn(Enum):
    FIXED_REFERENCE = "Fixed_Reference"
    VCC_REFERENCED = "VCC_Referenced"


class ChipModeClockDivider(Enum):
    VALUE_4 = "4"
    VALUE_2 = "2"
    VALUE_1 = "1"
    VALUE_0B11 = "0b11"


class ConfigurationSubzone0TypeValue(Enum):
    NORMAL = "Normal"
    DATA_SLOTS_DELETED = "Data_Slots_Deleted"


@dataclass
class DataBase64:
    """
    Binary data encoded in Base64.
    """
    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"[\sA-Za-z0-9+/]*[\s=]*",
        }
    )
    encoding: str = field(
        init=False,
        default="Base64",
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class DataHex10BytesEncoding(Enum):
    HEX = "Hex"


class DataHex11BytesEncoding(Enum):
    HEX = "Hex"


class DataHex12BytesEncoding(Enum):
    HEX = "Hex"


class DataHex13BytesEncoding(Enum):
    HEX = "Hex"


class DataHex14BytesEncoding(Enum):
    HEX = "Hex"


class DataHex15BytesEncoding(Enum):
    HEX = "Hex"


class DataHex16BytesEncoding(Enum):
    HEX = "Hex"


class DataHex1ByteEncoding(Enum):
    HEX = "Hex"


class DataHex2BytesEncoding(Enum):
    HEX = "Hex"


class DataHex3BytesEncoding(Enum):
    HEX = "Hex"


class DataHex4BytesEncoding(Enum):
    HEX = "Hex"


class DataHex5BytesEncoding(Enum):
    HEX = "Hex"


class DataHex6BytesEncoding(Enum):
    HEX = "Hex"


class DataHex7BytesEncoding(Enum):
    HEX = "Hex"


class DataHex8BytesEncoding(Enum):
    HEX = "Hex"


class DataHex9BytesEncoding(Enum):
    HEX = "Hex"


@dataclass
class DataSourcesWriterType:
    """
    :ivar source_name: The name of the source of data, whether that is a
        named Data_Source item or Function.
    :ivar description:
    :ivar target:
    """
    source_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Source_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    target: Optional[str] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"Slot (0|[1-9][0-9]*)",
        }
    )


class DataTypeEnum(Enum):
    BYTES = "Bytes"
    ECC_PRIVATE_KEY = "ECC_Private_Key"
    ECC_PUBLIC_KEY = "ECC_Public_Key"
    RSA_PRIVATE_KEY = "RSA_Private_Key"
    RSA_PUBLIC_KEY = "RSA_Public_Key"
    DATE_TIME = "Date_Time"


@dataclass
class DateTimeModifyType:
    input: Optional[str] = field(
        default=None,
        metadata={
            "name": "Input",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    add_period: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "Add_Period",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


class DefinitionEncoding(Enum):
    STRING_UTF8 = "String_UTF8"
    HEX = "Hex"


class EcccurveEnum(Enum):
    SECP160K1 = "secp160k1"
    SECP160R1 = "secp160r1"
    SECP160R2 = "secp160r2"
    SECT163K1 = "sect163k1"
    SECT163R1 = "sect163r1"
    SECT163R2 = "sect163r2"
    SECP192K1 = "secp192k1"
    SECP192R1 = "secp192r1"
    SECT193R1 = "sect193r1"
    SECT193R2 = "sect193r2"
    SECP224K1 = "secp224k1"
    SECP224R1 = "secp224r1"
    SECT233K1 = "sect233k1"
    SECT233R1 = "sect233r1"
    SECT239K1 = "sect239k1"
    SECP256K1 = "secp256k1"
    SECP256R1 = "secp256r1"
    SECP384R1 = "secp384r1"
    SECP521R1 = "secp521r1"
    BRAINPOOL_P160R1 = "brainpoolP160r1"
    BRAINPOOL_P160T1 = "brainpoolP160t1"
    BRAINPOOL_P192T1 = "brainpoolP192t1"
    BRAINPOOL_P224R1 = "brainpoolP224r1"
    BRAINPOOL_P224T1 = "brainpoolP224t1"
    BRAINPOOL_P256R1 = "brainpoolP256r1"
    BRAINPOOL_P256T1 = "brainpoolP256t1"
    BRAINPOOL_P320R1 = "brainpoolP320r1"
    BRAINPOOL_P320T1 = "brainpoolP320t1"
    BRAINPOOL_P384R1 = "brainpoolP384r1"
    BRAINPOOL_P384T1 = "brainpoolP384t1"
    BRAINPOOL_P512R1 = "brainpoolP512r1"
    BRAINPOOL_P512T1 = "brainpoolP512t1"


class EccpublicKeyFormatEnum(Enum):
    """
    :cvar RAW_XY: X and Y integers as big endian unsigned bytes.
    :cvar UNCOMPRESSED_POINT: Uncompressed elliptic curve point as
        defined by ANSI X9.62 section 4.3.6 and SEC1 v2.0.
    :cvar COMPRESSED_POINT: Compressed elliptic curve point as defined
        by ANSI X9.62 section 4.3.6 and SEC1 v2.0.
    :cvar SUBJECT_PUBLIC_KEY_INFO: ASN.1 DER encoded
        SubjectPublicKeyInfo as defined in RFC 5280 and RFC 3279. Public
        key will be an uncompressed point.
    :cvar SUBJECT_PUBLIC_KEY_INFO_COMPRESSED_POINT: ASN.1 DER encoded
        SubjectPublicKeyInfo as defined in RFC 5280 and RFC 3279. Public
        key will be a compressed point.
    """
    RAW_XY = "Raw_XY"
    UNCOMPRESSED_POINT = "Uncompressed_Point"
    COMPRESSED_POINT = "Compressed_Point"
    SUBJECT_PUBLIC_KEY_INFO = "Subject_Public_Key_Info"
    SUBJECT_PUBLIC_KEY_INFO_COMPRESSED_POINT = "Subject_Public_Key_Info_Compressed_Point"


class EccFormat(Enum):
    UNCOMPRESSED = "Uncompressed"
    COMPRESSED = "Compressed"


class EcdsasignatureFormatEnum(Enum):
    """
    :cvar RAW_RS: R and S integers as big endian unsigned bytes.
    :cvar ECDSA_SIG_VALUE: ASN.1 DER encoded Ecdsa-Sig-Value as defined
        in RFC 3279 section 2.2.3.
    """
    RAW_RS = "Raw_RS"
    ECDSA_SIG_VALUE = "ECDSA_Sig_Value"


class EncryptionAlgorithmEnum(Enum):
    AES256_GCM = "AES256_GCM"


class FixedSizeAlignment(Enum):
    PAD_RIGHT = "Pad_Right"
    PAD_LEFT = "Pad_Left"


@dataclass
class GenerateKeyRsatype:
    class Meta:
        name = "GenerateKeyRSAType"

    key_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "Key_Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "min_inclusive": 512,
        }
    )
    exponent: Optional[str] = field(
        default=None,
        metadata={
            "name": "Exponent",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"0x([0-9a-fA-F]{2})+",
        }
    )


class HashAlgorithmAndNoneEnum(Enum):
    NONE = "None"
    SHA1 = "SHA1"
    SHA224 = "SHA224"
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    SHA512 = "SHA512"


class HashAlgorithmEnum(Enum):
    SHA1 = "SHA1"
    SHA224 = "SHA224"
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    SHA512 = "SHA512"


class IdMethodIssuerAndSerialNumber(Enum):
    FROM_CA = "From_CA"


class IoOptionsInterface(Enum):
    SWI_PWM = "SWI_PWM"
    I2_C = "I2C"


class KeyIdentifierCalculatedEnum(Enum):
    RFC5280_METHOD1 = "RFC5280_Method1"
    RFC5280_METHOD2 = "RFC5280_Method2"
    RFC7093_METHOD1 = "RFC7093_Method1"
    RFC7093_METHOD2 = "RFC7093_Method2"
    RFC7093_METHOD3 = "RFC7093_Method3"
    RFC7093_METHOD4_SHA256 = "RFC7093_Method4_SHA256"
    RFC7093_METHOD4_SHA384 = "RFC7093_Method4_SHA384"
    RFC7093_METHOD4_SHA512 = "RFC7093_Method4_SHA512"


class MultipleAlignment(Enum):
    PAD_RIGHT = "Pad_Right"
    PAD_LEFT = "Pad_Left"


class PublicBinaryEncodingEnum(Enum):
    HEX = "Hex"
    BASE64 = "Base64"
    STRING_UTF8 = "String_UTF8"


class PublicDataTypeEnum(Enum):
    BYTES = "Bytes"
    ECC_PUBLIC_KEY = "ECC_Public_Key"
    RSA_PUBLIC_KEY = "RSA_Public_Key"
    DATE_TIME = "Date_Time"


@dataclass
class QiCertificateChainType:
    root_ca_certificate: Optional[str] = field(
        default=None,
        metadata={
            "name": "Root_CA_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    manufacturer_ca_certificate: Optional[str] = field(
        default=None,
        metadata={
            "name": "Manufacturer_CA_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    product_unit_certificate: Optional[str] = field(
        default=None,
        metadata={
            "name": "Product_Unit_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )


class RsapublicKeyFormatEnum(Enum):
    """
    :cvar SUBJECT_PUBLIC_KEY_INFO: ASN.1 DER encoded
        SubjectPublicKeyInfo as defined in RFC 5280 and RFC 3279.
    """
    SUBJECT_PUBLIC_KEY_INFO = "Subject_Public_Key_Info"


class RsasignatureFormatEnum(Enum):
    """
    :cvar RSA_SIGNATURE: S integer as big endian bytes.
    """
    RSA_SIGNATURE = "RSA_Signature"


@dataclass
class ReferenceMappingsType:
    """
    :ivar database_record_set_name: Customer database record set name
    :ivar counter_name: Customer counter name
    """
    database_record_set_name: List["ReferenceMappingsType.DatabaseRecordSetName"] = field(
        default_factory=list,
        metadata={
            "name": "Database_Record_Set_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    counter_name: List["ReferenceMappingsType.CounterName"] = field(
        default_factory=list,
        metadata={
            "name": "Counter_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )

    @dataclass
    class DatabaseRecordSetName:
        external: Optional[str] = field(
            default=None,
            metadata={
                "name": "External",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        internal: Optional[str] = field(
            default=None,
            metadata={
                "name": "Internal",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )

    @dataclass
    class CounterName:
        external: Optional[str] = field(
            default=None,
            metadata={
                "name": "External",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        internal: Optional[str] = field(
            default=None,
            metadata={
                "name": "Internal",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )


class SecretBinaryEncodingEnum(Enum):
    HEX = "Hex"
    BASE64 = "Base64"


class SignatureAlgorithmRsapsstypeTrailerField(Enum):
    VALUE_0X_BC = "0xBC"


class SlotConfig3WriteMode(Enum):
    CLEAR = "Clear"
    ENCRYPTED = "Encrypted"


@dataclass
class StaticPrivateKeyPublicType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    encoding: str = field(
        init=False,
        default="PEM",
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    format: str = field(
        init=False,
        default="PKCS8",
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class StaticPublicKeyPublicType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    encoding: str = field(
        init=False,
        default="PEM",
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    format: str = field(
        init=False,
        default="Subject_Public_Key_Info",
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class StringCaseType(Enum):
    UPPER = "Upper"
    LOWER = "Lower"


class X509BasicConstraintsTypeValue(Enum):
    NO_LIMIT = "No_Limit"


@dataclass
class X509CacertificateChainType:
    class Meta:
        name = "X509CACertificateChainType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    encoding: str = field(
        init=False,
        default="PEM",
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class X509IssuerUniqueIdtype(Enum):
    FROM_CA_SUBJECT_UNIQUE_ID = "From_CA_Subject_Unique_ID"


class X509SignatureAlgorithmRsapsstypeTrailerField(Enum):
    VALUE_0X_BC = "0xBC"


class X509TimeTypeType(Enum):
    AUTO = "Auto"
    UTC_TIME = "UTC_Time"
    GENERALIZED_TIME = "Generalized_Time"


class X509VersionType(Enum):
    V1 = "V1"
    V2 = "V2"
    V3 = "V3"


class X520DirectoryStringOrFromSourceTypeType(Enum):
    RAW = "Raw"
    PRINTABLE_STRING = "Printable_String"
    UTF8_STRING = "UTF8_String"


class X520Ia5StringOrFromSourceTypeType(Enum):
    RAW = "Raw"
    IA5_STRING = "IA5_String"


class X520PrintableStringOrFromSourceTypeType(Enum):
    RAW = "Raw"
    PRINTABLE_STRING = "Printable_String"


@dataclass
class BytesEncodeHexType:
    case: Optional[StringCaseType] = field(
        default=None,
        metadata={
            "name": "Case",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    separator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Separator",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class BytesPadType:
    input: Optional[str] = field(
        default=None,
        metadata={
            "name": "Input",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    fixed_size: Optional["BytesPadType.FixedSize"] = field(
        default=None,
        metadata={
            "name": "Fixed_Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    multiple: Optional["BytesPadType.Multiple"] = field(
        default=None,
        metadata={
            "name": "Multiple",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )

    @dataclass
    class FixedSize:
        output_size: Optional[int] = field(
            default=None,
            metadata={
                "name": "Output_Size",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        pad_byte: Optional[str] = field(
            default=None,
            metadata={
                "name": "Pad_Byte",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
                "pattern": r"0x0*[0-9a-fA-F]{2}",
            }
        )
        alignment: Optional[FixedSizeAlignment] = field(
            default=None,
            metadata={
                "name": "Alignment",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )

    @dataclass
    class Multiple:
        multiple_size: Optional[int] = field(
            default=None,
            metadata={
                "name": "Multiple_Size",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        pad_byte: Optional[str] = field(
            default=None,
            metadata={
                "name": "Pad_Byte",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
                "pattern": r"0x0*[0-9a-fA-F]{2}",
            }
        )
        alignment: Optional[MultipleAlignment] = field(
            default=None,
            metadata={
                "name": "Alignment",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )


@dataclass
class ClientDeviceDataItem:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    type: Optional[PublicDataTypeEnum] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class CounterType:
    counter_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Counter_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    size: Optional[int] = field(
        default=None,
        metadata={
            "name": "Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    byte_order: Optional[ByteOrderType] = field(
        default=None,
        metadata={
            "name": "Byte_Order",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    signed: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Signed",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class DerbinaryDataOrFromSourceType:
    class Meta:
        name = "DERBinaryDataOrFromSourceType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    from_source: Optional[BooleanType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    encoding: Optional[SecretBinaryEncodingEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class DataHex10Bytes:
    """
    10 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-10bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){10}",
        }
    )
    encoding: Optional[DataHex10BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex11Bytes:
    """
    11 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-11bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){11}",
        }
    )
    encoding: Optional[DataHex11BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex12Bytes:
    """
    12 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-12bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){12}",
        }
    )
    encoding: Optional[DataHex12BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex13Bytes:
    """
    13 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-13bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){13}",
        }
    )
    encoding: Optional[DataHex13BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex14Bytes:
    """
    14 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-14bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){14}",
        }
    )
    encoding: Optional[DataHex14BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex15Bytes:
    """
    15 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-15bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){15}",
        }
    )
    encoding: Optional[DataHex15BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex16Bytes:
    """
    16 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-16bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){16}",
        }
    )
    encoding: Optional[DataHex16BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex1Byte:
    """
    1 byte of binary data encoded as a hex octet.
    """
    class Meta:
        name = "DataHex-1byte"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        }
    )
    encoding: Optional[DataHex1ByteEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex2Bytes:
    """
    2 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-2bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
        }
    )
    encoding: Optional[DataHex2BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex3Bytes:
    """
    3 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-3bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){3}",
        }
    )
    encoding: Optional[DataHex3BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex4Bytes:
    """
    4 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-4bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){4}",
        }
    )
    encoding: Optional[DataHex4BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex5Bytes:
    """
    5 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-5bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){5}",
        }
    )
    encoding: Optional[DataHex5BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex6Bytes:
    """
    6 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-6bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){6}",
        }
    )
    encoding: Optional[DataHex6BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex7Bytes:
    """
    7 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-7bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){7}",
        }
    )
    encoding: Optional[DataHex7BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex8Bytes:
    """
    8 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-8bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){8}",
        }
    )
    encoding: Optional[DataHex8BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataHex9Bytes:
    """
    9 bytes of binary data encoded as hex octets.
    """
    class Meta:
        name = "DataHex-9bytes"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){9}",
        }
    )
    encoding: Optional[DataHex9BytesEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DataSourcesWrappedKeyType:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    key: Optional["DataSourcesWrappedKeyType.Key"] = field(
        default=None,
        metadata={
            "name": "Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    wrapping_public_key: Optional["DataSourcesWrappedKeyType.WrappingPublicKey"] = field(
        default=None,
        metadata={
            "name": "Wrapping_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class Key:
        value: str = field(
            default="",
            metadata={
                "required": True,
            }
        )
        algorithm: str = field(
            init=False,
            default="RSA_OAEP_SHA256",
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        encoding: Optional[SecretBinaryEncodingEnum] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )

    @dataclass
    class WrappingPublicKey:
        value: str = field(
            default="",
            metadata={
                "required": True,
            }
        )
        encoding: str = field(
            init=False,
            default="PEM",
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        format: str = field(
            init=False,
            default="Subject_Public_Key_Info",
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )


@dataclass
class DatabaseDataFieldType:
    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }
    )
    type: Optional[DataTypeEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class GenerateKeyEcctype:
    """
    :ivar curve:
    :ivar compact: If True, the generated key pair will have a public
        key that can be represented by the ECC Compact form as defined
        in https://tools.ietf.org/id/draft-jivsov-ecc-compact-05.html
    """
    class Meta:
        name = "GenerateKeyECCType"

    curve: Optional[EcccurveEnum] = field(
        default=None,
        metadata={
            "name": "Curve",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    compact: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Compact",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class HsmrandomType:
    class Meta:
        name = "HSMRandomType"

    size: Optional[int] = field(
        default=None,
        metadata={
            "name": "Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "min_inclusive": 1,
        }
    )
    secret_data: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Secret_Data",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class HashType:
    input: Optional[str] = field(
        default=None,
        metadata={
            "name": "Input",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    algorithm: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class KeyIdentifierCalculatedType:
    """
    :ivar method:
    :ivar truncated_size: Override the default key ID size for the
        chosen method.
    """
    method: Optional[KeyIdentifierCalculatedEnum] = field(
        default=None,
        metadata={
            "name": "Method",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    truncated_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "Truncated_Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class PublicBinaryDataType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    encoding: Optional[PublicBinaryEncodingEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class PublicKeyEncodeType:
    input: Optional[str] = field(
        default=None,
        metadata={
            "name": "Input",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    ecc_format: Optional[EccpublicKeyFormatEnum] = field(
        default=None,
        metadata={
            "name": "ECC_Format",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    rsa_format: Optional[RsapublicKeyFormatEnum] = field(
        default=None,
        metadata={
            "name": "RSA_Format",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class SecretBinaryDataBaseType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    encrypted: Optional[BooleanType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    algorithm: Optional[EncryptionAlgorithmEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    key_name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }
    )


@dataclass
class SignatureAlgorithmEcdsatype:
    class Meta:
        name = "SignatureAlgorithmECDSAType"

    hash: Optional[HashAlgorithmAndNoneEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class SignatureAlgorithmRsa15Type:
    class Meta:
        name = "SignatureAlgorithmRSA15Type"

    hash: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class SignatureAlgorithmRsapsstype:
    class Meta:
        name = "SignatureAlgorithmRSAPSSType"

    hash: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    mask_generation_function: Optional["SignatureAlgorithmRsapsstype.MaskGenerationFunction"] = field(
        default=None,
        metadata={
            "name": "Mask_Generation_Function",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    salt_length: Optional[int] = field(
        default=None,
        metadata={
            "name": "Salt_Length",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    trailer_field: Optional[SignatureAlgorithmRsapsstypeTrailerField] = field(
        default=None,
        metadata={
            "name": "Trailer_Field",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class MaskGenerationFunction:
        mgf1: Optional["SignatureAlgorithmRsapsstype.MaskGenerationFunction.Mgf1"] = field(
            default=None,
            metadata={
                "name": "MGF1",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )

        @dataclass
        class Mgf1:
            hash: Optional[HashAlgorithmEnum] = field(
                default=None,
                metadata={
                    "name": "Hash",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                    "required": True,
                }
            )


@dataclass
class SignatureEncodingType:
    ecdsa_format: Optional[EcdsasignatureFormatEnum] = field(
        default=None,
        metadata={
            "name": "ECDSA_Format",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    rsa_format: Optional[RsasignatureFormatEnum] = field(
        default=None,
        metadata={
            "name": "RSA_Format",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class SlotLocksType:
    class Meta:
        name = "Slot_Locks_Type"

    slot_0: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Slot_0",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    slot_1: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Slot_1",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    slot_2: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Slot_2",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    slot_3: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Slot_3",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class StringOrDataOrFromSourceType:
    """Base type for specifying static data or dynamic data from a data source.

    When from_source attribute is set to False, this indicates static
    data and the encoding attribute must be used to indicate how the
    data is encoded. Hex and Base64 are for expressing raw binary
    values. String_UTF8 indicates the element contents should be used as
    is. When from_source attribute is True, the element contains a data
    source reference for where to get the dynamic data from. The
    encoding attribute has no meaning in this case and should be
    omitted.
    """
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    from_source: Optional[BooleanType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    encoding: Optional[PublicBinaryEncodingEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class TemplateType:
    definition: Optional["TemplateType.Definition"] = field(
        default=None,
        metadata={
            "name": "Definition",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class Definition:
        value: str = field(
            default="",
            metadata={
                "required": True,
                "pattern": r"([^{]+|\{[^}]+\}|\{\{)*",
            }
        )
        encoding: Optional[DefinitionEncoding] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )


@dataclass
class X509BasicConstraintsType:
    critical: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Critical",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    ca: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "CA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    path_len_constraint: Optional[X509BasicConstraintsTypeValue] = field(
        default=None,
        metadata={
            "name": "Path_Len_Constraint",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class X509CertificateOrFromSource:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    from_source: Optional[BooleanType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    format: str = field(
        init=False,
        default="PEM",
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class X509ExtendedKeyUsageType:
    critical: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Critical",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    key_purpose_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "Key_Purpose_Id",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "pattern": r"[0-9]+(\.[0-9]+)*",
        }
    )


@dataclass
class X509KeyUsageType:
    critical: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Critical",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    digital_signature: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Digital_Signature",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    content_commitment: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Content_Commitment",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    key_encipherment: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Key_Encipherment",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    data_encipherment: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Data_Encipherment",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    key_agreement: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Key_Agreement",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    key_cert_sign: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Key_Cert_Sign",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    crl_sign: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "CRL_Sign",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    encipher_only: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Encipher_Only",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    decipher_only: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Decipher_Only",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class X509SerialNumberType:
    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    from_source: BooleanType = field(
        init=False,
        default=BooleanType.TRUE,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class X509SignatureAlgorithmEcdsatype:
    class Meta:
        name = "X509SignatureAlgorithmECDSAType"

    hash: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class X509SignatureAlgorithmRsa15Type:
    class Meta:
        name = "X509SignatureAlgorithmRSA15Type"

    hash: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class X509SignatureAlgorithmRsapsstype:
    class Meta:
        name = "X509SignatureAlgorithmRSAPSSType"

    hash: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    mask_generation_function: Optional["X509SignatureAlgorithmRsapsstype.MaskGenerationFunction"] = field(
        default=None,
        metadata={
            "name": "Mask_Generation_Function",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    salt_length: Optional[int] = field(
        default=None,
        metadata={
            "name": "Salt_Length",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    trailer_field: Optional[X509SignatureAlgorithmRsapsstypeTrailerField] = field(
        default=None,
        metadata={
            "name": "Trailer_Field",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class MaskGenerationFunction:
        mgf1: Optional["X509SignatureAlgorithmRsapsstype.MaskGenerationFunction.Mgf1"] = field(
            default=None,
            metadata={
                "name": "MGF1",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )

        @dataclass
        class Mgf1:
            hash: Optional[HashAlgorithmEnum] = field(
                default=None,
                metadata={
                    "name": "Hash",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                    "required": True,
                }
            )


@dataclass
class X509SubjectPublicKeyInfoType:
    key: Optional["X509SubjectPublicKeyInfoType.Key"] = field(
        default=None,
        metadata={
            "name": "Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    options: Optional["X509SubjectPublicKeyInfoType.Options"] = field(
        default=None,
        metadata={
            "name": "Options",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )

    @dataclass
    class Key:
        value: str = field(
            default="",
            metadata={
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )
        from_source: BooleanType = field(
            init=False,
            default=BooleanType.TRUE,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )

    @dataclass
    class Options:
        ecc: Optional["X509SubjectPublicKeyInfoType.Options.Ecc"] = field(
            default=None,
            metadata={
                "name": "ECC",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )

        @dataclass
        class Ecc:
            format: Optional[EccFormat] = field(
                default=None,
                metadata={
                    "name": "Format",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                    "required": True,
                }
            )


@dataclass
class X509SubjectUniqueIdtype:
    class Meta:
        name = "X509SubjectUniqueIDType"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    from_source: BooleanType = field(
        init=False,
        default=BooleanType.TRUE,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class X509TimeType:
    value: str = field(
        default="",
        metadata={
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    type: Optional[X509TimeTypeType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    from_source: Optional[BooleanType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class AsymmetricSecretBinaryDataType(SecretBinaryDataBaseType):
    """
    :ivar encoding: PEM encoding is only intended to be specified when
        the config has unencrypted secret values. Once encrypted, the
        encoding should be changed to one of the other options (Hex or
        Base64).
    """
    encoding: Optional[AsymmetricSecretBinaryEncodingEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class BytesEncodeType:
    input: Optional[str] = field(
        default=None,
        metadata={
            "name": "Input",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    algorithm: Optional["BytesEncodeType.Algorithm"] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class Algorithm:
        hex: Optional[BytesEncodeHexType] = field(
            default=None,
            metadata={
                "name": "Hex",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )


@dataclass
class ClientDeviceDataType:
    data_item: List[ClientDeviceDataItem] = field(
        default_factory=list,
        metadata={
            "name": "Data_Item",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "min_occurs": 1,
        }
    )


@dataclass
class ConfigurationSubzone0Type:
    """
    :ivar sn_0_1: First two bytes of the manufacturing ID, which is also
        the first two bytes of the serial number (SN[0:1]).
    :ivar sn_8: Third and last byte of the manufacturing ID, which is
        also the last byte of the serial number (SN[8]).
    :ivar io_options: Options for configuring device I/O.
    :ivar reserved_11: Must be zero.
    :ivar primary_deleted: Indicates whether the data slots of the
        device are deleted using the Delete command. Must be zero for
        provisioning.
    :ivar reserved_14: Must be zero.
    """
    class Meta:
        name = "Configuration_Subzone_0_Type"

    sn_0_1: Optional[DataHex2Bytes] = field(
        default=None,
        metadata={
            "name": "SN_0_1",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    sn_8: Optional[DataHex1Byte] = field(
        default=None,
        metadata={
            "name": "SN_8",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    io_options: Optional["ConfigurationSubzone0Type.IoOptions"] = field(
        default=None,
        metadata={
            "name": "IO_Options",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    reserved_11: Optional[DataHex2Bytes] = field(
        default=None,
        metadata={
            "name": "Reserved_11",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    primary_deleted: Optional[Union[str, ConfigurationSubzone0TypeValue]] = field(
        default=None,
        metadata={
            "name": "Primary_Deleted",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"0x0*[0-9a-fA-F]{2}",
        }
    )
    reserved_14: Optional[DataHex2Bytes] = field(
        default=None,
        metadata={
            "name": "Reserved_14",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class IoOptions:
        """
        :ivar interface: Selects SWI-PWM or I2C interface options.
        :ivar reserved: Must be zero.
        """
        interface: Optional[IoOptionsInterface] = field(
            default=None,
            metadata={
                "name": "Interface",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
                "pattern": r"0b0*[01]{7}",
            }
        )


@dataclass
class ConfigurationSubzone1Type:
    """
    :ivar chip_mode: Mode settings that apply to device as a whole,
        instead of individual slots.
    :ivar slot_config0: Configuration settings specific to slot 0.
    :ivar reserved_2: Must be zero.
    :ivar reserved_3: Must be zero.
    :ivar slot_config3: Configuration settings specific to slot 0.
    :ivar reserved_5: Must be zero.
    :ivar lock: If True, Configuration Subzone 1 will be locked.
    """
    class Meta:
        name = "Configuration_Subzone_1_Type"

    chip_mode: Optional["ConfigurationSubzone1Type.ChipMode"] = field(
        default=None,
        metadata={
            "name": "Chip_Mode",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    slot_config0: Optional["ConfigurationSubzone1Type.SlotConfig0"] = field(
        default=None,
        metadata={
            "name": "Slot_Config0",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    reserved_2: Optional[DataHex1Byte] = field(
        default=None,
        metadata={
            "name": "Reserved_2",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    reserved_3: Optional[DataHex1Byte] = field(
        default=None,
        metadata={
            "name": "Reserved_3",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    slot_config3: Optional["ConfigurationSubzone1Type.SlotConfig3"] = field(
        default=None,
        metadata={
            "name": "Slot_Config3",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    reserved_5: Optional[DataHex11Bytes] = field(
        default=None,
        metadata={
            "name": "Reserved_5",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    lock: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Lock",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class ChipMode:
        """
        :ivar cmos_en: Selects input level reference.
        :ivar clock_divider: Selects the clock divider. Note that 0b11
            will also result in a divide by 1 (fastest).
        :ivar rng_nrbg_health_test_auto_clear: The RNG NRBG health test
            failure bit is set after any time that a command fails as a
            result of a health test failure. If this option is set to
            True and the failure symptom is transient, then when run a
            second time, the command may pass. Otherwise, if set to
            False, The RNG NRBG health test failure bit remains set
            until it is explicitly cleared by a wake, power-up or
            successful self-test (mode includes RNG) execution.
        :ivar reserved: Must be zero.
        """
        cmos_en: Optional[ChipModeCmosEn] = field(
            default=None,
            metadata={
                "name": "CMOS_En",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        clock_divider: Optional[ChipModeClockDivider] = field(
            default=None,
            metadata={
                "name": "Clock_Divider",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        rng_nrbg_health_test_auto_clear: Optional[BooleanType] = field(
            default=None,
            metadata={
                "name": "RNG_NRBG_Health_Test_Auto_Clear",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
                "pattern": r"0b0*[01]{4}",
            }
        )

    @dataclass
    class SlotConfig0:
        """
        :ivar limited_use: If True, key usage is limited by the
            monotonic counter. Otherwise, if False, there are no usage
            limitations.
        :ivar reserved: Must be zero.
        """
        limited_use: Optional[BooleanType] = field(
            default=None,
            metadata={
                "name": "Limited_Use",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
                "pattern": r"0b0*[01]{7}",
            }
        )

    @dataclass
    class SlotConfig3:
        """
        :ivar write_mode: If set to Clear, the key can be written in the
            clear. If set to Encrypted, the key must be encrypted and an
            authorizing input MAC is required.
        :ivar limited_use: If True, key usage is limited by the
            monotonic counter. Otherwise, if False, there are no usage
            limitations.
        :ivar reserved: Must be zero.
        """
        write_mode: Optional[SlotConfig3WriteMode] = field(
            default=None,
            metadata={
                "name": "Write_Mode",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        limited_use: Optional[BooleanType] = field(
            default=None,
            metadata={
                "name": "Limited_Use",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
                "pattern": r"0b0*[01]{6}",
            }
        )


@dataclass
class ConfigurationSubzone2Type:
    """
    :ivar counts_remaining: Number of counts remaining in the counter
        (10000 to 0). This will be converted to a count value (10000 -
        Counts_Remaining) and then translated to the custom binary
        format in the device configuration zone.
    :ivar counter_value: Counter value in counts (0 to 10000). Counter
        is monotonic and counts up to a max of 10000. This will be
        translated to the custom binary format in the device
        configuration zone.
    :ivar counter: Raw binary counter value in the custom binary format.
    :ivar lock: If True, Configuration Subzone 2 will be locked.
    """
    class Meta:
        name = "Configuration_Subzone_2_Type"

    counts_remaining: Optional[int] = field(
        default=None,
        metadata={
            "name": "Counts_Remaining",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "min_inclusive": 0,
            "max_inclusive": 10000,
        }
    )
    counter_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "Counter_Value",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "min_inclusive": 0,
            "max_inclusive": 10000,
        }
    )
    counter: Optional[DataHex16Bytes] = field(
        default=None,
        metadata={
            "name": "Counter",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    lock: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Lock",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class ConfigurationSubzone3Type:
    """
    :ivar device_address: Address used to identify the device in either
        I2C or SWI mode. Address is the least significant 7-bits. Most
        significant bit must be zero.
    :ivar cmp_mode: If True, forces compliance to some certification
        regimes.
    :ivar reserved_1: Must be 0.
    :ivar reserved_2: Must be 0.
    :ivar lock: If True, Configuration Subzone 3 will be locked.
    """
    class Meta:
        name = "Configuration_Subzone_3_Type"

    device_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "Device_Address",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"0x0*[0-9a-fA-F]{2}",
        }
    )
    cmp_mode: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "CMP_Mode",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    reserved_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reserved_1",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"0b0*[01]{7}",
        }
    )
    reserved_2: Optional[DataHex14Bytes] = field(
        default=None,
        metadata={
            "name": "Reserved_2",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    lock: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Lock",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class CustomCacertificateType:
    class Meta:
        name = "CustomCACertificateType"

    level: Optional[int] = field(
        default=None,
        metadata={
            "name": "Level",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    certificate: Optional[PublicBinaryDataType] = field(
        default=None,
        metadata={
            "name": "Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    certificate_from_source: Optional[str] = field(
        default=None,
        metadata={
            "name": "Certificate_From_Source",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )


@dataclass
class DatabaseDataType:
    record_set_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Record_Set_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    fields: Optional["DatabaseDataType.Fields"] = field(
        default=None,
        metadata={
            "name": "Fields",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class Fields:
        field_value: List[DatabaseDataFieldType] = field(
            default_factory=list,
            metadata={
                "name": "Field",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "min_occurs": 1,
            }
        )


@dataclass
class DeviceGenerateKeyType:
    rsa: Optional[GenerateKeyRsatype] = field(
        default=None,
        metadata={
            "name": "RSA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    ecc: Optional[GenerateKeyEcctype] = field(
        default=None,
        metadata={
            "name": "ECC",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    target: Optional[str] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"Slot (0|[1-9][0-9]*)",
        }
    )


@dataclass
class HkdfexpandType:
    """
    Performs an HKDF-Expand operation as defined by RFC 5869 section 2.3.

    :ivar pseudorandom_key: A key of at least the hash length.
        Typically, the output of an HKDF-Extract operation, however that
        step can be skipped if the key supplied here is
        cryptographically strong. See discussion in RFC 5869 section
        3.3.
    :ivar info: Context and/or application specific data.
    :ivar output_size: Size of the output in bytes. Maximum size is 255
        * hash length.
    :ivar hash: Hash algorithm to use for the HKDF operation.
    """
    class Meta:
        name = "HKDFExpandType"

    pseudorandom_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Pseudorandom_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    info: Optional[StringOrDataOrFromSourceType] = field(
        default=None,
        metadata={
            "name": "Info",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    output_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "Output_Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    hash: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class HkdfextractType:
    """
    Performs an HKDF-Extract operation as defined by RFC 5869 section 2.2.

    :ivar initial_keying_material:
    :ivar salt: Optional salt value. If omitted, an all-zero value of
        the hash output length will be used.
    :ivar output_size: Size of the output in bytes. Max (and normal)
        size is the length of the hash algorithm specified. Smaller
        sizes will be a truncation of the normal output.
    :ivar hash: Hash algorithm to use for the HKDF operation.
    """
    class Meta:
        name = "HKDFExtractType"

    initial_keying_material: Optional[str] = field(
        default=None,
        metadata={
            "name": "Initial_Keying_Material",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    salt: Optional[StringOrDataOrFromSourceType] = field(
        default=None,
        metadata={
            "name": "Salt",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    output_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "Output_Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    hash: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class Hmactype:
    """
    Defines an HMAC operation as defined by RFC 5869 section 2.3.

    :ivar key:
    :ivar text:
    :ivar output_size: Size of the output in bytes. Max (and normal)
        size is the length of the hash algorithm specified. Smaller
        sizes will be a truncation of the normal output.
    :ivar hash: Hash algorithm to use for the HMAC operation.
    """
    class Meta:
        name = "HMACType"

    key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    text: Optional[StringOrDataOrFromSourceType] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    output_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "Output_Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    hash: Optional[HashAlgorithmEnum] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class HsmgenerateKeyType:
    class Meta:
        name = "HSMGenerateKeyType"

    rsa: Optional[GenerateKeyRsatype] = field(
        default=None,
        metadata={
            "name": "RSA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    ecc: Optional[GenerateKeyEcctype] = field(
        default=None,
        metadata={
            "name": "ECC",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class SecretBinaryDataType(SecretBinaryDataBaseType):
    encoding: Optional[SecretBinaryEncodingEnum] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class SignatureAlgorithmType:
    """
    Similar to X509SignatureAlgorithmType, except Hashes can be set to None to
    indicate a raw signing operation.
    """
    ecdsa: Optional[SignatureAlgorithmEcdsatype] = field(
        default=None,
        metadata={
            "name": "ECDSA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    rsassa_pkcs1_v1_5: Optional[SignatureAlgorithmRsa15Type] = field(
        default=None,
        metadata={
            "name": "RSASSA_PKCS1_V1_5",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    rsassa_pss: Optional[SignatureAlgorithmRsapsstype] = field(
        default=None,
        metadata={
            "name": "RSASSA_PSS",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class ValueType:
    bytes: Optional[PublicBinaryDataType] = field(
        default=None,
        metadata={
            "name": "Bytes",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Date_Time",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    ecc_public_key: Optional[StaticPublicKeyPublicType] = field(
        default=None,
        metadata={
            "name": "ECC_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    rsa_public_key: Optional[StaticPublicKeyPublicType] = field(
        default=None,
        metadata={
            "name": "RSA_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class X509AuthorityKeyIdentifierType:
    critical: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Critical",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    id_method: Optional["X509AuthorityKeyIdentifierType.IdMethod"] = field(
        default=None,
        metadata={
            "name": "ID_Method",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class IdMethod:
        key_identifier: Optional["X509AuthorityKeyIdentifierType.IdMethod.KeyIdentifier"] = field(
            default=None,
            metadata={
                "name": "Key_Identifier",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        issuer_and_serial_number: Optional[IdMethodIssuerAndSerialNumber] = field(
            default=None,
            metadata={
                "name": "Issuer_And_Serial_Number",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )

        @dataclass
        class KeyIdentifier:
            from_ca_subject_key_identifier: Optional[object] = field(
                default=None,
                metadata={
                    "name": "From_CA_Subject_Key_Identifier",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                }
            )
            calculated: Optional[KeyIdentifierCalculatedType] = field(
                default=None,
                metadata={
                    "name": "Calculated",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                }
            )


@dataclass
class X509ExtensionType:
    extn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Extn_ID",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[0-9]+(\.[0-9]+)*",
        }
    )
    critical: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Critical",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    extn_value: Optional[DerbinaryDataOrFromSourceType] = field(
        default=None,
        metadata={
            "name": "Extn_Value",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class X509SignatureAlgorithmType:
    ecdsa: Optional[X509SignatureAlgorithmEcdsatype] = field(
        default=None,
        metadata={
            "name": "ECDSA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    rsassa_pkcs1_v1_5: Optional[X509SignatureAlgorithmRsa15Type] = field(
        default=None,
        metadata={
            "name": "RSASSA_PKCS1_V1_5",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    rsassa_pss: Optional[X509SignatureAlgorithmRsapsstype] = field(
        default=None,
        metadata={
            "name": "RSASSA_PSS",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class X509SubjectKeyIdentifierType:
    critical: Optional[BooleanType] = field(
        default=None,
        metadata={
            "name": "Critical",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    key_identifier: Optional["X509SubjectKeyIdentifierType.KeyIdentifier"] = field(
        default=None,
        metadata={
            "name": "Key_Identifier",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class KeyIdentifier:
        from_source: Optional[str] = field(
            default=None,
            metadata={
                "name": "From_Source",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )
        calculated: Optional[KeyIdentifierCalculatedType] = field(
            default=None,
            metadata={
                "name": "Calculated",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )


@dataclass
class X520DirectoryStringOrFromSourceType(StringOrDataOrFromSourceType):
    """Express a string using either the PrintableString or UTF8String types.

    Also allows specifying a data source as the data. While technically
    this is meant to mirror the X520name definition, the rarely used
    TeletexString, UniversalString, and BMPString types are unsupported.
    The Raw type allows one to specify the raw ASN.1 data for the value.
    Data must include a properly formed tag, length, and value in DER
    encoding. encoding attribute must be Hex or Base64 for this type.
    """
    type: Optional[X520DirectoryStringOrFromSourceTypeType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class X520Ia5StringOrFromSourceType(StringOrDataOrFromSourceType):
    """Express a string using the IA5String type directly or from a data source.

    The Raw type allows one to specify the raw ASN.1 data for the value
    must include properly formed tag, length, and value in DER encoding.
    encoding attribute must be Hex or Base64 for this type.
    """
    class Meta:
        name = "X520IA5StringOrFromSourceType"

    type: Optional[X520Ia5StringOrFromSourceTypeType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class X520PrintableStringOrFromSourceType(StringOrDataOrFromSourceType):
    """Express a string using the PrintableString type directly or from a data
    source.

    The Raw type allows one to specify the raw ASN.1 data for the value.
    Data must include properly formed tag, length, and value in DER
    encoding. encoding attribute must be Hex or Base64 for this type.
    """
    type: Optional[X520PrintableStringOrFromSourceTypeType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class ClientDataItemType:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    value: Optional[ValueType] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class HsmsignType:
    """
    :ivar message: Message/data to be signed.
    :ivar signing_public_key:
    :ivar signature_algorithm:
    :ivar signature_encoding:
    """
    class Meta:
        name = "HSMSignType"

    message: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    signing_public_key: Optional[StaticPublicKeyPublicType] = field(
        default=None,
        metadata={
            "name": "Signing_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    signature_algorithm: Optional[SignatureAlgorithmType] = field(
        default=None,
        metadata={
            "name": "Signature_Algorithm",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    signature_encoding: Optional[SignatureEncodingType] = field(
        default=None,
        metadata={
            "name": "Signature_Encoding",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class Kdftype:
    class Meta:
        name = "KDFType"

    hkdf_extract: Optional[HkdfextractType] = field(
        default=None,
        metadata={
            "name": "HKDF_Extract",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    hkdf_expand: Optional[HkdfexpandType] = field(
        default=None,
        metadata={
            "name": "HKDF_Expand",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    hmac: Optional[Hmactype] = field(
        default=None,
        metadata={
            "name": "HMAC",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class LogCustomCertificateType:
    device_public_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Device_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    device_certificate: Optional[str] = field(
        default=None,
        metadata={
            "name": "Device_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    ca_certificate: List[CustomCacertificateType] = field(
        default_factory=list,
        metadata={
            "name": "CA_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "min_occurs": 1,
        }
    )


@dataclass
class Mactype:
    class Meta:
        name = "MACType"

    hmac: Optional[Hmactype] = field(
        default=None,
        metadata={
            "name": "HMAC",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class StaticBytesType:
    public: Optional[PublicBinaryDataType] = field(
        default=None,
        metadata={
            "name": "Public",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    secret: Optional[SecretBinaryDataType] = field(
        default=None,
        metadata={
            "name": "Secret",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class StaticPrivateKeySecretType(AsymmetricSecretBinaryDataType):
    format: str = field(
        init=False,
        default="PKCS8",
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class StaticPublicKeySecretType(AsymmetricSecretBinaryDataType):
    format: str = field(
        init=False,
        default="Subject_Public_Key_Info",
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class X509ExtensionsType:
    extension: List[X509ExtensionType] = field(
        default_factory=list,
        metadata={
            "name": "Extension",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    authority_key_identifier: List[X509AuthorityKeyIdentifierType] = field(
        default_factory=list,
        metadata={
            "name": "Authority_Key_Identifier",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    subject_key_identifier: List[X509SubjectKeyIdentifierType] = field(
        default_factory=list,
        metadata={
            "name": "Subject_Key_Identifier",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    key_usage: List[X509KeyUsageType] = field(
        default_factory=list,
        metadata={
            "name": "Key_Usage",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    basic_constraints: List[X509BasicConstraintsType] = field(
        default_factory=list,
        metadata={
            "name": "Basic_Constraints",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    extended_key_usage: List[X509ExtendedKeyUsageType] = field(
        default_factory=list,
        metadata={
            "name": "Extended_Key_Usage",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class X509NameType:
    relative_distinguished_name: List["X509NameType.RelativeDistinguishedName"] = field(
        default_factory=list,
        metadata={
            "name": "Relative_Distinguished_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )

    @dataclass
    class RelativeDistinguishedName:
        attribute_type_and_value: Optional["X509NameType.RelativeDistinguishedName.AttributeTypeAndValue"] = field(
            default=None,
            metadata={
                "name": "Attribute_Type_And_Value",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        common_name: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Common_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        surname: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Surname",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        serial_number: Optional[X520PrintableStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Serial_Number",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        country_name: Optional[X520PrintableStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Country_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        locality_name: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Locality_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        state_or_province_name: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "State_Or_Province_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        organization_name: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Organization_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        organizational_unit_name: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Organizational_Unit_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        title: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Title",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        given_name: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Given_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        initials: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Initials",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        generation_qualifier: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Generation_Qualifier",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        dn_qualifier: Optional[X520PrintableStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "DN_Qualifier",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        pseudonym: Optional[X520DirectoryStringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Pseudonym",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        domain_component: Optional[X520Ia5StringOrFromSourceType] = field(
            default=None,
            metadata={
                "name": "Domain_Component",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )

        @dataclass
        class AttributeTypeAndValue:
            type: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Type",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                    "required": True,
                    "pattern": r"[0-9]+(\.[0-9]+)*",
                }
            )
            value: Optional[DerbinaryDataOrFromSourceType] = field(
                default=None,
                metadata={
                    "name": "Value",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                    "required": True,
                }
            )


@dataclass
class ClientDataType:
    data_item: List[ClientDataItemType] = field(
        default_factory=list,
        metadata={
            "name": "Data_Item",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class StaticPrivateKeyType:
    secret: Optional[StaticPrivateKeySecretType] = field(
        default=None,
        metadata={
            "name": "Secret",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class StaticPublicKeyType:
    public: Optional[StaticPublicKeyPublicType] = field(
        default=None,
        metadata={
            "name": "Public",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    secret: Optional[StaticPublicKeySecretType] = field(
        default=None,
        metadata={
            "name": "Secret",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class X509CertificateType:
    tbs_certificate: Optional["X509CertificateType.TbsCertificate"] = field(
        default=None,
        metadata={
            "name": "TBS_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    signature_algorithm: Optional[X509SignatureAlgorithmType] = field(
        default=None,
        metadata={
            "name": "Signature_Algorithm",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    ca_certificate_chain: Optional[X509CacertificateChainType] = field(
        default=None,
        metadata={
            "name": "CA_Certificate_Chain",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class TbsCertificate:
        version: Optional[X509VersionType] = field(
            default=None,
            metadata={
                "name": "Version",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        serial_number: Optional[X509SerialNumberType] = field(
            default=None,
            metadata={
                "name": "Serial_Number",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        validity: Optional["X509CertificateType.TbsCertificate.Validity"] = field(
            default=None,
            metadata={
                "name": "Validity",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        subject: Optional[X509NameType] = field(
            default=None,
            metadata={
                "name": "Subject",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        subject_public_key_info: Optional[X509SubjectPublicKeyInfoType] = field(
            default=None,
            metadata={
                "name": "Subject_Public_Key_Info",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )
        issuer_unique_id: Optional[X509IssuerUniqueIdtype] = field(
            default=None,
            metadata={
                "name": "Issuer_Unique_ID",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        subject_unique_id: Optional[X509SubjectUniqueIdtype] = field(
            default=None,
            metadata={
                "name": "Subject_Unique_ID",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )
        extensions: Optional[X509ExtensionsType] = field(
            default=None,
            metadata={
                "name": "Extensions",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            }
        )

        @dataclass
        class Validity:
            not_before: Optional[X509TimeType] = field(
                default=None,
                metadata={
                    "name": "Not_Before",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                    "required": True,
                }
            )
            not_after: Optional[X509TimeType] = field(
                default=None,
                metadata={
                    "name": "Not_After",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                    "required": True,
                }
            )


@dataclass
class DataSourceType:
    """
    :ivar name: The name of the Data_Source, which is directly
        referenced by either Functions or Writers.
    :ivar description: An arbitrary description of what this Data_Source
        is used for. Not required.
    :ivar static_bytes: Static data that is sourced from this
        configuration.
    :ivar static_ecc_private_key: Static ECC Private Key definition.
    :ivar static_ecc_public_key: Static ECC Public Key definition.
    :ivar static_rsa_private_key: Static RSA Public Key definition.
    :ivar static_rsa_public_key: Static RSA Public Key definition.
    :ivar static_date_time: Static date and time
    :ivar database_data: Data that is sourced from the database, such as
        Record Sets, counters, etc.
    :ivar hsm_generate_key: Generates an asymmetric key pair in the HSM.
        Has two outputs, Public_Key and Private_Key.
    :ivar force_nonnegative_fixed_size: Treats the input bytes as a big
        endian signed integer (e.g. ASN.1 format). Sets the upper most
        bits to 0b01 to make the value positive and fixed size
        (untrimmable).
    :ivar hsm_random:
    :ivar process_info: Provides information about the provisioning
        process and the device being provisioned. Device information may
        depend on the device being provisioned. - Serial_Number: Bytes -
        Also known as the Unique ID
    :ivar bytes_encode:
    :ivar date_time_modify:
    :ivar current_date_time:
    :ivar template:
    :ivar x509_certificate:
    :ivar counter:
    :ivar device_generate_key: Generates a command to have the device
        being provisioned internally generate an asymmetric key pair.
        Single output is the public key generated and returned by the
        device.
    :ivar client_device_data: Per-device public data supplied by the
        provisioning client.
    :ivar bytes_pad: Pads Bytes data out to a fixed size.
    :ivar kdf: Generate secret key using a Key Diversification Function
        (KDF).
    :ivar mac: Generate a MAC using a key and text.
    :ivar hash:
    :ivar qi_certificate_chain:
    :ivar public_key_encode: Encode a public key into bytes with a
        specific format and encoding.
    :ivar hsm_sign: Sign a raw message with an HSM held key.
    :ivar log_custom_certificate: Logs a custom (non X.509) certificate
        to the database for the device being provisioned. No output.
    """
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    static_bytes: Optional[StaticBytesType] = field(
        default=None,
        metadata={
            "name": "Static_Bytes",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    static_ecc_private_key: Optional[StaticPrivateKeyType] = field(
        default=None,
        metadata={
            "name": "Static_ECC_Private_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    static_ecc_public_key: Optional[StaticPublicKeyType] = field(
        default=None,
        metadata={
            "name": "Static_ECC_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    static_rsa_private_key: Optional[StaticPrivateKeyType] = field(
        default=None,
        metadata={
            "name": "Static_RSA_Private_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    static_rsa_public_key: Optional[StaticPublicKeyType] = field(
        default=None,
        metadata={
            "name": "Static_RSA_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    static_date_time: Optional["DataSourceType.StaticDateTime"] = field(
        default=None,
        metadata={
            "name": "Static_Date_Time",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    database_data: Optional[DatabaseDataType] = field(
        default=None,
        metadata={
            "name": "Database_Data",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    hsm_generate_key: Optional[HsmgenerateKeyType] = field(
        default=None,
        metadata={
            "name": "HSM_Generate_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    force_nonnegative_fixed_size: Optional["DataSourceType.ForceNonnegativeFixedSize"] = field(
        default=None,
        metadata={
            "name": "Force_Nonnegative_Fixed_Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    hsm_random: Optional[HsmrandomType] = field(
        default=None,
        metadata={
            "name": "HSM_Random",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    process_info: Optional[object] = field(
        default=None,
        metadata={
            "name": "Process_Info",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    bytes_encode: Optional[BytesEncodeType] = field(
        default=None,
        metadata={
            "name": "Bytes_Encode",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    date_time_modify: Optional[DateTimeModifyType] = field(
        default=None,
        metadata={
            "name": "Date_Time_Modify",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    current_date_time: Optional[object] = field(
        default=None,
        metadata={
            "name": "Current_Date_Time",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    template: Optional[TemplateType] = field(
        default=None,
        metadata={
            "name": "Template",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    x509_certificate: Optional[X509CertificateType] = field(
        default=None,
        metadata={
            "name": "X509_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    counter: Optional[CounterType] = field(
        default=None,
        metadata={
            "name": "Counter",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    device_generate_key: Optional[DeviceGenerateKeyType] = field(
        default=None,
        metadata={
            "name": "Device_Generate_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    client_device_data: Optional[ClientDeviceDataType] = field(
        default=None,
        metadata={
            "name": "Client_Device_Data",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    bytes_pad: Optional[BytesPadType] = field(
        default=None,
        metadata={
            "name": "Bytes_Pad",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    kdf: Optional[Kdftype] = field(
        default=None,
        metadata={
            "name": "KDF",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    mac: Optional[Mactype] = field(
        default=None,
        metadata={
            "name": "MAC",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    hash: Optional[HashType] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    qi_certificate_chain: Optional[QiCertificateChainType] = field(
        default=None,
        metadata={
            "name": "Qi_Certificate_Chain",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    public_key_encode: Optional[PublicKeyEncodeType] = field(
        default=None,
        metadata={
            "name": "Public_Key_Encode",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    hsm_sign: Optional[HsmsignType] = field(
        default=None,
        metadata={
            "name": "HSM_Sign",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    log_custom_certificate: Optional[LogCustomCertificateType] = field(
        default=None,
        metadata={
            "name": "Log_Custom_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )

    @dataclass
    class StaticDateTime:
        public: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "Public",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
            }
        )

    @dataclass
    class ForceNonnegativeFixedSize:
        input: Optional[str] = field(
            default=None,
            metadata={
                "name": "Input",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )


@dataclass
class DataSourcesType:
    """
    :ivar data_source: Data source objects for specifying static and
        dynamic data along with functions affecting it.
    :ivar writer: Writer types specify where named Data_Source items or
        Function results should be written to on a device.
    :ivar wrapped_key: A wrapped key item, which was used to encrypt one
        or more secret Data_Source items.
    """
    data_source: List[DataSourceType] = field(
        default_factory=list,
        metadata={
            "name": "Data_Source",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    writer: List[DataSourcesWriterType] = field(
        default_factory=list,
        metadata={
            "name": "Writer",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    wrapped_key: List[DataSourcesWrappedKeyType] = field(
        default_factory=list,
        metadata={
            "name": "Wrapped_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )


@dataclass
class Ecc204Ta010ConfigType:
    """
    :ivar config_name:
    :ivar additional_data: Allows one to define public data to be sent
        to the client. This allows one to add data to the provisioning
        config that the provisioning client can use that may not be part
        of the standard configuration. This data can also be referenced
        in the Data_Sources section.
    :ivar configuration_subzone_0: Configuration Subzone 0 (CSZ0)
        contains information that can only be set by Microchip.
    :ivar configuration_subzone_1: Configuration Subzone 1 (CSZ1)
        contains the primary configuration options associated with the
        device.
    :ivar configuration_subzone_2: Configuration Subzone 2 (CSZ2) stores
        the value of the monotonic counter.
    :ivar configuration_subzone_3: Configuration Subzone 3 (CSZ3) is
        used to store the address of the device and compliance mode
        settings.
    :ivar slot_locks: Controls which slots should be locked after
        provisioning.
    :ivar data_sources:
    """
    class Meta:
        name = "ECC204_TA010_Config_Type"

    config_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Config_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    additional_data: Optional[ClientDataType] = field(
        default=None,
        metadata={
            "name": "Additional_Data",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
        }
    )
    configuration_subzone_0: Optional[ConfigurationSubzone0Type] = field(
        default=None,
        metadata={
            "name": "Configuration_Subzone_0",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    configuration_subzone_1: Optional[ConfigurationSubzone1Type] = field(
        default=None,
        metadata={
            "name": "Configuration_Subzone_1",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    configuration_subzone_2: Optional[ConfigurationSubzone2Type] = field(
        default=None,
        metadata={
            "name": "Configuration_Subzone_2",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    configuration_subzone_3: Optional[ConfigurationSubzone3Type] = field(
        default=None,
        metadata={
            "name": "Configuration_Subzone_3",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    slot_locks: Optional[SlotLocksType] = field(
        default=None,
        metadata={
            "name": "Slot_Locks",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )
    data_sources: Optional[DataSourcesType] = field(
        default=None,
        metadata={
            "name": "Data_Sources",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/ECC204_TA010_Config_1.1",
            "required": True,
        }
    )


@dataclass
class Ecc204Config(Ecc204Ta010ConfigType):
    class Meta:
        name = "ECC204_Config"
        namespace = "https://www.microchip.com/schema/ECC204_TA010_Config_1.1"


@dataclass
class Ecc206Config(Ecc204Ta010ConfigType):
    class Meta:
        name = "ECC206_Config"
        namespace = "https://www.microchip.com/schema/ECC204_TA010_Config_1.1"


@dataclass
class Ta010Config(Ecc204Ta010ConfigType):
    class Meta:
        name = "TA010_Config"
        namespace = "https://www.microchip.com/schema/ECC204_TA010_Config_1.1"
