Do some inspection and filtering on the macOS clipboard.

* `pb types [type]`: show available types on the clipboard, optionally showing conformance information to a specified type
* `pb paste [type]`: write raw clipboard data to stdout, optionally specifying the type of data to write
* `pb quicklook [type]`: show what's on the clipboard in Quick Look, optionally specifying the type of data to display
* `pb filter <type>`: replace the clipboard contents with the first thing that conforms with _type_
    * `pb image` and `pb text` are shorthand for filtering to `public.image` and `public.plain-text`, respectively

Also works via one- or two-character shorthand for the above commands; see `pb --help` for details.

Requires pyobjc, but that should install automatically if you use pip. Types are Apple [uniform type identifiers](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/understanding_utis/understand_utis_intro/understand_utis_intro.html). Useful ones you might want to filter for include:
* public.html
* public.plain-text
* public.image

Install:

```pip install -IU git+https://github.com/rolandcrosby/pasteboard --user```
