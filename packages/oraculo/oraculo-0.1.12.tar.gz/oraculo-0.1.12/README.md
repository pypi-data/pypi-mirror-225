# Project: Oráculo

Oráculo is a versatile CLI and WebApp application developed for transcription of audios and semantic search. It leverages Sentence Transformers and embeddings to create a compact search engine that aids in retrieving and organizing important information from a collection of documents.

This application is particularly useful for professionals dealing with substantial amounts of audio data and requiring an efficient system to transcribe and conduct semantic search operations on the data.

## Features:

- Audio Transcription: Oráculo can transcribe audio files. You can transcribe a single file or bulk transcribe a folder.
- Semantic Search: A web app to perform semantic searches on the transcribed audio data.

## Requirements:

- Python 3.10
- FFmpeg
- Git
- Docker (in future)

## Installation:

You can install Oráculo with pip:

```bash
pip install oraculo
```

## Usage:

To start the Semantic Search Application, use the following command:

```bash
oraculo webapp
```

To initiate a transcription for a single file:

```bash
oraculo transcribe
```

To initiate bulk transcription for a folder:

```bash 
oraculo bulk-transcribe
```

## About

- Version: 0.1.11
- Author: Joao Tedeschi
- Contact: joaorafaelbt@gmail.com

The development of Oráculo is aimed at evolving data analytics and information retrieval capabilities for businesses and individual users. Please feel free to reach out with any feedback or suggestions to improve Oráculo further.
