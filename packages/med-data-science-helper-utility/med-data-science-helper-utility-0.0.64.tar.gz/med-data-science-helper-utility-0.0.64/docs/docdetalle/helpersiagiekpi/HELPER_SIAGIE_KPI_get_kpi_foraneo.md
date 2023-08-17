Función **GENERAR_KPIS_TRASLADO**
==============================
<p1> Esta función permite obtener indicadores dicotomicos para determinar si el ubigeo del lugar de nacimiento del estudiante es el miesmo que el ubigeo del servicio educativo con el objetivo de determinar si es foraneo a nivel de Departamento, provincia o distrito</p1>

**<h2>Parámetros</h2>**

<p> Esta función cuenta con cinco parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.get_kpi_foraneo(df,anio_df=None, anio_h=None ,t_anios=1,cache=False):

```
<p1><strong>df</strong> (Requerido): Dataframe de servicios.</p1>

<p1><strong>anio_df</strong>: Número entero que representa el año de los datos del dataframe <strong>df</strong>.</p1>

<p1><strong>anio_h</strong>: Número entero que indica el año desde el cual se tomará en cuenta para calcular un histórico. </p1>

<p1><strong>t_anios</strong>: Número entero que indica la cantidad de años que se tomará en cuenta para el histórico. </p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>FORANEO_DIST_T </strong>, <strong>FORANEO_PROV_T</strong>, <strong>FORANEO_DEP_T</strong>, <strong>FORANEO_DEP_T</strong>, <strong>FORANEO_DIST_T_MENOS_1</strong>, <strong>FORANEO_PROV_T_MENOS_1</strong> y <strong>FORANEO_DEP_T_MENOS_1 </strong>.</p1>

<p1> </p1>

**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk

anio_df = 2020
anio_h = 2018


# df_reg_temp: Dataframe que contiene los datos de los servicios
df_reg_temp = hsk.get_kpi_foraneo(df_reg_temp,anio_df=anio, anio_h= anio_h_1,cache=True)

```

**<h3>Output :</h3>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>FORANEO_DIST_T </strong>, <strong>FORANEO_PROV_T</strong>, <strong>FORANEO_DEP_T</strong>, <strong>FORANEO_DEP_T</strong>, <strong>FORANEO_DIST_T_MENOS_1</strong>, <strong>FORANEO_PROV_T_MENOS_1</strong> y <strong>FORANEO_DEP_T_MENOS_1 </strong>.</p1>


```Python
#df: 
print(df_reg_temp.shape)
# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 1 año de histórico:
agregar_kpi_foraneo
key_2020_2019_1
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpi_foraneo.h5
NEW : FORANEO_DIST_T_MENOS_1
NEW : FORANEO_PROV_T_MENOS_1
NEW : FORANEO_DEP_T_MENOS_1
(128114, 182)

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
