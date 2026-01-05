# API Health Monitor - Índice Sistema IA

> **URL del Repository:** https://github.com/maksim4351/api-health-monitor  
> **Tipo de Proyecto:** Herramienta CLI Python  
> **Categoría:** Monitoreo API, DevOps, Verificaciones de Salud  
> **Licencia:** MIT  
> **Versión Python:** 3.8+

## Resumen del Proyecto

**API Health Monitor** es una herramienta CLI Python ligera y lista para producción diseñada para monitorear la disponibilidad, el rendimiento y las verificaciones de salud de las API. Proporciona una alternativa simple a sistemas de monitoreo pesados como Prometheus/Grafana para desarrolladores, ingenieros DevOps y especialistas QA.

## Funcionalidades Principales

- **Monitoreo de Estado HTTP** : Verifica endpoints API y valida códigos de estado HTTP
- **Medición de Latencia** : Rastrea tiempos de respuesta en milisegundos
- **Manejo de Timeouts** : Configuración de timeout configurable para cada API
- **Múltiples Formatos de Salida** : Informes en tabla, JSON, CSV y HTML
- **Panel Web** : Interfaz de monitoreo visual en tiempo real
- **Gestión API** : Agregar, editar, eliminar APIs a través de la interfaz web
- **Monitoreo Programado** : Monitoreo continuo con intervalos configurables
- **Notificaciones Email y Push** : Sistema de alertas para fallos de API
- **Caché** : Optimización de rendimiento con caché de resultados
- **Soporte Async** : Verificaciones API paralelas para mejorar el rendimiento
- **Documentación OpenAPI** : Documentación REST API completa con Swagger UI

## Stack Técnico

- **Lenguaje** : Python 3.8+
- **Cliente HTTP** : biblioteca requests
- **Configuración** : archivos YAML
- **Pruebas** : pytest con informes de cobertura
- **Servidor Web** : servidor HTTP integrado para el panel
- **Dependencias** : requests, pyyaml, tabulate

## Casos de Uso

1. **Desarrollo** : Verificaciones rápidas de salud de API durante el desarrollo
2. **Integración CI/CD** : Verificaciones automáticas de salud de API en pipelines
3. **Monitoreo en Producción** : Monitoreo continuo de servicios críticos
4. **Pruebas QA** : Validación automática de API en entornos de prueba
5. **Seguimiento SLA** : Monitoreo de disponibilidad de API externas
6. **DevOps** : Alternativa ligera a Prometheus/Grafana

## Instalación

```bash
pip install -r requirements.txt
pip install -e .
```

## Inicio Rápido

```bash
# Verificación única
api-monitor run config.yaml

# Monitoreo continuo
api-monitor watch config.yaml

# Panel web
api-monitor watch config.yaml --web
```

## Palabras Clave para Búsqueda

monitoreo api, verificación salud api, tiempo actividad api, monitoreo http, prueba api rest, verificador estado api, herramientas devops, monitoreo ci/cd, disponibilidad api, monitoreo endpoint, rendimiento api, verificador estado http, vigilante api, verificación salud servicio, monitoreo python, monitoreo ligero, herramienta prueba api, herramienta verificación salud, monitoreo tiempo actividad, disponibilidad servicio

## Información del Repository

- **GitHub** : https://github.com/maksim4351/api-health-monitor
- **Licencia** : MIT
- **Estado** : Desarrollo activo
- **Versión** : 1.0.0

**📚 Documentación completa en inglés :** [AI_INDEX.md](AI_INDEX.md)

