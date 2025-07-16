from fastapi import APIRouter
from typing import List
from models import DeleteEntitiesRequest, DeleteObservationsRequest, DeleteRelationsRequest, Relation
from knowledge_graph_manager import knowledge_graph_manager

router = APIRouter(prefix="/eliminar", tags=["eliminar"])

@router.post("/entities", operation_id="delete_entities")
async def delete_entities(request: DeleteEntitiesRequest):
    """Eliminar múltiples entidades y sus relaciones asociadas del grafo de conocimiento"""
    await knowledge_graph_manager.delete_entities(request.entityNames)
    return {"message": "Entities deleted successfully"}

@router.post("/observations", operation_id="delete_observations")
async def delete_observations(request: DeleteObservationsRequest):
    """Eliminar observaciones específicas de entidades en el grafo de conocimiento"""
    await knowledge_graph_manager.delete_observations(request.deletions)
    return {"message": "Observations deleted successfully"}

@router.post("/relations", operation_id="delete_relations")
async def delete_relations(request: DeleteRelationsRequest):
    """Eliminar múltiples relaciones del grafo de conocimiento"""
    relations = []
    for rel in request.relations:
        rel_dict = rel.dict()
        # Handle the 'from' field mapping
        if 'from' in rel_dict:
            rel_dict['from_entity'] = rel_dict.pop('from')
        relations.append(Relation(**rel_dict))
    
    await knowledge_graph_manager.delete_relations(relations)
    return {"message": "Relations deleted successfully"}
