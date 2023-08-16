Graphviz utility functions.

*Latest release 20230816*:
DOTNodeMixin: new dot_node_attrs_str for transcribing a node attributes list.

See also the [https://www.graphviz.org/documentation/](graphviz documentation)
and particularly the [https://graphviz.org/doc/info/lang.html](DOT language specification)
and the [https://www.graphviz.org/doc/info/command.html](`dot` command line tool).

## Class `DOTNodeMixin`

A mixin providing methods for things which can be drawn as
nodes in a DOT graph description.

*Method `DOTNodeMixin.__getattr__(self, attr: str)`*:
Recognise various `dot_node_*` attributes.

`dot_node_*color` is an attribute derives from `self.DOT_NODE_COLOR_*PALETTE`.

*Method `DOTNodeMixin.dot_node(self, label=None, **node_attrs) -> str`*:
A DOT syntax node definition for `self`.

*Method `DOTNodeMixin.dot_node_attrs(self) -> Mapping[str, str]`*:
The default DOT node attributes.

*Method `DOTNodeMixin.dot_node_attrs_str(attrs)`*:
An attributes mapping transcribed for DOT,
ready for insertion between `[]` in a node definition.

*Property `DOTNodeMixin.dot_node_id`*:
An id for this DOT node.

*Method `DOTNodeMixin.dot_node_label(self) -> str`*:
The default node label.
This implementation returns `str(serlf)`
and a common implementation might return `self.name` or similar.

*Property `DOTNodeMixin.dot_node_palette_key`*:
Default palette index is `self.fsm_state`,
overriding `DOTNodeMixin.dot_node_palette_key`.

## Function `gvdata(dot_s, **kw)`

Convenience wrapper for `gvprint` which returns the binary image data.

## Function `gvdataurl(dot_s, **kw)`

Convenience wrapper for `gvprint` which returns the binary image data
as a `data:` URL.

## Function `gvprint(dot_s, file=None, fmt=None, layout=None, dataurl_encoding=None, **dot_kw)`

Print the graph specified by `dot_s`, a graph in graphViz DOT syntax,
to `file` (default `sys.stdout`)
in format `fmt` using the engine specified by `layout` (default `'dot'`).

If `fmt` is unspecified it defaults to `'png'` unless `file`
is a terminal in which case it defaults to `'sixel'`.

In addition to being a file or file descriptor,
`file` may also take the following special values:
* `GVCAPTURE`: causes `gvprint` to return the image data as `bytes`
* `GVDATAURL`: causes `gvprint` to return the image data as a `data:` URL

For `GVDATAURL`, the parameter `dataurl_encoding` may be used
to override the default encoding, which is `'utf8'` for `fmt`
values `'dot'` and `'svg'`, otherwise `'base64'`.

This uses the graphviz utility `dot` to draw graphs.
If printing in SIXEL format the `img2sixel` utility is required,
see [https://saitoha.github.io/libsixel/](libsixel).

Example:

    data_url = gvprint('digraph FOO {A->B}', file=GVDATAURL, fmt='svg')

## Function `gvsvg(dot_s, **kw)`

Convenience wrapper for `gvprint` which returns an SVG string.

## Function `quote(s)`

Quote a string for use in DOT syntax.
This implementation passes identifiers and sequences of decimal numerals
through unchanged and double quotes other strings.

# Release Log



*Release 20230816*:
DOTNodeMixin: new dot_node_attrs_str for transcribing a node attributes list.

*Release 20221207*:
New gvsvg() convenience function to return SVG.

*Release 20221118*:
* quote: provide escape sequence for newline.
* DOTNodeMixin: provide .dot_node_id property, default `str(id(self))`.
* DOTNodeMixin.dot_node: omit [attrs] if they are empty.
* DOTNodeMixin: new .dot_node_palette_key property, new __getattr__ for .dot_node_*color attributes, new empty default DOT_NODE_COLOR_PALETTE and DOT_NODE_FILLCOLOR_PALETTE class attributes.
* DOTNodeMixin.dot_node: include the node label in the attributes.
* Add colours to DOTNodeMixin.dot_node_attrs and fix "fontcolor".

*Release 20220827.1*:
gvprint: new optional parameter dataurl_encoding to specify the data URL encoding.

*Release 20220827*:
* Remove dependency on cs.lex - now we need only the stdlib.
* New GVCAPTURE value for gvprint(file=) to return the binary image data as a bytes object; associated gvdata() convenience function.
* New GVDATAURL value for gvprint(file=) to return the binary image data as a data URL; associated gvdataurl() convenience function.

*Release 20220805.1*:
New DOTNodeMixin, a mixin for classes which can be rendered as a DOT node.

*Release 20220805*:
Initial PyPI release.
