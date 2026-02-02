"""
Deep Research System - Backend API
FastAPI + LangGraph backend for multi-agent research orchestration.
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="Deep Research API",
    description="Multi-Agent Deep Research System with LangGraph & Ollama",
    version="0.1.0",
)

# Mount docs directory for static files
docs_path = Path(__file__).parent / "docs"
if docs_path.exists():
    app.mount("/docs-static", StaticFiles(directory=str(docs_path)), name="docs-static")


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    """Root endpoint redirects to API docs."""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Deep Research API</title>
            <meta http-equiv="refresh" content="0; url=/docs" />
        </head>
        <body>
            <p>Redirecting to <a href="/docs">API Documentation</a>...</p>
        </body>
    </html>
    """


@app.get("/docs", response_class=FileResponse)
async def custom_docs() -> FileResponse:
    """Serve custom API documentation."""
    docs_file = Path(__file__).parent / "docs" / "index.html"
    return FileResponse(str(docs_file))


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for Docker and monitoring."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "services": {
            "api": "online",
        },
    }


@app.get("/api/status")
async def api_status() -> dict:
    """Detailed API status with all connected services."""
    return {
        "status": "operational",
        "version": "0.1.0",
        "features": {
            "planner": "not_implemented",
            "source_finder": "not_implemented",
            "summarizer": "not_implemented",
            "reviewer": "not_implemented",
            "writer": "not_implemented",
        },
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
