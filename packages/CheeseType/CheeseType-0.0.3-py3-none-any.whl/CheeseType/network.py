import re

from CheeseType.default import NonNegativeInt

class Port(NonNegativeInt):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to Port: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to Port: {value}')

        if isinstance(value, Port):
            return value

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if value > 65535:
            raise error

        return value

class IPv4(str):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to IPv4: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to IPv4: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', value):
            return value

        raise error

class IPv6(str):
    def __new__(cls, value):
        error = ValueError(f'could not convert {value.__class__.__name__} to IPv6: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to IPv6: {value}')

        try:
            value = super().__new__(cls, value)
        except:
            raise error

        if re.match(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$', value):
            return value

        raise error

class IP(str):
    def __new__(cls, value):
        try:
            value = IPv4(value)
        except:
            try:
                value = IPv6(value)
            except:
                raise ValueError(f'could not convert {value.__class__.__name__} to IP: \'{value}\'' if isinstance(value, str) else f'could not convert {value.__class__.__name__} to IP: {value}')
        return super().__new__(cls, value)
