from pydantic import BaseModel


class FastORMModel(BaseModel):
    """BaseMixin for converting tuple to Pydantic Model."""

    @classmethod
    def from_list(cls, tpl):
        """Util function for converting DTO."""
        return cls(**dict(zip(cls.__fields__.keys(), tpl)))
