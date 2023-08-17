import folium
import geopandas as gpd
import json
import streamlit as st
from streamlit_folium import folium_static

Perimetro = gpd.read_file("ITUZAINGO\GeoJSON\Perimetro.geojson")
AreasDelParque = gpd.read_file("ITUZAINGO\GeoJSON\AreasDelParque.geojson")
Arroyo = gpd.read_file("ITUZAINGO\GeoJSON\Arroyo.geojson")
CallePrincipal = gpd.read_file("ITUZAINGO\GeoJSON\CallePrincipal.geojson")
CallesSecundarias = gpd.read_file("ITUZAINGO\GeoJSON\CallesSecundarias.geojson")
Empresas = gpd.read_file("ITUZAINGO\GeoJSON\Empresas.geojson")
Parcelas = gpd.read_file("ITUZAINGO\GeoJSON\Parcelas.geojson")
SuperficiesCubiertas = gpd.read_file("ITUZAINGO\GeoJSON\SuperficiesCubiertas.geojson")
Vegetacion = gpd.read_file("ITUZAINGO\GeoJSON\Vegetacion.geojson")

mapa = folium.Map(location=[-27.619921, -56.843410], zoom_start=14)

capas = [
    ("Perimetro", Perimetro, {'color': 'red', 'fillColor': 'transparent', 'weight': 2}),
    ("AreasDelParque", AreasDelParque, {'color': 'red', 'fillColor': 'transparent', 'weight': 2}),
    ("Arroyo", Arroyo, {'color': 'blue', 'fillColor': 'blue', 'weight': 0.5}),
    ("Parcelas", Parcelas, {'color': 'orange', 'fillColor': 'yellow', 'weight': 2}),
    ("CallePrincipal", CallePrincipal, {'color': 'red', 'fillColor': 'red', 'weight': 2}),
    ("CallesSecundarias", CallesSecundarias, {'color': 'red', 'fillColor': 'red', 'weight': 2}),
    ("SuperficiesCubiertas", SuperficiesCubiertas, {'color': 'blue', 'fillColor': 'blue', 'weight': 2}),
    ("Vegetacion", Vegetacion, {'color': 'green', 'fillColor': 'green', 'weight': 0.5})
]

folium_layers = {}
for nombre, capa, estilo in capas:
    folium_layer = folium.GeoJson(capa, name=nombre, style_function=lambda feature, style=estilo: style)
    folium_layer.add_to(mapa)
    folium_layers[nombre] = folium_layer

with open('ITUZAINGO\GeoJSON\Empresas.geojson', 'r') as geojson_file:
    data = json.load(geojson_file)
    empresas_features = data['features']

#marker_cluster = MarkerCluster().add_to(mapa)

def popup_content(properties):
    popup_html = "<ul>"
    for key, value in properties.items():
        if value is not None and key != 'id':
            popup_html += f"<li><b>{key}:</b> {value}</li>"
    popup_html += "</ul>"
    return popup_html

for feature in empresas_features:
    nombre = feature['properties']['EMPRESA']
    estilo = {'color': 'red', 'fillColor': 'transparent', 'weight': 2}
    geojson_layer = folium.GeoJson(
        feature,
        name=nombre,
        style_function=lambda x: estilo,
        tooltip=folium.GeoJsonTooltip(fields=['EMPRESA'], labels=True),
        popup=folium.Popup(parse_html=True, max_width=300).add_child(folium.Html(popup_content(feature['properties']), script=True))
    )
    geojson_layer.add_to(mapa)

# Agregar control de capas al mapa



def main():
    st.title("Mapa Parque Industrial de Ituzaingo")

    folium_static(mapa)
    
    
    st.sidebar.subheader("Colores de las capas")
    for nombre, _, estilo in capas:
        color_hex = estilo['color']
        color_html = f"<div style='display: flex; align-items: center;'><div style='width: 20px; height: 10px; background-color: {color_hex}; margin-right: 5px;'></div> {nombre}</div>"
        st.sidebar.markdown(color_html, unsafe_allow_html=True)

    st.header("Información de Empresas")

    selected_marker = st.selectbox("Selecciona una empresa:", [feature['properties']['EMPRESA'] for feature in empresas_features])

    selected_feature = next(feature for feature in empresas_features if feature['properties']['EMPRESA'] == selected_marker)

    st.table(selected_feature['properties'])

if __name__ == "__main__":
    main()