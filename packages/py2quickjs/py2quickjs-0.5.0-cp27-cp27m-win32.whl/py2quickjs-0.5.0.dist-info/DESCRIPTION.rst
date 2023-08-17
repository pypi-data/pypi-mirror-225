Python wrapper around https://bellard.org/quickjs/ .

Translates types like `str`, `float`, `bool`, `list`, `dict` and combinations
thereof to and from Javascript.

QuickJS is currently thread-hostile, so this wrapper makes sure that all calls
to the same JS runtime comes from the same thead.


