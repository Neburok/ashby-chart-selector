# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto AshbyChart Selector! Esta guía te ayudará a empezar.

## 🚀 Cómo Contribuir

### 1. Fork y Clone
```bash
# Haz fork del repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU_USUARIO/ashby-chart-selector.git
cd ashby-chart-selector
```

### 2. Configurar Entorno de Desarrollo
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install pytest flake8 black isort
```

### 3. Crear Rama para tu Feature
```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

## 📋 Tipos de Contribuciones

### 🐛 Reportar Bugs
- Usa el template de issues para bugs
- Incluye pasos para reproducir
- Adjunta screenshots si es necesario
- Especifica versiones de Python y dependencias

### ✨ Nuevas Funcionalidades
- Abre un issue primero para discutir la idea
- Asegúrate de que esté alineada con el roadmap
- Implementa tests si es aplicable
- Actualiza la documentación

### 📚 Mejoras de Documentación
- Corrige errores tipográficos
- Mejora explicaciones
- Agrega ejemplos
- Traduce contenido

### 🧪 Agregar Materiales
```python
# Formato para nuevos materiales
'Nuevo Material': {
    'family': 'Familia Apropiada',
    'color': '#HEXCOLOR',
    'young_modulus': [min_val, max_val],
    'yield_strength': [min_val, max_val],
    'density': [min_val, max_val],
    # ... otras propiedades
}
```

## 🔧 Estándares de Desarrollo

### Estilo de Código
```bash
# Formatear código
black ashby_app.py

# Ordenar imports
isort ashby_app.py

# Verificar estilo
flake8 ashby_app.py
```

### Tests
```bash
# Ejecutar tests
python -m pytest tests/

# Test básico de importación
python -c "import ashby_app; print('✅ OK')"
```

### Commits
Usa conventional commits:
```
feat: agregar visualización 3D
fix: corregir filtrado de materiales
docs: actualizar README
style: mejorar interfaz de usuario
refactor: optimizar cálculos de elipses
test: agregar tests para base de datos
```

## 📝 Pull Request Process

### 1. Antes de Enviar
- [ ] El código funciona localmente
- [ ] Tests pasan (si existen)
- [ ] Documentación actualizada
- [ ] Changelog actualizado (si es necesario)

### 2. Template de PR
```markdown
## Descripción
Breve descripción de los cambios

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## Testing
- [ ] Tests existentes pasan
- [ ] Nuevos tests agregados
- [ ] Testing manual completado

## Screenshots (si aplica)
```

### 3. Review Process
- Al menos 1 review requerido
- CI debe pasar
- Conflictos resueltos
- Documentación actualizada

## 🌟 Reconocimientos

### Contributors
Todos los contribuidores son listados en:
- README.md
- Releases notes
- Hall of Fame (próximamente)

### Tipos de Contribución
- 💻 Código
- 📖 Documentación
- 🐛 Bug reports
- 💡 Ideas
- 🤔 Preguntas respondidas
- ⚠️ Tests
- 🚇 Infraestructura
- 🔧 Herramientas

## 📞 Obtener Ayuda

### Canales de Comunicación
- **Issues**: Para bugs y features
- **Discussions**: Para preguntas generales
- **Email**: [tu-email] para contacto directo

### Recursos Útiles
- [Documentación de Streamlit](https://docs.streamlit.io)
- [Plotly Python Docs](https://plotly.com/python/)
- [Método de Ashby](https://en.wikipedia.org/wiki/Materials_selection)

## 🎯 Roadmap de Contribuciones

### Prioridad Alta
- [ ] Tests automatizados
- [ ] Más materiales en la base de datos
- [ ] Validación de entrada de datos
- [ ] Optimización de rendimiento

### Prioridad Media
- [ ] Plantillas de aplicación
- [ ] Exportación avanzada
- [ ] Temas personalizables
- [ ] Documentación en múltiples idiomas

### Prioridad Baja
- [ ] API REST
- [ ] Integración con bases de datos externas
- [ ] Machine Learning para recomendaciones
- [ ] Modo colaborativo

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones sean licenciadas bajo la [MIT License](LICENSE).

---

¡Gracias por contribuir al futuro de la selección de materiales! 🔬✨