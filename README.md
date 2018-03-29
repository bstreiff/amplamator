# Amplamator

Amplamator is a font derived from the funky stylings of [Toejam & Earl](https://en.wikipedia.org/wiki/ToeJam_%26_Earl).

It comes in two variants:
* "Amplamator" is the main game font.
* "Amplamator Timer" uses the level digits for 0-9, with the addition of characters for plus, minus, colon, and period, suitable for a [LiveSplit](https://livesplit.github.io/) timer.

Characters are present for the 7-bit ASCII characters, which should be
sufficient for English text. Full Unicode is not supported.

It was a challenge to develop a good font-editing workflow. I was most
comfortable using [Inkscape](https://inkscape.org/en/), but with editing
all of the characters of the font simultaneously (so as to make it easier
to see everything at once). My eventual solution entailed a SVG file that
consisted of a collection of paths, with a character index as the `id`.
The `split_svg.py` script then builds a collection of SVG images that each
contain only a single path (but retain all other size and scale
information). [FontForge](https://fontforge.github.io/en-US/) is then used
to import each SVG as a glyph into a font.

## Additional thanks

Thanks to DrKelexo for making [this sprite sheet](https://www.spriters-resource.com/genesis_32x_scd/tjnearl/sheet/88574/)
which was quite helpful when building my initial SVG images.
