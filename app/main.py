from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.utils import get_cat_fact, get_current_timestamp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Profile API application")
    yield
    # Shutdown
    logger.info("Shutting down Profile API application")

app = FastAPI(
    title="Profile API",
    description="Dynamic profile endpoint with cat facts",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Profile API",
        "version": "1.0.0",
        "endpoints": {
            "profile": "/me",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": get_current_timestamp()}

@app.get("/me", response_model=dict)
async def get_profile():
    """
    Get profile information with dynamic cat fact
    """
    try:
        # Fetch cat fact asynchronously
        fact = await get_cat_fact()
        
        # Prepare response
        response = {
            "status": "success",
            "user": {
                "email": settings.user_email,
                "name": settings.user_name,
                "stack": settings.user_stack
            },
            "timestamp": get_current_timestamp(),
            "fact": fact
        }
        
        logger.info("Successfully processed profile request")
        return JSONResponse(content=response, media_type="application/json")
    
    except Exception as e:
        logger.error(f"Error in profile endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )