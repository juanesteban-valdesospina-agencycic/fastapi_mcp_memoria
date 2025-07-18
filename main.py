# main.py
from fastapi import FastAPI, Depends
from enrutadores.obtener import router as obtener_router
from enrutadores.crear import router as crear_router
from enrutadores.eliminar import router as eliminar_router
from fastapi_mcp import FastApiMCP
import uvicorn

app = FastAPI(
    title="Knowledge Graph MCP Server",
    description="A FastAPI implementation of the Memory Context Protocol server",
    version="0.6.3"
)

# Include routers
app.include_router(obtener_router)
app.include_router(crear_router)
app.include_router(eliminar_router)

# Configure MCP with operation_ids from endpoints
mcp = FastApiMCP(
    app, 
    include_operations=[
        "read_graph",
        "search_nodes", 
        "open_nodes",
        "create_entities",
        "create_relations",
        "add_observations",
        "delete_entities",
        "delete_observations",
        "delete_relations"
    ]
)
mcp.mount()

@app.get("/", tags=["info"])
async def root():
    return {
        "message": "Knowledge Graph MCP Server",
        "version": "0.6.3",
        "status": "running"
    }

@app.get("/health", tags=["info"])
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
