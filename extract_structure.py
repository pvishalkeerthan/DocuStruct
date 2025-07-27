import os
import json
import logging
import pdfplumber
import unicodedata
from collections import Counter, defaultdict

# --------------------------
# Logging Configuration
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --------------------------
# Color Mapping Function
# --------------------------
def rgb_to_name(rgb):
    if not rgb or not isinstance(rgb, (list, tuple)) or len(rgb) < 3:
        return "unknown"

    try:
        r, g, b = [int(255 * x) for x in rgb[:3]]
    except Exception:
        return "unknown"

    if r > 200 and g < 50 and b < 50:
        return "red"
    elif r < 50 and g > 200 and b < 50:
        return "green"
    elif r < 50 and g < 50 and b > 200:
        return "blue"
    elif r > 200 and g > 200 and b < 100:
        return "yellow"
    elif r > 200 and g > 200 and b > 200:
        return "white"
    elif r < 50 and g < 50 and b < 50:
        return "black"
    else:
        return f"rgb({r},{g},{b})"

# --------------------------
# CJK Character Detection
# --------------------------
def contains_cjk(text):
    return any("CJK" in unicodedata.name(char, "") for char in text)

# --------------------------
# PDF Heading Extraction
# --------------------------
def extract_headings(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_fonts = []
        headings = []
        title_text = ""

        # Step 1: Collect font sizes across the document
        for page_num, page in enumerate(pdf.pages, start=1):
            try:
                words = page.extract_words(extra_attrs=["size", "fontname", "top", "non_stroking_color"])
                for w in words:
                    size = round(float(w['size']), 1)
                    all_fonts.append(size)
            except Exception as e:
                logging.warning(f"Failed to parse page {page_num}: {e}")
                continue

        if not all_fonts:
            raise ValueError("No font sizes found in the PDF.")

        # Step 2: Determine heading levels by font size
        font_counter = Counter(all_fonts)
        common_sizes = sorted([fs for fs, _ in font_counter.most_common(5)], reverse=True)

        heading_levels = {}
        if len(common_sizes) >= 3:
            heading_levels = {
                common_sizes[0]: "H1",
                common_sizes[1]: "H2",
                common_sizes[2]: "H3"
            }
        elif len(common_sizes) == 2:
            heading_levels = {
                common_sizes[0]: "H1",
                common_sizes[1]: "H2"
            }
        elif len(common_sizes) == 1:
            heading_levels = {
                common_sizes[0]: "H1"
            }

        logging.info(f"Detected heading font sizes: {heading_levels}")

        # Step 3: Extract headings per page
        for page_num, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(extra_attrs=["size", "fontname", "top", "non_stroking_color"])
            lines = defaultdict(list)

            for w in words:
                try:
                    text = w['text'].strip()
                    if not text:
                        continue

                    size = round(float(w['size']), 1)
                    top = round(float(w['top']), 1)

                    # Extract color from non-stroking color field
                    non_stroke = w.get("non_stroking_color", (0, 0, 0))
                    if isinstance(non_stroke, (float, int)):
                        rgb = (non_stroke, non_stroke, non_stroke)
                    elif isinstance(non_stroke, (list, tuple)) and len(non_stroke) == 1:
                        rgb = (non_stroke[0], non_stroke[0], non_stroke[0])
                    elif isinstance(non_stroke, (list, tuple)) and len(non_stroke) >= 3:
                        rgb = tuple(non_stroke[:3])
                    else:
                        rgb = (0, 0, 0)

                    color = rgb_to_name(rgb)

                    if size in heading_levels:
                        lines[(top, size)].append((w['x0'], text, color))
                except Exception as e:
                    logging.warning(f"Skipping word due to error: {e}")
                    continue

            # Merge and format line items
            for (top, size), word_items in sorted(lines.items()):
                sorted_words = sorted(word_items)
                line_text_parts = [text for _, text, _ in sorted_words]

                # Avoid adding spaces for CJK languages
                use_space = not any(contains_cjk(part) for part in line_text_parts)
                line_text = (" " if use_space else "").join(line_text_parts).strip()
                first_color = sorted_words[0][2]

                headings.append({
                    "level": heading_levels[size],
                    "text": line_text,
                    "color": first_color,
                    "page": page_num
                })

            # Step 4: Extract document title from first page
            if page_num == 1:
                bold_words = [w for w in words if 'bold' in w.get('fontname', '').lower()]
                if bold_words:
                    bold_words.sort(key=lambda w: w['size'], reverse=True)
                    title_text = bold_words[0]['text'].strip()
                else:
                    text_lines = page.extract_text().split("\n") if page.extract_text() else []
                    top_lines = text_lines[:min(5, len(text_lines))]
                    title_text = max(top_lines, key=len) if top_lines else ""

        return {
            "title": title_text,
            "outline": headings
        }

# --------------------------
# Main Script Entry
# --------------------------
def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_dir, filename)
        logging.info(f"Processing {pdf_path}...")

        try:
            result = extract_headings(pdf_path)

            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logging.info(f"Saved to {output_path}")
        except Exception as e:
            logging.error(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    main()
