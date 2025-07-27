#  Adobe India Hackathon - Round 1A
##  PDF Outline Extractor

This project extracts a structured outline from PDF files, identifying:
-  Title
-  Headings: H1, H2, H3 (with page number)

The solution works completely **offline**, runs on **CPU**, and outputs clean JSON.

##  How It Works

- Font sizes are analyzed across the document
- Top 3 sizes are mapped to H1, H2, H3 (heuristically)
- Largest font block is chosen as title

---

##  Input

Place one or more PDF files (up to 50 pages each) in the `input/` directory.

##  Output

You might get output json file in  `output/` directory with inputfile_name.json.
