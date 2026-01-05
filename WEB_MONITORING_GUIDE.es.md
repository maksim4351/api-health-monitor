# 🌐 Guía de Monitoreo Web API

## 🚀 Inicio Rápido

### ⚡ Método Más Simple (Windows)

**Simplemente haga doble clic en el archivo:**
```
run_web_monitoring.bat
```

**Lo que sucederá:**
1. ✅ Verifica automáticamente Python
2. ✅ Instala dependencias
3. ✅ Verifica `config.yaml`
4. ✅ Solicita intervalo de verificación
5. ✅ Inicia servidor web
6. ✅ Abre automáticamente el navegador en `http://localhost:8080`

**💡 Importante:**
- Si el puerto 8080 está ocupado, el sistema encuentra automáticamente un puerto libre
- El navegador se abre automáticamente en el puerto correcto
- Presione `Ctrl+C` para detener

## 🌐 Panel Web - Características

### 📊 Pestaña "Monitoring"

- Estadísticas en tiempo real
- Tabla de resultados con indicadores de color
- Actualización automática cada 5 segundos

### 🎛️ Pestaña "Gestión API"

**Agregar nuevos API:**
- Formulario con validación
- Campos: Nombre, URL, Método, Timeout, Estado esperado
- 20 API populares para adición rápida
- Notificaciones de éxito/error

**Gestión de API:**
- Ver todos los API agregados
- Editar API existentes
- Eliminar API con confirmación

### 📚 Documentación OpenAPI

- **Swagger UI** disponible en `/api/docs`
- Documentación interactiva para todos los endpoints REST

## 🔔 Notificaciones

- Notificaciones push del navegador
- Notificaciones por correo electrónico (si está configurado)
- Alertas sobre errores de API

## 🛠️ Métodos de Inicio Alternativos

```bash
# Por línea de comandos
api-monitor watch config.yaml --web

# Con intervalo personalizado
api-monitor watch config.yaml --web --interval 30

# Con puerto personalizado
api-monitor watch config.yaml --web --port 9000
```

## 📚 Documentación Completa

**📖 Para la documentación completa en inglés, ver :** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)

---

**🔗 Enlaces útiles:**
- 📖 **Documentación completa:** [WEB_MONITORING_GUIDE.md](WEB_MONITORING_GUIDE.md)
- 🌐 **Proyecto:** https://github.com/maksim4351/api-health-monitor

