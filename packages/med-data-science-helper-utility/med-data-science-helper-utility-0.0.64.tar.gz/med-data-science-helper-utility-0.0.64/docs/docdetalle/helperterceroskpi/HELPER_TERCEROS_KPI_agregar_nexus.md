Función **AGREGAR_NEXUS**
==============================
<p1> Esta función permite obtener información sobre ratios de tipo de contratación de docentes que tiene un determinado servicio educativo</p1>

**<h2>Parámetros</h2>**

<p> Esta función cuenta con tres parámetros, los cuales se detallan a continuación</p>

```Python

helper_terceros_kpi.agregar_nexus(df,anio_df=None,df_nexus=None,anio_h=2020, cache=False ):

```
<p1><strong>df</strong> (Requerido): Dataframe que contiene el nivel socioeconómico del hogar.</p1>

<p1><strong>df_sisfoh</strong>: Dataframe Sisfoh, si no se indica, la función lo consultara por si misma.</p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1><strong>df</strong>: Retorna un dataframe que contiene la siguiente columna adicional: <strong>SISFOH_CSE</strong>(contiene los niveles socioeconómicos tales como POBRE_EXTREMO, POBRE).</p1>

<p1> </p1>

**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_terceros_kpi as htk


# df: Dataframe que contiene los niveles socioeconomicos
df_new = htk.agregar_nexus(df_reg,anio_df=anio, anio_h=anio_h_1,cache=True)

```

**<h3>Output :</h3>**

<p1><strong>df</strong>: Retorna un dataframe que contiene la siguiente columna adicional: <strong>SISFOH_CSE</strong>(contiene los niveles socioeconómicos tales como POBRE_EXTREMO, POBRE).</p1>


```Python
#df: 
print(df_reg_temp.shape)
# Impresión durante la ejecucion del DataFrame df de prueba
agregar_nexus
key_2019_DOCENTE_Activo_Encargatura
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\nexus_2018_2019.xlsb.h5
NEW : RATIO_CONT_X_CMOD_T_MENOS_1
NEW : RATIO_NOMB_X_CMOD_T_MENOS_1
NEW : RATIO_OT_X_CMOD_T_MENOS_1
(136684, 187)

```

[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
