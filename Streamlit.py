import folium
import geopandas as gpd
import json
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd

def Ituzaingo():

    Perimetro = gpd.read_file("./ITUZAINGO/GeoJSON/Perimetro.geojson")
    AreasDelParque = gpd.read_file("./ITUZAINGO/GeoJSON/AreasDelParque.geojson")
    Arroyo = gpd.read_file("./ITUZAINGO/GeoJSON/Arroyo.geojson")
    CallePrincipal = gpd.read_file("./ITUZAINGO/GeoJSON/CallePrincipal.geojson")
    CallesSecundarias = gpd.read_file("./ITUZAINGO/GeoJSON/CallesSecundarias.geojson")
    Empresas = gpd.read_file("./ITUZAINGO/GeoJSON/Empresas.geojson")
    Parcelas = gpd.read_file("./ITUZAINGO/GeoJSON/Parcelas.geojson")
    SuperficiesCubiertas = gpd.read_file("./ITUZAINGO/GeoJSON/SuperficiesCubiertas.geojson")
    Vegetacion = gpd.read_file("./ITUZAINGO/GeoJSON/Vegetacion.geojson")


    st.title("Mapa Parque Industrial de Ituzaingo")

    mapa = folium.Map(location=[-27.619921, -56.843410], zoom_start=14)

    capas = [
        ("Perimetro", Perimetro, {'color': 'red', 'fillColor': 'transparent', 'weight': 2}),
        ("AreasDelParque", AreasDelParque, {'color': 'red', 'fillColor': 'transparent', 'weight': 2}),
        ("Arroyo", Arroyo, {'color': 'blue', 'fillColor': 'blue', 'weight': 0.5}),
        ("Parcelas", Parcelas, {'color': 'orange', 'fillColor': 'yellow', 'weight': 2}),
        ("CallePrincipal", CallePrincipal, {'color': 'red', 'fillColor': 'black', 'weight': 2}),
        ("CallesSecundarias", CallesSecundarias, {'color': 'red', 'fillColor': 'black', 'weight': 2}),
        ("SuperficiesCubiertas", SuperficiesCubiertas, {'color': 'blue', 'fillColor': 'blue', 'weight': 2}),
        ("Vegetacion", Vegetacion, {'color': 'green', 'fillColor': 'green', 'weight': 0.5})
    ]

    with open('./ITUZAINGO/GeoJSON/Empresas.geojson', 'r') as geojson_file:
        data = json.load(geojson_file)
        empresas_features = data['features']


    def popup_content(properties):
        popup_html = "<ul>"
        for key, value in properties.items():
            if value is not None and key != 'id':
                popup_html += f"<li><b>{key}:</b> {value}</li>"
        popup_html += "</ul>"
        return popup_html





    # Crear una lista de elementos para el checklist
    opciones = ["Perimetro", "Arroyo", "Parcelas", "CallePrincipal", "CallesSecundarias", "SuperficiesCubiertas", "Vegetacion", "Empresas"]
    elementos_seleccionados = []

    # Mostrar casillas de selección para cada elemento
    for elemento in opciones:
        seleccionado = st.sidebar.checkbox(elemento, value=True)
        if seleccionado:
            elementos_seleccionados.append(elemento)
        elif elemento in elementos_seleccionados:
            elementos_seleccionados.remove(elemento)
    
    folium_layers = {}
    for nombre, capa, estilo in capas:
        if nombre in elementos_seleccionados:
            folium_layer = folium.GeoJson(capa, name=nombre, style_function=lambda feature, style=estilo: style)
            folium_layer.add_to(mapa)
            folium_layers[nombre] = folium_layer
        else:
            continue


    if "Empresas" in elementos_seleccionados:
        for feature in empresas_features:
            nombre = feature['properties']['EMPRESA']
            estilo = {'color': 'red', 'fillColor': 'transparent', 'weight': 2}
            
            # Crear contenido HTML del popup con un botón
            popup_content = f"Empresa: {nombre}"
            
            
            geojson_layer = folium.GeoJson(
                feature,
                name=nombre,
                style_function=lambda x: estilo,
                tooltip=folium.GeoJsonTooltip(fields=['EMPRESA'], labels=True),
                popup=folium.Popup(html=popup_content, parse_html=True, max_width=300)
            )
            geojson_layer.add_to(mapa)



    empresas_nombres = [feature['properties']['EMPRESA'] for feature in empresas_features]
    empresas_nombres_ordenadas = sorted(empresas_nombres)

    selected_marker = st.selectbox("Selecciona una empresa:", empresas_nombres_ordenadas)

    selected_feature = next(feature for feature in empresas_features if feature['properties']['EMPRESA'] == selected_marker)

    # Obtener la ubicación de la empresa seleccionada
    latitude = selected_feature['geometry']['coordinates'][1]
    longitude = selected_feature['geometry']['coordinates'][0]

    # Cambiar el color del pin según la empresa seleccionada
    icon = folium.Icon(color="red")

    # Agregar el marcador al mapa con el ícono personalizado
    marker = folium.Marker(location=[latitude, longitude], popup="Empresa seleccionada: " + selected_marker, icon=icon)
    marker.add_to(mapa)

    folium_static(mapa)

    st.header("Información de la Empresa")

    df = pd.DataFrame(selected_feature)
    df2 = df["properties"]

    df2.name = "Datos"
    df2.dropna(inplace=True)
    st.table(df2)

def Mercedes():

    Perimetro = gpd.read_file("./MERCEDES/GeoJSON/Perimetro.geojson")
    AreasDelParque = gpd.read_file("./MERCEDES/GeoJSON/AreasDelParque.geojson")
    CallePrincipal = gpd.read_file("./MERCEDES/GeoJSON/CallePrincipal.geojson")
    CallesSecundarias = gpd.read_file("./MERCEDES/GeoJSON/CallesSecundarias.geojson")
    #Empresas = gpd.read_file("./MERCEDES/GeoJSON/Empresas.geojson")
    Parcela = gpd.read_file("./MERCEDES/GeoJSON/Parcela.geojson")
    SuperficieCubierta = gpd.read_file("./MERCEDES/GeoJSON/SuperficieCubierta.geojson")
    CirculacionPeatonal = gpd.read_file("./MERCEDES/GeoJSON/CirculacionPeatonal.geojson")

    st.title("Mapa Parque Industrial de Mercedes")

    mapa = folium.Map(location=[-29.157215175081003, -58.107231912495159], zoom_start=16)

    capas = [
        ("Perimetro", Perimetro, {'color': 'red', 'fillColor': 'transparent', 'weight': 2}),
        #("AreasDelParque", AreasDelParque, {'color': 'red', 'fillColor': 'transparent', 'weight': 2}),
        ("Parcela", Parcela, {'color': 'orange', 'fillColor': 'yellow', 'weight': 2}),
        ("CallePrincipal", CallePrincipal, {'color': 'red', 'fillColor': 'black', 'weight': 2}),
        ("CallesSecundarias", CallesSecundarias, {'color': 'red', 'fillColor': 'black', 'weight': 2}),
        ("SuperficieCubierta", SuperficieCubierta, {'color': 'blue', 'fillColor': 'blue', 'weight': 2}),
        ("CirculacionPeatonal", CirculacionPeatonal, {'color': 'green', 'fillColor': 'green', 'weight': 0.5})
    ]

    with open('./MERCEDES/GeoJSON/Empresas.geojson', 'r') as geojson_file:
        data = json.load(geojson_file)
        empresas_features = data['features']


    def popup_content(properties):
        popup_html = "<ul>"
        for key, value in properties.items():
            if value is not None and key != 'id':
                popup_html += f"<li><b>{key}:</b> {value}</li>"
        popup_html += "</ul>"
        return popup_html





    # Crear una lista de elementos para el checklist
    opciones = ["Perimetro", "Parcela", "CallePrincipal", "CallesSecundarias", "SuperficieCubierta", "CirculacionPeatonal", "Empresas"]
    elementos_seleccionados = []

    # Mostrar casillas de selección para cada elemento
    for elemento in opciones:
        seleccionado = st.sidebar.checkbox(elemento, value=True)
        if seleccionado:
            elementos_seleccionados.append(elemento)
        elif elemento in elementos_seleccionados:
            elementos_seleccionados.remove(elemento)
    
    folium_layers = {}
    for nombre, capa, estilo in capas:
        if nombre in elementos_seleccionados:
            folium_layer = folium.GeoJson(capa, name=nombre, style_function=lambda feature, style=estilo: style)
            folium_layer.add_to(mapa)
            folium_layers[nombre] = folium_layer
        else:
            continue


    if "Empresas" in elementos_seleccionados:
        for feature in empresas_features:
            nombre = feature['properties']['empresa']
            estilo = {'color': 'red', 'fillColor': 'transparent', 'weight': 2}
            
            # Verificar si hay geometría antes de continuar
            if feature['geometry'] is not None:
                popup_content = f"Empresa: {nombre}"
                
                geojson_layer = folium.GeoJson(
                    feature,
                    name=nombre,
                    style_function=lambda x: estilo,
                    tooltip=folium.GeoJsonTooltip(fields=['empresa'], labels=True),
                    popup=folium.Popup(html=popup_content, parse_html=True, max_width=300)
                )
                geojson_layer.add_to(mapa)



    empresas_nombres = [feature['properties']['empresa'] for feature in empresas_features]
    empresas_nombres_ordenadas = sorted(empresas_nombres)

    selected_marker = st.selectbox("Selecciona una empresa:", empresas_nombres_ordenadas)

    selected_feature = next(feature for feature in empresas_features if feature['properties']['empresa'] == selected_marker)

    # Obtener la ubicación de la empresa seleccionada
    latitude = selected_feature['geometry']['coordinates'][1]
    longitude = selected_feature['geometry']['coordinates'][0]

    # Cambiar el color del pin según la empresa seleccionada
    icon = folium.Icon(color="red")

    # Agregar el marcador al mapa con el ícono personalizado
    marker = folium.Marker(location=[latitude, longitude], popup="Empresa seleccionada: " + selected_marker, icon=icon)
    marker.add_to(mapa)

    folium_static(mapa)

    st.header("Información de la Empresa")

    df = pd.DataFrame(selected_feature)
    df2 = df["properties"]

    df2.name = "Datos"
    df2.dropna(inplace=True)
    st.table(df2)

def main():
    # La clave de acceso única
    access_key = "subseindustria2023"
    user_input = st.text_input("Ingrese la clave de acceso:", type="password")
    if user_input == access_key:
        seleccion = st.radio("Selecciona un parque:", ("Ituzaingó", "Mercedes"))
        if seleccion == "Ituzaingó":
            Ituzaingo()
        elif seleccion == "Mercedes":
            Mercedes()

if __name__ == "__main__":
    main()