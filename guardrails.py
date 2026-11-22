class Guardrails:
    def validate_project_input(self, text: str) -> tuple[bool, str]:
        """Valida si la entrada es apta para una auditoría territorial."""
        clean_text = text.strip()

        if len(clean_text) < 15:
            return (
                False,
                (
                    "Entrada insuficiente. Describa brevemente el proyecto, uso de suelo"
                    " o ubicación a auditar."
                ),
            )

        keywords = [
            "construir", "instalar", "lote", "terreno", "zona", "área", "area",
            "serrana", "rural", "urbana", "galpon", "galpón", "industria",
            "vivienda", "comercio", "fraccionamiento", "subdivision",
            "subdivisión", "altura", "piso", "edificio", "ruta", "tandil",
        ]
        lowercase_text = clean_text.lower()
        has_context = any(keyword in lowercase_text for keyword in keywords)

        if not has_context:
            return (
                False,
                (
                    "Consulta fuera de tema (Off-topic). Este auditor solo evalúa"
                    " proyectos urbanísticos, territoriales y de uso de suelo en Tandil."
                ),
            )

        return True, ""