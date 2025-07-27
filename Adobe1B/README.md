# Adobe Hackathon Round 1B: Persona-Driven Document Intelligence

This solution extracts and ranks the most relevant sections from multiple PDFs based on a user persona and task.

---

## Features

- Uses sentence similarity to match PDF sections with persona goal
- Outputs:
  - Top sections with title + page + document
  - Refined subsection analysis
- Runs offline, on CPU only
- Model size < 100MB

---

## Inputs

- Place all PDFs in `/input`
- Create `persona/persona.json` like:

