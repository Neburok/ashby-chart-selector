import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from pathlib import Path
import math

# Configuración de la página
st.set_page_config(
    page_title="AshbyChart Selector",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .property-filter {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .results-panel {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

class MaterialDatabase:
    """Clase para manejar la base de datos de materiales"""
    
    def __init__(self):
        self.materials = self._create_materials_database()
        self.properties = {
            'Módulo de Young (GPa)': 'young_modulus',
            'Límite Elástico (MPa)': 'yield_strength', 
            'Densidad (kg/m³)': 'density',
            'Tenacidad a la Fractura (MPa√m)': 'fracture_toughness',
            'Conductividad Térmica (W/m·K)': 'thermal_conductivity',
            'Coef. Expansión Térmica (µm/m°C)': 'thermal_expansion',
            'Temp. Máx. Servicio (°C)': 'max_service_temp',
            'Precio (€/kg)': 'price'
        }
    
    def _create_materials_database(self):
        """Crea la base de datos de materiales con propiedades representativas"""
        materials_data = {
            'Aceros': {
                'family': 'Metales',
                'color': '#FF6B6B',
                'young_modulus': [200, 220],
                'yield_strength': [200, 1500],
                'density': [7800, 8000],
                'fracture_toughness': [50, 200],
                'thermal_conductivity': [40, 60],
                'thermal_expansion': [11, 13],
                'max_service_temp': [400, 600],
                'price': [0.5, 2.0]
            },
            'Aleaciones de Aluminio': {
                'family': 'Metales',
                'color': '#4ECDC4',
                'young_modulus': [70, 85],
                'yield_strength': [30, 600],
                'density': [2700, 2900],
                'fracture_toughness': [20, 45],
                'thermal_conductivity': [120, 240],
                'thermal_expansion': [22, 25],
                'max_service_temp': [150, 300],
                'price': [1.5, 4.0]
            },
            'Aleaciones de Titanio': {
                'family': 'Metales',
                'color': '#45B7D1',
                'young_modulus': [100, 120],
                'yield_strength': [200, 1200],
                'density': [4400, 4900],
                'fracture_toughness': [30, 100],
                'thermal_conductivity': [6, 20],
                'thermal_expansion': [8, 10],
                'max_service_temp': [400, 600],
                'price': [15, 40]
            },
            'Polietileno (PE)': {
                'family': 'Polímeros',
                'color': '#96CEB4',
                'young_modulus': [0.5, 1.5],
                'yield_strength': [10, 40],
                'density': [910, 970],
                'fracture_toughness': [1, 5],
                'thermal_conductivity': [0.3, 0.5],
                'thermal_expansion': [100, 200],
                'max_service_temp': [80, 120],
                'price': [1.0, 2.5]
            },
            'Polipropileno (PP)': {
                'family': 'Polímeros',
                'color': '#FFEAA7',
                'young_modulus': [1.0, 2.0],
                'yield_strength': [20, 40],
                'density': [900, 920],
                'fracture_toughness': [2, 4],
                'thermal_conductivity': [0.1, 0.3],
                'thermal_expansion': [80, 150],
                'max_service_temp': [100, 140],
                'price': [1.2, 2.8]
            },
            'Resinas Epóxicas': {
                'family': 'Polímeros',
                'color': '#DDA0DD',
                'young_modulus': [2.5, 4.5],
                'yield_strength': [50, 90],
                'density': [1100, 1400],
                'fracture_toughness': [0.5, 2],
                'thermal_conductivity': [0.15, 0.25],
                'thermal_expansion': [45, 80],
                'max_service_temp': [120, 200],
                'price': [5, 15]
            },
            'Alúmina (Al₂O₃)': {
                'family': 'Cerámicos',
                'color': '#FFB347',
                'young_modulus': [350, 400],
                'yield_strength': [300, 500],
                'density': [3900, 4000],
                'fracture_toughness': [3, 5],
                'thermal_conductivity': [20, 35],
                'thermal_expansion': [7, 9],
                'max_service_temp': [1500, 1800],
                'price': [10, 30]
            },
            'Circonia (ZrO₂)': {
                'family': 'Cerámicos',
                'color': '#F4A460',
                'young_modulus': [200, 250],
                'yield_strength': [800, 1200],
                'density': [6000, 6200],
                'fracture_toughness': [5, 12],
                'thermal_conductivity': [2, 3],
                'thermal_expansion': [9, 11],
                'max_service_temp': [1000, 1500],
                'price': [20, 60]
            },
            'Fibra de Carbono/Epoxy': {
                'family': 'Compuestos',
                'color': '#2C3E50',
                'young_modulus': [120, 200],
                'yield_strength': [1000, 2000],
                'density': [1500, 1700],
                'fracture_toughness': [15, 30],
                'thermal_conductivity': [1, 10],
                'thermal_expansion': [-1, 1],
                'max_service_temp': [120, 200],
                'price': [50, 200]
            },
            'Fibra de Vidrio/Poliéster': {
                'family': 'Compuestos',
                'color': '#7D3C98',
                'young_modulus': [15, 35],
                'yield_strength': [200, 500],
                'density': [1600, 2000],
                'fracture_toughness': [10, 25],
                'thermal_conductivity': [0.3, 0.8],
                'thermal_expansion': [15, 25],
                'max_service_temp': [80, 150],
                'price': [3, 10]
            },
            'Madera (Pino)': {
                'family': 'Naturales',
                'color': '#8B4513',
                'young_modulus': [8, 15],
                'yield_strength': [30, 80],
                'density': [400, 600],
                'fracture_toughness': [5, 15],
                'thermal_conductivity': [0.1, 0.2],
                'thermal_expansion': [3, 7],
                'max_service_temp': [100, 200],
                'price': [0.5, 2.0]
            }
        }
        
        return materials_data
    
    def get_dataframe(self):
        """Convierte la base de datos a DataFrame para facilitar el manejo"""
        data = []
        for material, props in self.materials.items():
            row = {'Material': material, 'Familia': props['family'], 'Color': props['color']}
            for prop_name, prop_key in self.properties.items():
                if prop_key in props:
                    row[f'{prop_name}_min'] = props[prop_key][0]
                    row[f'{prop_name}_max'] = props[prop_key][1]
            data.append(row)
        return pd.DataFrame(data)

class AshbyChartGenerator:
    """Clase para generar y manejar los gráficos de Ashby"""
    
    def __init__(self, database):
        self.database = database
        
    def create_ashby_chart(self, x_property, y_property, filtered_materials=None):
        """Crea un gráfico de Ashby interactivo"""
        
        if filtered_materials is None:
            materials_to_plot = self.database.materials
        else:
            materials_to_plot = filtered_materials
            
        fig = go.Figure()
        
        # Configurar los ejes como logarítmicos
        fig.update_layout(
            xaxis_type="log",
            yaxis_type="log",
            title=f"Gráfico de Ashby: {y_property} vs {x_property}",
            xaxis_title=x_property,
            yaxis_title=y_property,
            template="plotly_white",
            height=600,
            showlegend=True
        )
        
        # Obtener las claves de propiedades
        x_key = self.database.properties[x_property]
        y_key = self.database.properties[y_property]
        
        # Agregar elipses para cada material
        for material_name, material_data in materials_to_plot.items():
            if x_key in material_data and y_key in material_data:
                self._add_material_ellipse(
                    fig, material_name, material_data,
                    x_key, y_key, x_property, y_property
                )
        
        return fig
    
    def _add_material_ellipse(self, fig, material_name, material_data, x_key, y_key, x_label, y_label):
        """Agrega una elipse representando el rango de propiedades de un material"""
        
        x_min, x_max = material_data[x_key]
        y_min, y_max = material_data[y_key]
        
        # Calcular centro y radios de la elipse
        x_center = np.sqrt(x_min * x_max)  # Media geométrica
        y_center = np.sqrt(y_min * y_max)
        
        # Radios en escala logarítmica
        x_radius = np.log10(x_max) - np.log10(x_center)
        y_radius = np.log10(y_max) - np.log10(y_center)
        
        # Generar puntos de la elipse
        theta = np.linspace(0, 2*np.pi, 50)
        x_ellipse = x_center * (10 ** (x_radius * np.cos(theta)))
        y_ellipse = y_center * (10 ** (y_radius * np.sin(theta)))
        
        # Agregar la elipse como un scatter plot con línea
        fig.add_trace(go.Scatter(
            x=x_ellipse,
            y=y_ellipse,
            mode='lines',
            fill='toself',
            fillcolor=material_data['color'],
            opacity=0.3,
            line=dict(color=material_data['color'], width=2),
            name=material_name,
            hovertemplate=f"""
            <b>{material_name}</b><br>
            Familia: {material_data['family']}<br>
            {x_label}: {x_min:.2f} - {x_max:.2f}<br>
            {y_label}: {y_min:.2f} - {y_max:.2f}<br>
            <extra></extra>
            """
        ))

class MaterialFilter:
    """Clase para manejar el filtrado de materiales"""
    
    def __init__(self, database):
        self.database = database
        
    def apply_filters(self, filters):
        """Aplica filtros a la base de datos de materiales"""
        filtered_materials = {}
        
        for material_name, material_data in self.database.materials.items():
            include_material = True
            
            for property_name, filter_config in filters.items():
                if not filter_config['active']:
                    continue
                    
                prop_key = self.database.properties[property_name]
                if prop_key not in material_data:
                    continue
                    
                material_min, material_max = material_data[prop_key]
                filter_min, filter_max = filter_config['range']
                
                # Verificar si hay solapamiento entre el rango del material y el filtro
                if material_max < filter_min or material_min > filter_max:
                    include_material = False
                    break
            
            if include_material:
                filtered_materials[material_name] = material_data
                
        return filtered_materials

def main():
    """Función principal de la aplicación"""
    
    # Título principal
    st.markdown('<h1 class="main-header">🔬 AshbyChart Selector</h1>', unsafe_allow_html=True)
    st.markdown("### Aplicación Interactiva para la Selección de Materiales")
    
    # Inicializar base de datos
    if 'database' not in st.session_state:
        st.session_state.database = MaterialDatabase()
        st.session_state.chart_generator = AshbyChartGenerator(st.session_state.database)
        st.session_state.material_filter = MaterialFilter(st.session_state.database)
    
    # Sidebar para controles
    with st.sidebar:
        st.header("🎛️ Controles")
        
        # Selección de propiedades para los ejes
        st.subheader("Selección de Ejes")
        property_options = list(st.session_state.database.properties.keys())
        
        x_property = st.selectbox("Eje X:", property_options, index=2)  # Densidad por defecto
        y_property = st.selectbox("Eje Y:", property_options, index=0)  # Módulo de Young por defecto
        
        # Filtros de propiedades
        st.subheader("🔍 Filtros de Propiedades")
        
        filters = {}
        for prop_name, prop_key in st.session_state.database.properties.items():
            with st.expander(f"Filtrar {prop_name}"):
                # Obtener rango completo de la propiedad
                all_values = []
                for material_data in st.session_state.database.materials.values():
                    if prop_key in material_data:
                        all_values.extend(material_data[prop_key])
                
                if all_values:
                    min_val, max_val = min(all_values), max(all_values)
                    
                    active = st.checkbox(f"Activar filtro", key=f"filter_{prop_key}")
                    
                    if active:
                        range_values = st.slider(
                            f"Rango de {prop_name}",
                            min_value=float(min_val),
                            max_value=float(max_val),
                            value=(float(min_val), float(max_val)),
                            key=f"range_{prop_key}"
                        )
                    else:
                        range_values = (min_val, max_val)
                    
                    filters[prop_name] = {
                        'active': active,
                        'range': range_values
                    }
        
        # Botón para limpiar filtros
        if st.button("🗑️ Limpiar Filtros"):
            for key in st.session_state.keys():
                if key.startswith('filter_') or key.startswith('range_'):
                    del st.session_state[key]
            st.experimental_rerun()
    
    # Área principal dividida en columnas
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Aplicar filtros
        filtered_materials = st.session_state.material_filter.apply_filters(filters)
        
        # Generar gráfico
        fig = st.session_state.chart_generator.create_ashby_chart(
            x_property, y_property, filtered_materials
        )
        
        # Mostrar gráfico
        st.plotly_chart(fig, use_container_width=True)
        
        # Herramientas adicionales
        st.subheader("🛠️ Herramientas de Análisis")
        
        with st.expander("Índices de Rendimiento"):
            st.write("Próximamente: Herramienta para trazar líneas de índices de rendimiento")
            
            # Selector de índice común
            index_type = st.selectbox(
                "Tipo de índice:",
                ["E/ρ (Rigidez específica)", "σy/ρ (Resistencia específica)", "Personalizado"]
            )
            
            if index_type != "Personalizado":
                st.info(f"Índice seleccionado: {index_type}")
            else:
                custom_index = st.text_input("Fórmula del índice (ej: prop1/prop2):")
                if custom_index:
                    st.info(f"Índice personalizado: {custom_index}")
    
    with col2:
        st.markdown('<div class="results-panel">', unsafe_allow_html=True)
        st.subheader("📊 Resultados")
        
        # Mostrar estadísticas de filtrado
        total_materials = len(st.session_state.database.materials)
        filtered_count = len(filtered_materials)
        
        st.metric("Materiales Totales", total_materials)
        st.metric("Materiales Filtrados", filtered_count)
        st.metric("% Filtrado", f"{(filtered_count/total_materials)*100:.1f}%")
        
        # Lista de materiales filtrados
        if filtered_materials:
            st.subheader("Materiales Candidatos:")
            for material_name, material_data in filtered_materials.items():
                st.write(f"• **{material_name}** ({material_data['family']})")
        else:
            st.warning("No hay materiales que cumplan los criterios de filtrado.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Información adicional
    with st.expander("ℹ️ Información sobre la Aplicación"):
        st.markdown("""
        **AshbyChart Selector** es una aplicación interactiva para la selección de materiales
        basada en el método de Michael Ashby.
        
        **Características:**
        - Gráficos de propiedades interactivos (Ashby Charts)
        - Filtrado avanzado por propiedades
        - Base de datos de materiales representativa
        - Visualización por familias de materiales
        
        **Cómo usar:**
        1. Selecciona las propiedades para los ejes X e Y
        2. Aplica filtros según tus criterios de diseño
        3. Analiza los materiales candidatos en el gráfico
        4. Revisa los resultados en el panel lateral
        """)
    
    # Mostrar información técnica en el pie de página
    st.markdown("---")
    st.markdown(
        "<small>Desarrollado con Streamlit y Plotly | "
        "Base de datos con propiedades representativas de materiales comunes</small>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()