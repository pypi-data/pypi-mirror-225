import typer
import subprocess
import chromadb
from rich import print
from chromadb.config import Settings
from rich import print
from pathlib import Path
import yaml
from oraculo.functions.audio import audio_to_text, download_yt
from oraculo.functions.data import get_collections
from typing_extensions import Annotated
import logging
import glob
from rich.progress import track

logging.basicConfig(level=logging.INFO)

APP_NAME = "oraculo"
app = typer.Typer()

app_dir = typer.get_app_dir(APP_NAME)
config_path: Path = Path(app_dir) / "config/config.yaml"

BASE_DIR = Path(__file__).resolve().parent.parent


@app.command()
def transcribe(
    embeddings: Annotated[
        bool,
        typer.Option(
            help="Create embeddings from the segments of the transcription and persists them to a vector database."
        ),
    ] = False,
    collection: Annotated[
        str,
        typer.Option(
            help="Name of the collection to persist the embeddings to. If the collection does not exist, a new collection will be created.",
        ),
    ] = None,
):
    path = typer.prompt("Path to audio file: ", default=None)
    language = typer.prompt("Input Audio Language: ", default="pt")
    model = typer.prompt("Model: ", default="base")
    output = typer.prompt("Output file: ", default=None)
    metadata = {}

    client = chromadb.Client(
        Settings(persist_directory=".chromadb", chroma_db_impl="duckdb+parquet")
    )

    if embeddings:
        # check if collections exist
        collections = get_collections(client)
        print("Collections found:")
        print(collections)

        if collection in collections:
            print(f"Collection {collection} found.")
            metadata = {"collection_name": collection}
        else:
            print(f"Collection not found. Creating new collection...")
            if collection is None:
                collection = typer.prompt("Enter collection name")
                metadata = {"collection_name": collection}
            else:
                metadata = {"collection_name": collection}

    print("Transcribing... :floppy_disk:")

    audio_to_text(
        path=path,
        language=language,
        model=model,
        output=output,
        embeddings=embeddings,
        metadata=metadata if embeddings else None,
        client=client if embeddings else None,
    )


@app.command()
def bulk_transcribe(
    embeddings: Annotated[
        bool,
        typer.Option(
            help="Create embeddings from the segments of the transcription and persists them to a vector database."
        ),
    ] = False,
    collection: Annotated[
        str,
        typer.Option(
            help="Name of the collection to persist the embeddings to. If the collection does not exist, a new collection will be created.",
        ),
    ] = None,
):
    path = typer.prompt("Path to folder: ", default=None)
    language = typer.prompt("Input Audio Language: ", default="pt")
    model = typer.prompt("Model: ", default="base")
    # default path is the same as input path
    output = typer.prompt("Output folder path: ", default=path)
    metadata = {}

    client = chromadb.Client(
        Settings(persist_directory=".chromadb", chroma_db_impl="duckdb+parquet")
    )

    if embeddings:
        # check if collections exist
        collections = get_collections(client)
        print("Collections found:")
        print(collections)

        if collection in collections:
            print(f"Collection {collection} found.")
            metadata = {"collection_name": collection}
        else:
            print(f"Collection not found. Creating new collection...")
            if collection is None:
                collection = typer.prompt("Enter collection name")
                metadata = {"collection_name": collection}
            else:
                metadata = {"collection_name": collection}
    # read all files in folder that have .mp3, .wav, .m4a, .flac extension
    files = (
        glob.glob(path + "/*.mp3")
        + glob.glob(path + "/*.wav")
        + glob.glob(path + "/*.m4a")
        + glob.glob(path + "/*.flac")
        + glob.glob(path + "/*.mp4")
    )

    for file in track(files, "Transcribing... :hourglass:"):
        filename = file.split("/")[-1].split(".")[0]
        output_file = f"{output}/{filename}.txt"

        print(f"Transcribing {filename}...")

        audio_to_text(
            path=file,
            language=language,
            model=model,
            output=output_file,
            embeddings=embeddings,
            metadata=metadata if embeddings else None,
            client=client if embeddings else None,
        )


@app.command()
def webapp():
    print("Starting webapp...")
    print(f"BASE_DIR: {BASE_DIR}")
    subprocess.run(
        [
            "streamlit",
            "run",
            f"{BASE_DIR}/oraculo/webapp/hello_world.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
        ]
    )



@app.command()
def transcribe_yt(
    embeddings: Annotated[
        bool,
        typer.Option(
            help="Create embeddings from the segments of the transcription and persists them to a vector database."
        ),
    ] = False,
    collection: Annotated[
        str,
        typer.Option(
            help="Name of the collection to persist the embeddings to. If the collection does not exist, a new collection will be created.",
        ),
    ] = None,
):
    path = typer.prompt("Folder path: ", default=None)
    url = typer.prompt("Youtube URL: ", default=None)
    language = typer.prompt("Input Audio Language: ", default="pt")
    model = typer.prompt("Model: ", default="base")
    metadata = {}

    client = chromadb.Client(
        Settings(persist_directory=".chromadb", chroma_db_impl="duckdb+parquet")
    )

    if embeddings:
        # check if collections exist
        collections = get_collections(client)
        print("Collections found:")
        print(collections)

        if collection in collections:
            print(f"Collection {collection} found.")
            metadata = {"collection_name": collection}
        else:
            print(f"Collection not found. Creating new collection...")
            if collection is None:
                collection = typer.prompt("Enter collection name")
                metadata = {"collection_name": collection}
            else:
                metadata = {"collection_name": collection}

    print("Transcribing... :floppy_disk:")

    # download video
    audio_path , audio_metadata = download_yt(url, path)

    if audio_path is None:
        print("Download failed.")
        return None

    metadata = {**metadata, **audio_metadata}

    audio_to_text(
        path=audio_path,
        language=language,
        model=model,
        output=path + "/" + audio_metadata["title"] + ".txt",
        embeddings=embeddings,
        metadata=metadata if embeddings else None,
        client=client if embeddings else None,
    )



@app.command()
def test():
    audio_to_text(
        path="/home/jrtedeschi/projetos/Gravando.m4a",
        language="pt",
        model="base",
        output="/home/jrtedeschi/projetos/Gravando.txt",
        embeddings=True,
        metadata={"collection_name": "teste"},
    )


if __name__ == "__main__":
    app()
