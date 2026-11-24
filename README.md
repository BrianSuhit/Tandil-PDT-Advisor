# 🏛️ EcoTandil - Auditor PDT

>  **MVP de auditoría y validación rapida de proyectos urbanísticos frente al Plan de Desarrollo Territorial (PDT) de Tandil.**

## Demostración

### Probar la aplicación
> 👉 **Demo interactiva:** [Probar la aplicación en vivo en Streamlit](https://ecotandil-auditor-tzpabtht7vqt2pj63ta4v9.streamlit.app/)

### Vista Previa

| Caso apto | Caso no apto |
| :--- | :--- |
| **Cabaña turística de madera** en zona urbana permitida, con pozo ciego reglamentario y compostaje. | **Cabaña turística con pileta climatizada** y riego constante en ladera serrana de Tandil. |
| <img src="https://github.com/user-attachments/assets/0da42809-1192-4b60-bc87-01bd8349f31b" width="420" alt="Proyecto apto en EcoTandil Auditor" /> | <img src="https://github.com/user-attachments/assets/62dca8aa-cf97-431d-9c60-7397fa52b63b" width="420" alt="Proyecto no apto en EcoTandil Auditor" /> |

## Contexto
Finalizado el generador de tips, quise cambiar el enfoque, si en el primero me pregunte como abordar la educacion en este la pregunta viro hacia la infraestructura y me pregunté: 
**si alguien quiere construir o emprender en Tandil, ¿qué es lo primero que tiene que consultar?**

Ahí di con el **Plan de Desarrollo Territorial (PDT)**, el marco normativo que regula los usos del suelo, densidades y zonas protegidas. Mi objetivo fue crear un asistente de doble frente: que le sirva tanto al sector privado (arquitectos, desarrolladores o vecinos que necesitan validar una idea rápido antes de presentarla) como al sector público (para agilizar la revisión preliminar de expedientes).

Como policía entiendo la importancia de la formalidad, la precisión legal y de presentar documentos con estructuras rigidas sin lugar a ambigüedades. Por eso, este fue probablemente el proyecto quirurgico: acá no había margen para el error, y aprendí que en sistemas RAG sobre marcos legales, el *chunking* (la fragmentación de los textos) merece todo el respeto del mundo, ya que un artículo mal cortado invalida cualquier respuesta jurídica.

## Decisiones de Diseño y Trade-offs
Para este prototipo me enfoqué en lograr rigor normativo sin perder velocidad, asumiendo los siguientes compromisos técnicos:

**RAG con ChromaDB (en vez de pasar todo el PDF en la ventana de contexto):**
-  *Pro:* Armé un script (index_pdfs.py) que corta la ordenanza respetando artículos y números romanos, y le mete metadatos (`archivo`, `seccion`) a ChromaDB. Así el modelo recupera artículos enteros con su contexto legal y no pedazos rotos.
-  *Contra:* Si el PDF cambia de formato o mete anexos con otra estructura, los regex pueden saltear secciones.

**Salida estrictamente estructurada en vez de texto libre:**
-  *Pro:* Garantiza un contrato de datos formal (dictamen de viabilidad, artículos específicos citados, justificación técnica y recomendaciones de adecuación). Esto permite renderizar en Streamlit tarjetas visuales limpias, ordenadas y sin respuestas vagas.
-  *Contra:* Mayor rigidez. Si una propuesta urbanística cae en una "zona gris" o un vacío normativo de la ordenanza, el modelo está obligado a encajar su análisis en campos predefinidos. Ademas puede generar errores si una persona ingresa un proyecto con requisitos contrapuestos o intenta validar mas de uno a la vez.

**Guardrails previos (en vez de mandar cualquier texto directo al RAG):**
-  *Pro:* Filtran entradas maliciosas, intentos de inyección de prompt o consultas totalmente ajenas al urbanismo y la construcción antes de tocar la base vectorial o gastar llamadas a la API de Gemini.
-  *Contra:* Añaden una pequeña latencia al inicio del flujo al tener que evaluar la consulta antes de proceder a la auditoría. El guardrails deberia refactorizarse por uno mas robusto o un framework especifico en produccion.

**Modelo rápido (Gemini 2.5 Flash-Lite) vs. Modelo de frontera:**
- *Pro:* Respuestas en pocos segundos y costo casi nulo para iterar y validar este MVP.
- *Contra:* Para auditar normativas complejas en producción real no alcanza con un modelo liviano: se necesitaría un modelo de frontera con alto nivel de razonamiento (*thinking*) o una arquitectura con un segundo evaluador (*LLM-as-a-judge*) para verificar que el dictamen no tenga fallas lógicas antes de mostrarlo.

## Mejoras a futuro
Cosas que no forman parte de este prototipo pero que son el paso siguiente para llevarlo a la práctica:

-  **Búsqueda avanzada por metadatos y filtros híbridos:** Explotar al máximo los metadatos ya indexados (`seccion`, `archivo`) para combinar búsqueda semántica vectorial con filtros exactos por zona o tipo de norma.
-  **Citas exactas con metadatos:** Aprovechar la metadata guardada en ChromaDB para devolverle al usuario el artículo exacto, la sección y la página oficial del PDF original.
-  **Modelo con mayor razonamiento (Thinking / Frontera):** Pasar a un modelo con razonamiento profundo o implementar un validador (*LLM-as-a-judge*) para auditar que el dictamen no tenga fallas lógicas frente a normativas cruzadas.
-  **Monitoreo y observabilidad:** Medir consumo de tokens, latencias de búsqueda vectorial, costos y trazabilidad de fallos en producción.

## Stack Tecnológico
- **Lenguaje:** Python 3.14
- **Frontend / UI:** Streamlit
- **LLM:** Google Gemini (`gemini-3.1-flash-lite` vía `google-genai`)
- **base de datos:** ChromaDB

## Estructura del Proyecto
```text
ecotandil-ecotips/
├── app.py            # Interfaz de usuario con Streamlit
├── auditor.py        # Servicio desacoplado para interactuar con Gemini
├── database.py       # Conexión, cliente y consultas vectoriales en ChromaDB
├── guardrails.py     # Validaciones de entrada (seguridad, off-topic y formato)
├── index_pdfs.py     # Script de ingesta, fragmentación e indexación del PDT en ChromaDB
└── models.py         # Modelos Pydantic (esquema estructurado de auditoría: PDTAudit)
```

## Quickstart (Cómo correrlo en local)

### 1. Clonar el repositorio

```bash
git clone https://github.com/BrianSuhit/EcoTandil-Auditor.git
cd EcoTandil-Auditor
```

### 2. Instalar dependencias con uv

```bash
uv sync
```

### 3. Configurar variables de entorno

Creá un archivo `.env` en la raíz del proyecto (o exportá la variable en tu terminal):

```env
GEMINI_API_KEY="tu_api_key_aqui"
```

### 4. Iniciar la aplicación

```bash
uv run streamlit run app.py
```
