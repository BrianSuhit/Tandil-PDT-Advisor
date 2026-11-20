from auditor import AuditorPDTService
from guardrails import Guardrails


def main():
    pregunta = "Quiero instalar una industria pesada en el área serrana cerca de la Ruta 226."
    
    guardrails = Guardrails()
    es_valido, motivo_error = guardrails.validar_entrada_proyecto(pregunta)
    if not es_valido:
        print(f"🛑 RECHAZADO: {motivo_error}")
        return

    print("Procesando auditoría...", flush=True)
    auditor = AuditorPDTService()
    resultado = auditor.auditar(pregunta)
    print(f"Proyecto: {pregunta}")
    print(f"Compatible: {resultado.es_compatible}")
    print(f"Artículo: {resultado.articulo_infringido}")
    print(f"Motivo: {resultado.motivo}")
    print("Recomendaciones:")
    for recomendacion in resultado.recomendaciones:
        print(f" - {recomendacion}")


if __name__ == "__main__":
    main()