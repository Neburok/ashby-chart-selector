# AshbyChart Selector

Aplicación interactiva para la selección de materiales basada en el método de Michael Ashby.

## 🚀 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clona o descarga el proyecto**
   ```bash
   # Si tienes git instalado
   git clone <url-del-repositorio>
   cd ashby-chart-selector
   ```

2. **Crea un entorno virtual (recomendado)**
   ```bash
   python -m venv ashby_env
   
   # En Windows:
   ashby_env\Scripts\activate
   
   # En macOS/Linux:
   source ashby_env/bin/activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Ejecución

Para ejecutar la aplicación:

```bash
streamlit run ashby_app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📋 Funcionalidades

### ✅ Implementadas
- **Base de datos de materiales**: 11 familias de materiales con 8 propiedades cada uno
- **Gráficos de Ashby interactivos**: Visualización logarítmica con elipses representando rangos de propiedades
- **Sistema de filtrado avanzado**: Filtros por rangos de propiedades con actualización en tiempo real
- **Interfaz intuitiva**: Selección de ejes X e Y mediante menús desplegables
- **Tooltips informativos**: Información detallada al pasar el cursor sobre las elipses
- **Panel de resultados**: Estadísticas y lista de materiales candidatos

### 🚧 En desarrollo
- **Índices de rendimiento**: Trazado de líneas de guía para optimización
- **Selección gráfica**: Herramienta de caja de selección directa en el gráfico
- **Exportación de resultados**: Guardar gráficos y listas de materiales

## 🗂️ Estructura de Datos

### Familias de Materiales Incluidas
- **Metales**: Aceros, Aleaciones de Aluminio, Aleaciones de Titanio
- **Polímeros**: Polietileno, Polipropileno, Resinas Epóxicas
- **Cerámicos**: Alúmina, Circonia
- **Compuestos**: Fibra de Carbono/Epoxy, Fibra de Vidrio/Poliéster
- **Naturales**: Madera (Pino)

### Propiedades Disponibles
1. **Módulo de Young (GPa)**: Rigidez del material
2. **Límite Elástico (MPa)**: Resistencia máxima antes de deformación permanente
3. **Densidad (kg/m³)**: Masa por unidad de volumen
4. **Tenacidad a la Fractura (MPa√m)**: Resistencia a la propagación de grietas
5. **Conductividad Térmica (W/m·K)**: Capacidad de conducir calor
6. **Coef. Expansión Térmica (µm/m°C)**: Cambio dimensional con temperatura
7. **Temp. Máx. Servicio (°C)**: Temperatura máxima de operación
8. **Precio (€/kg)**: Costo aproximado por kilogramo

## 🎯 Cómo Usar la Aplicación

### 1. Selección de Propiedades
- Usa los menús desplegables en la barra lateral para seleccionar las propiedades de los ejes X e Y
- El gráfico se actualiza automáticamente

### 2. Aplicación de Filtros
- Abre los expandibles en la sección "Filtros de Propiedades"
- Activa el checkbox para habilitar un filtro
- Ajusta el rango usando el slider
- Los materiales se filtran en tiempo real

### 3. Interpretación del Gráfico
- Cada elipse representa una familia de materiales
- El tamaño de la elipse indica el rango de propiedades
- Los colores distinguen las diferentes familias
- Usa el zoom y paneo para explorar en detalle

### 4. Análisis de Resultados
- El panel derecho muestra estadísticas de filtrado
- La lista de "Materiales Candidatos" incluye solo los que pasan todos los filtros
- Usa esta información para la selección final

## 🔧 Extensión y Personalización

### Agregar Nuevos Materiales
Edita la función `_create_materials_database()` en la clase `MaterialDatabase`:

```python
'Nuevo Material': {
    'family': 'Familia',
    'color': '#HEXCOLOR',
    'young_modulus': [min, max],
    'yield_strength': [min, max],
    # ... otras propiedades
}
```

### Agregar Nuevas Propiedades
1. Actualiza el diccionario `properties` en `MaterialDatabase`
2. Agrega los valores correspondientes a todos los materiales
3. La interfaz se actualizará automáticamente

## 🐛 Solución de Problemas

### Error de módulos no encontrados
```bash
pip install --upgrade -r requirements.txt
```

### La aplicación no se abre
- Verifica que el puerto 8501 esté disponible
- Usa `streamlit run ashby_app.py --server.port 8502` para cambiar el puerto

### Gráfico no se muestra
- Verifica que Plotly esté instalado correctamente
- Actualiza tu navegador

## 📧 Contacto y Contribuciones

Si encuentras errores o tienes sugerencias de mejora, por favor:
1. Crea un issue en el repositorio
2. Envía un pull request con tus cambios
3. Contacta al desarrollador

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.