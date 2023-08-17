Función **agregar_distancia_ini_pri**
==============================
<p1> Esta función solo se aplica a los estudiantes del nivel inicial y permite agregar al dataframe la distancia de la IE de nivel primaria mas cercana.</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con dos parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.agregar_distancia_prim_sec(df, cache=False):

```
<p1><strong>df</strong> (Requerido): Dataframe de estudiantes proveniente de siagie.</p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1><strong>df</strong> : Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>DISTANCIA</strong> y <strong>GRUPO_DISTANCIA</strong>(Categorización de la variable DISTANCIA  en: 0K, 1K_5K, MENOR_1K, MAYOR_5K). </p1>

<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk


# df_reg_temp: Dataframe que contiene los datos de los estudiantes
df_reg_temp = hsk.agregar_distancia_prim_sec(df_reg_temp, cache=True)    

```

**<h3>Output :</h3>**

<p1><strong>df</strong> : Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>DISTANCIA</strong> y <strong>GRUPO_DISTANCIA</strong>(Categorización de la variable DISTANCIA  en: 0K, 1K_5K, MENOR_1K, MAYOR_5K).</p1>


```Python
#df: 
# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 3 años de histórico:
agregar_distancia_ini_prim
key_distancia_ini_prim
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\distancia_ini_prim.h5
NEW : DISTANCIA_PRIM
NEW : GRUPO_DISTANCIA_PRIM

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
