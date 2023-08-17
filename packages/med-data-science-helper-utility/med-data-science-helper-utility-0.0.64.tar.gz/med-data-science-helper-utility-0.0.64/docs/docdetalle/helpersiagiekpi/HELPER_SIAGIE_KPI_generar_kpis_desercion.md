Función **GENERAR_KPIS_DESERCION**
==============================
<p1>Función que permite obtener información sobre indicadores de deserción escolar a partir de datos históricos. Se generan principalmente indicadores relacionados con totales, medias y std a nivel de estudiante</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con cinco parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.generar_kpis_desercion(df,anio_df=None, anio_h=None ,t_anios=1,cache=False)

```
<p1><strong>df</strong> (Requerido): Dataframe de estudiantes proveniente de siagie.</p1>

<p1><strong>anio_df</strong>: Número entero que representa el año de los datos del dataframe <strong>df</strong>.</p1>

<p1><strong>anio_h</strong>: Número entero que representa el año de referencia a partir del cual se desea consultar información sobre dicho indicador. ejemplo: 2020.</p1>

<p1><strong>t_anios</strong>: Número entero que indica la cantidad de años que se tomará en cuenta para el histórico.</p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1><strong>df</strong> : Retorna un dataframe con columnas que tienen las siguientes valores: Total deserciones, promedio de deserciones, desviación estandar de deserciones en diversos años.</p1>

<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk

anio=2020 
anio_h_1 = anio-3
kpis_hist = 3

# df_reg_temp: Dataframe que contiene los datos de los estudiantes
df_reg_temp = hsk.generar_kpis_desercion(df_reg_temp,anio_df=anio, anio_h=anio_h_2 ,t_anios=kpis_hist,cache=True)    

```

**<h3>Output :</h3>**

<p1><strong>df</strong> : Retorna un dataframe con columnas adicionales que tienen las siguientes valores: Total deserciones, promedio de deserciones, desviación estandar de deserciones en diversos años.</p1>

```Python
#df: 
print(df.shape)
# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 3 años de histórico:
generar_kpis_desercion
key_2020_2018_3
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_desercion.h5
No hay cache disponible para los parametros ingresados
NEW : TOTAL_DESERCIONES
NEW : MEAN_DESERCIONES
NEW : STD_DESERCIONES
guardando cache
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_desercion.h5
(128114, 137)

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
