from enum import Enum

class Bool:
    def __new__(cls, value):
        if value in [ True, 'true', 'True', 'TRUE' ]:
            return True
        if value in [ False, 'false', 'False', 'FALSE' ]:
            return False
        raise ValueError(f'could not convert {value.__class__.__name__} to Bool: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to Bool: {value}')

class PositiveInt(int):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to PositiveInt: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to PositiveInt: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value <= 0:
            raise error

        return value

class NonNegativeInt(int):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to NonNegativeInt: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to NonNegativeInt: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value < 0:
            raise error

        return value

class NegativeInt(int):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to NegativeInt: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to NegativeInt: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value >= 0:
            raise error

        return value

class NonPositiveInt(int):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to NonPositiveInt: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to NonPositiveInt: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value > 0:
            raise error

        return value

class PositiveFloat(float):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to PositiveFloat: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to PositiveFloat: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value <= 0:
            raise error

        return value

class NonNegativeFloat(float):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to NonNegativeFloat: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to NonNegativeFloat: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value < 0:
            raise error

        return value

class NegativeFloat(float):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to NegativeFloat: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to NegativeFloat: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value >= 0:
            raise error

        return value

class NonPositiveFloat(float):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to NonPositiveFloat: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to NonPositiveFloat: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value > 0:
            raise error

        return value

class System(Enum):
    WINDOWS = 'WINDOWS'
    MACOS = 'MACOS'
    LINUX = 'LINUX'
    OTHER = 'OTHER'
