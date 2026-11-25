# Inspecciones de seguridad alimentaria en Madrid (2018-2019)

Proyecto conjunto del taller (grupo 3): análisis exploratorio de un dataset público.

## Participantes

| Nombre | Usuario de GitHub |
|---|---|
| Carlos Andrés Gamboa Rodríguez | [carlosgamboa15](https://github.com/carlosgamboa15) |
| Dayron Rumbaut Rangel | [drr00049](https://github.com/drr00049) |
| Juan Ignacio Torralbo Correas | [Juator](https://github.com/Juator) |
| Miguel Sánchez Colmenero | [Msanchez67](https://github.com/Msanchez67) |
| César Enrique Polo Castro | [cpc591](https://github.com/cpc591) |

## Dataset

**Resultados de las inspecciones de seguridad alimentaria en establecimientos de Madrid**,
publicado por [Civio Datos](https://datos.civio.es/) con datos de Madrid Salud (Ayuntamiento de Madrid).

Contiene la última inspección hecha a cada bar, restaurante, comercio alimentario o comedor colectivo
(colegios, residencias, escuelas infantiles) de la ciudad entre el 01/01/2018 y el 30/06/2019.
Para cada establecimiento se indican el rótulo, la dirección, el epígrafe de actividad, la fecha y el tipo
de inspección, el resultado higiénico-sanitario, el distrito y las coordenadas. Si el establecimiento
también se inspeccionó en 2018, aparece el resultado anterior y si mejoró o empeoró.

- Fichero: [data/inspecciones_madrid.csv](data/inspecciones_madrid.csv) (CSV, UTF-8, 3,5 MB)
- **11.228 filas × 25 columnas**

## Cómo ejecutarlo

```bash
pip install pandas matplotlib
python analisis.py
```

El script imprime el resumen por consola y guarda las figuras en [figuras/](figuras/).
## Calidad de los datos

La función `calidad_datos()` examina los valores faltantes y los duplicados antes
de ejecutar el análisis exploratorio. No elimina registros, imputa valores ni
modifica el CSV original.

Al ejecutar `python analisis.py`, se generan:

- [Tabla de faltantes](resultados/valores_faltantes.csv): cantidad y porcentaje
  por variable, con el total de filas como denominador.
- [Resumen de calidad](resultados/resumen_calidad.csv): dimensiones, filas con
  algún faltante, duplicados, fechas ausentes o no interpretables, coordenadas
  incompletas, distritos desconocidos y estados ausentes.
- [Figura de faltantes](figuras/07_valores_faltantes.png): porcentaje de ausencia
  por variable. Si no hay faltantes, la figura lo indica.

Los faltantes incluyen los reconocidos por `pandas.read_csv` y, para este
diagnóstico, los textos vacíos o compuestos solo por espacios. La etiqueta
`Desconocido` se cuenta por separado en la variable distrito.

Los duplicados se comprueban sobre todas las columnas del CSV leído, antes de
convertir fechas o normalizar blancos. Se distingue entre copias adicionales
(`duplicated()`) y todas las filas implicadas (`duplicated(keep=False)`). Si una
fila aparece tres veces, hay dos copias adicionales y tres filas implicadas.
Esta comprobación no identifica establecimientos repetidos con otros valores
diferentes ni sustituye la revisión de un identificador de establecimiento.
## Resultados principales

| Variable | Valores distintos | Valor más frecuente |
|---|---|---|
| Estado higiénico sanitario | 3 | Favorable (66,7 %) |
| Tipo de establecimiento | 3 | Comercio (49,0 %) |
| Perfil de la actividad | 4 | Prioridad media (48,4 %) |
| Frecuencia de inspección | 4 | Media (35,1 %) |
| Tipo de actuación | 3 | Programada (91,3 %) |
| Distrito | 21 (+ «Desconocido») | Villaverde (8,6 %) |
| Epígrafe de actividad | 72 | Comedor en centros educativos (1.132) |

- **El 24 % de las inspecciones fueron desfavorables** y un 9,3 % favorables condicionadas.
- Los **bares y restaurantes** tienen la mayor tasa de desfavorables (30,2 %), frente al 23,1 % del comercio
  y el 11,2 % de los comedores colectivos.
- Por distrito, **Arganzuela (62,9 %)** y **Centro (43,9 %)** tienen las tasas más altas de inspecciones desfavorables;
  Moratalaz, San Blas-Canillejas y Retiro, las más bajas (menos del 7 %).
- De los 2.517 establecimientos que también se inspeccionaron en 2018, el 62 % siguió igual,
  el 26 % mejoró y el 13 % empeoró.
- Coordenadas: latitud entre 40,33 y 40,55 (media 40,42); longitud entre -3,86 y -3,53 (media -3,68).

## Figuras

| | |
|---|---|
| ![Estado](figuras/01_estado_higienico.png) | ![Por tipo](figuras/02_estado_por_tipo.png) |
| ![Distritos](figuras/03_desfavorables_por_distrito.png) | ![Por mes](figuras/04_inspecciones_por_mes.png) |
| ![Mapa](figuras/05_mapa.png) | ![Actividades](figuras/06_top_actividades.png) |

## Licencia de los datos

Datos de Civio Datos. Según sus condiciones de uso: cita y enlaza la fuente.

## Conclusiones
Existe un elevado porcentaje de establecimientos que fueron desfavorables o favorables con condiciones. Exactamente un 33,30 %
Esto supone un tercio de los establecimientos.
Además llama la atención que bastante más del 50 % siguió igual. Exactamente un 62% y, tan solo un 26 % mejoró
Llama la atención que los bares y restaurantes tiene la mayor tasa desfavorable (30,20 %). Teniendo en cuenta que son establecimientos de alimentación, es preocupante.
Como conclusión, en una primera valoración el resultado es elevado

## Conclusiones

- Aunque el 66,7 % de las inspecciones presenta un resultado favorable, resulta significativo que aproximadamente una de cada cuatro tenga una valoración desfavorable, lo que pone de manifiesto la importancia de mantener los controles de seguridad alimentaria.

- Los bares y restaurantes presentan el mayor porcentaje de inspecciones desfavorables (30,2 %), frente al comercio (23,1 %) y los comedores sociales (11,2 %), lo que evidencia diferencias importantes entre los tipos de establecimientos inspeccionados.

- El distrito de Arganzuela destaca con un 62,9 % de inspecciones desfavorables, superando ampliamente la media de Madrid (24 %). Sería interesante analizar si estas diferencias están relacionadas con el tipo de establecimientos inspeccionados y el número de inspecciones realizadas.

- Dado que los datos de 2019 solo abarcan hasta finales de junio, considero necesario tener en cuenta esta limitación temporal al realizar comparaciones entre ambos años.

## Conclusiones

Sobre las inspecciones en Madrid, estos son los puntos clave:

Tipo de establecimiento que más suspende: Los bares y restaurantes lideran los resultados desfavorables, con cerca de un 30 % de suspensos (superando la media general del 24 % que muestra el primer gráfico). Les sigue el comercio (alrededor del 23 %) y, por último, el comedor social (con apenas un 11 % aproximadamente).

Distritos que destacan:

Con más inspecciones desfavorables: Arganzuela encabeza la lista por amplio margen (superando las 60 inspecciones desfavorables), seguido por Centro (alrededor de 44) y Tetuán (cerca de 38). En total, 10 distritos superan la media de Madrid (situada en torno a 24).

Con menos inspecciones desfavorables: En el extremo opuesto, destacan Moratalaz, San Blas-Canillejas, Retiro y Vicálvaro, todos por debajo de las 10 inspecciones desfavorables.

Variación de las inspecciones por mes: El volumen muestra una clara tendencia al alza entre 2018 y 2019, combinada con fuertes caídas estacionales en periodos vacacionales:

En 2018: El ritmo es moderado (entre 350 y 625 inspecciones), con picos en mayo (~625) y octubre (~800), pero sufre desplomes pronunciados en verano (julio y agosto, bajando a ~350) y en diciembre (~365).

En 2019: Tras el bajón navideño, la actividad repunta con fuerza a partir de febrero, estabilizándose en un nivel mucho más alto (entre 840 y 1.000 inspecciones mensuales) y alcanzando su máximo histórico de toda la serie en mayo de 2019 (~1.000 inspecciones).

