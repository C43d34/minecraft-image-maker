import sys
from PIL import Image

# Braille Unicode blocks start at 0x2800
BRAILLE_BASE = 0x2800

# Braille dots: 1 4
#               2 5
#               3 6
#               7 8
BRAILLE_DOTS = [
    (0, 0),  # dot 1
    (0, 1),  # dot 2
    (0, 2),  # dot 3
    (1, 0),  # dot 4
    (1, 1),  # dot 5
    (1, 2),  # dot 6
    (0, 3),  # dot 7
    (1, 3)   # dot 8
]

def img_to_braille_ascii(file_path, width=38, height=14):
    """
    Convert an image to Braille ASCII art of specified width and height.
    Uses a single dot braille (0x2800) for empty space.
    The output is a single, continuous string (no newline characters).
    """
    # Braille cell: 2x4 pixels each
    cell_w, cell_h = 2, 4
    img_w, img_h = width * cell_w, height * cell_h

    # Open and convert image to grayscale
    img = Image.open(file_path)
    img = img.convert('L')
    img = img.resize((img_w, img_h), Image.BILINEAR)

    # Threshold for dot on/off
    threshold = 127

    braille_lines = []
    for y in range(0, img_h, cell_h):
        line = ""
        for x in range(0, img_w, cell_w):
            dots = 0
            for idx, (dx, dy) in enumerate(BRAILLE_DOTS):
                px = x + dx
                py = y + dy
                if px < img_w and py < img_h:
                    val = img.getpixel((px, py))
                    if val < threshold:
                        dots |= (1 << idx)
            braille_char = chr(BRAILLE_BASE + dots)
            line += braille_char
        braille_lines.append(line)
        
    # --- MODIFIED PART ---
    # The original code used "\n".join(braille_lines)
    # This change joins the lines with an empty string ("") instead of "\n"
    return "".join(braille_lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python braille_ascii_art.py <input_image> [output.txt]")
        sys.exit(1)
        
    input_img = sys.argv[1]
    art = img_to_braille_ascii(input_img)
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(art)
            print(f"Created single-line ascii file: {output_file}")
        except IOError as e:
             print(f"Error writing to file {output_file}: {e}", file=sys.stderr)
             sys.exit(1)
    else:
        # Note: If printed to console, it may wrap based on your terminal window size.
        print(art)