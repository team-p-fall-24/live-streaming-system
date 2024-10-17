# Real-time live streaming multilingual subtitles system

## Prerequisite and installation

Built and tested with Python 3.12 and FFmpeg version 7.0.2_1

### Required Libraries

#### FFmpeg library

- For Mac, please use `brew install ffmpeg`

- To deploy on Linux server, we need to follow this guideline https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#FFmpeg for install latest version instead of using apt install.

#### Librosa library

- For MacOS users, please use
```
git clone https://github.com/librosa/librosa.git
python -m pip install -e librosa
```

- Otherwises, install librosa with `pip install librosa`

### Project Configuration

```
# Create vitural env
python3 -m venv env

# Activate environment
source env/bin/activate

# Install requirements
pip3 install -r requirements.txt

# If there exists additional install library when developing, please update requirements.txt
pip3 freeze > requirements.txt
```

Run server

```
uvicorn app.main:app --reload
```

Swagger UI for API docs can be checked via http://127.0.0.1:8000/docs

## Project Structure Overview

```
live-streaming-system/
├── app/
│   ├── __init__.py                # Initialization file for the app module
│   ├── main.py                    # Entry point for the FastAPI application
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuration settings for the project
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api_v1/
│   │   │   ├── __init__.py
│   │   │   ├── api.py             # API routing for version 1
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── live_stream.py # Endpoints related to live streaming
│   │   │   │   ├── audio_processing.py # Endpoints related to audio processing
│   │   │   │   ├── subtitle_sync.py    # Endpoints related to subtitle synchronization
│   ├── models/
│   │   ├── __init__.py            # Placeholder for database models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── live_stream.py         # Pydantic schemas for live streaming
│   │   ├── audio_processing.py    # Pydantic schemas for audio processing
│   │   ├── subtitle_sync.py       # Pydantic schemas for subtitle synchronization
│   ├── services/
│   │   ├── __init__.py
│   │   ├── live_stream_service.py # Business logic for live streaming
│   │   ├── audio_service.py       # Business logic for audio processing
│   │   ├── subtitle_service.py    # Business logic for subtitle synchronization
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── background_tasks.py    # Background task management
│   └── db/
│       ├── __init__.py
│       ├── base.py                # Base model class for ORM
│       └── session.py             # Database session management
├── .env                           # Environment variables
├── .gitignore                     # Git ignore file
├── requirements.txt               # Project dependencies
├── .github                        # GitHub configuration for CI/CD and GitHub PR/Issues Template
└── README.md                      # Project documentation
```