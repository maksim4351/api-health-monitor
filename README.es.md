# API Health Monitor

> **Repositorio:** https://github.com/maksim4351/api-health-monitor  
> **Licencia:** MIT  
> **Python:** 3.8+  
> **Estado:** ✅ Listo para producción

🚀 **Monitoreo rápido de disponibilidad y latencia de API sin sistemas complejos**

**API Health Monitor** es una herramienta CLI ligera de Python para monitorear la disponibilidad, el rendimiento y el estado de las API REST, servicios web y endpoints HTTP. Perfecto para desarrolladores, ingenieros DevOps y especialistas QA que necesitan verificaciones rápidas del estado de las API sin implementar sistemas de monitoreo pesados.

## 🔍 Palabras clave de búsqueda

`monitoreo api` | `verificación salud api` | `tiempo actividad api` | `monitoreo http` | `prueba api rest` | `verificador estado api` | `herramientas devops` | `monitoreo ci/cd` | `disponibilidad api` | `monitoreo endpoint` | `rendimiento api` | `verificador estado http` | `vigilante api` | `verificación salud servicio` | `monitoreo python` | `monitoreo ligero` | `herramienta prueba api` | `herramienta verificación salud` | `monitoreo tiempo actividad` | `disponibilidad servicio`

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/maksim4351/api-health-monitor/actions/workflows/test.yml/badge.svg)](https://github.com/maksim4351/api-health-monitor/actions)

**🔑 Palabras clave:** `monitoreo api`, `verificación salud api`, `tiempo actividad api`, `monitoreo http`, `prueba api rest`, `verificador estado api`, `herramientas devops`, `monitoreo ci/cd`, `disponibilidad api`, `monitoreo endpoint`, `rendimiento api`, `verificador estado http`, `vigilante api`, `verificación salud servicio`, `monitoreo python`, `monitoreo ligero`, `herramienta prueba api`, `herramienta verificación salud`, `monitoreo tiempo actividad`, `disponibilidad servicio`

## 📋 Descripción

**API Health Monitor** es una herramienta CLI simple pero potente para monitorear la disponibilidad y el rendimiento de las API, servicios web y endpoints HTTP. La herramienta verifica las API especificadas según un horario o manualmente, recopila métricas (estado HTTP, latencia, timeouts) y genera informes en varios formatos (tabla, JSON, CSV, HTML).

### 🎯 Casos de uso principales

- **Monitoreo de API en producción** — seguimiento continuo de servicios críticos
- **Integración CI/CD** — verificaciones automáticas del estado de las API antes del despliegue
- **Pruebas QA** — validación de API en entornos de prueba
- **Monitoreo SLA** — seguimiento de la disponibilidad de servicios externos
- **Desarrollo** — verificaciones rápidas de API durante el desarrollo
- **DevOps** — alternativa ligera a Prometheus/Grafana

### 🔍 Ventajas clave

- ⚡ **Inicio rápido** — funciona de inmediato, configuración mínima
- 🎯 **Simplicidad** — no se requiere infraestructura compleja
- 📊 **Informes flexibles** — tabla, JSON, CSV para integración con otras herramientas
- 🔧 **Listo para CI/CD** — códigos de salida apropiados para automatización
- 🐍 **Python 3.8+** — funciona en todos los sistemas modernos
- 📝 **Configuración YAML** — clara y fácil de editar

## 🚀 Inicio rápido

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/maksim4351/api-health-monitor.git
cd api-health-monitor

# Instalar dependencias
pip install -r requirements.txt

# Instalación de desarrollo
pip install -e .
```

### Uso

```bash
# Verificación única
api-monitor run config.yaml

# Monitoreo continuo
api-monitor watch config.yaml

# Interfaz web
api-monitor watch config.yaml --web
```

## 📖 Documentación completa

📚 **Para la documentación completa en inglés, ver:** [README.md](README.md)

- Guía completa: [README.md](README.md)
- Guía de monitoreo web: [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- Guía de contribución: [CONTRIBUTING.md](CONTRIBUTING.md)

## ✨ Características principales

- ✅ Verificaciones de estado HTTP y latencia para API
- ✅ Timeouts configurables para cada API
- ✅ Soporte para todos los métodos HTTP (GET, POST, PUT, DELETE, PATCH)
- ✅ Validación del código de estado esperado
- ✅ Encabezados HTTP personalizados
- ✅ Informes en formatos tabla, JSON, CSV, HTML
- ✅ Panel web en tiempo real
- ✅ Notificaciones por correo electrónico y push
- ✅ Caché de resultados
- ✅ Verificaciones asíncronas (solicitudes paralelas)

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**🔗 Enlaces útiles:**
- 📖 **Documentación completa:** https://github.com/maksim4351/api-health-monitor#readme
- 🌐 **Monitoreo web:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🤖 **Índice AI:** [AI_INDEX.md](AI_INDEX.md) - información para sistemas de IA

