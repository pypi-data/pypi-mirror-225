from dataclasses import field
from enum import Enum
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass
from xsdata.models.datatype import XmlDateTime, XmlDuration

__NAMESPACE__ = "https://www.microchip.com/schema/TA100_Config_1.1"


class BasicConstraintsValue(Enum):
    NO_LIMIT = "No_Limit"


class BinaryDataOrFromSourceEncoding(Enum):
    HEX = "Hex"
    BASE64 = "Base64"


class BinaryDataEncoding(Enum):
    HEX = "Hex"
    BASE64 = "Base64"


class Boolean(Enum):
    """
    Boolean types used in TA100 config XML structure.
    """
    TRUE = "True"
    FALSE = "False"


class BooleanEnabled(Enum):
    """
    Boolean types used in TA100 config XML structure.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class ByteOrder(Enum):
    BIG = "Big"
    LITTLE = "Little"


class DataValue(Enum):
    FROM_SOURCE = "From_Source"


class DefinitionEncoding(Enum):
    STRING_UTF8 = "String_UTF8"
    HEX = "Hex"


class DirectoryStringOrFromSourceType(Enum):
    RAW = "Raw"
    PRINTABLE_STRING = "Printable_String"
    UTF8_STRING = "UTF8_String"


class EccFormat(Enum):
    UNCOMPRESSED = "Uncompressed"
    COMPRESSED = "Compressed"


class ElementTypeAccessLimit(Enum):
    ALWAYS = "Always"
    SECURE_BOOT = "Secure_Boot"
    ONE_TIME_CLEAR = "One_Time_Clear"
    ONE_TIME_SET = "One_Time_Set"


class ElementTypeClass(Enum):
    PUBLIC_KEY = "Public_Key"
    PRIVATE_KEY = "Private_Key"
    SYMMETRIC_KEY = "Symmetric_Key"
    DATA = "Data"
    EXTRACTED_CERTIFICATE = "Extracted_Certificate"
    RESERVED = "Reserved"
    FAST_CRYPTO_KEY_GROUP = "Fast_Crypto_Key_Group"
    CRL = "CRL"


class ElementTypeValue(Enum):
    ECC_P256 = "ECC_P256"
    ECC_P224 = "ECC_P224"
    ECC_P384 = "ECC_P384"
    RESERVED_3 = "Reserved_3"
    RSA_1024 = "RSA_1024"
    RSA_2048 = "RSA_2048"
    RSA_3072 = "RSA_3072"
    RESERVED_7 = "Reserved_7"
    HMAC_SHA256 = "HMAC_SHA256"
    ECC_SECP256_K1 = "ECC_SECP256K1"
    ECC_BRAINPOOL_P256_R1 = "ECC_Brainpool_P256R1"
    RESERVED_11 = "Reserved_11"
    AES128 = "AES128"
    RESERVED_13 = "Reserved_13"
    RESERVED_14 = "Reserved_14"
    RESERVED_15 = "Reserved_15"


class FieldType(Enum):
    BYTES = "Bytes"
    ECC_PRIVATE_KEY = "ECC_Private_Key"
    ECC_PUBLIC_KEY = "ECC_Public_Key"
    RSA_PRIVATE_KEY = "RSA_Private_Key"
    RSA_PUBLIC_KEY = "RSA_Public_Key"
    DATE_TIME = "Date_Time"


class GpioOutputDefaultState(Enum):
    LOW = "Low"
    HIGH = "High"


class HmacSha256Value(Enum):
    FROM_SOURCE = "From_Source"


class HashAlgorithms(Enum):
    SHA1 = "SHA1"
    SHA224 = "SHA224"
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    SHA512 = "SHA512"


class HexCase(Enum):
    UPPER = "Upper"
    LOWER = "Lower"


class Ia5StringOrFromSourceType(Enum):
    RAW = "Raw"
    IA5_STRING = "IA5_String"


class IdMethodIssuerAndSerialNumber(Enum):
    FROM_CA = "From_CA"


class KeyIdentifierCalculatedTokens(Enum):
    RFC5280_METHOD1 = "RFC5280_Method1"
    RFC5280_METHOD2 = "RFC5280_Method2"
    RFC7093_METHOD1 = "RFC7093_Method1"
    RFC7093_METHOD2 = "RFC7093_Method2"
    RFC7093_METHOD3 = "RFC7093_Method3"
    RFC7093_METHOD4_SHA256 = "RFC7093_Method4_SHA256"
    RFC7093_METHOD4_SHA384 = "RFC7093_Method4_SHA384"
    RFC7093_METHOD4_SHA512 = "RFC7093_Method4_SHA512"


class KeyAlgorithm(Enum):
    RSA_OAEP_SHA256 = "RSA_OAEP_SHA256"


class PassthroughBehavior(Enum):
    """
    Passthrough behavior options.
    """
    INDEPENDENT = "Independent"
    ANDED = "ANDed"


class PermissionsType(Enum):
    NEVER = "Never"
    ALWAYS = "Always"
    AUTH = "Auth"
    RIGHTS = "Rights"


class PrintableStringOrFromSourceType(Enum):
    RAW = "Raw"
    PRINTABLE_STRING = "Printable_String"


class PrivateKeyAgreeUse(Enum):
    NONE = "None"
    ANY_TARGET = "Any_Target"
    RW_NEVER = "RW_Never"
    USAGE_KEY = "Usage_Key"


class PrivateKeySignUse(Enum):
    NONE = "None"
    ALL = "All"
    MESSAGE_ONLY = "Message_Only"
    INTERNAL_ONLY = "Internal_Only"


class PublicBinaryDataEncoding(Enum):
    HEX = "Hex"
    BASE64 = "Base64"
    STRING_UTF8 = "String_UTF8"


class PublicKeyRoot(Enum):
    FALSE = "False"
    RESERVED_1 = "Reserved_1"
    RESERVED_2 = "Reserved_2"
    TRUE = "True"


class PublicKeyValue(Enum):
    UNRESTRICTED = "Unrestricted"


class RevocationSize(Enum):
    VALUE_0 = 0
    VALUE_16 = 16
    VALUE_24 = 24
    VALUE_32 = 32


class SecretAlgorithm(Enum):
    AES256_GCM = "AES256_GCM"


class SecretFormat(Enum):
    TA100_WRITE = "TA100_Write"
    PKCS8 = "PKCS8"


class SecureBootMode(Enum):
    DISABLED = "Disabled"
    FULL_ASYMMETRIC = "Full_Asymmetric"
    FULL_STORED = "Full_Stored"
    PARTIAL = "Partial"
    RESERVED_4 = "Reserved_4"
    RESERVED_5 = "Reserved_5"
    RESERVED_6 = "Reserved_6"
    RESERVED_7 = "Reserved_7"


class SecureBootValue(Enum):
    DISABLED = "Disabled"


class SessionUseEncryptedSession(Enum):
    NA = "NA"
    OPTIONAL = "Optional"
    MANDATORY = "Mandatory"


class SessionUseSessionRandomNonce(Enum):
    NA = "NA"
    OPTIONAL = "Optional"
    MANDATORY = "Mandatory"


class SessionUseUseForAuth(Enum):
    NEVER = "Never"
    EITHER = "Either"
    ONLY = "Only"


class SessionUseUseForTransfer(Enum):
    NO = "No"
    ONLY = "Only"


class StringOrDataOrFromSourceEncoding(Enum):
    HEX = "Hex"
    BASE64 = "Base64"
    STRING_UTF8 = "String_UTF8"


class SymmetricKeySymUsage(Enum):
    MAC = "MAC"
    ENC = "ENC"
    ANY = "ANY"
    KDF_SHA = "KDF_SHA"


class TbsCertificateIssuerUniqueId(Enum):
    FROM_CA_SUBJECT_UNIQUE_ID = "From_CA_Subject_Unique_ID"


class TbsCertificateVersion(Enum):
    V1 = "V1"
    V2 = "V2"
    V3 = "V3"


class WrappingPublicKeyEncoding(Enum):
    PEM = "PEM"


class WrappingPublicKeyFormat(Enum):
    SUBJECT_PUBLIC_KEY_INFO = "Subject_Public_Key_Info"


@dataclass
class WriterItem:
    """
    :ivar source_name: The name of the source of data, whether that is a
        named Data_Source item or Function.
    :ivar description:
    :ivar target:
    """
    class Meta:
        name = "Writer_Item"

    source_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Source_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    target: Optional[str] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )


class X509TimeType(Enum):
    AUTO = "Auto"
    UTC_TIME = "UTC_Time"
    GENERALIZED_TIME = "Generalized_Time"


@dataclass
class BinaryData:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    encoding: Optional[BinaryDataEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class BinaryDataOrFromSource:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    from_source: Optional[Boolean] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    encoding: Optional[BinaryDataOrFromSourceEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ElementType:
    """
    :ivar name: Customer-defined name for the element. Not programmed
        into the device, just for reference within this configuration.
    :ivar handle: Element handle value. Value between 0x8000 and 0xBFFF.
        Note that values between 0x8000 and 0x80FF are linkable and can
        be referenced by an attribute link in an element attribute list.
    :ivar details: Value of the Details parameter when using the Create
        command for this element. Only HMAC_SHA256 keys have extra
        options here.
    :ivar class_value:
    :ivar key_type: The core algorithm and key size corresponding to
        this element. Use NA for Data and CRL elements, however, the
        value is technically ignored for those classes.
    :ivar alg_mode:
    :ivar property:
    :ivar usage_key: Handle of key that must be used to initiate
        authorization session for usage. Value between 0x8000 and
        0x80FF. If Usage_Perm is Rights, this field contains rights
        required to use the key as an 8-bit bit string (e.g.
        0b01010101).
    :ivar write_key: Handle of key that must be used to initiate
        authorization session for writing or deleting. Value between
        0x8000 and 0x80FF. If Write_Perm is Rights, this field contains
        rights required to write the key as an 8-bit bit string (e.g.
        0b01010101). If this key is a root public key, this field
        contains the rights that can be inherited by children of this
        root as an 8-bit bit string (e.g. 0b01010101).
    :ivar read_key: Handle of key that must be used to initiate
        authorization session for reading. Value between 0x8000 and
        0x80FF. If Usage_Perm is Rights, this field contains rights
        required to read the key as an 8-bit bit string (e.g.
        0b01010101).
    :ivar usage_perm: Never: Cannot be used in any command, but can be
        read or written if allowed. Always: No usage restrictions,
        optional to run in authorization session. Auth: Any command
        using this element must be run within an authorization session
        created with "Usage_Key". Rights: The use of the element
        requires rights in "Usage_Key".
    :ivar write_perm: Never: This element can never be written with the
        Write command. Always: Always legal to write. Auth: Writes of
        this element must be run within an authorization session created
        with "Write_Key". Rights: Writes require rights in "Write_Key".
    :ivar read_perm: Never: This element can never be read with the Read
        command. Always: Always legal to read. Auth: Read requires auth
        using "Read_Key". Rights: Read requires rights in "Read_Key".
    :ivar deletion_perm: Never: This element may not be deleted, only
        modified per write permissions. Always: Always legal to delete.
        Auth: Deletion requires authorization using "Write_Key". Rights:
        Deletion requires rights in "Write_Key".
    :ivar use_count: If False, use of this key is not tied to a
        monotonic counter. Otherwise, set to the monotonic counter
        number (1 - 3) to be incremented when this key is used. Counter
        0 cannot be incremented via this mechanism.
    :ivar reserved_58:
    :ivar exportable: If True, this element can be exported from the
        chip.
    :ivar lockable: False: Permanently locking of this element is not
        permitted. True: This element can be permanently locked - both
        writes and deletions are prohibited.
    :ivar access_limit: Limits access (usage, read, write, and delete)
        depending on the chip's state. Always: Access unlimited.
        Secure_Boot: Access prohibited until secure boot has been
        completed successfully. One_Time_Clear: Access permitted if
        One_Time status bit is 0. One_Time_Set: Access permitted if
        One_Time status bit is 1.
    :ivar reserved_63:
    """
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    handle: Optional[str] = field(
        default=None,
        metadata={
            "name": "Handle",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0x[0-9a-fA-F]{4}",
        }
    )
    details: Optional["ElementType.Details"] = field(
        default=None,
        metadata={
            "name": "Details",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    class_value: Optional[ElementTypeClass] = field(
        default=None,
        metadata={
            "name": "Class",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    key_type: Optional[Union[str, ElementTypeValue]] = field(
        default=None,
        metadata={
            "name": "Key_Type",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0b[01]{4}",
        }
    )
    alg_mode: Optional[Union[str, ElementTypeValue]] = field(
        default=None,
        metadata={
            "name": "Alg_Mode",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0b[01]",
        }
    )
    property: Optional["ElementType.Property"] = field(
        default=None,
        metadata={
            "name": "Property",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    usage_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Usage_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0x80[0-9a-fA-F]{2}",
        }
    )
    write_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Write_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0x80[0-9a-fA-F]{2}",
        }
    )
    read_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Read_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0x80[0-9a-fA-F]{2}",
        }
    )
    usage_perm: Optional[PermissionsType] = field(
        default=None,
        metadata={
            "name": "Usage_Perm",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    write_perm: Optional[PermissionsType] = field(
        default=None,
        metadata={
            "name": "Write_Perm",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    read_perm: Optional[PermissionsType] = field(
        default=None,
        metadata={
            "name": "Read_Perm",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    deletion_perm: Optional[PermissionsType] = field(
        default=None,
        metadata={
            "name": "Deletion_Perm",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    use_count: Optional[ElementTypeValue] = field(
        default=None,
        metadata={
            "name": "Use_Count",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    reserved_58: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reserved_58",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0b[01]",
        }
    )
    exportable: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "Exportable",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    lockable: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "Lockable",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    access_limit: Optional[ElementTypeAccessLimit] = field(
        default=None,
        metadata={
            "name": "Access_Limit",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    reserved_63: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reserved_63",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0b[01]",
        }
    )

    @dataclass
    class Details:
        hmac_sha256: Optional["ElementType.Details.HmacSha256"] = field(
            default=None,
            metadata={
                "name": "HMAC_SHA256",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        unused: Optional[str] = field(
            default=None,
            metadata={
                "name": "Unused",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "pattern": r"0x[0-9a-fA-F]{4}",
            }
        )

        @dataclass
        class HmacSha256:
            """
            :ivar reserved_0:
            :ivar size: Size of the HMAC-SHA256 key from 16 to 64 bytes.
                Can also be From_Source to indicate that the size should
                be set from the data source that Writes into this
                element during personalization.
            :ivar reserved_15:
            """
            reserved_0: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved_0",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{8}",
                }
            )
            size: Optional[HmacSha256Value] = field(
                default=None,
                metadata={
                    "name": "Size",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            reserved_15: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved_15",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]",
                }
            )

    @dataclass
    class Property:
        public_key: Optional["ElementType.Property.PublicKey"] = field(
            default=None,
            metadata={
                "name": "Public_Key",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        private_key: Optional["ElementType.Property.PrivateKey"] = field(
            default=None,
            metadata={
                "name": "Private_Key",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        symmetric_key: Optional["ElementType.Property.SymmetricKey"] = field(
            default=None,
            metadata={
                "name": "Symmetric_Key",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        data: Optional["ElementType.Property.Data"] = field(
            default=None,
            metadata={
                "name": "Data",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        extracted_certificate: Optional["ElementType.Property.ExtractedCertificate"] = field(
            default=None,
            metadata={
                "name": "Extracted_Certificate",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "pattern": r"0x[0-9a-fA-F]{4}",
            }
        )
        fast_crypto_key_group: Optional["ElementType.Property.FastCryptoKeyGroup"] = field(
            default=None,
            metadata={
                "name": "Fast_Crypto_Key_Group",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        crl: Optional["ElementType.Property.Crl"] = field(
            default=None,
            metadata={
                "name": "CRL",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )

        @dataclass
        class PublicKey:
            """
            :ivar path_length: For root public keys, this field encodes
                the path length restrictions. 0 means that no child can
                be a CA through 254. The value 'Unrestricted' means that
                there are no path length restrictions. This field must
                be set to 0 if all other bits in the property word are
                0.
            :ivar secure_boot: If True, this key can be used to validate
                host code signatures on boot. If the "Root" field
                indicates that this is a root key, then it can also be
                used as a CA to sign certificates of keys that can be
                used for this purpose.
            :ivar root: False: A public key that can be used for the
                Verify command, but not the Manage_Cert command. True: A
                root public key which can be used by the Manage_Cert
                and/or Secure_Boot commands.
            :ivar crl_sign: If True, this key can sign a CRL. If the
                "Root" field indicates that this is a root key, then it
                can also be used as a CA to sign certificates that can
                do so.
            :ivar special_only: If False, this CA can be used to sign
                any type of X.509 certificate. If True, this CA can be
                used to sign only X.509 certificates that have one of
                the special properties (Secure_Boot or CRL_Sign)
                asserted in the extensions field. This field must be
                False if the "Root" property is not True.
            :ivar reserved:
            """
            path_length: Optional[PublicKeyValue] = field(
                default=None,
                metadata={
                    "name": "Path_Length",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            secure_boot: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Secure_Boot",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            root: Optional[PublicKeyRoot] = field(
                default=None,
                metadata={
                    "name": "Root",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            crl_sign: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "CRL_Sign",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            special_only: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Special_Only",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{3}",
                }
            )

        @dataclass
        class PrivateKey:
            """
            :ivar pub_key: Handle containing the corresponding public
                key. May point to either a public key or a certificate.
                This attribute is entirely advisory in nature, it is
                neither used nor checked by any internal TA100
                operation. If the external system software depends on
                this field, then it should be properly filled out.
            :ivar session: If True, it can be used by the Share_Key
                sequence to create/exchange session keys. Sign_Use must
                also be True.
            :ivar key_gen: If True, then regardless of the Write_Perm,
                the Write command cannot be used to load a key value
                into this element – keys with this bit set have always
                been generated within this TA100 device. If False,
                either the Write or Key_Gen command can be used to load
                this element.
            :ivar sign_use: None: Key cannot be used for signature
                generation. All: Key can sign internally or externally
                generated digests. Message_Only: Key can be used to sign
                digests internally created from messages passed to the
                chip. It cannot be used to sign a digest supplied
                externally. Internal_Only: Key can be used to sign
                internally generated messages but cannot be used to sign
                externally supplied messages or digests.
            :ivar agree_use: None: Key cannot be used for Key Agreement
                if it is an ECC key. If it is an RSA key it cannot be
                used for RSA decrypt. Any_Target: The key agreement
                target can be the output buffer or any memory element
                without regard to the read/write/usage requirements.
                RW_Never: The key agreement target must be a the shared
                data element or volatile register with both Read_Perm
                and Write_Perm = Never Usage_Key: Usage restrictions for
                the key agreement target are related to the
                priv_key.usage_key, as above.
            :ivar reserved:
            """
            pub_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Pub_Key",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0x80[0-9a-fA-F]{2}",
                }
            )
            session: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Session",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            key_gen: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Key_Gen",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            sign_use: Optional[PrivateKeySignUse] = field(
                default=None,
                metadata={
                    "name": "Sign_Use",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            agree_use: Optional[PrivateKeyAgreeUse] = field(
                default=None,
                metadata={
                    "name": "Agree_Use",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{2}",
                }
            )

        @dataclass
        class SymmetricKey:
            """
            :ivar granted_rights: Rights that have been granted to this
                key, either through inheritance or during the
                manufacturing setup phase.
            :ivar sym_usage: MAC: Key can only be used for MAC/CMAC/HMAC
                calculation/validation via the MAC, FC_Config and
                Authorize (CMAC or HMAC) commands. ENC: Key can only be
                used for AES encryption or decryption via the KDF (AES)
                or Authorize (GCM) commands. ANY: Key can be used for
                any purpose for which a symmetric key is appropriate.
                KDF_SHA: Key can only be used as the input to the SHA-
                based modes (HKDF or PRF) of the KDF command.
            :ivar session_use: If this key can be used to establish an
                authorization session and restrictions on the session,
                if so.
            :ivar key_group_ok: False: This key cannot be used as part
                of a key group. True: this key may be referenced as part
                of a handle-list based key group.
            :ivar reserved:
            :ivar partial_forbidden: False: Accesses of this element may
                read/write/use any number of bytes within the element.
                True: Accesses of this element must use all the bytes
                within the element.
            """
            granted_rights: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Granted_Rights",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{8}",
                }
            )
            sym_usage: Optional[SymmetricKeySymUsage] = field(
                default=None,
                metadata={
                    "name": "Sym_Usage",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            session_use: Optional["ElementType.Property.SymmetricKey.SessionUse"] = field(
                default=None,
                metadata={
                    "name": "Session_Use",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            key_group_ok: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Key_Group_OK",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]",
                }
            )
            partial_forbidden: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Partial_Forbidden",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )

            @dataclass
            class SessionUse:
                """
                :ivar use_for_auth: Never: This key can never be used to
                    establish an authorization session, regardless of
                    the value of the usage field. Encrypted_Session must
                    be NA, Session_Random_Nonce must be NA, and
                    Use_For_Transfer must be No. Either: The key can be
                    used for either session establishment or other
                    symmetric key usage such as MAC, etc. Only: This key
                    can only be used for authorization session
                    establishment (the generate phase) and cannot be
                    used for any other purpose.
                :ivar encrypted_session: NA: Not applicable, use when
                    Use_For_Auth is Never. Optional: The key can be used
                    for either encrypted authorization sessions or MAC-
                    only sessions. Mandatory: This key can only be used
                    for encrypted authorization session. MAC-only
                    session not allowed. Session_Random_Nonce must also
                    be set to Mandatory.
                :ivar session_random_nonce: NA: Not applicable, use when
                    Use_For_Auth is Never. Optional: Authorization
                    sessions with this key may use specified or random
                    nonce. Mandatory: Authorization sessions with this
                    key must use an internally generated random nonce.
                :ivar use_for_transfer: No: Transfer functions are not
                    allowed. Only: Authorization session with this key
                    may only be used for the transfer functions
                    supported by the Read and Write commands.
                    Use_For_Auth must be Only, Encrypted_Session must be
                    Mandatory, and Session_Random_Nonce must be
                    Mandatory.
                """
                use_for_auth: Optional[SessionUseUseForAuth] = field(
                    default=None,
                    metadata={
                        "name": "Use_For_Auth",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )
                encrypted_session: Optional[SessionUseEncryptedSession] = field(
                    default=None,
                    metadata={
                        "name": "Encrypted_Session",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )
                session_random_nonce: Optional[SessionUseSessionRandomNonce] = field(
                    default=None,
                    metadata={
                        "name": "Session_Random_Nonce",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )
                use_for_transfer: Optional[SessionUseUseForTransfer] = field(
                    default=None,
                    metadata={
                        "name": "Use_For_Transfer",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )

        @dataclass
        class Data:
            """
            :ivar size: Number of bytes within this data element. Can
                also be From_Source to indicate that the size should be
                set from the data source that Writes into this element
                during personalization.
            :ivar template: If True, this element can be used as a
                template with the Sign (Internal) command or for any
                other general purpose. If False, this is a general
                purpose element that cannot be used with Sign
                (Internal).
            :ivar reserved:
            :ivar partial_forbidden: If True, Accesses of this element
                may read/write/use any number of bytes within the
                element. If False, All accesses of this element must use
                all the bytes within the element.
            """
            size: Optional[DataValue] = field(
                default=None,
                metadata={
                    "name": "Size",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            template: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Template",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{2}",
                }
            )
            partial_forbidden: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Partial_Forbidden",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )

        @dataclass
        class ExtractedCertificate:
            """
            :ivar granted_rights: Rights that have been granted to this
                certificate, either through inheritance or during the
                manufacturing setup phase.
            :ivar secure_boot: If True, this key can be used to validate
                host code digests on boot.
            :ivar ca_ok: If False, this element contains only a public
                key and identity digest. It cannot be used as the parent
                validating key for the Manage_Cert command. If True,
                this certificate can be the parent for Manage_Cert.
            :ivar ca_parent: False: This element can be used as the
                parent for Manage_Cert, but the child (target) extracted
                certificate must have CA_OK set to False. True: OK for
                this key to be the parent of CA. Note: If CA_OK is
                False, this bit is ignored.
            :ivar crl_sign: If True, this key can be used to sign a CRL.
            :ivar special_only: False: This CA can be used to sign any
                type of X.509 certificate. True: This CA can be used to
                sign only X.509 certificates that have one of the
                special properties (Secure_Boot or CRL_Sign) asserted in
                the extensions field. Note: This field must be False if
                CA_OK is False.
            :ivar reserved:
            """
            granted_rights: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Granted_Rights",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{8}",
                }
            )
            secure_boot: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Secure_Boot",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            ca_ok: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "CA_OK",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            ca_parent: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "CA_Parent",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            crl_sign: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "CRL_Sign",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            special_only: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Special_Only",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{3}",
                }
            )

        @dataclass
        class FastCryptoKeyGroup:
            """
            :ivar num_keys: Number of keys in the group (1 to 32).
            :ivar handles: False: The element contains all the keys
                concatenated together. True: The element stores all the
                handles to the key group keys concatenated together.
            :ivar reserved:
            :ivar partial_forbidden: False: Accesses of this element may
                read/write/use any number of bytes within the element.
                True: All accesses of this element must use all the
                bytes within the element.
            """
            num_keys: Optional[int] = field(
                default=None,
                metadata={
                    "name": "Num_Keys",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "min_inclusive": 1,
                    "max_inclusive": 32,
                }
            )
            handles: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Handles",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{9}",
                }
            )
            partial_forbidden: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Partial_Forbidden",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )

        @dataclass
        class Crl:
            """
            :ivar num_digests: Number of identity digests in this list.
            :ivar reserved:
            """
            num_digests: Optional[int] = field(
                default=None,
                metadata={
                    "name": "Num_Digests",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "min_inclusive": 1,
                    "max_inclusive": 256,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0b[01]{8}",
                }
            )


@dataclass
class GpiopinType:
    """
    :ivar gpio_input: GPIO is configured as an input. Reading the
        corresponding GPIO always returns the current state. No
        authorization is required to read a pin state.
    :ivar gpio_output:
    :ivar gpio_secure_boot:
    :ivar gpio_pulse:
    :ivar gpio_boot_level:
    :ivar gpio_reserved_5:
    :ivar gpio_reserved_6:
    :ivar gpio_reserved_7:
    """
    class Meta:
        name = "GPIOPinType"

    gpio_input: Optional["GpiopinType.GpioInput"] = field(
        default=None,
        metadata={
            "name": "GPIO_Input",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    gpio_output: Optional["GpiopinType.GpioOutput"] = field(
        default=None,
        metadata={
            "name": "GPIO_Output",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    gpio_secure_boot: Optional["GpiopinType.GpioSecureBoot"] = field(
        default=None,
        metadata={
            "name": "GPIO_Secure_Boot",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    gpio_pulse: Optional["GpiopinType.GpioPulse"] = field(
        default=None,
        metadata={
            "name": "GPIO_Pulse",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    gpio_boot_level: Optional["GpiopinType.GpioBootLevel"] = field(
        default=None,
        metadata={
            "name": "GPIO_Boot_Level",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    gpio_reserved_5: Optional["GpiopinType.GpioReserved5"] = field(
        default=None,
        metadata={
            "name": "GPIO_Reserved_5",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    gpio_reserved_6: Optional["GpiopinType.GpioReserved6"] = field(
        default=None,
        metadata={
            "name": "GPIO_Reserved_6",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    gpio_reserved_7: Optional["GpiopinType.GpioReserved7"] = field(
        default=None,
        metadata={
            "name": "GPIO_Reserved_7",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )

    @dataclass
    class GpioInput:
        """
        :ivar reserved: Reserved, must be 0b00000
        """
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"0b[01]{5}",
            }
        )

    @dataclass
    class GpioOutput:
        """
        GPIO is configured as an output controlled via the Write command.

        :ivar default_state: On power-up, brownout, RESET pin assertion,
            or other boot events, the pin will be forced to this default
            state. Low or High.
        :ivar auth_required: If True, the Write command must be executed
            in an authorization session initiated with
            config.gpio_auth_key.
        :ivar reserved: Reserved, must be 0b000
        """
        default_state: Optional[GpioOutputDefaultState] = field(
            default=None,
            metadata={
                "name": "Default_State",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        auth_required: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Auth_Required",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"0b[01]{3}",
            }
        )

    @dataclass
    class GpioSecureBoot:
        """GPIO will be configured to drive this pin to match the complement of the
        Secure_Boot VCC latch.

        On power-up, brownout, RESET pin assertion, or other boot
        events, this pin will be driven high. When a successful secure
        boot completes, this pin will be driven low.

        :ivar reserved: Reserved, must be 0b00000
        """
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"0b[01]{5}",
            }
        )

    @dataclass
    class GpioPulse:
        """GPIO_1 can effectively be configured to operate as an output following the
        Reset state of the device.

        When configured to be in this mode with Command_Complete,
        Init_Complete, Secure_Boot_Warn, and Secure_Boot_Clear set to
        False, the GPIO_1 output will be driven low during a POR, RESET
        pin assertion, brown-out, soft reboot, or any internal fault. It
        will then be driven high after a short delay (~1.5 ms) after the
        device reset source is released, as the device reboots. GPIO_1
        will not be driven low when the device is in Sleep mode.

        :ivar command_complete: If True, the TA100 device will pulse
            this pin low for ~1 μs near the completion of a command. A
            short time after the rising edge of this pin, response data
            are available to be read. The host can begin polling the
            CSR.RRDY bit at this time to reduce the time spent polling
            for the completion of the command.
        :ivar init_complete: If True, the TA100 device will pulse this
            pin low for ~2 μs when the initialization process has
            completed and the device is about ready to accept a command.
            This mode may not be useful for GPIO_1, which will be driven
            low immediately after reset/power-up, then driven high when
            the configuration memory is read from the internal EEPROM,
            then driven low a little later when the initialization
            process has completed.
        :ivar secure_boot_warn: If True, the TA100 device will pulse
            this GPIO pin low for ~3 μs when the secure boot warning
            timer expires, which occurs at 50% of the overall
            secure_boot timer. If the timer expires while the TA100
            device is asleep, the pin will still be asserted without
            causing the device to wake up.
        :ivar secure_boot_clear: If True, the TA100 device will pulse
            this GPIO pin low for ~4 μs when the secure boot clear_timer
            expires, or the secure boot retry count is reached.
        :ivar reserved: Reserved, must be 0b0
        """
        command_complete: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Command_Complete",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        init_complete: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Init_Complete",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        secure_boot_warn: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Secure_Boot_Warn",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        secure_boot_clear: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Secure_Boot_Clear",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"0b[01]",
            }
        )

    @dataclass
    class GpioBootLevel:
        """Drive this GPIO pin high when the TA100 device has completed its
        initialization process and is about ready to accept a command.

        It will be driven low on a power-up, brown-out, RESET pin
        assertion, soft reboot, or other internal fault events. It is
        also driven low when the device is in Sleep mode. Do not use
        this configuration for any pin other than GPIO_1.

        :ivar reserved: Reserved, must be 0b00000
        """
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"0b[01]{5}",
            }
        )

    @dataclass
    class GpioReserved5:
        """
        :ivar reserved: Reserved, must be 0b00000
        """
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"0b[01]{5}",
            }
        )

    @dataclass
    class GpioReserved6:
        """
        :ivar reserved: Reserved, must be 0b00000
        """
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"0b[01]{5}",
            }
        )

    @dataclass
    class GpioReserved7:
        """
        :ivar reserved: Reserved, must be 0b00000
        """
        reserved: Optional[str] = field(
            default=None,
            metadata={
                "name": "Reserved",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"0b[01]{5}",
            }
        )


@dataclass
class PublicBinaryData:
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    encoding: Optional[PublicBinaryDataEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class PullUpConfig:
    cs_sck_si: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "CS_SCK_SI",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    sda_scl: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "SDA_SCL",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    so: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "SO",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    gpio_1: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "GPIO_1",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    gpio_2: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "GPIO_2",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    gpio_3: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "GPIO_3",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    reset: Optional[Boolean] = field(
        default=None,
        metadata={
            "name": "RESET",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    unbonded: Optional["PullUpConfig.Unbonded"] = field(
        default=None,
        metadata={
            "name": "Unbonded",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class Unbonded:
        rst2: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "RST2",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )


@dataclass
class SelfTests:
    """
    :ivar fc_aes: AES-CMAC in the Fast Crypto Engine
    :ivar fc_sha: SHA and SHA-HMAC in the Fast Crypto Engine
    :ivar cmac: AES-CMAC in the main command Processor
    :ivar gcm: AES-GCM in the main command processor
    :ivar kdf: KDF - SP800-108 based on SHA256/HMAC Counter mode in the
        main command processor
    :ivar sha: SHA and SHA-HMAC in the main command processor
    :ivar prf: PRF based on SHA256/HMAC
    :ivar hkdf: HKDF Based on SHA256/HMAC
    :ivar nrbg: RNG health test of noise source
    :ivar drbg: RNG digital test using AES_CTR mode DRBG
    :ivar reserved_10: Reserved, must be 0b0
    :ivar ecdsa: ECC (ECDSA) sign and verify, P256 curve
    :ivar ecdh: ECDH, P256 Curve
    :ivar rsa: RSA sign and verify, 2048-bit modulus
    :ivar ecbd: ECBD, P224 curve
    :ivar key: Stored key integrity test using the CRC algorithm
    :ivar reserved_16: Reserved, must be 0b0
    :ivar rom: Integrity tests of all ROMs within the device and any
        loaded patch code in the EEPROM.
    :ivar reserved_18: Reserved, must be 0b0000000000000
    """
    fc_aes: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "FC_AES",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    fc_sha: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "FC_SHA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    cmac: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "CMAC",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    gcm: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "GCM",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    kdf: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "KDF",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    sha: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "SHA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    prf: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "PRF",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    hkdf: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "HKDF",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    nrbg: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "NRBG",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    drbg: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "DRBG",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    reserved_10: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reserved_10",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0b[01]",
        }
    )
    ecdsa: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "ECDSA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    ecdh: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "ECDH",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    rsa: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "RSA",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    ecbd: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "ECBD",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    key: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "KEY",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    reserved_16: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reserved_16",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0b[01]",
        }
    )
    rom: Optional[BooleanEnabled] = field(
        default=None,
        metadata={
            "name": "ROM",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    reserved_18: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reserved_18",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"0b[01]{14}",
        }
    )


@dataclass
class StringOrDataOrFromSource:
    """Base type for specifying static data or dynamic data from a data source.

    When from_source attribute is set to False, this indicates static
    data and the encoding attribute must be used to indicate how the
    data is encoded. Hex and Base64 are for expressing raw binary
    values. String indicates the element contents should be used as is.
    When from_source attribute is True, the element contains a data
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
    from_source: Optional[Boolean] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    encoding: Optional[StringOrDataOrFromSourceEncoding] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class X509Time:
    value: str = field(
        default="",
        metadata={
            "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
        }
    )
    type: Optional[X509TimeType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    from_source: Optional[Boolean] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class DirectoryStringOrFromSource(StringOrDataOrFromSource):
    """Express a string using either the PrintableString or UTF8String types.

    Also allows specifying a data source as the data. While technically
    this is meant to mirror the X520name definition, the rarely used
    TeletexString, UniversalString, and BMPString types are unsupported.
    The Raw type allows one to specify the raw ASN.1 data for the value.
    Data must include a properly formed tag, length, and value in DER
    encoding. encoding attribute must be Hex or Base64 for this type.
    """
    type: Optional[DirectoryStringOrFromSourceType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Ia5StringOrFromSource(StringOrDataOrFromSource):
    """Express a string using the IA5String type directly or from a data source.

    The Raw type allows one to specify the raw ASN.1 data for the value
    must include properly formed tag, length, and value in DER encoding.
    encoding attribute must be Hex or Base64 for this type.
    """
    class Meta:
        name = "IA5StringOrFromSource"

    type: Optional[Ia5StringOrFromSourceType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class PrintableStringOrFromSource(StringOrDataOrFromSource):
    """Express a string using the PrintableString type directly or from a data
    source.

    The Raw type allows one to specify the raw ASN.1 data for the value.
    Data must include properly formed tag, length, and value in DER
    encoding. encoding attribute must be Hex or Base64 for this type.
    """
    type: Optional[PrintableStringOrFromSourceType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class StaticDataPrivateKey:
    secret: Optional["StaticDataPrivateKey.Secret"] = field(
        default=None,
        metadata={
            "name": "Secret",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )

    @dataclass
    class Secret(BinaryData):
        encrypted: Optional[Boolean] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        algorithm: Optional[SecretAlgorithm] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        format: Optional[SecretFormat] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
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
class StaticDataPublicKey:
    public: Optional["StaticDataPublicKey.Public"] = field(
        default=None,
        metadata={
            "name": "Public",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    secret: Optional["StaticDataPublicKey.Secret"] = field(
        default=None,
        metadata={
            "name": "Secret",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )

    @dataclass
    class Public:
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
    class Secret(BinaryData):
        encrypted: Optional[Boolean] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        algorithm: Optional[SecretAlgorithm] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        format: Optional[SecretFormat] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
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
class WrappedKeyItem:
    class Meta:
        name = "Wrapped_Key_Item"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    key: Optional["WrappedKeyItem.Key"] = field(
        default=None,
        metadata={
            "name": "Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )
    wrapping_public_key: Optional["WrappedKeyItem.WrappingPublicKey"] = field(
        default=None,
        metadata={
            "name": "Wrapping_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
        }
    )

    @dataclass
    class Key(BinaryData):
        algorithm: Optional[KeyAlgorithm] = field(
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
        encoding: Optional[WrappingPublicKeyEncoding] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        format: Optional[WrappingPublicKeyFormat] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )


@dataclass
class X509Name:
    relative_distinguished_name: List["X509Name.RelativeDistinguishedName"] = field(
        default_factory=list,
        metadata={
            "name": "Relative_Distinguished_Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )

    @dataclass
    class RelativeDistinguishedName:
        attribute_type_and_value: Optional["X509Name.RelativeDistinguishedName.AttributeTypeAndValue"] = field(
            default=None,
            metadata={
                "name": "Attribute_Type_And_Value",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        common_name: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Common_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        surname: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Surname",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        serial_number: Optional[PrintableStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Serial_Number",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        country_name: Optional[PrintableStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Country_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        locality_name: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Locality_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        state_or_province_name: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "State_Or_Province_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        organization_name: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Organization_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        organizational_unit_name: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Organizational_Unit_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        title: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Title",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        given_name: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Given_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        initials: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Initials",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        generation_qualifier: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Generation_Qualifier",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        dn_qualifier: Optional[PrintableStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "DN_Qualifier",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        pseudonym: Optional[DirectoryStringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Pseudonym",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        domain_component: Optional[Ia5StringOrFromSource] = field(
            default=None,
            metadata={
                "name": "Domain_Component",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )

        @dataclass
        class AttributeTypeAndValue:
            type: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Type",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"[0-9]+(\.[0-9]+)*",
                }
            )
            value: Optional[BinaryDataOrFromSource] = field(
                default=None,
                metadata={
                    "name": "Value",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )


@dataclass
class DataSourceItem:
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
        process and the device being provisioned.  Device information
        depends on the device being provisioned. TA100 - Serial_Number:
        Bytes
    :ivar bytes_encode:
    :ivar date_time_modify:
    :ivar current_date_time:
    :ivar template:
    :ivar x509_certificate:
    :ivar counter:
    :ivar hash:
    :ivar qi_certificate_chain:
    """
    class Meta:
        name = "Data_Source_Item"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            "required": True,
            "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    static_bytes: Optional["DataSourceItem.StaticBytes"] = field(
        default=None,
        metadata={
            "name": "Static_Bytes",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    static_ecc_private_key: Optional[StaticDataPrivateKey] = field(
        default=None,
        metadata={
            "name": "Static_ECC_Private_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    static_ecc_public_key: Optional[StaticDataPublicKey] = field(
        default=None,
        metadata={
            "name": "Static_ECC_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    static_rsa_private_key: Optional[StaticDataPrivateKey] = field(
        default=None,
        metadata={
            "name": "Static_RSA_Private_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    static_rsa_public_key: Optional[StaticDataPublicKey] = field(
        default=None,
        metadata={
            "name": "Static_RSA_Public_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    static_date_time: Optional["DataSourceItem.StaticDateTime"] = field(
        default=None,
        metadata={
            "name": "Static_Date_Time",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    database_data: Optional["DataSourceItem.DatabaseData"] = field(
        default=None,
        metadata={
            "name": "Database_Data",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    hsm_generate_key: Optional["DataSourceItem.HsmGenerateKey"] = field(
        default=None,
        metadata={
            "name": "HSM_Generate_Key",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    force_nonnegative_fixed_size: Optional["DataSourceItem.ForceNonnegativeFixedSize"] = field(
        default=None,
        metadata={
            "name": "Force_Nonnegative_Fixed_Size",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    hsm_random: Optional["DataSourceItem.HsmRandom"] = field(
        default=None,
        metadata={
            "name": "HSM_Random",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    process_info: Optional[object] = field(
        default=None,
        metadata={
            "name": "Process_Info",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    bytes_encode: Optional["DataSourceItem.BytesEncode"] = field(
        default=None,
        metadata={
            "name": "Bytes_Encode",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    date_time_modify: Optional["DataSourceItem.DateTimeModify"] = field(
        default=None,
        metadata={
            "name": "Date_Time_Modify",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    current_date_time: Optional[object] = field(
        default=None,
        metadata={
            "name": "Current_Date_Time",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    template: Optional["DataSourceItem.Template"] = field(
        default=None,
        metadata={
            "name": "Template",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    x509_certificate: Optional["DataSourceItem.X509Certificate"] = field(
        default=None,
        metadata={
            "name": "X509_Certificate",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    counter: Optional["DataSourceItem.Counter"] = field(
        default=None,
        metadata={
            "name": "Counter",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    hash: Optional["DataSourceItem.Hash"] = field(
        default=None,
        metadata={
            "name": "Hash",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )
    qi_certificate_chain: Optional["DataSourceItem.QiCertificateChain"] = field(
        default=None,
        metadata={
            "name": "Qi_Certificate_Chain",
            "type": "Element",
            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
        }
    )

    @dataclass
    class StaticBytes:
        public: Optional[PublicBinaryData] = field(
            default=None,
            metadata={
                "name": "Public",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        secret: Optional["DataSourceItem.StaticBytes.Secret"] = field(
            default=None,
            metadata={
                "name": "Secret",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )

        @dataclass
        class Secret(BinaryData):
            encrypted: Optional[Boolean] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )
            algorithm: Optional[SecretAlgorithm] = field(
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
    class StaticDateTime:
        public: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "Public",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

    @dataclass
    class DatabaseData:
        record_set_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "Record_Set_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        fields: Optional["DataSourceItem.DatabaseData.Fields"] = field(
            default=None,
            metadata={
                "name": "Fields",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

        @dataclass
        class Fields:
            field_value: List["DataSourceItem.DatabaseData.Fields.Field"] = field(
                default_factory=list,
                metadata={
                    "name": "Field",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "min_occurs": 1,
                }
            )

            @dataclass
            class Field:
                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                        "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*",
                    }
                )
                type: Optional[FieldType] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )

    @dataclass
    class HsmGenerateKey:
        rsa: Optional["DataSourceItem.HsmGenerateKey.Rsa"] = field(
            default=None,
            metadata={
                "name": "RSA",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )
        ecc: Optional["DataSourceItem.HsmGenerateKey.Ecc"] = field(
            default=None,
            metadata={
                "name": "ECC",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
            }
        )

        @dataclass
        class Rsa:
            key_size: Optional[int] = field(
                default=None,
                metadata={
                    "name": "Key_Size",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "min_inclusive": 512,
                }
            )
            exponent: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Exponent",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                    "pattern": r"0x([0-9a-fA-F]{2})+",
                }
            )

        @dataclass
        class Ecc:
            """
            :ivar curve:
            :ivar compact: If True, the generated key pair will have a
                public key that can be represented by the ECC Compact
                form as defined in https://tools.ietf.org/id/draft-
                jivsov-ecc-compact-05.html
            """
            curve: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Curve",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            compact: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Compact",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                }
            )

    @dataclass
    class ForceNonnegativeFixedSize:
        input: Optional[str] = field(
            default=None,
            metadata={
                "name": "Input",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )

    @dataclass
    class HsmRandom:
        size: Optional[int] = field(
            default=None,
            metadata={
                "name": "Size",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "min_inclusive": 1,
            }
        )
        secret_data: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Secret_Data",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

    @dataclass
    class BytesEncode:
        input: Optional[str] = field(
            default=None,
            metadata={
                "name": "Input",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )
        algorithm: Optional["DataSourceItem.BytesEncode.Algorithm"] = field(
            default=None,
            metadata={
                "name": "Algorithm",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

        @dataclass
        class Algorithm:
            hex: Optional["DataSourceItem.BytesEncode.Algorithm.Hex"] = field(
                default=None,
                metadata={
                    "name": "Hex",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                }
            )

            @dataclass
            class Hex:
                case: Optional[HexCase] = field(
                    default=None,
                    metadata={
                        "name": "Case",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )
                separator: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Separator",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )

    @dataclass
    class DateTimeModify:
        input: Optional[str] = field(
            default=None,
            metadata={
                "name": "Input",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )
        add_period: Optional[XmlDuration] = field(
            default=None,
            metadata={
                "name": "Add_Period",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

    @dataclass
    class Template:
        definition: Optional["DataSourceItem.Template.Definition"] = field(
            default=None,
            metadata={
                "name": "Definition",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

        @dataclass
        class Definition:
            value: str = field(
                default="",
                metadata={
                    "required": True,
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
    class X509Certificate:
        tbs_certificate: Optional["DataSourceItem.X509Certificate.TbsCertificate"] = field(
            default=None,
            metadata={
                "name": "TBS_Certificate",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        signature_algorithm: Optional["DataSourceItem.X509Certificate.SignatureAlgorithm"] = field(
            default=None,
            metadata={
                "name": "Signature_Algorithm",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        ca_certificate_chain: Optional["DataSourceItem.X509Certificate.CaCertificateChain"] = field(
            default=None,
            metadata={
                "name": "CA_Certificate_Chain",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

        @dataclass
        class TbsCertificate:
            version: Optional[TbsCertificateVersion] = field(
                default=None,
                metadata={
                    "name": "Version",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            serial_number: Optional["DataSourceItem.X509Certificate.TbsCertificate.SerialNumber"] = field(
                default=None,
                metadata={
                    "name": "Serial_Number",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            validity: Optional["DataSourceItem.X509Certificate.TbsCertificate.Validity"] = field(
                default=None,
                metadata={
                    "name": "Validity",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            subject: Optional[X509Name] = field(
                default=None,
                metadata={
                    "name": "Subject",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            subject_public_key_info: Optional["DataSourceItem.X509Certificate.TbsCertificate.SubjectPublicKeyInfo"] = field(
                default=None,
                metadata={
                    "name": "Subject_Public_Key_Info",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    "required": True,
                }
            )
            issuer_unique_id: Optional[TbsCertificateIssuerUniqueId] = field(
                default=None,
                metadata={
                    "name": "Issuer_Unique_ID",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                }
            )
            subject_unique_id: Optional["DataSourceItem.X509Certificate.TbsCertificate.SubjectUniqueId"] = field(
                default=None,
                metadata={
                    "name": "Subject_Unique_ID",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                }
            )
            extensions: Optional["DataSourceItem.X509Certificate.TbsCertificate.Extensions"] = field(
                default=None,
                metadata={
                    "name": "Extensions",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                }
            )

            @dataclass
            class SerialNumber:
                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                        "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
                    }
                )
                from_source: Boolean = field(
                    init=False,
                    default=Boolean.TRUE,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )

            @dataclass
            class Validity:
                not_before: Optional[X509Time] = field(
                    default=None,
                    metadata={
                        "name": "Not_Before",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )
                not_after: Optional[X509Time] = field(
                    default=None,
                    metadata={
                        "name": "Not_After",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )

            @dataclass
            class SubjectPublicKeyInfo:
                key: Optional["DataSourceItem.X509Certificate.TbsCertificate.SubjectPublicKeyInfo.Key"] = field(
                    default=None,
                    metadata={
                        "name": "Key",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )
                options: Optional["DataSourceItem.X509Certificate.TbsCertificate.SubjectPublicKeyInfo.Options"] = field(
                    default=None,
                    metadata={
                        "name": "Options",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
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
                    from_source: Boolean = field(
                        init=False,
                        default=Boolean.TRUE,
                        metadata={
                            "type": "Attribute",
                            "required": True,
                        }
                    )

                @dataclass
                class Options:
                    ecc: Optional["DataSourceItem.X509Certificate.TbsCertificate.SubjectPublicKeyInfo.Options.Ecc"] = field(
                        default=None,
                        metadata={
                            "name": "ECC",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        }
                    )

                    @dataclass
                    class Ecc:
                        format: Optional[EccFormat] = field(
                            default=None,
                            metadata={
                                "name": "Format",
                                "type": "Element",
                                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                                "required": True,
                            }
                        )

            @dataclass
            class SubjectUniqueId:
                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                        "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
                    }
                )
                from_source: Boolean = field(
                    init=False,
                    default=Boolean.TRUE,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )

            @dataclass
            class Extensions:
                extension: List["DataSourceItem.X509Certificate.TbsCertificate.Extensions.Extension"] = field(
                    default_factory=list,
                    metadata={
                        "name": "Extension",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    }
                )
                authority_key_identifier: List["DataSourceItem.X509Certificate.TbsCertificate.Extensions.AuthorityKeyIdentifier"] = field(
                    default_factory=list,
                    metadata={
                        "name": "Authority_Key_Identifier",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    }
                )
                subject_key_identifier: List["DataSourceItem.X509Certificate.TbsCertificate.Extensions.SubjectKeyIdentifier"] = field(
                    default_factory=list,
                    metadata={
                        "name": "Subject_Key_Identifier",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    }
                )
                key_usage: List["DataSourceItem.X509Certificate.TbsCertificate.Extensions.KeyUsage"] = field(
                    default_factory=list,
                    metadata={
                        "name": "Key_Usage",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    }
                )
                basic_constraints: List["DataSourceItem.X509Certificate.TbsCertificate.Extensions.BasicConstraints"] = field(
                    default_factory=list,
                    metadata={
                        "name": "Basic_Constraints",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    }
                )
                extended_key_usage: List["DataSourceItem.X509Certificate.TbsCertificate.Extensions.ExtendedKeyUsage"] = field(
                    default_factory=list,
                    metadata={
                        "name": "Extended_Key_Usage",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                    }
                )

                @dataclass
                class Extension:
                    extn_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Extn_ID",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                            "pattern": r"[0-9]+(\.[0-9]+)*",
                        }
                    )
                    critical: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Critical",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    extn_value: Optional[BinaryDataOrFromSource] = field(
                        default=None,
                        metadata={
                            "name": "Extn_Value",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )

                @dataclass
                class AuthorityKeyIdentifier:
                    critical: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Critical",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    id_method: Optional["DataSourceItem.X509Certificate.TbsCertificate.Extensions.AuthorityKeyIdentifier.IdMethod"] = field(
                        default=None,
                        metadata={
                            "name": "ID_Method",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )

                    @dataclass
                    class IdMethod:
                        key_identifier: Optional["DataSourceItem.X509Certificate.TbsCertificate.Extensions.AuthorityKeyIdentifier.IdMethod.KeyIdentifier"] = field(
                            default=None,
                            metadata={
                                "name": "Key_Identifier",
                                "type": "Element",
                                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            }
                        )
                        issuer_and_serial_number: Optional[IdMethodIssuerAndSerialNumber] = field(
                            default=None,
                            metadata={
                                "name": "Issuer_And_Serial_Number",
                                "type": "Element",
                                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            }
                        )

                        @dataclass
                        class KeyIdentifier:
                            from_ca_subject_key_identifier: Optional[object] = field(
                                default=None,
                                metadata={
                                    "name": "From_CA_Subject_Key_Identifier",
                                    "type": "Element",
                                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                                }
                            )
                            calculated: Optional["DataSourceItem.X509Certificate.TbsCertificate.Extensions.AuthorityKeyIdentifier.IdMethod.KeyIdentifier.Calculated"] = field(
                                default=None,
                                metadata={
                                    "name": "Calculated",
                                    "type": "Element",
                                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                                }
                            )

                            @dataclass
                            class Calculated:
                                """
                                :ivar method:
                                :ivar truncated_size: Override the
                                    default key ID size for the chosen
                                    method.
                                """
                                method: Optional[KeyIdentifierCalculatedTokens] = field(
                                    default=None,
                                    metadata={
                                        "name": "Method",
                                        "type": "Element",
                                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                                        "required": True,
                                    }
                                )
                                truncated_size: Optional[int] = field(
                                    default=None,
                                    metadata={
                                        "name": "Truncated_Size",
                                        "type": "Element",
                                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                                    }
                                )

                @dataclass
                class SubjectKeyIdentifier:
                    critical: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Critical",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    key_identifier: Optional["DataSourceItem.X509Certificate.TbsCertificate.Extensions.SubjectKeyIdentifier.KeyIdentifier"] = field(
                        default=None,
                        metadata={
                            "name": "Key_Identifier",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
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
                                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
                            }
                        )
                        calculated: Optional["DataSourceItem.X509Certificate.TbsCertificate.Extensions.SubjectKeyIdentifier.KeyIdentifier.Calculated"] = field(
                            default=None,
                            metadata={
                                "name": "Calculated",
                                "type": "Element",
                                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            }
                        )

                        @dataclass
                        class Calculated:
                            """
                            :ivar method:
                            :ivar truncated_size: Override the default
                                key ID size for the chosen method.
                            """
                            method: Optional[KeyIdentifierCalculatedTokens] = field(
                                default=None,
                                metadata={
                                    "name": "Method",
                                    "type": "Element",
                                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                                    "required": True,
                                }
                            )
                            truncated_size: Optional[int] = field(
                                default=None,
                                metadata={
                                    "name": "Truncated_Size",
                                    "type": "Element",
                                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                                }
                            )

                @dataclass
                class KeyUsage:
                    critical: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Critical",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    digital_signature: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Digital_Signature",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    content_commitment: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Content_Commitment",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    key_encipherment: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Key_Encipherment",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    data_encipherment: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Data_Encipherment",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    key_agreement: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Key_Agreement",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    key_cert_sign: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Key_Cert_Sign",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    crl_sign: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "CRL_Sign",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    encipher_only: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Encipher_Only",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    decipher_only: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Decipher_Only",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )

                @dataclass
                class BasicConstraints:
                    critical: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Critical",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    ca: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "CA",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    path_len_constraint: Optional[BasicConstraintsValue] = field(
                        default=None,
                        metadata={
                            "name": "Path_Len_Constraint",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        }
                    )

                @dataclass
                class ExtendedKeyUsage:
                    critical: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "Critical",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "required": True,
                        }
                    )
                    key_purpose_id: List[str] = field(
                        default_factory=list,
                        metadata={
                            "name": "Key_Purpose_Id",
                            "type": "Element",
                            "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                            "pattern": r"[0-9]+(\.[0-9]+)*",
                        }
                    )

        @dataclass
        class SignatureAlgorithm:
            ecdsa: Optional["DataSourceItem.X509Certificate.SignatureAlgorithm.Ecdsa"] = field(
                default=None,
                metadata={
                    "name": "ECDSA",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                }
            )
            rsassa_pkcs1_v1_5: Optional["DataSourceItem.X509Certificate.SignatureAlgorithm.RsassaPkcs1V15"] = field(
                default=None,
                metadata={
                    "name": "RSASSA_PKCS1_V1_5",
                    "type": "Element",
                    "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                }
            )

            @dataclass
            class Ecdsa:
                hash: Optional[HashAlgorithms] = field(
                    default=None,
                    metadata={
                        "name": "Hash",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )

            @dataclass
            class RsassaPkcs1V15:
                hash: Optional[HashAlgorithms] = field(
                    default=None,
                    metadata={
                        "name": "Hash",
                        "type": "Element",
                        "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                        "required": True,
                    }
                )

        @dataclass
        class CaCertificateChain:
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

    @dataclass
    class Counter:
        counter_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "Counter_Name",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        size: Optional[int] = field(
            default=None,
            metadata={
                "name": "Size",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        byte_order: Optional[ByteOrder] = field(
            default=None,
            metadata={
                "name": "Byte_Order",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )
        signed: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Signed",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

    @dataclass
    class Hash:
        input: Optional[str] = field(
            default=None,
            metadata={
                "name": "Input",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )
        algorithm: Optional[HashAlgorithms] = field(
            default=None,
            metadata={
                "name": "Algorithm",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
            }
        )

    @dataclass
    class QiCertificateChain:
        root_ca_certificate: Optional[str] = field(
            default=None,
            metadata={
                "name": "Root_CA_Certificate",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )
        manufacturer_ca_certificate: Optional[str] = field(
            default=None,
            metadata={
                "name": "Manufacturer_CA_Certificate",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )
        product_unit_certificate: Optional[str] = field(
            default=None,
            metadata={
                "name": "Product_Unit_Certificate",
                "type": "Element",
                "namespace": "https://www.microchip.com/schema/TA100_Config_1.1",
                "required": True,
                "pattern": r"[a-zA-Z_][0-9a-zA-Z_]*(\.[a-zA-Z_][0-9a-zA-Z_]*)?",
            }
        )


@dataclass
class Ta100Config:
    """
    :ivar config_name:
    :ivar internal:
    :ivar nonvolatile_configuration_memory: TA100 configuration settings
        that apply to the device as a whole.
    :ivar shared_data_memory: List of elements to be created in the
        shared data memory.
    :ivar data_sources: Data sources, actions, and destinations
        (elements) are defined here.
    """
    class Meta:
        name = "TA100_Config"
        namespace = "https://www.microchip.com/schema/TA100_Config_1.1"

    config_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Config_Name",
            "type": "Element",
            "required": True,
        }
    )
    internal: Optional["Ta100Config.Internal"] = field(
        default=None,
        metadata={
            "name": "Internal",
            "type": "Element",
            "required": True,
        }
    )
    nonvolatile_configuration_memory: Optional["Ta100Config.NonvolatileConfigurationMemory"] = field(
        default=None,
        metadata={
            "name": "Nonvolatile_Configuration_Memory",
            "type": "Element",
            "required": True,
        }
    )
    shared_data_memory: Optional["Ta100Config.SharedDataMemory"] = field(
        default=None,
        metadata={
            "name": "Shared_Data_Memory",
            "type": "Element",
            "required": True,
        }
    )
    data_sources: Optional["Ta100Config.DataSources"] = field(
        default=None,
        metadata={
            "name": "Data_Sources",
            "type": "Element",
            "required": True,
        }
    )

    @dataclass
    class Internal:
        """
        Internal provisioning information for the TA100 device.

        :ivar group_number: Common number for all devices in a group
            assigned by Microchip. Used for certain internal operations.
        :ivar pull_up_map: Pin pull-ups to be enabled.
        :ivar dev_update: TA100 firmware patch information.
        :ivar options: Internal options.
        """
        group_number: Optional[str] = field(
            default=None,
            metadata={
                "name": "Group_Number",
                "type": "Element",
                "required": True,
                "pattern": r"0x[0-9a-fA-F]{4}",
            }
        )
        pull_up_map: Optional["Ta100Config.Internal.PullUpMap"] = field(
            default=None,
            metadata={
                "name": "Pull_Up_Map",
                "type": "Element",
                "required": True,
            }
        )
        dev_update: Optional["Ta100Config.Internal.DevUpdate"] = field(
            default=None,
            metadata={
                "name": "Dev_Update",
                "type": "Element",
                "required": True,
            }
        )
        options: Optional["Ta100Config.Internal.Options"] = field(
            default=None,
            metadata={
                "name": "Options",
                "type": "Element",
                "required": True,
            }
        )

        @dataclass
        class PullUpMap:
            soic8_spi: Optional["Ta100Config.Internal.PullUpMap.Soic8Spi"] = field(
                default=None,
                metadata={
                    "name": "SOIC8_SPI",
                    "type": "Element",
                }
            )
            soic8_i2_c: Optional["Ta100Config.Internal.PullUpMap.Soic8I2C"] = field(
                default=None,
                metadata={
                    "name": "SOIC8_I2C",
                    "type": "Element",
                }
            )
            soic14_spi_i2_c: Optional[PullUpConfig] = field(
                default=None,
                metadata={
                    "name": "SOIC14_SPI_I2C",
                    "type": "Element",
                }
            )
            vqfn24_spi_i2_c: Optional[PullUpConfig] = field(
                default=None,
                metadata={
                    "name": "VQFN24_SPI_I2C",
                    "type": "Element",
                }
            )
            die: Optional["Ta100Config.Internal.PullUpMap.Die"] = field(
                default=None,
                metadata={
                    "name": "DIE",
                    "type": "Element",
                }
            )

            @dataclass
            class Soic8Spi:
                cs_sck_si: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "CS_SCK_SI",
                        "type": "Element",
                        "required": True,
                    }
                )
                so: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "SO",
                        "type": "Element",
                        "required": True,
                    }
                )
                reset: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "RESET",
                        "type": "Element",
                        "required": True,
                    }
                )
                gpio_3: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "GPIO_3",
                        "type": "Element",
                        "required": True,
                    }
                )
                unbonded: Optional["Ta100Config.Internal.PullUpMap.Soic8Spi.Unbonded"] = field(
                    default=None,
                    metadata={
                        "name": "Unbonded",
                        "type": "Element",
                        "required": True,
                    }
                )

                @dataclass
                class Unbonded:
                    sda_scl: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "SDA_SCL",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    gpio_1: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "GPIO_1",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    gpio_2: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "GPIO_2",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    rst: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "RST",
                            "type": "Element",
                            "required": True,
                        }
                    )

            @dataclass
            class Soic8I2C:
                sda_scl: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "SDA_SCL",
                        "type": "Element",
                        "required": True,
                    }
                )
                gpio_1: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "GPIO_1",
                        "type": "Element",
                        "required": True,
                    }
                )
                gpio_2: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "GPIO_2",
                        "type": "Element",
                        "required": True,
                    }
                )
                gpio_3: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "GPIO_3",
                        "type": "Element",
                        "required": True,
                    }
                )
                reset: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "RESET",
                        "type": "Element",
                        "required": True,
                    }
                )
                unbonded: Optional["Ta100Config.Internal.PullUpMap.Soic8I2C.Unbonded"] = field(
                    default=None,
                    metadata={
                        "name": "Unbonded",
                        "type": "Element",
                        "required": True,
                    }
                )

                @dataclass
                class Unbonded:
                    cs_sck_si: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "CS_SCK_SI",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    rst2: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "RST2",
                            "type": "Element",
                            "required": True,
                        }
                    )
                    so: Optional[Boolean] = field(
                        default=None,
                        metadata={
                            "name": "SO",
                            "type": "Element",
                            "required": True,
                        }
                    )

            @dataclass
            class Die:
                cs_sck_si: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "CS_SCK_SI",
                        "type": "Element",
                        "required": True,
                    }
                )
                sda_scl: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "SDA_SCL",
                        "type": "Element",
                        "required": True,
                    }
                )
                rst2: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "RST2",
                        "type": "Element",
                        "required": True,
                    }
                )
                so: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "SO",
                        "type": "Element",
                        "required": True,
                    }
                )
                gpio_1: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "GPIO_1",
                        "type": "Element",
                        "required": True,
                    }
                )
                gpio_2: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "GPIO_2",
                        "type": "Element",
                        "required": True,
                    }
                )
                gpio_3: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "GPIO_3",
                        "type": "Element",
                        "required": True,
                    }
                )
                rst: Optional[Boolean] = field(
                    default=None,
                    metadata={
                        "name": "RST",
                        "type": "Element",
                        "required": True,
                    }
                )

        @dataclass
        class DevUpdate:
            """
            :ivar update_pub_key: Public key used to validate firmware
                patches to the TA100 itself (DevUpdate). Must be an ECC
                P256 public key.
            :ivar info: Update package information. Must match what is
                in the actual package.
            :ivar package: Custom update package to be applied to the
                TA100. Omit element if there is no update package or
                managed by Microchip.
            """
            update_pub_key: Optional["Ta100Config.Internal.DevUpdate.UpdatePubKey"] = field(
                default=None,
                metadata={
                    "name": "Update_Pub_Key",
                    "type": "Element",
                    "required": True,
                }
            )
            info: Optional["Ta100Config.Internal.DevUpdate.Info"] = field(
                default=None,
                metadata={
                    "name": "Info",
                    "type": "Element",
                    "required": True,
                }
            )
            package: Optional[BinaryData] = field(
                default=None,
                metadata={
                    "name": "Package",
                    "type": "Element",
                }
            )

            @dataclass
            class UpdatePubKey:
                value: str = field(
                    default="",
                    metadata={
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
                encoding: str = field(
                    init=False,
                    default="PEM",
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )

            @dataclass
            class Info:
                update_major: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "Update_Major",
                        "type": "Element",
                        "required": True,
                        "min_inclusive": 0,
                        "max_inclusive": 65535,
                    }
                )
                update_minor: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "Update_Minor",
                        "type": "Element",
                        "required": True,
                        "min_inclusive": 0,
                        "max_inclusive": 65535,
                    }
                )
                update_id: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Update_ID",
                        "type": "Element",
                        "required": True,
                        "pattern": r"0x[0-9a-fA-F]{4}",
                    }
                )

        @dataclass
        class Options:
            disable_aes: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Disable_AES",
                    "type": "Element",
                    "required": True,
                }
            )
            force_fips: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Force_FIPS",
                    "type": "Element",
                    "required": True,
                }
            )
            bsd: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "BSD",
                    "type": "Element",
                    "required": True,
                }
            )
            disable_rsa: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Disable_RSA",
                    "type": "Element",
                    "required": True,
                }
            )

    @dataclass
    class NonvolatileConfigurationMemory:
        """
        :ivar self_test: On particular events, the TA100 device
            automatically initiates a self-test of specified
            cryptographic elements within the device. Generally, they
            can be configured to run on wake, power-up, or before the
            first use, also known as on-demand.
        :ivar i2_c_address: Address on the I2C bus to which this TA100
            will respond. The LSb of this byte is ignored.
        :ivar idle: Configuration for the idle timer
        :ivar chip_options: Various chip configuration options
        :ivar passthrough: Enable GPIO inputs to pass through the device
            to other GPIO outputs
        :ivar reserved_21: Reserved, must be zeros.
        :ivar gpio: Configures the modes of the 3 GPIO pins.
        :ivar revocation: Enable revocation and set the size of the
            digest.
        :ivar compliance_options: Various options enabled when in
            compliance mode
        :ivar update_options: Options associated with device update.
        :ivar soft_reboot: Controls the availability of the soft reboot
            function. The TA100 device provides an optional method of
            forcing an internal reboot via the Power command. This may
            be useful for systems in which control of the RESET pin is
            unavailable to the host system, since the TA100 device is
            designed to be rebooted at the same time that the host MCU
            is rebooted.
        :ivar master_delete: Controls the master delete function. The
            master delete function can be used to erase all confidential
            and private/secret key material within the device including
            those within Special Handles and any internal-only keys.
        :ivar one_time: Controls the one-time function. When enabled,
            the one-time function can be used in conjunction with the
            Access_Limit field of the element attributes to limit use of
            a stored element to either portion of the power cycle before
            or after the setting of this bit.
        :ivar secure_boot: Configures the secure boot method.
        :ivar gpio_auth_key: If any of the GPIOs are configured to
            require authorization, this is the key that must be used to
            initiate that authorization session. Values from 0x8000 to
            0x80FF are permitted.
        :ivar global_export: Control the functioning of the Import and
            Export commands.
        :ivar reserved_42: Reserved, must be zeros.
        :ivar configuration_lock: Set to True, if the config zone is to
            be locked. False if it should be left unlocked.
        """
        self_test: Optional["Ta100Config.NonvolatileConfigurationMemory.SelfTest"] = field(
            default=None,
            metadata={
                "name": "Self_Test",
                "type": "Element",
                "required": True,
            }
        )
        i2_c_address: Optional["Ta100Config.NonvolatileConfigurationMemory.I2CAddress"] = field(
            default=None,
            metadata={
                "name": "I2C_Address",
                "type": "Element",
                "required": True,
            }
        )
        idle: Optional["Ta100Config.NonvolatileConfigurationMemory.Idle"] = field(
            default=None,
            metadata={
                "name": "Idle",
                "type": "Element",
                "required": True,
            }
        )
        chip_options: Optional["Ta100Config.NonvolatileConfigurationMemory.ChipOptions"] = field(
            default=None,
            metadata={
                "name": "Chip_Options",
                "type": "Element",
                "required": True,
            }
        )
        passthrough: Optional["Ta100Config.NonvolatileConfigurationMemory.Passthrough"] = field(
            default=None,
            metadata={
                "name": "Passthrough",
                "type": "Element",
                "required": True,
            }
        )
        reserved_21: Optional["Ta100Config.NonvolatileConfigurationMemory.Reserved21"] = field(
            default=None,
            metadata={
                "name": "Reserved_21",
                "type": "Element",
                "required": True,
            }
        )
        gpio: Optional["Ta100Config.NonvolatileConfigurationMemory.Gpio"] = field(
            default=None,
            metadata={
                "name": "GPIO",
                "type": "Element",
                "required": True,
            }
        )
        revocation: Optional["Ta100Config.NonvolatileConfigurationMemory.Revocation"] = field(
            default=None,
            metadata={
                "name": "Revocation",
                "type": "Element",
                "required": True,
            }
        )
        compliance_options: Optional["Ta100Config.NonvolatileConfigurationMemory.ComplianceOptions"] = field(
            default=None,
            metadata={
                "name": "Compliance_Options",
                "type": "Element",
                "required": True,
            }
        )
        update_options: Optional["Ta100Config.NonvolatileConfigurationMemory.UpdateOptions"] = field(
            default=None,
            metadata={
                "name": "Update_Options",
                "type": "Element",
                "required": True,
            }
        )
        soft_reboot: Optional["Ta100Config.NonvolatileConfigurationMemory.SoftReboot"] = field(
            default=None,
            metadata={
                "name": "Soft_Reboot",
                "type": "Element",
                "required": True,
            }
        )
        master_delete: Optional["Ta100Config.NonvolatileConfigurationMemory.MasterDelete"] = field(
            default=None,
            metadata={
                "name": "Master_Delete",
                "type": "Element",
                "required": True,
            }
        )
        one_time: Optional["Ta100Config.NonvolatileConfigurationMemory.OneTime"] = field(
            default=None,
            metadata={
                "name": "One_Time",
                "type": "Element",
                "required": True,
            }
        )
        secure_boot: Optional["Ta100Config.NonvolatileConfigurationMemory.SecureBoot"] = field(
            default=None,
            metadata={
                "name": "Secure_Boot",
                "type": "Element",
                "required": True,
            }
        )
        gpio_auth_key: Optional[str] = field(
            default=None,
            metadata={
                "name": "GPIO_Auth_Key",
                "type": "Element",
                "required": True,
                "pattern": r"0x80[0-9a-fA-F]{2}",
            }
        )
        global_export: Optional["Ta100Config.NonvolatileConfigurationMemory.GlobalExport"] = field(
            default=None,
            metadata={
                "name": "Global_Export",
                "type": "Element",
                "required": True,
            }
        )
        reserved_42: Optional["Ta100Config.NonvolatileConfigurationMemory.Reserved42"] = field(
            default=None,
            metadata={
                "name": "Reserved_42",
                "type": "Element",
                "required": True,
            }
        )
        configuration_lock: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Configuration_Lock",
                "type": "Element",
                "required": True,
            }
        )

        @dataclass
        class SelfTest:
            """
            :ivar power_up: Determines which blocks within the TA100
                device will be automatically tested when power is
                applied, on assertion of the input RESET pin, or after a
                brown-out, when VCC rises above VPOR. These tests are
                not run on a wake from sleep.
            :ivar wake: Determines which blocks within the TA100 device
                will be automatically tested on a wake for I/O activity.
                These tests are not run on a power-up.
            :ivar on_demand: Tests in this list will not be
                automatically run until a command requiring the
                corresponding algorithm is executed.
            :ivar failure_clear: Determines which blocks within the
                TA100 device must pass any self-test instance before the
                device clears the Self_Test_Failure state. All tests
                indicated in this list must pass a single self-test
                instance to clear the Failure mode.
            """
            power_up: Optional[SelfTests] = field(
                default=None,
                metadata={
                    "name": "Power_Up",
                    "type": "Element",
                    "required": True,
                }
            )
            wake: Optional[SelfTests] = field(
                default=None,
                metadata={
                    "name": "Wake",
                    "type": "Element",
                    "required": True,
                }
            )
            on_demand: Optional[SelfTests] = field(
                default=None,
                metadata={
                    "name": "On_Demand",
                    "type": "Element",
                    "required": True,
                }
            )
            failure_clear: Optional[SelfTests] = field(
                default=None,
                metadata={
                    "name": "Failure_Clear",
                    "type": "Element",
                    "required": True,
                }
            )

        @dataclass
        class I2CAddress:
            """
            :ivar i2_c_address_7bit: 7-bit address on the I2C bus to
                which this TA100 will respond.
            :ivar lsb: Least significant bit of the I2C_Address field.
                Ignored, but should be 0b0.
            """
            i2_c_address_7bit: Optional[str] = field(
                default=None,
                metadata={
                    "name": "I2C_Address_7bit",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0x[0-7][0-9a-fA-F]",
                }
            )
            lsb: Optional[str] = field(
                default=None,
                metadata={
                    "name": "LSB",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]",
                }
            )

        @dataclass
        class Idle:
            """The idle time delay should be set such that the host is sure to issue each
            command in a sequence before the timer expires, which causes the internal state
            of the TA100 device to be reset.

            Setting the idle timer to a low value will optimize the
            power consumption by ensuring that the device goes into
            Sleep mode at the earliest possible time.

            :ivar enable: False: Idle timer is disabled. True: Idle
                timer is enabled.
            :ivar time: The number of seconds between
                command/instructions before the idle timer will expire.
                Time can be between 1 and 16 secs.
            :ivar reserved: Reserved, must be 0b000
            """
            enable: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Enable",
                    "type": "Element",
                    "required": True,
                }
            )
            time: Optional[int] = field(
                default=None,
                metadata={
                    "name": "Time",
                    "type": "Element",
                    "required": True,
                    "min_inclusive": 1,
                    "max_inclusive": 16,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{3}",
                }
            )

        @dataclass
        class ChipOptions:
            """
            :ivar reset_fail: False: The Self-Test Failure condition can
                be reset via an explicit Self_Test command that includes
                in the map parameter all the bits that are set in the
                self_test_config.failure_clear map. The failure
                condition is always cleared on a power-up or RESET pin
                assertion. True: On a self-test failure only a power-up
                or RESET pin assertion will cause the Self-Test Failure
                state to be cleared. This value may be required for some
                certification regimes.
            :ivar copy_vol_reg: False: Volatile registers cannot be
                copied to shared data elements. True: Under certain
                constraints, volatile registers can be copied to shared
                data elements.
            :ivar revoke_locked: False: Permanently locked elements
                cannot be deleted via the CRL process. True: The locking
                on permanently locked extracted certificate elements can
                be overridden if the certificate is found within a CRL.
            :ivar compliance: False: No specific compliance regime is
                enforced. True: Forces compliance to some certification
                regimes.
            :ivar power_increment: False: If the time-based counter is
                enabled it will not increment on a power-up. True: If
                the time-based counter is enabled, then always increment
                the counter on a power-up.
            :ivar time_count: False: Disables the time-based counter.
                True: Enables the time-based counter.
            :ivar wake_gpio: False: GPIO_3 transitions will be ignored
                during sleep. True: The chip will wake from sleep on a
                high to low transition of the GPIO_3 pin. GPIO_3 must be
                configured as an input.
            :ivar transfer_enable: False: An attempt to perform this
                kind of transfer will result in an error return. True:
                The transfer modes of the Read and Write commands are
                enabled.
            :ivar import_cert: False: The extracted cert may not be
                exported or imported. True: The extracted certificates
                may be exported from and imported to the chip.
            :ivar hdcp_enable: False: The special HDCP features are
                disabled. Recommended for normal operation. True:
                Enables special HDCP features.
            :ivar ecbd_disable: False: ECBD function enabled. True: ECBD
                function is disabled. For best security, Microchip
                recommends that this bit always be set unless the ECBD
                computation function is known to be required for the
                application.
            :ivar sign_internal_auth: False: The FCE or SHA commands can
                be used to calculate the digest for Sign if
                prop.Sign_Use is Message_Only (2). Write(SHA) is
                forbidden. True:  SHA commands run in an auth session
                must be used to calculate the digest for Sign if
                prop.Sign_Use is Message_Only (2). FCE use is forbidden.
            :ivar hkdf_split_enable: KDF Command HKDF. Enable the
                extract and expand functions to run independently.
                False: HKDF will run extract and expand together. Zero
                length Salt or Info is an error. True: Split of HKDF
                extract and expand functions enabled.
            :ivar reserved: Reserved, must be 0b000.
            """
            reset_fail: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Reset_Fail",
                    "type": "Element",
                    "required": True,
                }
            )
            copy_vol_reg: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Copy_Vol_Reg",
                    "type": "Element",
                    "required": True,
                }
            )
            revoke_locked: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Revoke_Locked",
                    "type": "Element",
                    "required": True,
                }
            )
            compliance: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Compliance",
                    "type": "Element",
                    "required": True,
                }
            )
            power_increment: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Power_Increment",
                    "type": "Element",
                    "required": True,
                }
            )
            time_count: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Time_Count",
                    "type": "Element",
                    "required": True,
                }
            )
            wake_gpio: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Wake_GPIO",
                    "type": "Element",
                    "required": True,
                }
            )
            transfer_enable: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Transfer_Enable",
                    "type": "Element",
                    "required": True,
                }
            )
            import_cert: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Import_Cert",
                    "type": "Element",
                    "required": True,
                }
            )
            hdcp_enable: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "HDCP_Enable",
                    "type": "Element",
                    "required": True,
                }
            )
            ecbd_disable: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "ECBD_Disable",
                    "type": "Element",
                    "required": True,
                }
            )
            sign_internal_auth: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Sign_Internal_Auth",
                    "type": "Element",
                    "required": True,
                }
            )
            hkdf_split_enable: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "HKDF_Split_Enable",
                    "type": "Element",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{3}",
                }
            )

        @dataclass
        class Passthrough:
            """
            :ivar gpio_1_2: Independent: GPIO_2 operation is independent
                of GPIO_1 ANDed: GPIO_1 output is the GPIO_2 input ANDed
                with the configured function for the GPIO_1 output
            :ivar gpio_1_3: Independent: GPIO_3 operation is independent
                of GPIO_1 ANDed: GPIO_1 output is the GPIO_3 input ANDed
                with the configured function for the GPIO_1 output
            :ivar reserved: Reserved, must be 0b000000.
            """
            gpio_1_2: Optional[PassthroughBehavior] = field(
                default=None,
                metadata={
                    "name": "GPIO_1_2",
                    "type": "Element",
                    "required": True,
                }
            )
            gpio_1_3: Optional[PassthroughBehavior] = field(
                default=None,
                metadata={
                    "name": "GPIO_1_3",
                    "type": "Element",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{6}",
                }
            )

        @dataclass
        class Reserved21:
            value: str = field(
                default="",
                metadata={
                    "required": True,
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
                }
            )
            encoding: str = field(
                init=False,
                default="Hex",
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )

        @dataclass
        class Gpio:
            gpio_1: Optional[GpiopinType] = field(
                default=None,
                metadata={
                    "name": "GPIO_1",
                    "type": "Element",
                    "required": True,
                }
            )
            gpio_2: Optional[GpiopinType] = field(
                default=None,
                metadata={
                    "name": "GPIO_2",
                    "type": "Element",
                    "required": True,
                }
            )
            gpio_3: Optional[GpiopinType] = field(
                default=None,
                metadata={
                    "name": "GPIO_3",
                    "type": "Element",
                    "required": True,
                }
            )

        @dataclass
        class Revocation:
            """
            :ivar enable: False: Revocation is disabled. True:
                Revocation is enabled.
            :ivar size: The size of the possibly truncated identity
                digest used for revocation. Algorithm is always SHA256.
                The values can be 16 or 24 or 32.
            :ivar reserved: Reserved, must be 0b00000
            """
            enable: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Enable",
                    "type": "Element",
                    "required": True,
                }
            )
            size: Optional[RevocationSize] = field(
                default=None,
                metadata={
                    "name": "Size",
                    "type": "Element",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{5}",
                }
            )

        @dataclass
        class ComplianceOptions:
            """
            :ivar power_fail: If Config.chip_options.reset_fail is set
                to True Disabled: The self-test Failure state may only
                be cleared by a power cycle or assertion of the RESET
                pin. Enabled: The self-test Failure state may only be
                cleared by a power cycle. Assertion of the RESET pin
                will not suffice.
            :ivar chip_erase: Disabled: The Master_Delete function is
                disabled, attempts to execute this mode of the Delete
                command will return an error. Enabled: When authorized
                using the Master_Delete key, the entire chip contents
                can be erased. Configuration memory Master_Delete Enable
                must be True.
            :ivar config_test: Disabled: Self-test operations are not
                run when the configuration memory is locked. Enabled:
                Executes the self-test operation on all algorithms
                within the chip when the configuration memory is locked.
            :ivar always_auth: Disabled: Commands can optionally be run
                within an authorization session. Enabled: All commands
                other than Info, Power, Self_Test, Secure_Boot, and
                Manage_Cert must be run within an authorization session.
            :ivar use_hmac: Disabled: The integrity tests will use the
                CRC16 algorithm. This bit is honored even if not in
                Compliance mode. Enabled: Uses HMAC as the integrity
                test for the internal ROMs and code EEPROMs.
            :ivar update_test: Disabled: The self-test will not be
                automatically run but can be explicitly initiated by the
                host if desired. Enabled: Runs a complete self-test
                prior to any device update operation.
            :ivar public_auth: Disabled: No restrictions required to
                use, read or write Public keys or digest calculation for
                Verify, Manage_Cert and/or RSA_Enc. Enabled: All uses of
                any Public key for Verify, Manage_Cert and/or RSA_Enc
                must be authorized. None of Read_Perm, Write_Perm or
                Usage_Perm can be Always on element creation. Digest
                calculation for these commands must use a SHA context
                attached to an auth session. FCE cannot be used for
                digest creation.
            :ivar rw_sha_ctx: Disabled: The Read(SHA) and Write(SHA)
                commands used to load/store a SHA context are forbidden
                if the digest is attached to an authorization session.
                Enabled: Contexts may be read within the authorization
                session in which it was created. Write(SHA) will result
                in the new context being attached to the current
                authorization session.
            :ivar reserved: Reserved, must be 0b0000000
            """
            power_fail: Optional[BooleanEnabled] = field(
                default=None,
                metadata={
                    "name": "Power_Fail",
                    "type": "Element",
                    "required": True,
                }
            )
            chip_erase: Optional[BooleanEnabled] = field(
                default=None,
                metadata={
                    "name": "Chip_Erase",
                    "type": "Element",
                    "required": True,
                }
            )
            config_test: Optional[BooleanEnabled] = field(
                default=None,
                metadata={
                    "name": "Config_Test",
                    "type": "Element",
                    "required": True,
                }
            )
            always_auth: Optional[BooleanEnabled] = field(
                default=None,
                metadata={
                    "name": "Always_Auth",
                    "type": "Element",
                    "required": True,
                }
            )
            use_hmac: Optional[BooleanEnabled] = field(
                default=None,
                metadata={
                    "name": "Use_HMAC",
                    "type": "Element",
                    "required": True,
                }
            )
            update_test: Optional[BooleanEnabled] = field(
                default=None,
                metadata={
                    "name": "Update_Test",
                    "type": "Element",
                    "required": True,
                }
            )
            public_auth: Optional[BooleanEnabled] = field(
                default=None,
                metadata={
                    "name": "Public_Auth",
                    "type": "Element",
                    "required": True,
                }
            )
            rw_sha_ctx: Optional[BooleanEnabled] = field(
                default=None,
                metadata={
                    "name": "RW_SHA_CTX",
                    "type": "Element",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{8}",
                }
            )

        @dataclass
        class UpdateOptions:
            """
            :ivar downgrade_ok: False: All updates must have a higher
                revision number than that currently or previously
                loaded. True: A new update may have a lower revision
                than that currently or previously loaded.
            :ivar erase_ok: False: The currently loaded update may not
                be erased via a special erase-only update package. True:
                Special erase-only update packages are permitted.
            :ivar power_up_check: False: No check of the update is
                performed on a startup for fast operation. True: On
                power-up, any loaded update image is completely verified
                before command execution can start.
            :ivar auth_update: False: Device update commands can be run
                without authorization. True: Authorization required
                using the Update_Key
            :ivar update_key: If Auth_Update is True, then the key
                stored at the Update_Key handle must be used to initiate
                the Auth_Session in which the Dev_Update command is run.
                Valid values are 0x80F0 through 0x80FF.
            """
            downgrade_ok: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Downgrade_OK",
                    "type": "Element",
                    "required": True,
                }
            )
            erase_ok: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Erase_OK",
                    "type": "Element",
                    "required": True,
                }
            )
            power_up_check: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Power_Up_Check",
                    "type": "Element",
                    "required": True,
                }
            )
            auth_update: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Auth_Update",
                    "type": "Element",
                    "required": True,
                }
            )
            update_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Update_Key",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0x80[fF][0-9a-fA-F]",
                }
            )

        @dataclass
        class SoftReboot:
            """
            :ivar enable_reboot: False: The soft reboot function is
                disabled, attempts to execute this mode of the Power
                command will return an error. True: The soft reboot
                function is enabled.
            :ivar auth_reboot: False: The soft reboot function does not
                require an authorization session. True: Execution of the
                soft reboot mode of the Power command requires that the
                command be run in an authorization session initiated by
                Reboot_Key.
            :ivar reserved: Reserved, must be 0b00
            :ivar reboot_key: If Auth_Reboot is True, then the key
                stored at the special handle value must be used to
                initiate the authorization session. Valid handles are
                between 0x80F0 and 0x80FF.
            """
            enable_reboot: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Enable_Reboot",
                    "type": "Element",
                    "required": True,
                }
            )
            auth_reboot: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Auth_Reboot",
                    "type": "Element",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{2}",
                }
            )
            reboot_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reboot_Key",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0x80[fF][0-9a-fA-F]",
                }
            )

        @dataclass
        class MasterDelete:
            """
            :ivar enable: False: The master delete function is disabled,
                attempts to execute this mode of the Delete command will
                return an error. True: The Master Delete function is
                enabled.
            :ivar reserved: Reserved, m ust be 0b000
            :ivar auth_key: The key stored at this handle must be used
                to initiate an auth session prior to execution of the
                Master Delete operation. Valid handles are between
                0x80F0 and 0x80FF.
            """
            enable: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Enable",
                    "type": "Element",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{3}",
                }
            )
            auth_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Auth_Key",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0x80[fF][0-9a-fA-F]",
                }
            )

        @dataclass
        class OneTime:
            """
            :ivar enable_one_time: False: The one-time function is
                disabled. True: The one-time function is enabled.
            :ivar auth_req: False: Setting the one-time bit does not
                require an authorization session. True: Execution of the
                one-time mode of the Lock command requires that the
                command be run in an authorization session initiated by
                Auth_Key.
            :ivar reserved: Reserved, must be 0b00
            :ivar auth_key: If Auth_Req is True, then the key stored at
                this special handle must be used to initiate the
                authorization session. Valid handles are between 0x80F0
                and 0x80FF.
            """
            enable_one_time: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Enable_One_Time",
                    "type": "Element",
                    "required": True,
                }
            )
            auth_req: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Auth_Req",
                    "type": "Element",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{2}",
                }
            )
            auth_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Auth_Key",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0x80[fF][0-9a-fA-F]",
                }
            )

        @dataclass
        class SecureBoot:
            """
            :ivar mode: Mode can be one of the following: Disabled,
                Full_Asymmetric, Full_Stored, or Partial
            :ivar clr_brownout: False: Brownout will not affect the
                state of the Secure_Boot latch. True: Brownout will
                cause the Secure_Boot latch bit to be cleared.
            :ivar update_permit: False: Host code updates are
                restricted/prohibited. True: Host code updates are
                permitted and stored digests/memory maps can be changed
                in the field.
            :ivar secure_wake: False: A wake from sleep does not affect
                the secure boot or pre-boot latches. True: The
                secure_boot and pre-boot latches are cleared on every
                wake.
            :ivar por_timer: False: Secure boot timer is not enabled
                upon power-up or chip reset. True: Enables the secure
                boot timer immediately upon power-up or chip reset if
                Timer_Repeat is nonzero.
            :ivar allow_lock: False: Host can send a Secure_Boot command
                at any time. True: Secure_Boot command can be locked for
                a period of time.
            :ivar portion_count: For partial secure boot, the total
                number of portions in which the code should be split.
                Max legal value is 50. Min legal value is 1. The value
                of 0 is not legal.
            :ivar internal_sha: False: Code digest for the Boot phases
                can come from any source. True: Code digest for the Boot
                phases must come from the TA100 FCE or the SHA commands.
            :ivar pre_boot: False: The pre-boot phases are forbidden.
                True: Implement the pre-boot validation mechanism.
            :ivar timer_repeat: Disabled: disable the timed repeat of
                the secure boot operation. If nonzero, after this many
                minutes, the secure boot operation must be repeated.
                Must be a multiple of 2 up to a max of 510 minutes.
            :ivar boot_key: If Auth_Boot is True, then this byte
                contains the handle of the key which must be used to
                initiate the address and boot phases. Values from 0x8000
                to 0x80FF are permitted.
            :ivar retry: Number of failed attempts before secure boot
                attempts are locked out. If No_Limit, there are no
                limits on the number of retries. Otherwise can be a
                number between 1 and 15.
            :ivar latch_clear: False: The latch is not cleared until the
                retry count is exhausted. True: On any failure of any
                run-time boot phase during retry, the secure boot VCC
                latch will be cleared. This bit is ignored if Retry is
                No_Limit.
            :ivar auth_update: False: Execution of the update and
                complete phases do not occur within an authorization
                session. True: Execution of the update and complete
                phases must occur within an authorization session
                initiated using Update_Key.
            :ivar auth_boot: False: Execution of the address and boot
                phases do not occur within an authorization session.
                True: Execution of the address and boot phases must
                occur within an authorization session initiated using
                Boot_Key.
            :ivar auth_pre_boot: False: Execution of the pre-boot phase
                does not occur within an authorization session. True:
                Execution of the pre-boot phase must occur within an
                authorization session initiated using Boot_Key.
            :ivar update_key: If Auth_Update is True, then handle of the
                key which must be used to initiate the authorization
                session containing the update operation. Values from
                0x8000 to 0x80FF are permitted.
            :ivar reserved: Reserved, must be 0b0000000000000000
            """
            mode: Optional[SecureBootMode] = field(
                default=None,
                metadata={
                    "name": "Mode",
                    "type": "Element",
                    "required": True,
                }
            )
            clr_brownout: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Clr_Brownout",
                    "type": "Element",
                    "required": True,
                }
            )
            update_permit: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Update_Permit",
                    "type": "Element",
                    "required": True,
                }
            )
            secure_wake: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Secure_Wake",
                    "type": "Element",
                    "required": True,
                }
            )
            por_timer: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "POR_Timer",
                    "type": "Element",
                    "required": True,
                }
            )
            allow_lock: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Allow_Lock",
                    "type": "Element",
                    "required": True,
                }
            )
            portion_count: Optional[int] = field(
                default=None,
                metadata={
                    "name": "Portion_Count",
                    "type": "Element",
                    "required": True,
                    "min_inclusive": 0,
                    "max_inclusive": 63,
                }
            )
            internal_sha: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Internal_SHA",
                    "type": "Element",
                    "required": True,
                }
            )
            pre_boot: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Pre_Boot",
                    "type": "Element",
                    "required": True,
                }
            )
            timer_repeat: Optional[SecureBootValue] = field(
                default=None,
                metadata={
                    "name": "Timer_Repeat",
                    "type": "Element",
                    "required": True,
                }
            )
            boot_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Boot_Key",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0x80[0-9a-fA-F]{2}",
                }
            )
            retry: Optional[SecureBootValue] = field(
                default=None,
                metadata={
                    "name": "Retry",
                    "type": "Element",
                    "required": True,
                }
            )
            latch_clear: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Latch_Clear",
                    "type": "Element",
                    "required": True,
                }
            )
            auth_update: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Auth_Update",
                    "type": "Element",
                    "required": True,
                }
            )
            auth_boot: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Auth_Boot",
                    "type": "Element",
                    "required": True,
                }
            )
            auth_pre_boot: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Auth_Pre_Boot",
                    "type": "Element",
                    "required": True,
                }
            )
            update_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Update_Key",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0x80[0-9a-fA-F]{2}",
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{16}",
                }
            )

        @dataclass
        class GlobalExport:
            """
            :ivar forbid: False: Import and Export commands are
                available True: Both the Import and Export commands are
                forbidden to be run
            :ivar auth_req: False: Import and Export does not require
                authorization True: Import and Export commands must be
                run within an authorization session initiated by
                Auth_Key
            :ivar reserved: Reserved, must be 0b00
            :ivar auth_key: If Auth_Req is True, then the key stored at
                the special handle of Auth_Key must be used to initiate
                the auth session in which the Import and/or Export
                commands are run. Handle value must be between 0x80F0
                and 0x80FF.
            """
            forbid: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Forbid",
                    "type": "Element",
                    "required": True,
                }
            )
            auth_req: Optional[Boolean] = field(
                default=None,
                metadata={
                    "name": "Auth_Req",
                    "type": "Element",
                    "required": True,
                }
            )
            reserved: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Reserved",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0b[01]{2}",
                }
            )
            auth_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Auth_Key",
                    "type": "Element",
                    "required": True,
                    "pattern": r"0x80[fF][0-9a-fA-F]",
                }
            )

        @dataclass
        class Reserved42:
            value: str = field(
                default="",
                metadata={
                    "required": True,
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){6}",
                }
            )
            encoding: str = field(
                init=False,
                default="Hex",
                metadata={
                    "type": "Attribute",
                    "required": True,
                }
            )

    @dataclass
    class SharedDataMemory:
        """
        :ivar element:
        :ivar setup_lock: Set to True if the setup phase is completed
            once the specified elements are created and written.
        """
        element: List[ElementType] = field(
            default_factory=list,
            metadata={
                "name": "Element",
                "type": "Element",
                "max_occurs": 128,
            }
        )
        setup_lock: Optional[Boolean] = field(
            default=None,
            metadata={
                "name": "Setup_Lock",
                "type": "Element",
                "required": True,
            }
        )

    @dataclass
    class DataSources:
        """
        :ivar data_source: Data source objects for specifying static and
            dynamic data along with functions affecting it.
        :ivar writer: Writer types specify where named Data_Source items
            or Function results should be written to on a device.
        :ivar wrapped_key: A wrapped key item, which was used to encrypt
            one or more secret Data_Source items.
        """
        data_source: List[DataSourceItem] = field(
            default_factory=list,
            metadata={
                "name": "Data_Source",
                "type": "Element",
            }
        )
        writer: List[WriterItem] = field(
            default_factory=list,
            metadata={
                "name": "Writer",
                "type": "Element",
            }
        )
        wrapped_key: List[WrappedKeyItem] = field(
            default_factory=list,
            metadata={
                "name": "Wrapped_Key",
                "type": "Element",
            }
        )
