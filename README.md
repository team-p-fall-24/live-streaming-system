# Real-time live streaming multilingual subtitles system

## Prerequisite and installation

Built and tested with Python 3.12

### Required Libraries

#### FFmpeg library

- For Mac, please use `brew install ffmpeg`

- To deploy on Linux server, we need to follow this guideline https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#FFmpeg for install latest version instead of using apt install.

### Project configuration

```
# Create vitural env
python3 -m venv env

# Activate environment
source env/bin/activate

# Install requirements
pip3 install -r requirements.txt
```

Run server

```
python3 manage.py runserver
```

Before running the server, make sure to create and apply the database migrations (If needed):

```
python3 manage.py makemigrations
python3 manage.py migrate
```
