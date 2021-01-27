# UnicodeFontLists
A list of fonts organized by unicode script

This is a set of lists (JSON files) that reflect all the fonts that support a given unicode script (https://en.wikipedia.org/wiki/Script_(Unicode)). 

The fonts are organized in directories, one for each script. The directory name is the ISO-15924 code of the script, Latin is '[Latn](Fonts/Latn/Latn_font_support_details.json)', Simplified Chinese is '[Hani](Fonts/Hani/Hani_font_support_details.json)', Yezidi is '[Yezi](Fonts/Yezi/Yezi_font_support_details.json)' etc ... 

These lists are generated from a large collection gathered over time and include most recent fonts (some are after 2020) and the most reecent unicode scripts (Unicode version 14). 

For each font, we give the font full name, the foundry name, the family name, the format (truetype etc), the (truetype / opentype) file name and the set of languages that the font claims to support.

The lists were generated automatically using the excellent fontconfig and Pango tools with a snall python script. The source was run on a Debian linux machine.
