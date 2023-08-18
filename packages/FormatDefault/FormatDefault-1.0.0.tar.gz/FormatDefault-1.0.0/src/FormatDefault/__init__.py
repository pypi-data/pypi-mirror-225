"""str.format but with default values"""

__version__ = "1.0.0"

class _DefaultWrapper:
    def __init__(self, value, default: str = "NA") -> None:
        self.value = value
        self.default = default

    def __format__(self, fmt: str) -> str:
        try:
            return f"{self.value:{fmt}}"
        except ValueError:
            # `fmt` is invalid for type of `self.value`,
            # eg '#02x' is valid for an int but not for a str
            return self.default

def format_default(s: str, params: dict[str], default: str = "NA") -> str:
    params = params.copy()
    while True:
        try:
            return s.format(**{
                k: _DefaultWrapper(v, default = default)
                for k, v in params.items()
            })
        except KeyError as e:
            missing_key: str = e.args[0]
            params[missing_key] = default
