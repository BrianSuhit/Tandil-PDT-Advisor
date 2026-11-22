import streamlit as st

from auditor import PDTAuditorService
from guardrails import Guardrails


def main():
    st.title("🌿 EcoTandil - Auditor")
    st.write(
        "Audita proyectos según el PDT de Tandil y su enfoque de desarrollo "
        "sostenible: proteger el ambiente y usar responsablemente los recursos naturales."
    )

    project_description = st.text_area(
        "Descripción del proyecto",
        placeholder="Describí el proyecto, su actividad y ubicación en Tandil.",
    )

    if st.button("Auditar proyecto"):
        if not project_description.strip():
            st.warning("Ingresá una descripción del proyecto para continuar.")
            return

        guardrails = Guardrails()
        is_valid, validation_error = guardrails.validate_project_input(
            project_description
        )
        if not is_valid:
            st.error(f"🛑 RECHAZADO: {validation_error}")
            return

        auditor = PDTAuditorService()
        with st.spinner("Procesando auditoría..."):
            result = auditor.audit(project_description)

        st.subheader("Resultado de auditoría")
        st.write(f"**Proyecto:** {project_description}")
        st.write(f"**Compatible:** {result.is_compatible}")
        st.write(f"**Artículo (si lo infringe):** {result.violated_article}")
        st.write(f"**Motivo:** {result.reason}")
        st.write("**Recomendaciones:**")
        for recommendation in result.recommendations:
            st.write(f"- {recommendation}")


main()