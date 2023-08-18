# FormatDefault

`str.format` but with default values

Ideal for building a CLI program with format-able filepath arguments

Many existing string formatting tools use regex to find sections like `%(param)s`, but regex can be fiddly and is not as flexible as `str.format` when it comes to validating [format spec][FORMAT-SPEC].

[FORMAT-SPEC]: https://docs.python.org/3/library/string.html#formatspec

Why reinvent the wheel when one can just pass an `f`string-looking argument and allow Python (and this mini library) to do the heavy lifting, no regex required!

## Example Usage

```py
from FormatDefault import format_default

s = "Hello {x:#02x} {y} {y:#02x} {z}"
params = {"x": 100, "y": "hi"}

print(format_default(s, params))
# Hello 0x64 hi NA NA
```

---

```py
import argparse
from FormatDefault import format_default

parser = argparse.ArgumentParser()
parser.add_argument("-o",
    default = "YouTube/{uploader}/{title} - {camera_type} - {id}.{ext}"
)
args = parser.parse_args()

video_data = {
    "id": "jNQXAC9IVRw", "title": "Me at the zoo",
    "uploader": "jawed", "ext": "webm",
}

print(format_default(args.o, video_data))
# YouTube/jawed/Me at the zoo - NA - jNQXAC9IVRw.webm
```

## How it works

`format_default(s, params, default = "NA")` tries `str.format` in a while-loop with a copy of `params`.

`format_default` catches `KeyError`s from missing parameters and the parameter name is added to `params` with the value `default`.

The values in `params` are wrapped in a wrapper class `_DefaultWrapper` before being passed to `str.format`. This wrapper class implements the `__format__(self, fmt)` dunder method to intercept the format specifiers (parts after the colon, eg `"#02x"` in `"{foo = :#02x}"`).

`_DefaultWrapper.__format__` catches `ValueError`s from invalid format specifiers for its wrapped value and returns `default` in this case.
