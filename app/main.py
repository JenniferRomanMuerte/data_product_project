from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.data_products.product_dashboard import dashboard_router
from app.routers import user_router, domain_router, role_router, policy_router, data_product_router

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las orígenes. Puedes especificar dominios específicos.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP.
    allow_headers=["*"],  # Permite todos los headers.
)

app.include_router(dashboard_router.router, prefix="/api/v1", tags=["product_dashboard"])
app.include_router(user_router.router, prefix="/api/v1", tags=["users"])
app.include_router(domain_router.router, prefix="/api/v1", tags=["domains"])
app.include_router(role_router.router, prefix="/api/v1", tags=["roles"])
app.include_router(policy_router.router, prefix="/api/v1", tags=["policies"])
app.include_router(data_product_router.router, prefix="/api/v1", tags=["data_products"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
