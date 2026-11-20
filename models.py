from pydantic import BaseModel, Field


class AuditoriaPDT(BaseModel):
    es_compatible: bool = Field(
        description="True si cumple la normativa, False si la infringe o requiere excepción."
    )
    articulo_infringido: str | None = Field(
        default=None,
        description="Artículo o sección que se infringe (ej: 'I.1', 'II.7'), o None si es compatible.",
    )
    motivo: str = Field(
        description="Explicación concisa y técnica de por qué es compatible o qué restricción viola según el contexto."
    )
    recomendaciones: list[str] = Field(
        description="Pasos a seguir o ajustes para adecuarse a la norma."
    )
