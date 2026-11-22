from pathlib import Path
import re
from pypdf import PdfReader
from database import KnowledgeBase

pdf_files = list(Path("data").glob("*.pdf"))
if not pdf_files:
    print("⚠️ No se encontraron archivos PDF en la carpeta 'data'.")
    raise SystemExit(1)

chunks = []
metadata_entries = []

for pdf_file in pdf_files:
    reader = PdfReader(pdf_file)
    full_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"

    if re.search(r"[IVXLCDM]+\.\d+", full_text):
        section_parts = re.split(r"([IVXLCDM]+\.\d+)", full_text)
    elif "Artículo" in full_text:
        section_parts = re.split(r"(Artículo\s+\d+º?[^\n-]*)", full_text)
    else:
        continue

    for part_index in range(1, len(section_parts), 2):
        section_title = section_parts[part_index]
        section_content = section_parts[part_index + 1].strip()
        if section_content:
            chunks.append(f"{section_title}\n{section_content}")
            metadata_entries.append(
                {"archivo": pdf_file.name, "seccion": section_title.strip()}
            )

knowledge_base = KnowledgeBase()
for chunk_index, chunk in enumerate(chunks):
    knowledge_base.add_knowledge(
        knowledge_id=f"doc_{chunk_index}",
        knowledge_text=chunk,
        metadata=metadata_entries[chunk_index],
    )