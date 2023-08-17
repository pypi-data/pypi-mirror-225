Función **_GENERAR_KPIS_TRASLADO_A_PUBLICO**
==============================
<p1> Esta función permite obtener información sobre indicadores de traslado de privado a público, a partir de datos históricos.</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con seis parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.generar_kpis_traslado_a_publico(df,anio_df=None, anio_h =None ,t_anios=1,modalidad="EBR",cache=False):

```
<p1><strong>df</strong> (Requerido): Dataframe de estudiantes proveniente de siagie.</p1>

<p1><strong>anio_df</strong>: Número entero que representa el año de los datos del dataframe <strong>df</strong>.</p1>

<p1><strong>anio_h</strong>: Número entero que indica el año desde el cual se tomará en cuenta para calcular un histórico. </p1>

<p1><strong>t_anios</strong>: Número entero que indica la cantidad de años que se tomará en cuenta para el histórico. </p1>

<p1><strong>modalidad</strong>: String que indica la modalidad educativa, ejemplo: "EBR". </p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>TOTAL_TRASLADOS_A_PUBLICO</strong>, <strong>MEAN_TRASLADOS_A_PUBLICO</strong> y <strong>STD_TRASLADOS_A_PUBLICO</strong>.</p1>

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
df_reg_temp = hsk.generar_kpis_traslado_a_publico(df_reg_temp,anio_df=anio,anio_h=anio_h_1,t_anios=kpis_trl,cache=True)    

```

**<h3>Output :</h3>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>TOTAL_TRASLADOS_A_PUBLICO</strong>, <strong>MEAN_TRASLADOS_A_PUBLICO (media de traslados)</strong> y <strong>STD_TRASLADOS_A_PUBLICO (desviacion estandar de traslados)</strong>.</p1>

```Python
#df: 
print(df_reg_temp.shape)
# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 4 años de histórico:
generar_kpis_traslado_a_publico
key_2020_2019_4_EBR
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_traslado_a_publico.h5
No hay cache disponible para los parametros ingresados
Imprimiendo el anio servicio  2019
Imprimiendo el anio servicio  2018
Imprimiendo el anio servicio  2017
Imprimiendo el anio servicio  2016
NEW : TOTAL_TRASLADOS_A_PUBLICO
NEW : MEAN_TRASLADOS_A_PUBLICO
NEW : STD_TRASLADOS_A_PUBLICO
guardando cache
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_traslado_a_publico.h5
(128114, 159)

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
