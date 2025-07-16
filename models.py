from typing import List, Dict, Any
from pydantic import BaseModel

# Pydantic models for API
class EntityModel(BaseModel):
    name: str
    entityType: str
    observations: List[str]

class RelationModel(BaseModel):
    from_entity: str = None  # Will be mapped from 'from' field
    to: str
    relationType: str
    
    model_config = {'from_attributes': True, 'extra': 'allow'}

class CreateEntitiesRequest(BaseModel):
    entities: List[EntityModel]

class CreateRelationsRequest(BaseModel):
    relations: List[RelationModel]

class AddObservationsRequest(BaseModel):
    observations: List[Dict[str, Any]]  # entityName and contents

class DeleteEntitiesRequest(BaseModel):
    entityNames: List[str]

class DeleteObservationsRequest(BaseModel):
    deletions: List[Dict[str, Any]]  # entityName and observations

class DeleteRelationsRequest(BaseModel):
    relations: List[RelationModel]

class SearchNodesRequest(BaseModel):
    query: str

class OpenNodesRequest(BaseModel):
    names: List[str]

# Import dataclasses from knowledge_graph_manager for convenience
from knowledge_graph_manager import Entity, Relation, KnowledgeGraph
