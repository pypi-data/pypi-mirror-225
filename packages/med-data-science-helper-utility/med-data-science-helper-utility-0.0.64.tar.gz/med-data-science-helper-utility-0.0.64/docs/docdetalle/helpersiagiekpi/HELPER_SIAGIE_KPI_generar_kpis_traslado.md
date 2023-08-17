Función **GENERAR_KPIS_TRASLADO**
==============================
<p1> Esta función permite obtener información sobre indicadores de traslado escolar a partir de datos históricos.</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con cinco parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.generar_kpis_traslado(df, anio_df=None , anio_h=None ,t_anios=1, cache=False):

```
<p1><strong>df</strong> (Requerido): Dataframe de estudiantes proveniente de siagie.</p1>

<p1><strong>anio_df</strong>: Número entero que representa el año de los datos del dataframe <strong>df</strong>.</p1>

<p1><strong>anio_h</strong>: Número entero que indica el año desde el cual se tomará en cuenta para calcular un histórico. </p1>

<p1><strong>t_anios</strong>: Número entero que indica la cantidad de años que se tomará en cuenta para el histórico. </p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>TOTAL_TRASLADOS</strong>, <strong>MEAN_TRASLADOS</strong> y <strong>STD_TRASLADOS</strong>.</p1>

<p1> </p1>

**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk

anio_df = 2020
anio_h = 2018
kpis_trl = 2

# df_reg_temp: Dataframe que contiene los datos de los estudiantes
df_reg_temp = hsk.generar_kpis_traslado(df_reg_temp,anio_df=anio,anio_h=anio_h_1,t_anios=kpis_trl,cache=True)    

```

**<h3>Output :</h3>**

<p1><strong>df</strong> : Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>TOTAL_TRASLADOS</strong>, <strong>MEAN_TRASLADOS</strong> y <strong>STD_TRASLADOS</strong>.</p1>


```Python
#df: 
print(df_reg_temp.shape)
# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 3 años de histórico:
key_2020_2019_4
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_traslado.h5
No hay cache disponible para los parametros ingresados
NEW : TOTAL_TRASLADOS
NEW : MEAN_TRASLADOS
NEW : STD_TRASLADOS
guardando cache
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_traslado.h5
(128114, 156)

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
