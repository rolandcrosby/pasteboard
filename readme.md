Do some inspection and filtering on the macOS clipboard.

* `pb.py types [type]`: show available types on the clipboard, optionally showing conformance information if you pass a type
* `pb.py paste [type]`: write data that conforms to _type_ to stdout (or just write the first thing found on the clipboard)
* `pb.py filter <type>`: replace the clipboard contents with the first thing that conforms with _type_

Requires pyobjc to be installed. Types are Apple [uniform type identifiers](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/understanding_utis/understand_utis_intro/understand_utis_intro.html). Useful ones you might want to filter for include:
* public.html
* public.plain-text
* public.image