from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, products, cart, wishlist, orders, reviews

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FocoPet API",
    description="E-Commerce API for FocoPet - Pet Food & Supplies Store",
    version="1.0.0",
)

# CORS - Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(orders.router)
app.include_router(reviews.router)


@app.get("/")
def root():
    return {
        "name": "FocoPet API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
