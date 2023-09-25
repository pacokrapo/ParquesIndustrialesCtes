# ParquesIndustrialesCtes
Mapas de los parques industriales de la provincia de Corrientes

  En este proyecto trabajé con mapas que ya habían sido generados en QGIS. Este programa sirve para crear datos con geolocalización. Estos datos los transformé a GeoJSON usando el mismo programa y a partir de ahí los trabajé con Python.

  Utilicé principalmente la librería Streamlit para realizar la visualización de los datos, donde ingesté un mapa de Folium con los datos en formato GeoJSON, con la posibilidad de seleccionar y deseleccionar cada una de las capas trabajadas en QGIS (cada capa es un archivo GeoJSON distinto).

  También utilicé un poco de Pandas para trabajar con algunos datos almacenados en los archivos GeoJSON, específicamente la información de cada parcela y la empresa que la residía en ese momento, y GeoPandas para leer dichos archivos.

Pueden ver el resultado en la siguiente imagen y el proyecto en el siguiente link: 
[Proyecto Parques Industriales Ctes](https://parques-industriales-corrientes.onrender.com/)

![Imagen del resultado](https://github.com/pacokrapo/ParquesIndustrialesCtes/blob/main/imagenes/Parque%20Santa%20Rosa.png)

