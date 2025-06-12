import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
import math

class PerformanceIndexTool:
    """Herramienta para índices de rendimiento en gráficos de Ashby"""
    
    def __init__(self):
        self.common_indices = {
            'E/ρ (Rigidez específica)': {'numerator': 'young_modulus', 'denominator': 'density', 'slope': 1},
            'E^(1/2)/ρ (Rigidez específica optimizada)': {'numerator': 'young_modulus', 'denominator': 'density', 'slope': 0.5},
            'σy/ρ (Resistencia específica)': {'numerator': 'yield_strength', 'denominator': 'density', 'slope': 1},
            'E/ρ² (Placas en flexión)': {'numerator': 'young_modulus', 'denominator': 'density', 'slope': 2},
            'E^(1/3)/ρ (Barras en compresión)': {'numerator': 'young_modulus', 'denominator': 'density', 'slope': 1/3},
            'KIC/ρ (Tenacidad específica)': {'numerator': 'fracture_toughness', 'denominator': 'density', 'slope': 1}
        }
    
    def add_performance_line(self, fig, x_property, y_property, index_config, line_position=0.5):
        """Agrega una línea de índice de rendimiento al gráfico"""
        
        # Obtener rango del gráfico
        x_range = fig.layout.xaxis.range if fig.layout.xaxis.range else [1, 1000]
        y_range = fig.layout.yaxis.range if fig.layout.yaxis.range else [1, 1000]
        
        # Convertir de log a valores lineales
        x_min, x_max = 10**x_range[0], 10**x_range[1]
        y_min, y_max = 10**y_range[0], 10**y_range[1]
        
        # Calcular pendiente de la línea
        slope = index_config['slope']
        
        # Generar puntos de la línea
        x_line = np.logspace(np.log10(x_min), np.log10(x_max), 100)
        
        # Calcular intercepto basado en la posición deseada
        x_ref = x_min * (x_max/x_min)**line_position
        y_ref = y_min * (y_max/y_min)**line_position
        
        # y = C * x^slope, donde C se calcula para que pase por (x_ref, y_ref)
        C = y_ref / (x_ref**slope)
        y_line = C * (x_line**slope)
        
        # Agregar línea al gráfico
        fig.add_trace(go.Scatter(
            x=x_line,
            y=y_line,
            mode='lines',
            line=dict(color='red', width=3, dash='dash'),
            name=f'Línea de Rendimiento',
            hovertemplate=f'Índice: C·x^{slope}<extra></extra>'
        ))
        
        return fig

class GraphicalSelection:
    """Herramienta para selección gráfica directa"""
    
    def __init__(self):
        self.selection_mode = 'box'  # 'box', 'lasso', 'circle'
    
    def create_selection_tools(self):
        """Crea herramientas de selección gráfica"""
        st.subheader("🎯 Selección Gráfica")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selection_mode = st.selectbox(
                "Modo de selección:",
                ['Caja rectangular', 'Lazo libre', 'Círculo']
            )
        
        with col2:
            apply_selection = st.button("Aplicar Selección")
        
        return selection_mode, apply_selection
    
    def filter_by_selection(self, materials_data, selection_bounds, x_property, y_property):
        """Filtra materiales basado en selección gráfica"""
        # Esta función se implementaría con callbacks de Plotly
        # para capturar las coordenadas de selección del usuario
        pass

class MaterialAnalyzer:
    """Herramientas avanzadas de análisis de materiales"""
    
    def __init__(self, database):
        self.database = database
    
    def calculate_material_indices(self, materials_dict):
        """Calcula índices de rendimiento para los materiales"""
        indices_data = []
        
        for material_name, material_props in materials_dict.items():
            row = {'Material': material_name, 'Familia': material_props['family']}
            
            # Calcular índices comunes usando valores medios
            if 'young_modulus' in material_props and 'density' in material_props:
                E_avg = np.mean(material_props['young_modulus'])
                rho_avg = np.mean(material_props['density'])
                
                row['E/ρ'] = E_avg / rho_avg
                row['E^(1/2)/ρ'] = np.sqrt(E_avg) / rho_avg
                row['E^(1/3)/ρ'] = np.power(E_avg, 1/3) / rho_avg
            
            if 'yield_strength' in material_props and 'density' in material_props:
                sigma_avg = np.mean(material_props['yield_strength'])
                rho_avg = np.mean(material_props['density'])
                row['σy/ρ'] = sigma_avg / rho_avg
            
            if 'fracture_toughness' in material_props and 'density' in material_props:
                K_avg = np.mean(material_props['fracture_toughness'])
                rho_avg = np.mean(material_props['density'])
                row['KIC/ρ'] = K_avg / rho_avg
            
            indices_data.append(row)
        
        return pd.DataFrame(indices_data)
    
    def create_pareto_frontier(self, fig, materials_dict, x_property, y_property):
        """Agrega frontera de Pareto al gráfico"""
        
        # Extraer puntos para análisis de Pareto
        points = []
        materials = []
        
        x_key = self.database.properties[x_property]
        y_key = self.database.properties[y_property]
        
        for material_name, material_data in materials_dict.items():
            if x_key in material_data and y_key in material_data:
                # Usar valores máximos para Pareto (optimista)
                x_val = material_data[x_key][1]  # max
                y_val = material_data[y_key][1]  # max
                points.append([x_val, y_val])
                materials.append(material_name)
        
        if len(points) < 3:
            return fig
        
        points = np.array(points)
        
        # Calcular envolvente convexa (aproximación a frontera de Pareto)
        try:
            hull = ConvexHull(np.log10(points))  # En escala log
            hull_points = points[hull.vertices]
            
            # Agregar frontera de Pareto
            fig.add_trace(go.Scatter(
                x=hull_points[:, 0],
                y=hull_points[:, 1],
                mode='lines',
                line=dict(color='purple', width=2, dash='dot'),
                name='Frontera de Pareto',
                hovertemplate='Frontera de materiales óptimos<extra></extra>'
            ))
        
        except Exception as e:
            st.warning(f"No se pudo calcular la frontera de Pareto: {e}")
        
        return fig

class ExportTools:
    """Herramientas para exportar resultados"""
    
    def __init__(self):
        pass
    
    def create_export_panel(self):
        """Crea panel de herramientas de exportación"""
        st.subheader("💾 Exportar Resultados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Exportar Gráfico"):
                st.info("Funcionalidad en desarrollo")
        
        with col2:
            if st.button("📋 Exportar Lista"):
                st.info("Funcionalidad en desarrollo")
        
        with col3:
            if st.button("📄 Generar Reporte"):
                st.info("Funcionalidad en desarrollo")
    
    def export_materials_list(self, materials_dict, filename="materiales_seleccionados.csv"):
        """Exporta lista de materiales a CSV"""
        data = []
        for material_name, material_props in materials_dict.items():
            row = {
                'Material': material_name,
                'Familia': material_props['family']
            }
            
            # Agregar propiedades
            for prop_display, prop_key in self.database.properties.items():
                if prop_key in material_props:
                    min_val, max_val = material_props[prop_key]
                    row[f'{prop_display} (min)'] = min_val
                    row[f'{prop_display} (max)'] = max_val
            
            data.append(row)
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False)
    
    def generate_selection_report(self, materials_dict, filters_applied):
        """Genera reporte de selección de materiales"""
        
        report = f"""
# Reporte de Selección de Materiales

## Resumen
- **Materiales analizados**: {len(materials_dict)}
- **Fecha**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

## Filtros Aplicados
"""
        
        for filter_name, filter_config in filters_applied.items():
            if filter_config['active']:
                min_val, max_val = filter_config['range']
                report += f"- **{filter_name}**: {min_val:.2f} - {max_val:.2f}\n"
        
        report += "\n## Materiales Candidatos\n"
        
        for material_name, material_props in materials_dict.items():
            report += f"### {material_name}\n"
            report += f"- **Familia**: {material_props['family']}\n"
            report += "\n"
        
        return report

class AdvancedVisualization:
    """Herramientas de visualización avanzada"""
    
    def __init__(self, database):
        self.database = database
    
    def create_3d_plot(self, x_property, y_property, z_property, materials_dict):
        """Crea gráfico 3D de propiedades"""
        
        fig = go.Figure()
        
        x_key = self.database.properties[x_property]
        y_key = self.database.properties[y_property]
        z_key = self.database.properties[z_property]
        
        for material_name, material_data in materials_dict.items():
            if all(key in material_data for key in [x_key, y_key, z_key]):
                # Usar valores medios para el punto central
                x_val = np.mean(material_data[x_key])
                y_val = np.mean(material_data[y_key])
                z_val = np.mean(material_data[z_key])
                
                fig.add_trace(go.Scatter3d(
                    x=[x_val],
                    y=[y_val],
                    z=[z_val],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=material_data['color'],
                        opacity=0.8
                    ),
                    name=material_name,
                    hovertemplate=f"""
                    <b>{material_name}</b><br>
                    {x_property}: {x_val:.2f}<br>
                    {y_property}: {y_val:.2f}<br>
                    {z_property}: {z_val:.2f}<br>
                    <extra></extra>
                    """
                ))
        
        fig.update_layout(
            scene=dict(
                xaxis_title=x_property,
                yaxis_title=y_property,
                zaxis_title=z_property,
                xaxis_type="log",
                yaxis_type="log",
                zaxis_type="log"
            ),
            title=f"Gráfico 3D: {x_property} vs {y_property} vs {z_property}",
            height=600
        )
        
        return fig
    
    def create_radar_chart(self, materials_list, properties_list):
        """Crea gráfico de radar para comparar materiales"""
        
        fig = go.Figure()
        
        for material_name in materials_list:
            if material_name in self.database.materials:
                material_data = self.database.materials[material_name]
                
                values = []
                categories = []
                
                for prop_display in properties_list:
                    prop_key = self.database.properties[prop_display]
                    if prop_key in material_data:
                        # Normalizar valor (usar media del rango)
                        val = np.mean(material_data[prop_key])
                        values.append(val)
                        categories.append(prop_display)
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=material_name,
                    line_color=material_data['color']
                ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True)
            ),
            showlegend=True,
            title="Comparación de Materiales - Gráfico Radar"
        )
        
        return fig

# Función para integrar funcionalidades avanzadas en la aplicación principal
def add_advanced_features_to_app(database, chart_generator, filtered_materials):
    """Agrega funcionalidades avanzadas a la aplicación principal"""
    
    st.header("🔬 Herramientas Avanzadas")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Índices de Rendimiento", "Análisis 3D", "Comparación Radar", "Exportación"])
    
    with tab1:
        st.subheader("📈 Índices de Rendimiento")
        performance_tool = PerformanceIndexTool()
        
        # Selector de índice
        index_options = list(performance_tool.common_indices.keys())
        selected_index = st.selectbox("Seleccionar índice:", index_options)
        
        # Tabla de índices calculados
        analyzer = MaterialAnalyzer(database)
        indices_df = analyzer.calculate_material_indices(filtered_materials)
        
        if not indices_df.empty:
            st.dataframe(indices_df, use_container_width=True)
            
            # Gráfico de barras de índices
            if selected_index in indices_df.columns:
                fig_bar = px.bar(
                    indices_df.sort_values(selected_index, ascending=False),
                    x='Material',
                    y=selected_index,
                    color='Familia',
                    title=f"Ranking de Materiales por {selected_index}"
                )
                fig_bar.update_xaxes(tickangle=45)
                st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.subheader("🎲 Visualización 3D")
        viz_tool = AdvancedVisualization(database)
        
        property_options = list(database.properties.keys())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            x_prop_3d = st.selectbox("Eje X (3D):", property_options, key="3d_x")
        with col2:
            y_prop_3d = st.selectbox("Eje Y (3D):", property_options, key="3d_y", index=1)
        with col3:
            z_prop_3d = st.selectbox("Eje Z (3D):", property_options, key="3d_z", index=2)
        
        if st.button("Generar Gráfico 3D"):
            fig_3d = viz_tool.create_3d_plot(x_prop_3d, y_prop_3d, z_prop_3d, filtered_materials)
            st.plotly_chart(fig_3d, use_container_width=True)
    
    with tab3:
        st.subheader("🕸️ Gráfico de Radar")
        viz_tool = AdvancedVisualization(database)
        
        # Selector de materiales para comparar
        available_materials = list(filtered_materials.keys())
        selected_materials = st.multiselect(
            "Seleccionar materiales para comparar:",
            available_materials,
            default=available_materials[:3] if len(available_materials) >= 3 else available_materials
        )
        
        # Selector de propiedades para el radar
        property_options = list(database.properties.keys())
        selected_properties = st.multiselect(
            "Seleccionar propiedades:",
            property_options,
            default=property_options[:5]
        )
        
        if selected_materials and selected_properties:
            fig_radar = viz_tool.create_radar_chart(selected_materials, selected_properties)
            st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab4:
        st.subheader("💾 Exportación y Reportes")
        export_tool = ExportTools()
        export_tool.create_export_panel()
        
        # Mostrar datos para descarga
        if filtered_materials:
            # Crear DataFrame para descarga
            export_data = []
            for material_name, material_props in filtered_materials.items():
                row = {'Material': material_name, 'Familia': material_props['family']}
                for prop_display, prop_key in database.properties.items():
                    if prop_key in material_props:
                        min_val, max_val = material_props[prop_key]
                        row[f'{prop_display} (min)'] = min_val
                        row[f'{prop_display} (max)'] = max_val
                export_data.append(row)
            
            df_export = pd.DataFrame(export_data)
            
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="materiales_seleccionados.csv",
                mime="text/csv"
            )