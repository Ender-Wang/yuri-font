import os
import sys
from PIL import Image


def is_similar_color(c1, c2, tolerance=10):
    return all(abs(a - b) <= tolerance for a, b in zip(c1, c2))


def print_progress(current, total, bar_length=40):
    percent = current / total
    arrow = "=" * int(bar_length * percent)
    spaces = " " * (bar_length - len(arrow))
    print(f"\rProcessing: [{arrow}{spaces}] {percent*100:6.2f}%", end="", flush=True)


def remove_cross_color_fuzzy(
    directory, target_color=(180, 180, 180, 128), tolerance=10
):
    files = [f for f in os.listdir(directory) if f.lower().endswith(".png")]
    total_files = len(files)

    for idx, filename in enumerate(files):
        path = os.path.join(directory, filename)
        img = Image.open(path).convert("RGBA")
        data = img.getdata()
        new_data = []

        for item in data:
            if is_similar_color(item, target_color, tolerance):
                new_data.append((0, 0, 0, 0))  # Make pixel fully transparent
            else:
                new_data.append(item)

        img.putdata(new_data)
        new_filename = os.path.splitext(filename)[0] + ".png"
        img.save(os.path.join(directory, new_filename), "PNG")

        # Update progress bar
        print_progress(idx + 1, total_files)

    print("\nProcessing complete!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cross-remover.py /path/to/png_dir")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        sys.exit(1)

    remove_cross_color_fuzzy(folder_path)
