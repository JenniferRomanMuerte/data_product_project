
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import data_product_router



app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las orígenes. Puedes especificar dominios específicos.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP.
    allow_headers=["*"],  # Permite todos los headers.
)

app.include_router(data_product_router.router, prefix="/api/v1", tags=["data_products"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)