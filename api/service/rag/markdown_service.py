import os
import logging
from openai import OpenAI
import re
import sys
import glob
from markitdown import MarkItDown
from rich.console import Console
from rich.progress import track
import tiktoken
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from api.helpers.logger_builder import LoggerBuilder
from api.service.common.count_token import count_tokens


class Markdown_Service:
    def __init__(self):
        # Settings
        self.output_dir = "outputs/rag"

        # Other services can be used by this service
        self.console = Console()
        self.logger = logging.getLogger(LoggerBuilder.name)


class CreateMarkdown_Service(Markdown_Service):
    def __init__(self):
        super().__init__()
        # Other services can be used by this service
        self.md = MarkItDown()

    @staticmethod
    def get_urls() -> list[dict]:
        URLs = [
            {
                "url": "https://support.google.com/youtube/answer/9527654?hl=es",
                "name": "Configurar la audiencia de un canal o un vídeo",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/11913617?sjid=11557296865847177507-EU",
                "name": "Consejos para subir vídeos de YouTube",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/11908409?sjid=11557296865847177507-EU",
                "name": "Consejos para optimizar vídeos",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/12340300?sjid=11557296865847177507-EU",
                "name": "Consejos sobre miniaturas y títulos",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/12948449?sjid=11557296865847177507-EU",
                "name": "Consejos para las descripciones de los vídeos",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/13616979?sjid=11557296865847177507-EU",
                "name": "Consejos para programar subidas",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/11913513?sjid=11557296865847177507-EU",
                "name": "Consejos sobre equipos de vídeo",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/12340105?sjid=11557296865847177507-EU",
                "name": "Consejos de grabación",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/12948118?sjid=11557296865847177507-EU",
                "name": "Consejos para grabar con un dispositivo móvil",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/11221953?sjid=11557296865847177507-EU",
                "name": "Consejos para editar vídeos",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/15575746?sjid=11557296865847177507-EU",
                "name": "Consejos para las retiradas por infracción de derechos de autor",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/15577610?sjid=11557296865847177507-EU",
                "name": "Consejos para encontrar música de uso autorizado",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/11912631?sjid=11557296865847177507-EU",
                "name": "Consejos sobre las publicaciones",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/12929858?sjid=11557296865847177507-EU",
                "name": "Consejos para conseguir más acuerdos de marca",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/11912533?sjid=11557296865847177507-EU",
                "name": "Consejos para ganar dinero en YouTube",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/13615784?sjid=11557296865847177507-EU",
                "name": "Consejos sobre usuarios nuevos y recurrentes",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/13616340?sjid=11557296865847177507-EU",
                "name": "Consejos para saber qué contenido crear",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/11912632?sjid=11557296865847177507-EU",
                "name": "Consejos sobre Estadísticas de YouTube",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/11914225?sjid=11557296865847177507-EU",
                "name": "Consejos de búsqueda y descubrimiento",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/15086271?sjid=11557296865847177507-EU",
                "name": "Consejos para evitar que disminuya el tiempo de visualización",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/12950272?sjid=11557296865847177507-EU",
                "name": "Consejos sobre el banner del canal y la imagen de perfil",
                "collection_name": "my_collection",
            },
            {
                "url": "https://support.google.com/youtube/answer/12356784?sjid=11557296865847177507-EU",
                "name": "Consejos sobre los estrenos de YouTube",
                "collection_name": "my_collection",
            },
        ]
        return URLs

    @staticmethod
    def create_valid_filename(name: str) -> str:
        valid_name = re.sub(r"[^\w\s-]", "", name.lower())
        valid_name = re.sub(r"[-\s]+", "_", valid_name)
        return valid_name

    def create_markdown_from_url(self, item: dict) -> None:
        url = item["url"]
        name = item["name"]
        collection_name = item["collection_name"]

        # Convertir la URL a contenido markdown
        result = self.md.convert(url)

        # Crear nombre de archivo válido
        filename = self.create_valid_filename(name) + ".md"
        filepath = os.path.join(self.output_dir, collection_name, filename)

        # Guardar contenido en el archivo
        if result:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {name}\n\n")
                # Convertir el resultado a string si no lo es ya
                f.write(result.markdown)
            self.console.print(
                f":white_check_mark: [bold cyan]Archivo guardado:[/bold cyan] {filepath}"
            )
        else:
            self.console.print(
                f":x: [bold red]No se pudo convertir la URL:[/bold red] {url}"
            )

    def create_markdown_from_urls(self) -> None:
        urls = self.get_urls()
        for url in urls:
            self.create_markdown_from_url(url)


class Encode_Markdown_Service(Markdown_Service):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            base_url=os.getenv("GITHUB_MODELS_URL"),
            api_key=os.getenv("GITHUB_TOKEN"),
        )

        self.qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"))

        self.embeddings_model = os.getenv("GITHUB_MODELS_MODEL_FOR_EMBEDDINGS")

        self.limit_files_to_search = int(os.getenv("LIMIT_FILES_TO_SEARCH"))

        self.vector_params_size = int(os.getenv("VECTOR_PARAMS_SIZE"))

    def check_connection_qdrant(self) -> None:
        try:
            self.qdrant_client.get_collections()
            self.console.print(
                ":rocket: [bold green]Conexión a Qdrant establecida correctamente.[/bold green]"
            )
        except Exception as e:
            self.console.print(
                f":x: [bold red]Error al conectar a Qdrant:[/bold red] {e}"
            )
            self.console.print(
                ":warning: [yellow]No se puede continuar sin una conexión a Qdrant. Asegúrate de que el servidor esté funcionando.[/yellow]"
            )
            sys.exit(1)  # Sale del programa con código de error 1

    def recreate_qdrant_collection(self, collection_name: str) -> None:
        """
        Elimina y vuelve a crear la colección en Qdrant.
        """
        self.console.print(
            f":mag: [cyan]Comprobando si la colección [bold]{collection_name}[/bold] ya existe...[/cyan]"
        )

        collections = self.qdrant_client.get_collections()
        collection_names = [collection.name for collection in collections.collections]
        self.console.print(
            f":file_folder: [blue]Las colecciones disponibles son:[/blue] {collection_names}"
        )

        if collection_name in collection_names:
            self.console.print(
                f":wastebasket: [yellow]La colección '[bold]{collection_name}[/bold]' ya existe. Eliminándola...[/yellow]"
            )
            self.qdrant_client.delete_collection(collection_name)
            self.console.print(
                f":white_check_mark: [green]Colección '[bold]{collection_name}[/bold]' eliminada de Qdrant.[/green]"
            )

        self.qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=self.vector_params_size, distance=Distance.COSINE),
        )
        self.console.print(
            f":sparkles: [bold green]Colección '[bold]{collection_name}[/bold]' creada en Qdrant.[/bold green]"
        )

    @staticmethod
    def read_markdown_file(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def split_into_chunks(
        text: str, max_tokens: int = 8000, encoding_name: str = "cl100k_base"
    ) -> list[str]:
        """
        Divide el texto en fragmentos más pequeños que no superen el límite de tokens.
        """
        # Inicializar el codificador
        encoding = tiktoken.get_encoding(encoding_name)

        # Dividir el texto en párrafos (o por alguna otra unidad lógica)
        paragraphs = re.split(r"\n\n+", text)

        chunks = []
        current_chunk = []
        current_token_count = 0

        for paragraph in paragraphs:
            # Contar tokens del párrafo actual
            paragraph_tokens = len(encoding.encode(paragraph))

            # Si un párrafo individual excede el límite, dividirlo en frases
            if paragraph_tokens > max_tokens:
                sentences = re.split(r"(?<=[.!?])\s+", paragraph)
                for sentence in sentences:
                    sentence_tokens = len(encoding.encode(sentence))
                    if current_token_count + sentence_tokens <= max_tokens:
                        current_chunk.append(sentence)
                        current_token_count += sentence_tokens
                    else:
                        # Guardar el chunk actual y comenzar uno nuevo
                        if current_chunk:  # Evitar guardar chunks vacíos
                            chunks.append("\n\n".join(current_chunk))
                        current_chunk = [sentence]
                        current_token_count = sentence_tokens
            else:
                # Si agregar este párrafo excede el límite, guardar el chunk actual y comenzar uno nuevo
                if current_token_count + paragraph_tokens > max_tokens:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = [paragraph]
                    current_token_count = paragraph_tokens
                else:
                    current_chunk.append(paragraph)
                    current_token_count += paragraph_tokens

        # No olvidar guardar el último chunk
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

    def process_markdown_files(
        self, markdown_files: list[str], collection_name: str
    ) -> int:
        # Primero cuenta el número total de fragmentos
        total_chunks = 0
        file_chunks = []

        for markdown_file_path in markdown_files:
            file_name = os.path.basename(markdown_file_path)
            title = os.path.splitext(file_name)[0]

            with open(markdown_file_path, "r", encoding="utf-8") as file:
                markdown_content = file.read()

            chunks = self.split_into_chunks(text=markdown_content, max_tokens=7000)
            total_chunks += len(chunks)
            file_chunks.append((markdown_file_path, file_name, title, chunks))

        self.console.print(
            f":scissors: [yellow]Total de fragmentos a procesar: [bold]{total_chunks}[/bold][/yellow]"
        )

        # Ahora procesa todos los fragmentos con una única barra de progreso
        id_counter = 0
        with self.console.status("[bold green]Procesando fragmentos...") as status:
            for markdown_file_path, file_name, title, chunks in file_chunks:
                self.console.print(
                    f"\n:page_facing_up: [bold blue]Procesando archivo:[/bold blue] {file_name}"
                )
                self.console.print(
                    f":scissors: [yellow]El archivo tiene [bold]{len(chunks)}[/bold] fragmentos.[/yellow]"
                )

                all_embeddings = []
                for i, chunk in enumerate(chunks):
                    status.update(
                        f"[bold green]Procesando fragmento {i+1}/{len(chunks)} de {file_name}[/bold green]"
                    )
                    try:
                        response = self.client.embeddings.create(
                            model=self.embeddings_model,
                            input=chunk,
                        )
                        all_embeddings.append((response, title, i))
                    except Exception as e:
                        self.console.print(
                            f":x: [red]Error al procesar el fragmento {i+1} del archivo {file_name}: {e}[/red]"
                        )

                for i, (embedding_response, file_title, chunk_index) in enumerate(
                    all_embeddings
                ):
                    vector = embedding_response.data[0].embedding
                    self.qdrant_client.upsert(
                        collection_name=collection_name,
                        points=[
                            {
                                "id": id_counter,
                                "vector": vector,
                                "payload": {
                                    "titulo": file_title,
                                    "parte": chunk_index,
                                    "archivo": file_name,
                                    "text": chunks[i],
                                },
                            }
                        ],
                    )
                    id_counter += 1

                self.console.print(
                    f":floppy_disk: [bold green]Embeddings del archivo {file_name} guardados en Qdrant.[/bold green]"
                )
        return id_counter

    @staticmethod
    def get_markdown_files(directory: str):
        return glob.glob(pathname=os.path.join(directory,"**", "*.md"), recursive=True)

    def encode_markdowns_using_chunks(
        self, markdown_dir_path: str, collection_name: str
    ) -> None:
        self.console.print(
            ":sparkles: [bold green]Iniciando el proceso de creación de embeddings...[/bold green]"
        )

        self.console.print(
            ":wastebasket: [yellow]Creando la colección anterior de Qdrant (si existe)...[/yellow]"
        )
        self.recreate_qdrant_collection(collection_name=collection_name)

        markdown_files = self.get_markdown_files(directory=markdown_dir_path)
        self.console.print(
            f":mag: [cyan]Se encontraron [bold]{len(markdown_files)}[/bold] archivos Markdown para procesar.[/cyan]"
        )

        id_counter = self.process_markdown_files(
            markdown_files=markdown_files, collection_name=collection_name
        )

        self.console.print(
            "\n:star2: [bold green]Todos los archivos han sido procesados y guardados en Qdrant.[/bold green]"
        )
        self.console.print(
            f":chart_with_upwards_trend: [bold blue]Total de embeddings almacenados: {id_counter}[/bold blue]"
        )

    def query_embeddings(self, query: str, collection_name: str) -> list:
        self.console.print(
            ":mag: [bold cyan]Generando embedding para la consulta...[/bold cyan]"
        )
        embedding_response = self.client.embeddings.create(
            model=self.embeddings_model, input=query
        )
        query_vector = embedding_response.data[0].embedding

        self.console.print(
            ":satellite: [bold cyan]Buscando documentos similares en Qdrant...[/bold cyan]"
        )
        search_results = self.qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=self.limit_files_to_search,
            with_payload=True,
        ).points

        self.console.print(
            f":page_facing_up: [bold green]{len(search_results)} resultados encontrados.[/bold green]"
        )
        return search_results

    def generate_response_with_embeddings(
        self, query: str, search_results: list
    ) -> str:
        context = ""
        for i, result in enumerate(search_results):
            title = result.payload.get("titulo", "Sin título")
            part = result.payload.get("parte", 0)
            file_name = result.payload.get("archivo", "Sin archivo")
            context += f"\n--- Información relevante #{i+1} (de {title}, archivo {file_name}, parte {part}) ---\n"
            chunk_text = result.payload.get("text", "No hay texto disponible")
            context += chunk_text + "\n"

        prompt = f"""Responde a la siguiente consulta utilizando la información proporcionada.
                    Si la información proporcionada no es suficiente para responder, puedes indicarlo.

                    Contexto:
                    {context}

                    Consulta: {query}

                    Respuesta:"""

        system_prompt = (
            "Eres un asistente experto en creación de contenido para YouTube."
            "Tu tarea es responder a las preguntas de los usuarios utilizando la información proporcionada en el contexto."
            "Si la información no es suficiente, indícalo y sugiere buscar más información."
            "Siempre añade la referencia a la fuente de información utilizada para responder, en fragmento si es posible, y al final de la respuesta, utilizando el formato: "
            "Referencia: [nombre del archivo] [parte del archivo]"
        )

        self.console.print(
            ":robot: [bold cyan]Generando respuesta con el modelo...[/bold cyan]"
        )

        print(f"count_tokens(prompt): {count_tokens(prompt)}")

        response = self.client.chat.completions.create(
            model=os.getenv("GITHUB_MODELS_MODEL_FOR_GENERATION"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content

    def user_query_using_embeddings(self, query: str, collection_name: str) -> str:
        search_results = self.query_embeddings(
            query=query, collection_name=collection_name
        )
        response = self.generate_response_with_embeddings(
            query=query, search_results=search_results
        )
        return response
