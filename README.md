**<p align="center">Proyecto individual 1</p>**
**<p align="center">MACHINE LEARNING OPERATIONS (MLOPS)</p>**

## Introducción
<p style="text-align: justify;">Durante este proyecto se asumió el rol de un ingeniero de datos y un cientifico de datos (MLOPs engineer), trabajando para la empresa de STEAM, lacual es una plataforma de distribución digital de videojuegos desarrollada por Valve Corporation, lanzada en septiembre de 2003 buscando brindar actualizaciones automáticas para sus productos. Posteriormente se expandió y empezó a incluir títulos de terceros. Cuenta con una base de usuarios que supera los 325 millones, y un catálogo alberga más de 25,000 juegos. Cabe resaltar que las cifras proporcionadas por SteamSpy solo están disponibles hasta el año 2017, puesto que a principios de 2018 Steam implementó restricciones en el consumo de sus estadísticas. 
Para hacer posible este proyecto, se parte de distintas bases de datos en formato Json, se reailzan procesos de ETL, EDA, se crean funciones y un modelo de Machine Learning, y esto se deploya con render y Fast API, con el fin de disponibilizar la informacion y consultas para cualquier usuario en la nube.</p>

## Datos
<p style="text-align: justify;">Los datos se encontraron en 3 archivos .Json:

1. australian_user_reviews.Json : Contiene información sobre el usuario, sus reseñas y el año de posteo de las mismas.
2. australian_user_items.Json : Contiene información del usuario, el tiempo de juego en minutos, y los nombres de juegos consumidos.
3. output_steam_games.Json : Contiene toda la info sobre los juegos, nombre, publicador, desarrollador, género, fecha de lanzamiento, precio, etc.</p>

## ETL (Extracción, Transformación y Carga)
<p style="text-align: justify;">Para el proceso de ETL en los 3 archivos .Json se usó Python (con la ayuda de Pandas y numpy principalmente), se tomaron los archivos en bruto, se leyeron, se analizaron las columnas (en algunos casos fue necesario la desanidación de columnas con formato diccionario), sus tipos de datos y la información que estas representan, para luego realizar procesos cómo:
- Eliminación de nulos o vacíos.
- Eliminación de duplicados.
- Eliminación de Columnas que no se consideraron relevantes para las funciones de la API.
- Estandarización de nombres, por ejemplo, de 'item_id', a 'Item_Id'.
- Cambio de tipos de datos en las columnas.

Entre otros cambios que se pueden evidenciar en los 'ETL' notebooks, disponibles en la carpeta NoteBooks.
</p>

## EDA (Análisis Exploratorio de Datos)
<p style="text-align: justify;">Luego de realizar un primer acercamiento y una limpieza general de las bases de datos en los procesos de ETL, se realiza un análisis un tanto más riguroso, usando pandas, numpy, seaborn y matplotlib principalmente. Se crearon graficas y se obtuvieron estadísticas de los diferetes conjuntos de datos, para obtener por ejemplo:
- Usuarios con mayor cantidad de juegos.
- Generos más relevantes.
- Horas de juego en diferentes juegos y géneros.
- Calificaciones de diferentes juegos y cantidad de juegos para cada calificación.

Durante este análisis exploratorio tambíen se aprovechó para crear un rating teniendo en cuenta las calificaciones y las recomendaciones de los usuarios, de aquí salen tablas que serían útiles a futuro, como lo fue la tabla de 'recomendacion.parquet', usada en el modelo de recomendacion.

El EDA fue importante para tener un panorama general mucho más claro de nuestros datos, y para identificar variables útiles para las funciones y el modelo, todo este proceso se encuentra en el archivo 'EDA_.ipynb', en la carpeta de NoteBooks.
</p>

## Feature Engineering
<p style="text-align: justify;">En el archivo 'FEAT_ENG.ipynb' se encuentra el proceso de creación de la columna *'Sentiment_Analysis'*, esta columna contiene un numero entero, sea 0, 1 ó 2. Dónde 0 es Negative, 1 Neutral y 2 Positive.

Esta columna nace de desanidar la columna *Reviews* disponible en el archivo 'australian_user_reviews.Json', se toma la reseña dada por cada usuario y se somete a un análisis de sentimiento mediante la librería de nltk (Natural Language Tool Kit) y Vader Lexicon, estas analizan las reseñas y asignan un valor (0, 1 ó 2) según el sentimiento que estas representen, así por ejemplo, las palabras *'Funny'*, *'Great'*, *'Good'*, etc se toman como un 2, y palabras como *'Bad'*, *'Boring'*, etc, se toman como un 0.
Gracias a este proceso de categorizacion y con la columna *'Sentiment_Analysis'*, se creó al final del EDA una columna adicional llamada 'Rating' que toma el analisis de sentimiento y la recomendacion de cada usuario para generar una escala de 1 a 5.
</p>

## Funciones y Modelo de recomendación:
<p style="text-align: justify;"> Fueron solicitadas 5 funciones y un modelo:

1. --> def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.

Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

2. --> def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

3. --> def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)

Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

4. --> def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)

Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

5. --> def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.

6. MODELO: Sistema de recomendación item-item:

--> def recomendacion_juego( id de producto ): Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

Para poder dar vida a estas funciones, se tomaron los datos ya limpios generados en los ETL, y se crearon tablas mas pequeñas, que cuentan solamente con las columnas necesarias para cada función, estas tablas se guardan en formato .parquet con el fin de optimizar los limitados recursos que nos brinda render a la hora de deployar la API.

En el caso del modelo, se tomó la tabla creada en el EDA: 'Recomendacion.parquet', y se crea una matríz con los usuarios, juegos y calificaciones dadas a los mismos, luego de algunos procesos se obtienen los datos con los cuales se aplica la similitud del coseno (con la ayuda de la libreria de Scikit Learn), y se entrena el modelo, las matrices y el vector de similitudes obtenidos se pasan a dataframe y tambíen se guardan como .parquet.

Todo el proceso de creacion de funciones y del modelo (además de los archivos .parquet necesarios)están disponibles en el archivo 'Funciones_API.ipynb'. </p>

## Render y FastAPI
<p style="text-align: justify;">
En este punto, fue necesario el uso de un entorno virtual, creado en la carpeta local del proyecto, ya que ayuda a garantizar la consistencia, la reproducibilidad y la portabilidad del proyecto al implementarlo en diferentes entornos o servicios en la nube, como lo es render.
Para poder deployar nuestras funciones en Fast API usamos render, cuyo plan gratuito cuenta con 512mb de almacenamiento y 0.15 CPU, es por esto que fue necesario guardar los datos usados en las funciones como formato parquet y reducir las tablas lo máximo posible.

En render se usó la funcion de Web Services, se vinculó el repositorio 'https://github.com/StivenLopez712/Deploy_API' (se creó un repositorio solamente para el deploy con el fin de agilizar el proceso), y se configuró render con base a los pasos proporcionados en 'https://github.com/StivenLopez712/Deploy_AP'.
En el archivo main.py se colocaron las funciones ya creadas, cada una con su respectivo '(@app.get(‘/’))', adicionalmente, en el repo yacen los archivos .parquet necesarios, y los archivos requirementes.txt y docker.txt que necesita render.

Desde render podemos controlar cuando esté o no disponible nuestra API, el link de a misma es: 'https://deploy-api-i7um.onrender.com/docs', en ella podremos encontrar las 5 funciones y el modelo de recomendación, basta con desplegar la pestaña corespondiente a la funcion deseada, clickear en 'Try Out' y brindar el parametro de entrada correspondiente, como se ve en el video agregado al final de este readme.</p>

## Conclusiones

<p style="text-align: justify;">Durante este proyecto se observaron algunas cosas:

- Los procesos de ETL son sumamente importantes, ahorran espacio y optimizan capacidad de procesamiento, quitan datos poco útiles y ayudan a que tengamos los resultados deseados.
- En el proceso de ETL de los diferentes datets, se llevaron a cabo acciones importantes, como desanidado de columnas, eliminacion de nulos, duplicados y faltantes(en algunos caso rellenado).
- El EDA fue igual de importante, ayudó a identificar y determinar la importancia de determinados datos sobre otros, y a filtrar mejor la información despúes de los respectivos procesos de ETL.
- Render es una herramienta muy útil para realizar deployments, sin embargo, también se debe tener mucho cuidado con las rutas de los archivos, el peso de los mismos y la capacidad de procesamiento que estos pueden demandar, ya que si se trabaja con la versión gratuita, los recursos son muy limitados.
- Las herramientas usadas principalmente fueron:
   Visual Studio Code, Jupyter Notebook, Python, NumPy, Pandas, Matplotlib, scikit-learn, Render, FastAPI, Git, GitHub, Pyarrow y Markdown.

#**LINK AL VIDEO:**
https://youtu.be/sgdk6ikoDIU
