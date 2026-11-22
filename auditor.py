from database import KnowledgeBase
from google import genai
from google.genai.errors import APIError
from models import PDTAudit

class PDTAuditorService:
    def __init__(self):
        self.client = genai.Client()
        self.kb = KnowledgeBase()

    def audit(self, project_description: str, num_contexts: int = 5) -> PDTAudit:
        context = self.kb.search_knowledge(query=project_description, n_results=num_contexts)
        
        augmented_prompt = (
            f"Contexto Normativo: {context}\n"
            f"Proyecto a Auditar: {project_description}"
        )

        try:
            interaction = self.client.interactions.create(
                model="gemini-3.1-flash-lite",
                system_instruction="Actúa como experto en el Plan de Desarrollo Territorial de Tandil y responde usando el contexto proporcionado.",
                input=augmented_prompt,
                response_format={
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": PDTAudit.model_json_schema(),
                },
            )
            return PDTAudit.model_validate_json(interaction.output_text)
        except APIError as error:
            print(f"Error de API en PDTAuditorService: {error}")
            raise
        except Exception as error:
            print(f"Error inesperado en PDTAuditorService: {error}")
            raise