import folium
import geopandas as gpd
import json
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd


def main():

    Perimetro = gpd.read_file("./SANTA ROSA/GeoJSON/Perimetro.geojson")
    AreasDelParque = gpd.read_file("./SANTA ROSA/GeoJSON/AreasDelParque.geojson")
    CallePrincipal = gpd.read_file("./SANTA ROSA/GeoJSON/CallePrincipal.geojson")
    Ripio = gpd.read_file("./SANTA ROSA/GeoJSON/Ripio.geojson")
    Madera = gpd.read_file("./SANTA ROSA/GeoJSON/Madera.geojson")
    Parcelas = gpd.read_file("./SANTA ROSA/GeoJSON/Parcelas.geojson")
    SuperficieCubierta = gpd.read_file("./SANTA ROSA/GeoJSON/SuperficieCubierta.geojson")
    CirculacionPeatonal = gpd.read_file("./SANTA ROSA/GeoJSON/CirculacionPeatonal.geojson")
    DesaguePluvialBDT1 = gpd.read_file("./SANTA ROSA/GeoJSON/DesaguePluvialBDT1.geojson")
    DesaguePluvialBDT2 = gpd.read_file("./SANTA ROSA/GeoJSON/DesaguePluvialBDT2.geojson")
    DesaguePluvialCañerias1 = gpd.read_file("./SANTA ROSA/GeoJSON/DesaguePluvialCañerias1.geojson")
    DesaguePluvialCañerias2 = gpd.read_file("./SANTA ROSA/GeoJSON/DesaguePluvialCañerias2.geojson")
    RedDeAguaCañerias = gpd.read_file("./SANTA ROSA/GeoJSON/RedDeAguaCañerias.geojson")
    RedDeAguaHidrante = gpd.read_file("./SANTA ROSA/GeoJSON/RedDeAguaHidrante.geojson")
    RedDeAguaTanques = gpd.read_file("./SANTA ROSA/GeoJSON/RedDeAguaTanques.geojson")
    RedDeAguaVE = gpd.read_file("./SANTA ROSA/GeoJSON/RedDeAguaVE.geojson")
    Residuos = gpd.read_file("./SANTA ROSA/GeoJSON/Residuos.geojson")
    TendidoElectricoCircuito1 = gpd.read_file("./SANTA ROSA/GeoJSON/TendidoElectricoCircuitoEtapa1.geojson")
    TendidoElectricoCircuito2 = gpd.read_file("./SANTA ROSA/GeoJSON/TendidoElectricoCircuitoEtapa2.geojson")
    TendidoElectricoCircuito3 = gpd.read_file("./SANTA ROSA/GeoJSON/TendidoElectricoCircuitoEtapa3.geojson")
    Vegetacion = gpd.read_file("./SANTA ROSA/GeoJSON/Vegetacion.geojson")

    st.title("Mapa Parque Industrial de Santa Rosa")

    mapa = folium.Map(location=[-28.235098667253943, -58.066266439685712], zoom_start=16)

    capas = [
        ("Perimetro", Perimetro, {'color': 'red', 'fillColor': 'transparent', 'weight': 2}),
        ("AreasDelParque", AreasDelParque, {'color': 'red', 'fillColor': 'transparent', 'weight': 2}),
        ("CallePrincipal", CallePrincipal, {'color': 'red', 'fillColor': 'black', 'weight': 2}),
        ("Ripio", Ripio, {'color': 'brown', 'fillColor': 'brown', 'weight': 2}),
        ("Madera", Madera, {'color': 'brown', 'fillColor': 'brown', 'weight': 0.5}),
        ("Parcelas", Parcelas, {'color': 'orange', 'fillColor': 'yellow', 'weight': 2}),
        ("SuperficieCubierta", SuperficieCubierta, {'color': 'blue', 'fillColor': 'blue', 'weight': 2}),
        ("CirculacionPeatonal", CirculacionPeatonal, {'color': 'green', 'fillColor': 'green', 'weight': 0.5}),
        ("DesaguePluvialBDT1", DesaguePluvialBDT1, {'color': 'black', 'fillColor': 'purple', 'weight': 2}),
        ("DesaguePluvialBDT2", DesaguePluvialBDT2, {'color': 'black', 'fillColor': 'purple', 'weight': 2}),
        ("DesaguePluvialCañerias1", DesaguePluvialCañerias1, {'color': 'black', 'fillColor': 'purple', 'weight': 2}),
        ("DesaguePluvialCañerias2", DesaguePluvialCañerias2, {'color': 'black', 'fillColor': 'purple', 'weight': 2}),
        ("RedDeAguaCañerias", RedDeAguaCañerias, {'color': 'cyan', 'fillColor': 'blue', 'weight': 2}),
        ("RedDeAguaHidrante", RedDeAguaHidrante, {'color': 'cyan', 'fillColor': 'blue', 'weight': 2}),
        ("RedDeAguaTanques", RedDeAguaTanques, {'color': 'cyan', 'fillColor': 'blue', 'weight': 2}),
        ("RedDeAguaVE", RedDeAguaVE, {'color': 'cyan', 'fillColor': 'blue', 'weight': 2}),
        ("Residuos", Residuos, {'color': 'orange', 'fillColor': 'green', 'weight': 2}),
        ("TendidoElectricoCircuito1", TendidoElectricoCircuito1, {'color': 'orange', 'fillColor': 'transparent', 'weight': 2}),
        ("TendidoElectricoCircuito2", TendidoElectricoCircuito2, {'color': 'orange', 'fillColor': 'transparent', 'weight': 2}),
        ("TendidoElectricoCircuito3", TendidoElectricoCircuito3, {'color': 'orange', 'fillColor': 'transparent', 'weight': 2}),
        ("Vegetacion", Vegetacion, {'color': 'green', 'fillColor': 'green', 'weight': 0.5}),
    ]

    with open('./SANTA ROSA/GeoJSON/Empresas.geojson', 'r') as geojson_file:
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
    opciones = [
    "Perimetro",
    #"AreasDelParque",
    "CallePrincipal",
    "Ripio",
    "Parcelas",
    "SuperficieCubierta",
    "CirculacionPeatonal",
    "Empresas",
    "Madera",
    "Residuos"
    #"Vegetacion",

    ]
    DesaguePluvial = ["DesaguePluvialBDT1",
    "DesaguePluvialBDT2",
    "DesaguePluvialCañerias1",
    "DesaguePluvialCañerias2"]
    TendidoElectrico = ["TendidoElectricoCircuito1",
    "TendidoElectricoCircuito2",
    "TendidoElectricoCircuito3"]
    RedDeAgua = ["RedDeAguaCañerias",
    "RedDeAguaHidrante",
    "RedDeAguaTanques",
    "RedDeAguaVE"]

    elementos_seleccionados = []



    elementos_predeterminados = ["Perimetro", "CallePrincipal", "Parcelas", "Ripio", "SuperficieCubierta", "CirculacionPeatonal", "Empresas"]

    # Mostrar casillas de selección para cada elemento
    for elemento in opciones:
        if elemento in elementos_predeterminados:
            seleccionado = st.sidebar.checkbox(elemento, value=True)
        else:
            seleccionado = st.sidebar.checkbox(elemento, value=False)
        if seleccionado:
           elementos_seleccionados.append(elemento)
        elif elemento in elementos_seleccionados:
            elementos_seleccionados.remove(elemento)

    DesagueBarra = st.sidebar.checkbox("Desague Pluvial")
    if DesagueBarra:
        for elemento in DesaguePluvial:
            seleccionado = st.sidebar.checkbox(elemento)

            if seleccionado:
                elementos_seleccionados.append(elemento)
            elif elemento in elementos_seleccionados:
                elementos_seleccionados.remove(elemento)

    TendidoBarra = st.sidebar.checkbox("Tendido Electrico")
    if TendidoBarra:
        for elemento in TendidoElectrico:
            seleccionado = st.sidebar.checkbox(elemento)

            if seleccionado:
              elementos_seleccionados.append(elemento)
            elif elemento in elementos_seleccionados:
                elementos_seleccionados.remove(elemento)
    
    AguaBarra = st.sidebar.checkbox("Red de Agua")
    if AguaBarra:
        for elemento in RedDeAgua:
            seleccionado = st.sidebar.checkbox(elemento)

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
            
            # Verificar si hay geometría antes de continuar
            if feature['geometry'] is not None:
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
    empresas_nombres_ordenadas = sorted([nombre for nombre in empresas_nombres if nombre is not None])

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


if __name__ == "__main__":
    main()
