import json
import os
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from fastapi import HTTPException
from models import DeletionItem

# Define memory file path using environment variable with fallback
script_dir = Path(__file__).parent
default_memory_path = script_dir / "memory.json"

MEMORY_FILE_PATH = os.getenv("MEMORY_FILE_PATH")
if MEMORY_FILE_PATH:
    if not os.path.isabs(MEMORY_FILE_PATH):
        MEMORY_FILE_PATH = script_dir / MEMORY_FILE_PATH
else:
    MEMORY_FILE_PATH = default_memory_path

# Data models
@dataclass
class Entity:
    name: str
    entityType: str
    observations: List[str]

@dataclass
class Relation:
    from_entity: str  # 'from' is a Python keyword, so we use from_entity
    to: str
    relationType: str

@dataclass
class KnowledgeGraph:
    entities: List[Entity]
    relations: List[Relation]

# Knowledge Graph Manager
class KnowledgeGraphManager:
    def __init__(self):
        self.memory_file = Path(MEMORY_FILE_PATH)
    
    async def load_graph(self) -> KnowledgeGraph:
        try:
            if not self.memory_file.exists():
                return KnowledgeGraph(entities=[], relations=[])
            
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return KnowledgeGraph(entities=[], relations=[])
                
                lines = [line for line in content.split('\n') if line.strip()]
                entities = []
                relations = []
                
                for line in lines:
                    item = json.loads(line)
                    if item.get('type') == 'entity':
                        entity_data = {k: v for k, v in item.items() if k != 'type'}
                        entities.append(Entity(**entity_data))
                    elif item.get('type') == 'relation':
                        relation_data = {k: v for k, v in item.items() if k != 'type'}
                        # Handle the 'from' field mapping
                        if 'from' in relation_data:
                            relation_data['from_entity'] = relation_data.pop('from')
                        relations.append(Relation(**relation_data))
                
                return KnowledgeGraph(entities=entities, relations=relations)
        
        except FileNotFoundError:
            return KnowledgeGraph(entities=[], relations=[])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading graph: {str(e)}")
    
    async def save_graph(self, graph: KnowledgeGraph) -> None:
        try:
            lines = []
            
            for entity in graph.entities:
                entity_dict = asdict(entity)
                entity_dict['type'] = 'entity'
                lines.append(json.dumps(entity_dict))
            
            for relation in graph.relations:
                relation_dict = asdict(relation)
                # Map from_entity back to 'from' for storage
                if 'from_entity' in relation_dict:
                    relation_dict['from'] = relation_dict.pop('from_entity')
                relation_dict['type'] = 'relation'
                lines.append(json.dumps(relation_dict))
            
            # Ensure directory exists
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving graph: {str(e)}")
    
    async def create_entities(self, entities: List[Entity]) -> List[Entity]:
        graph = await self.load_graph()
        existing_names = {e.name for e in graph.entities}
        new_entities = [e for e in entities if e.name not in existing_names]
        graph.entities.extend(new_entities)
        await self.save_graph(graph)
        return new_entities
    
    async def create_relations(self, relations: List[Relation]) -> List[Relation]:
        graph = await self.load_graph()
        existing_relations = {
            (r.from_entity, r.to, r.relationType) for r in graph.relations
        }
        new_relations = [
            r for r in relations 
            if (r.from_entity, r.to, r.relationType) not in existing_relations
        ]
        graph.relations.extend(new_relations)
        await self.save_graph(graph)
        return new_relations
    

    async def add_observations(self, observations_to_add: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        graph = await self.load_graph()
        
        # Para una búsqueda más rápida, creamos un mapa de nombre de entidad a objeto entidad.
        entity_map = {e.name: e for e in graph.entities}
        
        results = []
        entities_modified = False

        for item in observations_to_add:
            entity_name = item.get("entityName")
            new_obs_list = item.get("observations", [])

            # --- Validación de la entrada ---
            if not entity_name:
                results.append({
                    "entityName": "DESCONOCIDO",
                    "status": "fallido",
                    "error": "El campo 'entityName' es obligatorio."
                })
                continue # Pasa al siguiente item

            if not isinstance(new_obs_list, list):
                results.append({
                    "entityName": entity_name,
                    "status": "fallido",
                    "error": f"El campo 'observations' debe ser una lista, pero se recibió un {type(new_obs_list).__name__}."
                })
                continue

            # --- Lógica de negocio ---
            entity = entity_map.get(entity_name)

            if not entity:
                results.append({
                    "entityName": entity_name,
                    "status": "fallido",
                    "error": f"La entidad '{entity_name}' no fue encontrada en el grafo."
                })
                continue
            
            # Filtra observaciones que ya existen para evitar duplicados.
            # Usar un set para la comprobación es más eficiente (O(1) en promedio).
            existing_obs_set = set(entity.observations)
            truly_new_observations = [obs for obs in new_obs_list if obs not in existing_obs_set]

            if truly_new_observations:
                entity.observations.extend(truly_new_observations)
                entities_modified = True
            
            results.append({
                "entityName": entity_name,
                "status": "exitoso",
                "addedObservations": truly_new_observations,
                "totalObservations": len(entity.observations)
            })

        # Guarda el grafo una sola vez al final, y solo si se hizo algún cambio.
        if entities_modified:
            await self.save_graph(graph)
            
        return results    
    
    
    async def delete_entities(self, entity_names: List[str]) -> None:
        graph = await self.load_graph()
        graph.entities = [e for e in graph.entities if e.name not in entity_names]
        graph.relations = [
            r for r in graph.relations 
            if r.from_entity not in entity_names and r.to not in entity_names
        ]
        await self.save_graph(graph)
    
    async def delete_observations(self, deletions: List[DeletionItem]) -> List[dict]:
        graph = await self.load_graph()
        entity_map = {e.name: e for e in graph.entities}
        results = []
        graph_modified = False

        for item in deletions:
            entity_name = item.entityName
            observations_to_delete = item.observations

            # --- Validación de la entrada ---
            if not entity_name:
                results.append({
                    "entityName": "DESCONOCIDO",
                    "status": "fallido",
                    "error": "El campo 'entityName' es obligatorio."
                })
                continue

            if not isinstance(observations_to_delete, list):
                results.append({
                    "entityName": entity_name,
                    "status": "fallido",
                    "error": f"El campo 'observations' debe ser una lista, pero se recibió un {type(observations_to_delete).__name__}."
                })
                continue

            # --- Lógica de negocio ---
            entity = entity_map.get(entity_name)

            if not entity:
                results.append({
                    "entityName": entity_name,
                    "status": "fallido",
                    "error": f"La entidad '{entity_name}' no fue encontrada en el grafo."
                })
                continue

            delete_set = set(observations_to_delete)
            initial_obs_count = len(entity.observations)
            entity.observations = [obs for obs in entity.observations if obs not in delete_set]
            final_obs_count = len(entity.observations)

            if initial_obs_count != final_obs_count:
                graph_modified = True

            results.append({
                "entityName": entity_name,
                "status": "exitoso",
                "observationsDeleted": initial_obs_count - final_obs_count,
                "observationsRemaining": final_obs_count
            })

        if graph_modified:
            await self.save_graph(graph)

        return results
    
    async def delete_relations(self, relations: List[Relation]) -> None:
        graph = await self.load_graph()
        relations_to_delete = {
            (r.from_entity, r.to, r.relationType) for r in relations
        }
        graph.relations = [
            r for r in graph.relations 
            if (r.from_entity, r.to, r.relationType) not in relations_to_delete
        ]
        await self.save_graph(graph)
    
    async def read_graph(self) -> KnowledgeGraph:
        return await self.load_graph()
    
    async def search_nodes(self, query: str) -> KnowledgeGraph:
        graph = await self.load_graph()
        query_lower = query.lower()
        
        # Filter entities
        filtered_entities = [
            e for e in graph.entities
            if (query_lower in e.name.lower() or 
                query_lower in e.entityType.lower() or
                any(query_lower in obs.lower() for obs in e.observations))
        ]
        
        # Create set of filtered entity names for quick lookup
        filtered_entity_names = {e.name for e in filtered_entities}
        
        # Filter relations to only include those between filtered entities
        filtered_relations = [
            r for r in graph.relations
            if r.from_entity in filtered_entity_names and r.to in filtered_entity_names
        ]
        
        return KnowledgeGraph(entities=filtered_entities, relations=filtered_relations)
    
    async def open_nodes(self, names: List[str]) -> KnowledgeGraph:
        graph = await self.load_graph()
        
        # Filter entities
        filtered_entities = [e for e in graph.entities if e.name in names]
        
        # Create set of filtered entity names for quick lookup
        filtered_entity_names = {e.name for e in filtered_entities}
        
        # Filter relations to only include those between filtered entities
        filtered_relations = [
            r for r in graph.relations
            if r.from_entity in filtered_entity_names and r.to in filtered_entity_names
        ]
        
        return KnowledgeGraph(entities=filtered_entities, relations=filtered_relations)

# Helper function to convert dataclass to dict for JSON serialization
def to_dict(obj):
    if isinstance(obj, (Entity, Relation, KnowledgeGraph)):
        result = asdict(obj)
        # Handle the from_entity -> from mapping for relations
        if isinstance(obj, Relation) and 'from_entity' in result:
            result['from'] = result.pop('from_entity')
        return result
    return obj

# Global instance
knowledge_graph_manager = KnowledgeGraphManager()