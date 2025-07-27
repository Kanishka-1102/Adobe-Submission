import os
import json
import fitz 
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    chunks = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if len(text) > 50:
            chunks.append({
                "doc": os.path.basename(pdf_path),
                "page": i + 1,
                "text": text
            })
    return chunks

def rank_sections(chunks, query_embedding, top_k=5):
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embeddings)[0]
    top_indices = scores.argsort(descending=True)[:top_k]

    top_sections = []
    for rank, idx in enumerate(top_indices, 1):
        c = chunks[idx]
        top_sections.append({
            "document": c["doc"],
            "page": c["page"],
            "section_title": c["text"][:60] + "...",
            "importance_rank": rank
        })
    return top_sections

def analyze_subsections(sections, chunks):
    refined = []
    for s in sections:
        for c in chunks:
            if c["doc"] == s["document"] and c["page"] == s["page"]:
                refined.append({
                    "document": c["doc"],
                    "page": c["page"],
                    "refined_text": c["text"]
                })
    return refined


input_dir = "input"
persona_file = "persona/persona.json"
output_file = "output/output.json"

with open(persona_file, "r") as f:
    persona_data = json.load(f)

persona_text = persona_data["persona"] + ". " + persona_data["job"]
query_embedding = model.encode(persona_text, convert_to_tensor=True)

all_chunks = []
for file in os.listdir(input_dir):
    if file.endswith(".pdf"):
        chunks = extract_text_chunks(os.path.join(input_dir, file))
        all_chunks.extend(chunks)

top_sections = rank_sections(all_chunks, query_embedding, top_k=5)
refined_sections = analyze_subsections(top_sections, all_chunks)

output = {
    "metadata": {
        "input_documents": [f for f in os.listdir(input_dir) if f.endswith(".pdf")],
        "persona": persona_data["persona"],
        "job": persona_data["job"],
        "timestamp": datetime.utcnow().isoformat()
    },
    "extracted_sections": top_sections,
    "subsection_analysis": refined_sections
}

with open(output_file, "w") as f:
    json.dump(output, f, indent=2)

print("Output saved to:", output_file)