from fastapi import APIRouter, HTTPException
from typing import List
from models import (
    CreateEntitiesRequest, CreateRelationsRequest, AddObservationsRequest,
    EntityModel, RelationModel, Entity, Relation
)
from knowledge_graph_manager import knowledge_graph_manager, to_dict

router = APIRouter(prefix="/crear", tags=["crear"])

@router.post("/entities", operation_id="create_entities")
async def create_entities(request: CreateEntitiesRequest):
    """Crear múltiples entidades nuevas en el grafo de conocimiento"""
    entities = [Entity(**entity.dict()) for entity in request.entities]
    result = await knowledge_graph_manager.create_entities(entities)
    return [to_dict(entity) for entity in result]

@router.post("/relations", operation_id="create_relations")
async def create_relations(request: CreateRelationsRequest):
    """Crear múltiples relaciones nuevas entre entidades en el grafo de conocimiento"""
    relations = []
    for rel in request.relations:
        rel_dict = rel.dict()
        # Handle the 'from' field mapping
        if 'from' in rel_dict:
            rel_dict['from_entity'] = rel_dict.pop('from')
        relations.append(Relation(**rel_dict))
    
    result = await knowledge_graph_manager.create_relations(relations)
    return [to_dict(relation) for relation in result]

@router.post("/observations", operation_id="add_observations")
async def add_observations(request: AddObservationsRequest):
    """Agregar nuevas observaciones a entidades existentes en el grafo de conocimiento"""
    result = await knowledge_graph_manager.add_observations(request.observations)
    return result
