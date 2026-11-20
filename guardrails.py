class Guardrails:
    def validar_entrada_proyecto(self, texto: str) -> tuple[bool, str]:
        """Valida si la entrada es apta para una auditoría territorial."""
        texto_limpio = texto.strip()

        if len(texto_limpio) < 15:
            return (
                False,
                "Entrada insuficiente. Describa brevemente el proyecto, uso de suelo"
                " o ubicación a auditar.",
            )

        palabras_clave = [
            "construir", "instalar", "lote", "terreno", "zona", "área", "area",
            "serrana", "rural", "urbana", "galpon", "galpón", "industria",
            "vivienda", "comercio", "fraccionamiento", "subdivision",
            "subdivisión", "altura", "piso", "edificio", "ruta", "tandil",
        ]
        texto_lower = texto_limpio.lower()
        tiene_contexto = any(palabra in texto_lower for palabra in palabras_clave)

        if not tiene_contexto:
            return (
                False,
                "Consulta fuera de tema (Off-topic). Este auditor solo evalúa"
                " proyectos urbanísticos, territoriales y de uso de suelo en Tandil.",
            )

        return True, ""
