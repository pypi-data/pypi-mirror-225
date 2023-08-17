Función **GENERAR_KPIS_AGG_SERVICIOS**
==============================
<p1> Esta función permite obtener información sobre indicadores de traslado escolar a partir de datos históricos.</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con seis parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.generar_kpis_agg_servicios(df, anio_df=None, anio_h =None, t_anios=1, modalidad=None, cache=False):

```
<p1><strong>df</strong> (Requerido): Dataframe de servicios.</p1>

<p1><strong>anio_df</strong>: Número entero que representa el año de los datos del dataframe <strong>df</strong>.</p1>

<p1><strong>anio_h</strong>: Número entero que indica el año desde el cual se tomará en cuenta para calcular un histórico. </p1>

<p1><strong>t_anios</strong>: Número entero que indica la cantidad de años que se tomará en cuenta para el histórico. </p1>

<p1><strong>modalidad</strong>: String que indica la modalidad educativa, ejemplo: "EBR". </p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>TOTAL_DESAPROBADO_SERVICIO_T</strong>, <strong>TOTAL_RETIRADO_SERVICIO_T</strong>, <strong>TOTAL_ESTUDIANTES_SERVICIO_T</strong>, <strong>RATIO_DESAPROBADO_SERVICIO_T</strong>, <strong>RATIO_RETIRADO_SERVICIO_T</strong>, <strong>STD_TRASLADOS</strong> y etc...</p1>

<p1> </p1>

**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>

**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk

anio_df = 2019
anio_h=2019
t_anios=3

# df_reg_temp: Dataframe que contiene los datos de los servicios
df_reg_temp = hsk.generar_kpis_agg_servicios(df_reg_temp, anio_df=anio, anio_h=anio_h_1, t_anios=1, cache=True)    

```

**<h3>Output :</h3>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>TOTAL_DESAPROBADO_SERVICIO_T</strong>, <strong>TOTAL_RETIRADO_SERVICIO_T</strong>, <strong>TOTAL_ESTUDIANTES_SERVICIO_T</strong>, <strong>RATIO_DESAPROBADO_SERVICIO_T</strong>, <strong>RATIO_RETIRADO_SERVICIO_T</strong>, <strong>STD_TRASLADOS</strong>  y etc...</p1>


```Python
#df: 
print(df_reg_temp.shape)
# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 3 años de histórico:
agregar_kpis_agg_servicios
key_2020_2019_1_None
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_agg_servicios.h5
NEW : TOTAL_DESAPROBADO_SERVICIO_T_MENOS_1
NEW : TOTAL_RETIRADO_SERVICIO_T_MENOS_1
NEW : TOTAL_ALUMNO_SERVICIO_T_MENOS_1
NEW : TOTAL_DOCENTE_SERVICIO_T_MENOS_1
NEW : TOTAL_SECCION_SERVICIO_T_MENOS_1
NEW : RATIO_ALUMNO_DOCENTE_SERVICIO_T_MENOS_1
NEW : RATIO_SECCION_DOCENTE_SERVICIO_T_MENOS_1
NEW : RATIO_DESAPROBADO_SERVICIO_T_MENOS_1
NEW : RATIO_RETIRADO_SERVICIO_T_MENOS_1
NEW : TOTAL_DESAPROBADO_SERVICIO
NEW : MEAN_DESAPROBADO_SERVICIO
NEW : STD_DESAPROBADO_SERVICIO
NEW : TOTAL_RETIRADO_SERVICIO
NEW : MEAN_RETIRADO_SERVICIO
NEW : STD_RETIRADO_SERVICIO
(128114, 174)

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
