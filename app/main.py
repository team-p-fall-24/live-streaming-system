# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api.api_v1.api import api_router


app = FastAPI()

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Serve static files (e.g., the HTML player)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Mount the static directory to serve video chunks
app.mount("/media", StaticFiles(directory="app/media/chunks"), name="media")

# Redirect root to the player page with an example .m3u8 URL (you can adjust this later)
@app.get("/")
async def main():
    # Example URL; replace with your server's .m3u8 streaming URL
    return RedirectResponse(url=f"/static/player.html")
