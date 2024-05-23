from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main.routes import configure_routes
import uvicorn

app = FastAPI(
    title="Assessment Creator",
    version="1.0",
    description="Assessment Creator Back-end"
)

# Apply CORS middleware to the FastAPI app to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configure_routes(app)  # Add the configured routes to the FastAPI app

def create_app():
    return app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
