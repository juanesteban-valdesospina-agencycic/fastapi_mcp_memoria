# Knowledge Graph MCP Server - FastAPI

Esta es una migración del servidor MCP (Model Context Protocol) de TypeScript a FastAPI de Python con soporte completo para MCP.

## Estructura del proyecto

```
mcp_memoria/
├── main.py                     # Aplicación FastAPI principal
├── models.py                   # Modelos Pydantic y dataclasses
├── knowledge_graph_manager.py  # Lógica de manejo del grafo
├── requirements.txt            # Dependencias Python
├── README.md                   # Esta documentación
├── memory.json                 # Archivo de persistencia (se crea automáticamente)
└── enrutadores/               # Routers organizados por funcionalidad
    ├── __init__.py
    ├── crear.py               # Endpoints de creación
    ├── obtener.py             # Endpoints de consulta
    └── eliminar.py            # Endpoints de eliminación
```

## Características

- **API REST completa** para gestión de grafos de conocimiento
- **Soporte MCP nativo** con FastAPI-MCP
- **Organización modular** con routers separados
- **Operation IDs** definidos para cada endpoint (requerido por MCP)
- **Gestión de entidades, relaciones y observaciones**
- **Búsqueda y filtrado de nodos**
- **Persistencia en archivo JSON**
- **Validación de datos con Pydantic**
- **Documentación automática con Swagger**

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor:
```bash
python main.py
```

O con uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints MCP disponibles

### Router: Crear (`/crear`)
- `POST /crear/entities` (operation_id: `create_entities`) - Crear nuevas entidades
- `POST /crear/relations` (operation_id: `create_relations`) - Crear nuevas relaciones
- `POST /crear/observations` (operation_id: `add_observations`) - Añadir observaciones

### Router: Obtener (`/obtener`)
- `GET /obtener/graph` (operation_id: `read_graph`) - Leer todo el grafo
- `POST /obtener/search` (operation_id: `search_nodes`) - Buscar nodos
- `POST /obtener/nodes` (operation_id: `open_nodes`) - Obtener nodos específicos

### Router: Eliminar (`/eliminar`)
- `POST /eliminar/entities` (operation_id: `delete_entities`) - Eliminar entidades
- `POST /eliminar/observations` (operation_id: `delete_observations`) - Eliminar observaciones
- `POST /eliminar/relations` (operation_id: `delete_relations`) - Eliminar relaciones

### Endpoints adicionales
- `GET /` - Información del servidor
- `GET /health` - Estado del servidor

## Configuración MCP

El servidor está configurado con FastAPI-MCP y expone las siguientes operaciones MCP:

```python
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
```

## Documentación

Una vez ejecutando el servidor, puedes acceder a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Variables de entorno

- `MEMORY_FILE_PATH`: Ruta del archivo de memoria (por defecto: memory.json en el directorio del script)

## Ejemplos de uso

### Crear entidades
```bash
curl -X POST "http://localhost:8000/create_entities" \
  -H "Content-Type: application/json" \
  -d '{
    "entities": [
      {
        "name": "Juan",
        "entityType": "persona",
        "observations": ["Es desarrollador", "Vive en Madrid"]
      }
    ]
  }'
```

### Crear relaciones
```bash
curl -X POST "http://localhost:8000/create_relations" \
  -H "Content-Type: application/json" \
  -d '{
    "relations": [
      {
        "from": "Juan",
        "to": "Madrid",
        "relationType": "vive_en"
      }
    ]
  }'
```

### Buscar nodos
```bash
curl -X POST "http://localhost:8000/search_nodes" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "desarrollador"
  }'
```

## Diferencias con la versión TypeScript

1. **Estructura de datos**: Se usan dataclasses de Python en lugar de interfaces de TypeScript
2. **Validación**: Pydantic para validación de entrada en lugar de esquemas JSON
3. **API**: REST endpoints en lugar de herramientas MCP
4. **Manejo de errores**: HTTPException de FastAPI
5. **Documentación**: Swagger UI automático
6. **Serializción**: Conversión manual a diccionarios para JSON

La funcionalidad core permanece idéntica, solo cambia la interfaz de comunicación.
