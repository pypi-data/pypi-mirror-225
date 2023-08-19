import whisper
import logging
import torch  # install steps: pytorch.org
import datetime
from oraculo.functions.data import create_embeddings
from pytube import YouTube


def audio_to_text(
    path: str,
    language: str = "pt",
    model: str = "base",
    output: str = None,
    embeddings: bool = False,
    metadata: dict = {},
    client=None,
):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logging.info(f"Using device: {device}")

    model = whisper.load_model("small")

    result = model.transcribe(
        path,
        word_timestamps=True,
        verbose=True,
        **{"task": "transcribe", "language": language, "fp16": False},
    )

    # if output is None get filename from path
    if output is None:
        output = path.split(".")[0] + ".txt"

    with open(output, "w") as f:
        for segment in result["segments"]:
            #
            start = str(datetime.timedelta(seconds=segment["start"]))[:-4]
            end = str(datetime.timedelta(seconds=segment["end"]))[:-4]
            f.write(f"[{start} --> {end}]\t {segment['text']}\n")

    if embeddings:
        metadata["title"] = output.split("/")[-1]
        logging.info("Creating embeddings for title: " + metadata["title"])
        create_embeddings(
            result["segments"],
            metadata=metadata,
            client=client,
        )


def download_yt(url: str, output: str):
    
    #check path
    if output is None:
        output = "./"

     
    yt = YouTube(url)
    logging.info(f"Downloading {yt.title}...")
    yt.streams.filter(only_audio=True).first().download(output_path=output)
    path = f"{output}/{yt.title}.mp4"
    logging.info(f"Downloaded {yt.title} to {path}")

    audio_info = (path, {
        "title": yt.title,
        "url": url,
        "author": yt.author,
        "length": yt.length,
        "rating": yt.rating,
        "views": yt.views,
        "keywords": yt.keywords,
        "description": yt.description,
    })

    return audio_info
