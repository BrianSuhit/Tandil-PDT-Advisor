from pathlib import Path
import re
from pypdf import PdfReader
from database import KnowledgeBase

archivos_pdf = Path("data").glob("*.pdf")
chunks = []
metadatas = []

for archivo in archivos_pdf:
    reader = PdfReader(archivo)
    texto_completo = ""
    chunks_archivo = 0

    for pagina in reader.pages:
        texto = pagina.extract_text()
        if texto:
            texto_completo += texto + "\n"

    if re.search(r"[IVXLCDM]+\.\d+", texto_completo):
        partes = re.split(r"([IVXLCDM]+\.\d+)", texto_completo)
    elif "Artículo" in texto_completo:
        partes = re.split(r"(Artículo\s+\d+º?[^\n-]*)", texto_completo)
    else:
        print(f"{archivo.name}: {chunks_archivo} chunks")
        continue

    for i in range(1, len(partes), 2):
        titulo = partes[i]
        contenido = partes[i + 1].strip()
        chunks.append(f"{titulo}\n{contenido}")
        metadatas.append({"archivo": archivo.name, "seccion": titulo.strip()})
        chunks_archivo += 1

    print(f"{archivo.name}: {chunks_archivo} chunks")

print(f"Total de chunks creados: {len(chunks)}")

kb = KnowledgeBase()
for i in range(len(chunks)):
    kb.add_knowledge(
        knowledge_id=f"doc_{i}",
        knowledge_text=chunks[i],
        metadata=metadatas[i],
    )