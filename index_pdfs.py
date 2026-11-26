from pathlib import Path
import re
from pypdf import PdfReader
from database import KnowledgeBase



def extract_pdf_text(pdf_file) -> str:
    """Abre un único PDF y junta el texto de todas sus páginas."""
    reader = PdfReader(pdf_file)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            full_text += page_text + "\n"
            
    return full_text


def split_into_sections(text: str) -> list[str]:
    """Detecta el tipo de norma y corta el texto en partes."""
    if re.search(r"[IVXLCDM]+\.\d+", text):
        return re.split(r"([IVXLCDM]+\.\d+)", text)
    elif "Artículo" in text:
        return re.split(r"(Artículo\s+\d+º?[^\n-]*)", text)
    return []


data_dir = Path("data")

pdf_files = list(data_dir.glob("*.pdf"))

if not pdf_files:
    print("⚠️ No se encontraron archivos PDF en la carpeta 'data'.")
    raise SystemExit(1)

chunks = []
metadata_entries = []

for pdf_file in pdf_files:
    
    full_text = extract_pdf_text(pdf_file)
    
    section_parts = split_into_sections(full_text)
    if not section_parts:
        continue
    
    titles = section_parts[1::2]
    contents = section_parts[2::2]

    for title, content in zip(titles, contents):
        cleaned_content = content.strip()
        if cleaned_content:
            chunks.append(f"{title}\n{cleaned_content}")
            metadata_entries.append(
                {"archivo": pdf_file.name, "seccion": title.strip()}
            )

knowledge_base = KnowledgeBase()
for chunk_index, chunk in enumerate(chunks):
    knowledge_base.add_knowledge(
        knowledge_id=f"doc_{chunk_index}",
        knowledge_text=chunk,
        metadata=metadata_entries[chunk_index],
    )