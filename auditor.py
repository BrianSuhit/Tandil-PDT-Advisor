from database import KnowledgeBase
from google import genai
from models import AuditoriaPDT


class AuditorPDTService:
    def __init__(self, model_name: str = "gemini-3.1-flash-lite"):
        self.client = genai.Client()
        self.kb = KnowledgeBase()
        self.model_name = model_name

    def auditar(self, descripcion_proyecto: str, n_contextos: int = 5) -> AuditoriaPDT:
        contexto = self.kb.search_knowledge(query=descripcion_proyecto, n_results=n_contextos)
        
        augmented_prompt = (
            f"Contexto Normativo: {contexto}\n"
            f"Proyecto a Auditar: {descripcion_proyecto}"
        )

        interaction = self.client.interactions.create(
            model=self.model_name,
            system_instruction="Actúa como experto en el Plan de Desarrollo Territorial de Tandil y responde usando el contexto proporcionado.",
            input=augmented_prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": AuditoriaPDT.model_json_schema(),
            },
        )
        return AuditoriaPDT.model_validate_json(interaction.output_text)