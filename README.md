# Chinese Character PNG Batch Generator

This project generates PNG images for each Chinese character from a specified character set (such as GB2312), grouping every 100 images into separate folders. Then, it imports these images into Glyphs 3 for font design.
The script is designed to work with the [Glyphs 3](https://glyphsapp.com/) font design software.

## Requirements

- Python 3.13.3+
- [Pillow](https://python-pillow.org/) image library
- [Glyphs 3](<https://glyphsapp.com/>) 3.3+ for importing images

It is recommended to use [pipenv](https://pipenv.pypa.io/) for dependency management.

## Install Dependencies

```bash
pipenv install pillow && pipenv shell
```

## Usage

1. Put Character Set file in the font-unicode folder. The file should be a plain text file with the following format:

    ```txt
    uni4E00
    uni4E01
    uni4E03
    uni4E07
    uni4E08
    uni4E09
    uni4E0A
    uni4E0B
    uni4E0C
    uni4E0D
    uni4E0E
    uni4E10
    ...
    ```

2. Prepare the png files, run the script with the path to your character set file as an argument:

    ```bash
    python3 png-generator.py <relative/path/to/your_char_set.txt>
    ```

    Example:

    ```bash
    python3 png-generator.py font-unicode/GB2312.txt
    ```

3. Output images will be saved in `png/GB2312/0001-0100/0001_一_u+4e00.png` and so on:

   - Output Structure:
     - `png/` — root directory for all output images
       - `GB2312/` — named by the character set (e.g., `GB2312`)
         - `0001-0100/` — subfolder for each group of 100 characters
           - `0001_一_u+4e00.png` — file format: "index_character_unicode.png"

4. Script each image using Procreate or any other image processing tool, and export the scripted images into one folder, such as putting them in the `Downloads` dir.

5. Run the `png-cleaner.py` script to remove the cross and background from the scripted images:

    ```bash
    python3 png-cleaner.py <relative/path/to/your_scripted_images>
    ```

    Example:

    ```bash
    python3 png-cleaner.py ~/Downloads/
    ```

6. Import scripted images into Glyphs 3:

   - Open Glyphs 3 > Macro Panel (Opt + CMD + M)
   - Paste the code from `glyphs-import.py` into the Macro Panel
   - Change param `image_folder` to where your scripted PNGs are, then run the script

## Notes

- If your input file format is different, adjust the parsing logic in the script.
- Each image is 1000x1000 pixels. You can change these values in the script.
