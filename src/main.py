from fastapi import FastAPI
import os
import uvicorn
from auth import router as auth_routes
from pix import router as pix_routes

app = FastAPI()

@app.get("/")
async def root():
	return {"message":"Welcome to Purrfect Pix!"}

app.include_router(auth_routes.router, prefix="/api/v1/auth")
app.include_router(pix_routes.router, prefix="/api/v1/pix")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
