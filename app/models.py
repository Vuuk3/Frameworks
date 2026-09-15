from dataclasses import dataclass, asdict


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str

    def to_dict(self):
        return asdict(self)


@dataclass
class Mentor:
    id: int
    name: str
    email: str
    specializations: list[int]

    def to_dict(self):
        return asdict(self)


@dataclass
class Specialization:
    id: int
    name: str
    description: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class Application:
    id: int
    user_id: int
    specialization_id: int
    status: str = "open"
    mentor_id: int | None = None

    def to_dict(self):
        return asdict(self)