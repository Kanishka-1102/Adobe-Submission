import fitz
import json
import os

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []

    for page_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = ""
                fonts = []
                for span in line["spans"]:
                    text += span["text"].strip() + " "
                    fonts.append(span["size"])
                text = text.strip()
                if text:
                    blocks.append({
                        "text": text,
                        "font_size": max(fonts),
                        "page": page_num
                    })

    unique_sizes = sorted(set([b["font_size"] for b in blocks]), reverse=True)
    heading_map = {size: f"H{i+1}" for i, size in enumerate(unique_sizes[:3])}

    outline = []
    title = ""
    for block in blocks:
        if block["font_size"] == unique_sizes[0] and not title:
            title = block["text"]
        level = heading_map.get(block["font_size"])
        if level:
            outline.append({
                "level": level,
                "text": block["text"],
                "page": block["page"]
            })

    return {
        "title": title,
        "outline": outline
    }

input_dir = "input"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        result = extract_outline(pdf_path)

        output_filename = os.path.splitext(filename)[0] + ".json"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"Processed {filename} → {output_filename}")