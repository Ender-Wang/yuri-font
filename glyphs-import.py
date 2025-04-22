import os
import re
from GlyphsApp import *
from Foundation import NSPoint

# Path to your PNG files
image_folder = os.path.expanduser("~/Downloads")
font = Glyphs.font  # current open font

# Match filenames like "0001【一】u+4e00.png"
pattern = re.compile(r".*?【.*?】u\+([0-9a-fA-F]{4,6})\.png")

for filename in os.listdir(image_folder):
    match = pattern.match(filename)
    if not match:
        continue

    unicode_hex = match.group(1).lower()
    image_path = os.path.join(image_folder, filename)

    # Try to find existing glyph
    glyph = font.glyphForUnicode_(unicode_hex.upper())
    if glyph is None:
        glyph_name = "uni" + unicode_hex.upper()
        print(f"Creating glyph: {glyph_name}")
        glyph = GSGlyph(glyph_name)
        glyph.unicode = unicode_hex.upper()
        font.glyphs.append(glyph)

    # Add image to first master layer
    master = font.masters[0]
    layer = glyph.layers[master.id]

    # ✅ Create and assign GSBackgroundImage properly
    bg_image = GSBackgroundImage.alloc().initWithPath_(image_path)
    layer.backgroundImage = bg_image
    # change transformation, scale to fit and adjust offset
    layer.backgroundImage.transform = (
        11 / 3,  # x scale factor
        0.0,  # x skew factor
        0.0,  # y skew factor
        11 / 3,  # y scale factor
        0.0,  # x position
        0.0,  # y position
    )
    bg_image.position = NSPoint(0, -200)

    print(f"✅ Imported {filename} into glyph '{glyph.name}'")
