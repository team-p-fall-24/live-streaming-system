# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api.api_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from os import makedirs


app = FastAPI()

# Configure CORS middleware to allow access from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing; be more specific in production
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Serve static files (e.g., the HTML player)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Mount the static directory to serve video chunks
makedirs("app/media/chunks", exist_ok=True)
app.mount("/media", StaticFiles(directory="app/media/chunks"), name="media")

# Redirect root to the player page with an example .m3u8 URL (you can adjust this later)
@app.get("/")
async def main():
    # Example URL; replace with your server's .m3u8 streaming URL
    return RedirectResponse(url=f"/static/player.html")
