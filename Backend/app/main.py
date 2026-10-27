from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import users, products, transactions
from app.db.init_db import init_db

# 1. Create the FastAPI app instance
app = FastAPI(
    title="Schulkassen API",
    description="Backend-REST-API für das Schul-Kassensystem mit NFC-Anbindung und Guthabenverwaltung.",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"
)

# 2. Configure CORS middleware
# Required for the iPad app (Flutter/React Native) to access the API on the local network
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # MVP: Allow requests from all devices/IPs on the school Wi-Fi
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE etc.
    allow_headers=["*"],  # Includes our custom 'X-NFC-Key' header
)

# 3. Automatically initialize database tables on startup
@app.on_event("startup")
def on_startup():
    init_db()

# 4. Health check endpoint for server status
@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "system": "Schulkassen-API",
        "version": "1.0.0"
    }

# 5. Register API routers with the /api/v1 prefix
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)