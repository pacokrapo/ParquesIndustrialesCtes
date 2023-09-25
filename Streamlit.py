import folium
import geopandas as gpd
import json
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
#-*- coding: utf-8 -*-

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
        ("SuperficiesCubiertas", SuperficiesCubiertas, {'color': 'gray', 'fillColor': 'blue', 'weight': 2}),
        ("Vegetacion", Vegetacion, {'color': 'green', 'fillColor': 'green', 'weight': 0.5})
    ]

    with open('./ITUZAINGO/GeoJSON/Empresas.geojson', 'r', encoding="utf-8") as geojson_file:
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
            latitud = feature['geometry']['coordinates'][1]
            longitud = feature['geometry']['coordinates'][0]
            
            # Verificar si hay geometría antes de continuar
            if feature['geometry'] is not None:
                popup_content = f"Empresa: {nombre}"

                icon = folium.Icon(icon="glyphicon-home", color="green")  # Cambia el icono y color según tu preferencia
        
                marker = folium.Marker(
                    location=[latitud, longitud],
                    icon=icon,
                    popup=folium.Popup(html=popup_content, parse_html=True, max_width=300)
                )
                
                marker.add_to(mapa)



    empresas_nombres = [feature['properties']['EMPRESA'] for feature in empresas_features]

    empresas_nombres_unicos = list(set(empresas_nombres))

    empresas_nombres_unicos = sorted(empresas_nombres_unicos)

    empresas_nombres_unicos = [empresa for empresa in empresas_nombres_unicos if empresa is not None]

    selected_marker = st.selectbox("Selecciona una empresa:", empresas_nombres_unicos)

    selected_features = [feature for feature in empresas_features if feature['properties']['EMPRESA'] == selected_marker]

    for feature in selected_features:
        latitude = feature['geometry']['coordinates'][1]
        longitude = feature['geometry']['coordinates'][0]
        icon = folium.Icon(color="red")
        marker = folium.Marker(location=[latitude, longitude], popup="Empresa seleccionada: " + feature['properties']['EMPRESA'], icon=icon)
        marker.add_to(mapa)

    folium_static(mapa)

    st.header("Información de la Empresa")

    data_dict = {}

    # Llenar el diccionario con los datos de cada lote
    for index, lote in enumerate(selected_features):
        properties = lote['properties']
        for key, value in properties.items():
            if key not in data_dict:
                data_dict[key] = [None] * len(selected_features)
            data_dict[key][index] = value

    # Crear el DataFrame a partir del diccionario
    df = pd.DataFrame(data_dict)

    df.dropna(axis=1, how='all', inplace=True)

    df = df.fillna("   -")

    # Mostrar el DataFrame
    st.write(df)

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
        ("SuperficieCubierta", SuperficieCubierta, {'color': 'gray', 'fillColor': 'blue', 'weight': 2}),
        ("CirculacionPeatonal", CirculacionPeatonal, {'color': 'green', 'fillColor': 'green', 'weight': 0.5})
    ]

    with open('./MERCEDES/GeoJSON/Empresas.geojson', 'r', encoding="utf-8") as geojson_file:
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
        if empresas_features is not None:
            for feature in empresas_features:
                if feature["properties"]["empresa"] == "AREA DE SERVICIOS":
                    nombre = feature['properties']['empresa']
                    latitud = feature['geometry']['coordinates'][1]
                    longitud = feature['geometry']['coordinates'][0]
                
                # Verificar si hay geometría antes de continuar
                    popup_content = f"Area de servicios"

                    icon = folium.Icon(icon="glyphicon-circle-arrow-down", color="green")  # Cambia el icono y color según tu preferencia
            
                    marker = folium.Marker(
                        location=[latitud, longitud],
                        icon=icon,
                        popup=folium.Popup(html=popup_content, parse_html=True, max_width=300)
                    )
                    
                    marker.add_to(mapa)
                else:
                    if feature['geometry'] is not None:
                        nombre = feature['properties']['empresa']
                        latitud = feature['geometry']['coordinates'][1]
                        longitud = feature['geometry']['coordinates'][0]
                    
                    # Verificar si hay geometría antes de continuar
                        popup_content = f"Empresa: {nombre}"

                        icon = folium.Icon(icon="glyphicon-home", color="green")  # Cambia el icono y color según tu preferencia
                
                        marker = folium.Marker(
                            location=[latitud, longitud],
                            icon=icon,
                            popup=folium.Popup(html=popup_content, parse_html=True, max_width=300)
                        )
                        
                        marker.add_to(mapa)

            


    empresas_nombres = [feature['properties']['empresa'] for feature in empresas_features]

    empresas_nombres_unicos = list(set(empresas_nombres))

    empresas_nombres_unicos = sorted(empresas_nombres_unicos)

    empresas_nombres_unicos = [empresa for empresa in empresas_nombres_unicos if empresa is not None and empresa not in ["AREA DE SERVICIOS", "AREA DE RESIDUOS"]]

    selected_marker = st.selectbox("Selecciona una empresa:", empresas_nombres_unicos)

    selected_features = [feature for feature in empresas_features if feature['properties']['empresa'] == selected_marker]

    for feature in selected_features:
        latitude = feature['geometry']['coordinates'][1]
        longitude = feature['geometry']['coordinates'][0]
        icon = folium.Icon(color="red")
        marker = folium.Marker(location=[latitude, longitude], popup="Empresa seleccionada: " + feature['properties']['empresa'], icon=icon)
        marker.add_to(mapa)

    folium_static(mapa)

    st.header("Información de la Empresa")

    data_dict = {}

    # Llenar el diccionario con los datos de cada lote
    for index, lote in enumerate(selected_features):
        properties = lote['properties']
        for key, value in properties.items():
            if key not in data_dict:
                data_dict[key] = [None] * len(selected_features)
            data_dict[key][index] = value

    # Crear el DataFrame a partir del diccionario
    df = pd.DataFrame(data_dict)

    df.dropna(axis=1, how='all', inplace=True)

    df = df.fillna("   -")

    # Mostrar el DataFrame
    st.write(df)

def SantaRosa():

    Perimetro = gpd.read_file("./SANTA ROSA/GeoJSON/Perimetro.geojson")
    AreasDelParque = gpd.read_file("./SANTA ROSA/GeoJSON/AreasDelParque.geojson")
    CallePrincipal = gpd.read_file("./SANTA ROSA/GeoJSON/CallePrincipal.geojson")
    Ripio = gpd.read_file("./SANTA ROSA/GeoJSON/Ripio.geojson")
    Madera = gpd.read_file("./SANTA ROSA/GeoJSON/Madera.geojson")
    Parcelas = gpd.read_file("./SANTA ROSA/GeoJSON/Parcelas.geojson")
    SuperficieCubierta = gpd.read_file("./SANTA ROSA/GeoJSON/SuperficieCubierta.geojson")
    CirculacionPeatonal = gpd.read_file("./SANTA ROSA/GeoJSON/CirculacionPeatonal.geojson")
    BDT1 = gpd.read_file("./SANTA ROSA/GeoJSON/DesaguePluvialBDT1.geojson")
    BDT2 = gpd.read_file("./SANTA ROSA/GeoJSON/DesaguePluvialBDT2.geojson")
    CañeriasD = gpd.read_file("./SANTA ROSA/GeoJSON/DesaguePluvialCañerias1.geojson")
    #DesaguePluvialCañerias2 = gpd.read_file("./SANTA ROSA/GeoJSON/DesaguePluvialCañerias2.geojson")
    CañeriasRA = gpd.read_file("./SANTA ROSA/GeoJSON/RedDeAguaCañerias.geojson")
    Hidrantes = gpd.read_file("./SANTA ROSA/GeoJSON/RedDeAguaHidrante.geojson")
    Tanques = gpd.read_file("./SANTA ROSA/GeoJSON/RedDeAguaTanques.geojson")
    VE = gpd.read_file("./SANTA ROSA/GeoJSON/RedDeAguaVE.geojson")
    Residuos = gpd.read_file("./SANTA ROSA/GeoJSON/Residuos.geojson")
    Circuito1 = gpd.read_file("./SANTA ROSA/GeoJSON/TendidoElectricoCircuitoEtapa1.geojson")
    Circuito2 = gpd.read_file("./SANTA ROSA/GeoJSON/TendidoElectricoCircuitoEtapa2.geojson")
    Circuito3 = gpd.read_file("./SANTA ROSA/GeoJSON/TendidoElectricoCircuitoEtapa3.geojson")
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
        ("SuperficieCubierta", SuperficieCubierta, {'color': 'grey', 'fillColor': 'blue', 'weight': 2}),
        ("CirculacionPeatonal", CirculacionPeatonal, {'color': 'green', 'fillColor': 'green', 'weight': 0.5}),
        ("BDT1", BDT1, {'color': 'black', 'fillColor': 'purple', 'weight': 2}),
        ("BDT2", BDT2, {'color': 'black', 'fillColor': 'purple', 'weight': 2}),
        ("CañeriasD", CañeriasD, {'color': 'blue', 'fillColor': 'purple', 'weight': 2}),
        #("DesaguePluvialCañerias2", DesaguePluvialCañerias2, {'color': 'black', 'fillColor': 'purple', 'weight': 2}),
        ("CañeriasRA", CañeriasRA, {'color': 'cyan', 'fillColor': 'blue', 'weight': 2}),
        ("Hidrantes", Hidrantes, {'color': 'cyan', 'fillColor': 'blue', 'weight': 2}),
        ("Tanques", Tanques, {'color': 'blue', 'fillColor': 'blue', 'weight': 5}),
        ("VE", VE, {'color': 'cyan', 'fillColor': 'blue', 'weight': 2}),
        ("Residuos", Residuos, {'color': 'orange', 'fillColor': 'green', 'weight': 2}),
        ("Circuito1", Circuito1, {'color': 'black', 'fillColor': 'transparent', 'weight': 2}),
        ("Circuito2", Circuito2, {'color': 'black', 'fillColor': 'transparent', 'weight': 2}),
        ("Circuito3", Circuito3, {'color': 'black', 'fillColor': 'transparent', 'weight': 2}),
        ("Vegetacion", Vegetacion, {'color': 'green', 'fillColor': 'green', 'weight': 0.5}),
    ]

    pinesdic = [#("Empresas": {'color': 'green', 'fillColor': 'green', 'weight': 2}),
        ("BDT1", BDT1, {'color': 'blue', 'fillColor': 'cyan', 'weight': 2, 'icon': 'glyphicon-cloud'}),
        ("BDT2", BDT2,  {'color': 'blue', 'fillColor': 'blue', 'weight': 2, 'icon': 'glyphicon-cloud'}),
        ("Hidrantes", Hidrantes, {'color': 'blue', 'fillColor': 'blue', 'weight': 2, 'icon': 'glyphicon-fire'}),
        ("VE",VE, {'color': 'blue', 'fillColor': 'blue', 'weight': 2, 'icon': 'glyphicon-tint'})]

    with open('./SANTA ROSA/GeoJSON/Empresas.geojson', 'r', encoding="utf-8") as geojson_file:
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
    DesaguePluvial = ["BDT1",
    "BDT2",
    "CañeriasD",
    #"DesaguePluvialCañerias2"
    ]
    TendidoElectrico = ["Circuito1",
    "Circuito2",
    "Circuito3"]
    RedDeAgua = ["CañeriasRA",
    "Hidrantes",
    "Tanques",
    "VE"]

    pines = ["Empresas", "BDT1", "BDT2", "Hidrantes", "VE"]

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
        st.sidebar.markdown('<div style="margin: 10px 0;"></div>', unsafe_allow_html=True)
        for elemento in DesaguePluvial:
            seleccionado = st.sidebar.checkbox(elemento)
            if seleccionado:
                elementos_seleccionados.append(elemento)
            elif elemento in elementos_seleccionados:
                elementos_seleccionados.remove(elemento)
        st.sidebar.markdown('<div style="margin: 10px 0;"></div>', unsafe_allow_html=True)

    TendidoBarra = st.sidebar.checkbox("Tendido Electrico")
    if TendidoBarra:
        st.sidebar.markdown('<div style="margin: 10px 0;"></div>', unsafe_allow_html=True)
        for elemento in TendidoElectrico:            
            seleccionado = st.sidebar.checkbox(elemento)
            if seleccionado:
              elementos_seleccionados.append(elemento)
            elif elemento in elementos_seleccionados:
                elementos_seleccionados.remove(elemento)
        st.sidebar.markdown('<div style="margin: 10px 0;"></div>', unsafe_allow_html=True)

    AguaBarra = st.sidebar.checkbox("Red de Agua")
    if AguaBarra:
        st.sidebar.markdown('<div style="margin: 10px 0;"></div>', unsafe_allow_html=True)
        for elemento in RedDeAgua:
            seleccionado = st.sidebar.checkbox(elemento)

            if seleccionado:
              elementos_seleccionados.append(elemento)
            elif elemento in elementos_seleccionados:
                elementos_seleccionados.remove(elemento)
        st.sidebar.markdown('<div style="margin: 10px 0;"></div>', unsafe_allow_html=True)
    
    folium_layers = {}
    for nombre, capa, estilo in capas:
        if nombre in elementos_seleccionados and nombre not in pines:
            folium_layer = folium.GeoJson(capa, name=nombre, style_function=lambda feature, style=estilo: style)
            folium_layer.add_to(mapa)
            folium_layers[nombre] = folium_layer
        else:
            continue

    for nombre, data, estilo in pinesdic:

        for point in data["geometry"]:
            if nombre in elementos_seleccionados:
                if point is not None:
                    coords = [point.x, point.y]
                    
                    folium.Marker(
                        location=[coords[1], coords[0]],
                        popup=nombre,
                        icon=folium.Icon(
                            color=estilo['color'],
                            icon_color=estilo['fillColor'],
                            icon=estilo["icon"],
                            prefix="glyphicon",
                        ),
                        weight=estilo['weight'],
                    ).add_to(mapa)

    if "Empresas" in elementos_seleccionados:
        for feature in empresas_features:
            nombre = feature['properties']['EMPRESA']
            latitud = feature['geometry']['coordinates'][1]
            longitud = feature['geometry']['coordinates'][0]
            
            # Verificar si hay geometría antes de continuar
            if feature["properties"]["EMPRESA"] is None:
                if feature['geometry'] is not None:
                    popup_content = f"Empresa: {nombre}"

                    icon = folium.Icon(icon="glyphicon-ok", color="green")  # Cambia el icono y color según tu preferencia
            
                    marker = folium.Marker(
                        location=[latitud, longitud],
                        icon=icon,
                        popup=folium.Popup(html="Parcela Disponible", parse_html=True, max_width=300)
                    )
                    marker.add_to(mapa)
            else:
                if feature['geometry'] is not None:
                        popup_content = f"Empresa: {nombre}"

                        icon = folium.Icon(icon="glyphicon-home", color="green")  # Cambia el icono y color según tu preferencia
                
                        marker = folium.Marker(
                            location=[latitud, longitud],
                            icon=icon,
                            popup=folium.Popup(html=popup_content, parse_html=True, max_width=300)
                        )
                        
                        marker.add_to(mapa)



    empresas_nombres = [feature['properties']['EMPRESA'] for feature in empresas_features]

    empresas_nombres_unicos = list(set(empresas_nombres))

    empresas_nombres_unicos = [empresa for empresa in empresas_nombres_unicos if empresa is not None]

    empresas_nombres_unicos = sorted(empresas_nombres_unicos)

    selected_marker = st.selectbox("Selecciona una empresa:", empresas_nombres_unicos)

    selected_features = [feature for feature in empresas_features if feature['properties']['EMPRESA'] == selected_marker]

    for feature in selected_features:
        latitude = feature['geometry']['coordinates'][1]
        longitude = feature['geometry']['coordinates'][0]
        icon = folium.Icon(color="red")
        marker = folium.Marker(location=[latitude, longitude], popup="Empresa seleccionada: " + feature['properties']['EMPRESA'], icon=icon)
        marker.add_to(mapa)

    folium_static(mapa)

    st.header("Información de la Empresa")

    data_dict = {}

    # Llenar el diccionario con los datos de cada lote
    for index, lote in enumerate(selected_features):
        properties = lote['properties']
        for key, value in properties.items():
            if key not in data_dict:
                data_dict[key] = [None] * len(selected_features)
            data_dict[key][index] = value

    # Crear el DataFrame a partir del diccionario
    df = pd.DataFrame(data_dict)

    df = df.fillna("   -")

    df.dropna(axis=1, how='all', inplace=True)

    # Mostrar el DataFrame
    st.write(df)


def main():
    # La clave de acceso única
    #access_key = "subseindustria2023"
    #user_input = st.text_input("Ingrese la clave de acceso:", type="password")
    #if user_input == access_key:
    seleccion = st.radio("Selecciona un parque:", ("Ituzaingó", "Mercedes", "Santa Rosa"))
    if seleccion == "Ituzaingó":
        Ituzaingo()
    elif seleccion == "Mercedes":
        Mercedes()
    elif seleccion == "Santa Rosa":
        SantaRosa()

if __name__ == "__main__":
    main()