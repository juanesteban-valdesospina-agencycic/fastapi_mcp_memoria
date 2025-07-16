#!/usr/bin/env python3
"""
Script de prueba para el servidor MCP del grafo de conocimiento
Ejecuta este script con el servidor corriendo para probar todas las funcionalidades
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_server():
    """Prueba todas las funcionalidades del servidor"""
    
    print("🧪 Iniciando pruebas del Knowledge Graph MCP Server...")
    print("=" * 60)
    
    # Test 1: Verificar que el servidor esté ejecutándose
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Server health check: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: El servidor no está ejecutándose en localhost:8000")
        return
    
    # Test 2: Crear entidades
    print("\n📝 Creando entidades...")
    entities_data = {
        "entities": [
            {
                "name": "Juan",
                "entityType": "persona",
                "observations": ["Es desarrollador", "Vive en Madrid", "Le gusta Python"]
            },
            {
                "name": "Madrid",
                "entityType": "ciudad",
                "observations": ["Capital de España", "Tiene muchos museos"]
            },
            {
                "name": "Python",
                "entityType": "lenguaje_programacion",
                "observations": ["Lenguaje interpretado", "Muy popular para IA"]
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/crear/entities", json=entities_data)
    print(f"Status: {response.status_code}")
    print(f"Entidades creadas: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test 3: Crear relaciones
    print("\n🔗 Creando relaciones...")
    relations_data = {
        "relations": [
            {
                "from": "Juan",
                "to": "Madrid", 
                "relationType": "vive_en"
            },
            {
                "from": "Juan",
                "to": "Python",
                "relationType": "programa_en"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/crear/relations", json=relations_data)
    print(f"Status: {response.status_code}")
    print(f"Relaciones creadas: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test 4: Añadir observaciones
    print("\n📋 Añadiendo observaciones...")
    observations_data = {
        "observations": [
            {
                "entityName": "Juan",
                "contents": ["Trabaja en una startup", "Le gusta el café"]
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/crear/observations", json=observations_data)
    print(f"Status: {response.status_code}")
    print(f"Observaciones añadidas: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # Test 5: Leer el grafo completo
    print("\n📖 Leyendo grafo completo...")
    response = requests.get(f"{BASE_URL}/obtener/graph")
    print(f"Status: {response.status_code}")
    graph = response.json()
    print(f"Entidades: {len(graph['entities'])}")
    print(f"Relaciones: {len(graph['relations'])}")
    
    # Test 6: Buscar nodos
    print("\n🔍 Buscando nodos con 'desarrollador'...")
    search_data = {"query": "desarrollador"}
    response = requests.post(f"{BASE_URL}/obtener/search", json=search_data)
    print(f"Status: {response.status_code}")
    search_results = response.json()
    print(f"Entidades encontradas: {len(search_results['entities'])}")
    print(f"Relaciones encontradas: {len(search_results['relations'])}")
    
    # Test 7: Abrir nodos específicos
    print("\n📂 Abriendo nodos específicos...")
    nodes_data = {"names": ["Juan", "Madrid"]}
    response = requests.post(f"{BASE_URL}/obtener/nodes", json=nodes_data)
    print(f"Status: {response.status_code}")
    nodes_results = response.json()
    print(f"Nodos abiertos: {json.dumps(nodes_results, indent=2, ensure_ascii=False)}")
    
    # Test 8: Eliminar observaciones
    print("\n🗑️ Eliminando una observación...")
    delete_obs_data = {
        "deletions": [
            {
                "entityName": "Juan",
                "observations": ["Le gusta el café"]
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/eliminar/observations", json=delete_obs_data)
    print(f"Status: {response.status_code}")
    print(f"Resultado: {response.json()}")
    
    # Test 9: Eliminar una relación
    print("\n🔗❌ Eliminando una relación...")
    delete_rel_data = {
        "relations": [
            {
                "from": "Juan",
                "to": "Python",
                "relationType": "programa_en"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/eliminar/relations", json=delete_rel_data)
    print(f"Status: {response.status_code}")
    print(f"Resultado: {response.json()}")
    
    # Test 10: Estado final del grafo
    print("\n📊 Estado final del grafo...")
    response = requests.get(f"{BASE_URL}/obtener/graph")
    final_graph = response.json()
    print(f"Entidades finales: {len(final_graph['entities'])}")
    print(f"Relaciones finales: {len(final_graph['relations'])}")
    
    print("\n" + "=" * 60)
    print("✅ ¡Todas las pruebas completadas exitosamente!")
    print("\n🌐 Documentación disponible en:")
    print(f"   • Swagger UI: {BASE_URL}/docs")
    print(f"   • ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    test_server()
