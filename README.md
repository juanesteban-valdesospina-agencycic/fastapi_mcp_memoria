# Servidor MCP de Grafo de Conocimiento

Una implementación basada en FastAPI del servidor Model Context Protocol (MCP) para gestión de grafos de conocimiento.

## Descripción

Este es un servidor MCP completo que proporciona capacidades de gestión de grafos de conocimiento a través de una interfaz API REST. Soporta todas las operaciones estándar de MCP para crear, leer, actualizar y eliminar entidades, relaciones y observaciones en un grafo de conocimiento.

## Características

- **Soporte Completo del Protocolo MCP**: Implementación completa de operaciones MCP
- **API REST**: Endpoints REST limpios basados en FastAPI
- **Gestión de Grafos de Conocimiento**: Entidades, relaciones y observaciones
- **Capacidades de Búsqueda**: Encontrar nodos por palabras clave y categorías
- **Persistencia de Datos**: Almacenamiento basado en archivos JSON
- **Validación de Entrada**: Modelos Pydantic para validación de request/response
- **Documentación Automática**: Integración con Swagger UI y ReDoc
- **Arquitectura Modular**: Organizado con routers de FastAPI

## Inicio Rápido

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/juanesteban-valdesospina-agencycic/fastapi_mcp_memoria.git
cd fastapi_mcp_memoria

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python main.py
```

El servidor estará disponible en `http://localhost:8000`

### Configuración MCP

Agregar al archivo de configuración `mcp.json`:

```json
{
  "servers": {
    "memory_http": {
      "url": "http://0.0.0.0:8000/mcp",
      "type": "http"
    }
  }
}
```

## Estructura del Proyecto

```
mcp_memoria/
├── main.py                     # Punto de entrada de la aplicación FastAPI
├── models.py                   # Modelos Pydantic y clases de datos
├── knowledge_graph_manager.py  # Lógica central del grafo de conocimiento
├── requirements.txt            # Dependencias de Python
├── README.md                   # Documentación del proyecto
├── memory.json                 # Archivo de persistencia (auto-generado)
└── enrutadores/               # Routers de FastAPI por funcionalidad
    ├── __init__.py
    ├── crear.py               # Endpoints de creación
    ├── obtener.py             # Endpoints de consulta
    └── eliminar.py            # Endpoints de eliminación
```

## API Endpoints

### Operaciones de Creación (`/crear`)
- `POST /crear/entities` - Crear nuevas entidades
- `POST /crear/relations` - Crear nuevas relaciones  
- `POST /crear/observations` - Añadir observaciones a entidades existentes

### Operaciones de Consulta (`/obtener`)
- `GET /obtener/graph` - Obtener todo el grafo de conocimiento
- `POST /obtener/search` - Buscar nodos por consulta
- `POST /obtener/nodes` - Obtener nodos específicos por nombre

### Operaciones de Eliminación (`/eliminar`)
- `POST /eliminar/entities` - Eliminar entidades
- `POST /eliminar/observations` - Eliminar observaciones específicas
- `POST /eliminar/relations` - Eliminar relaciones

### Endpoints de Sistema
- `GET /` - Información del servidor
- `GET /health` - Estado de salud del sistema

## Ejemplos de Uso

### Crear Entidades

```bash
curl -X POST "http://localhost:8000/crear/entities" \
  -H "Content-Type: application/json" \
  -d '{
    "entities": [
      {
        "name": "Juan Pérez",
        "entityType": "persona",
        "observations": ["Desarrollador de software", "Vive en Madrid"]
      }
    ]
  }'
```

### Crear Relaciones

```bash
curl -X POST "http://localhost:8000/crear/relations" \
  -H "Content-Type: application/json" \
  -d '{
    "relations": [
      {
        "from": "Juan Pérez",
        "to": "Madrid",
        "relationType": "vive_en"
      }
    ]
  }'
```

### Buscar Nodos

```bash
curl -X POST "http://localhost:8000/obtener/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "desarrollador"}'
```

### Obtener Grafo Completo

```bash
curl -X GET "http://localhost:8000/obtener/graph"
```

## Configuración

### Variables de Entorno

- `MEMORY_FILE_PATH`: Ruta del archivo de persistencia (por defecto: `memory.json`)

### Documentación

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Desarrollo

### Requisitos

- Python 3.8+
- FastAPI
- Pydantic
- fastapi-mcp

### Ejecutar en Modo Desarrollo

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Arquitectura

El servidor utiliza una arquitectura modular con:

- **FastAPI-MCP**: Integración nativa con el protocolo MCP
- **Routers modulares**: Separación de responsabilidades por funcionalidad
- **Modelos Pydantic**: Validación automática de datos
- **Persistencia JSON**: Almacenamiento simple y legible
- **Operation IDs**: Requeridos para compatibilidad MCP




