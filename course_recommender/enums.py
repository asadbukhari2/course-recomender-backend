from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class EmailTypes(BaseEnum):
    NO_REPLY = "NO REPLY"
    SUPPORT = "Support"
    ADMIN = "Admin"
    CONTACT = "Contact"
    ACCOUNT = "Account"
