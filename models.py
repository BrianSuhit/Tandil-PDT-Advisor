from pydantic import BaseModel, Field


class PDTAudit(BaseModel):
    is_compatible: bool = Field(
        alias="es_compatible",
        description="True si cumple la normativa, False si la infringe o requiere excepción."
    )
    violated_article: str | None = Field(
        default=None,
        alias="articulo_infringido",
        description="Artículo o sección que se infringe (ej: 'I.1', 'II.7'), o None si es compatible.",
    )
    reason: str = Field(
        alias="motivo",
        description="Explicación concisa y técnica de por qué es compatible o qué restricción viola según el contexto."
    )
    recommendations: list[str] = Field(
        alias="recomendaciones",
        description="Pasos a seguir o ajustes para adecuarse a la norma."
    )