from fastapi import APIRouter
from typing import List
from models import SearchNodesRequest, OpenNodesRequest
from knowledge_graph_manager import knowledge_graph_manager, to_dict

router = APIRouter(prefix="/obtener", tags=["obtener"])

@router.get("/graph", operation_id="read_graph")
async def read_graph():
    """Leer todo el grafo de conocimiento"""
    result = await knowledge_graph_manager.read_graph()
    return to_dict(result)

@router.post("/search", operation_id="search_nodes")
async def search_nodes(request: SearchNodesRequest):
    """Buscar nodos en el grafo de conocimiento basado en una consulta"""
    result = await knowledge_graph_manager.search_nodes(request.query)
    return to_dict(result)

@router.post("/nodes", operation_id="open_nodes")
async def open_nodes(request: OpenNodesRequest):
    """Abrir nodos específicos en el grafo de conocimiento por sus nombres"""
    result = await knowledge_graph_manager.open_nodes(request.names)
    return to_dict(result)
