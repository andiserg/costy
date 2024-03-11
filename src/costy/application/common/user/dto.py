from dataclasses import dataclass


@dataclass
class NewUserDTO:
    email: str
    password: str
