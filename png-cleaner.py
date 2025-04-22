import os
import sys
from PIL import Image


def is_black_pixel(pixel, tolerance=10):
    """Check if a pixel is black (0, 0, 0) within a given tolerance."""
    return all(abs(channel - 0) <= tolerance for channel in pixel[:3])  # Ignore alpha


def print_progress(current, total, bar_length=40):
    """Display a progress bar."""
    percent = current / total
    arrow = "=" * int(bar_length * percent)
    spaces = " " * (bar_length - len(arrow))
    print(f"\rProcessing: [{arrow}{spaces}] {percent*100:6.2f}%", end="", flush=True)


def remove_non_black_pixels(directory, tolerance=10):
    """Remove any pixel that is not black from PNGs."""
    files = [f for f in os.listdir(directory) if f.lower().endswith(".png")]
    total_files = len(files)

    for idx, filename in enumerate(files):
        path = os.path.join(directory, filename)
        img = Image.open(path).convert("RGBA")
        data = img.getdata()
        new_data = []

        for pixel in data:
            # Make non-black pixels fully transparent
            if is_black_pixel(pixel, tolerance):
                new_data.append(pixel)  # Keep black pixels
            else:
                new_data.append((0, 0, 0, 0))  # Fully transparent

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

    remove_non_black_pixels(folder_path)
