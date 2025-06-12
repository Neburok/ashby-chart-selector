# Ejemplo de cómo integrar las funcionalidades avanzadas en la aplicación principal
# Agrega este código al final del archivo ashby_app.py, antes de la función main()

def integrate_advanced_features():
    """Función para integrar las funcionalidades avanzadas"""
    
    # Importar las clases avanzadas
    try:
        from advanced_features import (
            PerformanceIndexTool, GraphicalSelection, MaterialAnalyzer,
            ExportTools, AdvancedVisualization, add_advanced_features_to_app
        )
        return True
    except ImportError:
        return False

# Modificación de la función main() para incluir funcionalidades avanzadas
def main_with_advanced_features():
    """Función principal con funcionalidades avanzadas integradas"""
    
    # ... (código existente hasta la generación del gráfico principal) ...
    
    # Después de mostrar el gráfico principal, agregar pestaña avanzada
    if 'show_advanced' not in st.session_state:
        st.session_state.show_advanced = False
    
    # Toggle para mostrar funcionalidades avanzadas
    show_advanced = st.sidebar.checkbox("🔬 Mostrar Herramientas Avanzadas", value=st.session_state.show_advanced)
    st.session_state.show_advanced = show_advanced
    
    if show_advanced and integrate_advanced_features():
        st.markdown("---")
        
        # Agregar funcionalidades avanzadas
        from advanced_features import add_advanced_features_to_app
        add_advanced_features_to_app(
            st.session_state.database,
            st.session_state.chart_generator,
            filtered_materials
        )
    
    elif show_advanced:
        st.error("Para usar las funcionalidades avanzadas, asegúrate de que el archivo 'advanced_features.py' esté en el mismo directorio.")

# Ejemplo de uso de índices de rendimiento en el gráfico principal
def add_performance_index_to_main_chart(fig, x_property, y_property):
    """Agrega línea de índice de rendimiento al gráfico principal"""
    
    if integrate_advanced_features():
        from advanced_features import PerformanceIndexTool
        
        performance_tool = PerformanceIndexTool()
        
        # Ejemplo: agregar línea E/ρ si las propiedades son compatibles
        if (x_property == 'Densidad (kg/m³)' and 
            y_property == 'Módulo de Young (GPa)'):
            
            index_config = performance_tool.common_indices['E/ρ (Rigidez específica)']
            fig = performance_tool.add_performance_line(
                fig, x_property, y_property, index_config, line_position=0.6
            )
    
    return fig

# Ejemplo de configuración completa con todas las funcionalidades
COMPLETE_CONFIG = {
    'base_features': {
        'materials_database': True,
        'ashby_charts': True,
        'property_filtering': True,
        'interactive_tooltips': True,
        'zoom_pan': True
    },
    'advanced_features': {
        'performance_indices': True,
        'graphical_selection': True,
        'pareto_frontier': True,
        '3d_visualization': True,
        'radar_charts': True,
        'material_analysis': True,
        'export_tools': True
    },
    'ui_enhancements': {
        'custom_css': True,
        'responsive_layout': True,
        'progress_indicators': True,
        'help_tooltips': True
    }
}

# Ejemplo de extensión de la base de datos con más materiales
EXTENDED_MATERIALS = {
    'Acero Inoxidable 316L': {
        'family': 'Metales',
        'color': '#C0392B',
        'young_modulus': [190, 210],
        'yield_strength': [170, 310],
        'density': [8000, 8100],
        'fracture_toughness': [100, 200],
        'thermal_conductivity': [13, 16],
        'thermal_expansion': [15, 17],
        'max_service_temp': [800, 1000],
        'price': [3.0, 8.0]
    },
    'Inconel 718': {
        'family': 'Metales',
        'color': '#8E44AD',
        'young_modulus': [200, 220],
        'yield_strength': [1000, 1400],
        'density': [8200, 8300],
        'fracture_toughness': [80, 120],
        'thermal_conductivity': [11, 15],
        'thermal_expansion': [12, 14],
        'max_service_temp': [650, 750],
        'price': [25, 50]
    },
    'PEEK': {
        'family': 'Polímeros',
        'color': '#E67E22',
        'young_modulus': [3.5, 4.5],
        'yield_strength': [90, 110],
        'density': [1300, 1320],
        'fracture_toughness': [3, 5],
        'thermal_conductivity': [0.25, 0.3],
        'thermal_expansion': [47, 50],
        'max_service_temp': [250, 300],
        'price': [80, 150]
    },
    'Carburo de Tungsteno': {
        'family': 'Cerámicos',
        'color': '#34495E',
        'young_modulus': [500, 700],
        'yield_strength': [3000, 5000],
        'density': [14000, 16000],
        'fracture_toughness': [10, 15],
        'thermal_conductivity': [80, 120],
        'thermal_expansion': [4, 6],
        'max_service_temp': [1000, 1500],
        'price': [30, 100]
    }
}

# Ejemplo de índices de rendimiento personalizados
CUSTOM_PERFORMANCE_INDICES = {
    'Resistencia/Peso': {
        'formula': 'yield_strength / density',
        'description': 'Resistencia específica para aplicaciones estructurales',
        'units': 'MPa·m³/kg',
        'higher_is_better': True
    },
    'Rigidez/Peso': {
        'formula': 'young_modulus / density',
        'description': 'Rigidez específica para minimizar deformaciones',
        'units': 'GPa·m³/kg',
        'higher_is_better': True
    },
    'Eficiencia Térmica': {
        'formula': 'thermal_conductivity / (thermal_expansion * density)',
        'description': 'Conductividad térmica normalizada por expansión y peso',
        'units': 'W·m²/(kg·K·µm)',
        'higher_is_better': True
    },
    'Costo-Beneficio': {
        'formula': 'yield_strength / price',
        'description': 'Resistencia por unidad de costo',
        'units': 'MPa/(€/kg)',
        'higher_is_better': True
    }
}

# Función de ejemplo para análisis multi-criterio
def multi_criteria_analysis(materials_dict, criteria_weights):
    """
    Realiza análisis multi-criterio para ranking de materiales
    
    Args:
        materials_dict: Diccionario de materiales filtrados
        criteria_weights: Pesos para cada criterio (suma = 1.0)
    
    Returns:
        DataFrame con puntuaciones y ranking
    """
    
    results = []
    
    for material_name, material_props in materials_dict.items():
        score = 0
        valid_criteria = 0
        
        # Calcular puntuación ponderada
        for criterion, weight in criteria_weights.items():
            if criterion in CUSTOM_PERFORMANCE_INDICES:
                index_config = CUSTOM_PERFORMANCE_INDICES[criterion]
                # Simplificación: usar valores medios
                # En implementación real, se calcularía según la fórmula
                normalized_value = 0.5  # Placeholder
                score += weight * normalized_value
                valid_criteria += 1
        
        if valid_criteria > 0:
            final_score = score / valid_criteria
            results.append({
                'Material': material_name,
                'Familia': material_props['family'],
                'Puntuación': final_score,
                'Ranking': 0  # Se calculará después
            })
    
    # Convertir a DataFrame y calcular ranking
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values('Puntuación', ascending=False)
        df['Ranking'] = range(1, len(df) + 1)
    
    return df

# Ejemplo de uso en Streamlit
def example_usage_in_streamlit():
    """Ejemplo de cómo usar las funcionalidades en la interfaz"""
    
    st.subheader("🎯 Análisis Multi-Criterio")
    
    # Selector de criterios y pesos
    criteria = list(CUSTOM_PERFORMANCE_INDICES.keys())
    
    st.write("Ajusta la importancia de cada criterio:")
    weights = {}
    total_weight = 0
    
    for criterion in criteria:
        weight = st.slider(
            f"{criterion}:",
            min_value=0.0,
            max_value=1.0,
            value=1.0/len(criteria),
            step=0.05,
            key=f"weight_{criterion}"
        )
        weights[criterion] = weight
        total_weight += weight
    
    # Normalizar pesos
    if total_weight > 0:
        weights = {k: v/total_weight for k, v in weights.items()}
    
    # Mostrar análisis
    if st.button("Realizar Análisis"):
        # Aquí se llamaría a la función con los materiales filtrados
        st.info("Análisis multi-criterio completado!")

# Documentación de uso
USAGE_EXAMPLES = {
    'basic_filtering': """
    # Filtrado básico
    1. Selecciona propiedades para ejes X e Y
    2. Activa filtros en el panel lateral
    3. Ajusta rangos con los sliders
    4. Observa resultados en tiempo real
    """,
    
    'performance_indices': """
    # Índices de rendimiento
    1. Selecciona un índice predefinido (E/ρ, σy/ρ, etc.)
    2. La línea de rendimiento se superpone al gráfico
    3. Los materiales más cercanos a la línea son óptimos
    4. Usa el slider para mover la línea
    """,
    
    'advanced_analysis': """
    # Análisis avanzado
    1. Activa "Herramientas Avanzadas" en la barra lateral
    2. Usa pestañas para diferentes análisis:
       - Índices: Ranking cuantitativo
       - 3D: Visualización tridimensional
       - Radar: Comparación multi-propiedad
       - Exportación: Guardar resultados
    """,
    
    'material_selection_workflow': """
    # Flujo completo de selección
    1. Define requisitos del diseño
    2. Establece filtros restrictivos
    3. Analiza gráfico de Ashby resultante
    4. Aplica índices de rendimiento relevantes
    5. Compara candidatos finales con gráfico radar
    6. Exporta lista final para análisis detallado
    """
}

# Configuración de temas personalizados
CUSTOM_THEMES = {
    'professional': {
        'primary_color': '#1f77b4',
        'background_color': '#ffffff',
        'secondary_color': '#ff7f0e',
        'text_color': '#333333'
    },
    'dark_mode': {
        'primary_color': '#00d4aa',
        'background_color': '#0e1117',
        'secondary_color': '#ff6b6b',
        'text_color': '#fafafa'
    },
    'academic': {
        'primary_color': '#2e86ab',
        'background_color': '#f8f9fa',
        'secondary_color': '#a23b72',
        'text_color': '#212529'
    }
}

# Función para aplicar temas
def apply_custom_theme(theme_name):
    """Aplica un tema personalizado a la aplicación"""
    
    if theme_name not in CUSTOM_THEMES:
        return
    
    theme = CUSTOM_THEMES[theme_name]
    
    custom_css = f"""
    <style>
        .stApp {{
            background-color: {theme['background_color']};
            color: {theme['text_color']};
        }}
        
        .main-header {{
            color: {theme['primary_color']};
        }}
        
        .stButton > button {{
            background-color: {theme['primary_color']};
            color: white;
            border: none;
            border-radius: 4px;
        }}
        
        .stSelectbox > div > div {{
            background-color: {theme['background_color']};
        }}
        
        .property-filter {{
            background-color: {theme['secondary_color']}20;
            border-left: 4px solid {theme['secondary_color']};
        }}
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

# Funciones de utilidad para análisis estadístico
def calculate_material_statistics(materials_dict):
    """Calcula estadísticas descriptivas de los materiales"""
    
    stats = {}
    
    for prop_display, prop_key in st.session_state.database.properties.items():
        values = []
        
        for material_data in materials_dict.values():
            if prop_key in material_data:
                # Usar valor medio del rango
                avg_val = np.mean(material_data[prop_key])
                values.append(avg_val)
        
        if values:
            stats[prop_display] = {
                'count': len(values),
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'median': np.median(values)
            }
    
    return stats

# Función para generar insights automáticos
def generate_material_insights(filtered_materials, original_materials):
    """Genera insights automáticos sobre la selección de materiales"""
    
    insights = []
    
    # Análisis de familias representadas
    families = {}
    for material_data in filtered_materials.values():
        family = material_data['family']
        families[family] = families.get(family, 0) + 1
    
    if families:
        dominant_family = max(families, key=families.get)
        insights.append(f"🔍 La familia dominante es **{dominant_family}** con {families[dominant_family]} materiales.")
    
    # Análisis de reducción
    original_count = len(original_materials)
    filtered_count = len(filtered_materials)
    reduction_percent = ((original_count - filtered_count) / original_count) * 100
    
    if reduction_percent > 50:
        insights.append(f"⚡ Los filtros han reducido las opciones en un {reduction_percent:.1f}%, facilitando la selección.")
    elif reduction_percent < 10:
        insights.append(f"⚠️ Los filtros son poco restrictivos ({reduction_percent:.1f}% de reducción). Considera criterios más estrictos.")
    
    # Análisis de rango de precios
    prices = []
    for material_data in filtered_materials.values():
        if 'price' in material_data:
            prices.extend(material_data['price'])
    
    if prices:
        min_price, max_price = min(prices), max(prices)
        if max_price / min_price > 10:
            insights.append(f"💰 Amplio rango de precios: {min_price:.1f} - {max_price:.1f} €/kg. Considera el presupuesto.")
    
    return insights

# Ejemplo de funcionalidad de comparación directa
def create_material_comparison_table(selected_materials, database):
    """Crea tabla de comparación detallada entre materiales seleccionados"""
    
    if not selected_materials:
        return pd.DataFrame()
    
    comparison_data = []
    
    for material_name in selected_materials:
        if material_name in database.materials:
            material_data = database.materials[material_name]
            row = {
                'Material': material_name,
                'Familia': material_data['family']
            }
            
            # Agregar todas las propiedades
            for prop_display, prop_key in database.properties.items():
                if prop_key in material_data:
                    min_val, max_val = material_data[prop_key]
                    avg_val = (min_val + max_val) / 2
                    row[prop_display] = f"{avg_val:.2f} ({min_val:.1f}-{max_val:.1f})"
                else:
                    row[prop_display] = "N/A"
            
            comparison_data.append(row)
    
    return pd.DataFrame(comparison_data)

# Función para validación de selección
def validate_material_selection(materials_dict, application_requirements):
    """Valida si los materiales seleccionados cumplen requisitos de aplicación"""
    
    validation_results = {}
    
    for material_name, material_data in materials_dict.items():
        passes_validation = True
        failed_requirements = []
        
        for req_property, req_value in application_requirements.items():
            prop_key = st.session_state.database.properties.get(req_property)
            
            if prop_key and prop_key in material_data:
                material_range = material_data[prop_key]
                
                # Verificar si el rango del material satisface el requisito
                if req_value['type'] == 'minimum':
                    if material_range[1] < req_value['value']:  # max del material < requisito
                        passes_validation = False
                        failed_requirements.append(f"{req_property} < {req_value['value']}")
                
                elif req_value['type'] == 'maximum':
                    if material_range[0] > req_value['value']:  # min del material > requisito
                        passes_validation = False
                        failed_requirements.append(f"{req_property} > {req_value['value']}")
        
        validation_results[material_name] = {
            'passes': passes_validation,
            'failed_requirements': failed_requirements
        }
    
    return validation_results

# Ejemplo de configuración de requisitos de aplicación
APPLICATION_TEMPLATES = {
    'Aeroespacial': {
        'Densidad (kg/m³)': {'type': 'maximum', 'value': 3000},
        'Módulo de Young (GPa)': {'type': 'minimum', 'value': 50},
        'Temp. Máx. Servicio (°C)': {'type': 'minimum', 'value': 200},
        'Precio (€/kg)': {'type': 'maximum', 'value': 50}
    },
    'Automotriz': {
        'Densidad (kg/m³)': {'type': 'maximum', 'value': 8000},
        'Límite Elástico (MPa)': {'type': 'minimum', 'value': 200},
        'Precio (€/kg)': {'type': 'maximum', 'value': 10},
        'Tenacidad a la Fractura (MPa√m)': {'type': 'minimum', 'value': 20}
    },
    'Electrónica': {
        'Conductividad Térmica (W/m·K)': {'type': 'minimum', 'value': 50},
        'Coef. Expansión Térmica (µm/m°C)': {'type': 'maximum', 'value': 15},
        'Temp. Máx. Servicio (°C)': {'type': 'minimum', 'value': 150},
        'Densidad (kg/m³)': {'type': 'maximum', 'value': 5000}
    },
    'Construcción': {
        'Límite Elástico (MPa)': {'type': 'minimum', 'value': 250},
        'Precio (€/kg)': {'type': 'maximum', 'value': 5},
        'Densidad (kg/m³)': {'type': 'maximum', 'value': 10000},
        'Temp. Máx. Servicio (°C)': {'type': 'minimum', 'value': 100}
    }
}

# Función para implementar en la interfaz principal
def add_application_templates_ui():
    """Agrega interfaz para plantillas de aplicación"""
    
    st.subheader("🎯 Plantillas de Aplicación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_template = st.selectbox(
            "Seleccionar plantilla:",
            ['Personalizado'] + list(APPLICATION_TEMPLATES.keys())
        )
    
    with col2:
        if st.button("Aplicar Plantilla") and selected_template != 'Personalizado':
            st.session_state.current_template = selected_template
            st.success(f"Plantilla '{selected_template}' aplicada!")
    
    # Mostrar requisitos de la plantilla
    if selected_template != 'Personalizado':
        st.write("**Requisitos de la aplicación:**")
        requirements = APPLICATION_TEMPLATES[selected_template]
        
        for prop, req in requirements.items():
            symbol = "≤" if req['type'] == 'maximum' else "≥"
            st.write(f"• {prop}: {symbol} {req['value']}")

if __name__ == "__main__":
    # Ejemplo de uso completo con todas las funcionalidades
    st.title("AshbyChart Selector - Versión Completa")
    
    # Aplicar tema
    theme = st.sidebar.selectbox("Tema:", list(CUSTOM_THEMES.keys()), index=0)
    apply_custom_theme(theme)
    
    # Resto de la aplicación...
    pass