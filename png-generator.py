import os
import sys
from PIL import Image, ImageDraw


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_unicode_char(unicode_str):
    """Convert a Unicode string like 'uni9FA0' to the actual character."""
    try:
        return chr(int(unicode_str[3:], 16))  # Extract the hex part and convert to char
    except ValueError:
        return None


def print_progress(current, total, bar_length=40):
    percent = current / total
    arrow = "=" * int(bar_length * percent)
    spaces = " " * (bar_length - len(arrow))
    print(
        f"\rGenerating PNGs: [{arrow}{spaces}] {percent*100:6.2f}%", end="", flush=True
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 png-generator.py <input_file_relative_path>")
        return

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print("File not found.")
        return

    # Use the input file's base name (without extension) as output dir
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = f"./png/{base_name}"

    # Set image size and DPI
    width = 1000
    height = 1000
    dpi = (300, 300)  # Set DPI for output PNG

    # Read all valid lines and count them
    with open(input_file, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    total = len(lines)
    # Determine the number of digits for the index and group folder names
    num_digits = len(str(total))
    group_digits = len(str((total - 1) // 100 * 100 + min(100, total)))

    # Process each line
    idx_valid = 0
    for idx, line in enumerate(lines):
        unicode_str = line.strip()
        if not unicode_str.startswith("uni") or len(unicode_str) < 6:
            print(f"Skipping invalid line: {line}")
            continue

        char = get_unicode_char(unicode_str)
        if char is None:
            print(f"Skipping invalid Unicode: {unicode_str}")
            continue

        unicode_hex = f"{ord(char):04x}"  # Get Unicode in lowercase hex
        index = f"{idx_valid + 1:0{num_digits}d}"  # Generate a dynamic n-digit index

        # Determine the subdirectory based on the current index
        group_start = (idx_valid // 100) * 100 + 1
        group_end = group_start + 99
        group_folder = f"{group_start:0{group_digits}d}-{group_end:0{group_digits}d}"
        group_path = os.path.join(output_dir, group_folder)
        ensure_dir(group_path)

        # Generate the filename
        filename = f"{index}【{char}】u+{unicode_hex}.png"
        out_path = os.path.join(group_path, filename)

        # Create transparent image
        img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Draw light gray dashed cross
        cross_color = (180, 180, 180, 128)
        dash_length = 40
        gap_length = 20

        # Horizontal dashed line
        y = height // 2
        for x in range(0, width, dash_length + gap_length):
            x_end = min(x + dash_length, width)
            draw.line([(x, y), (x_end, y)], fill=cross_color, width=2)

        # Vertical dashed line
        x = width // 2
        for y_ in range(0, height, dash_length + gap_length):
            y_end = min(y_ + dash_length, height)
            draw.line([(x, y_), (x, y_end)], fill=cross_color, width=2)

        # Save with DPI info
        img.save(out_path, dpi=dpi)

        idx_valid += 1
        print_progress(idx_valid, total)

    print("\nPNGs saved to /png.")


if __name__ == "__main__":
    main()
