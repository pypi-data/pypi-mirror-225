Función **AGREGAR_SHOCK_SOCIOECONOMICO**
==============================
<p1> Esta función permite obtener información sobre proyección de ingresos de los hogares de cada estudiante.</p1>

**<h2>Parámetros</h2>**

<p> Esta función cuenta con cinco parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.agregar_shock_economico(df, df_se=None, anio=None, modalidad="EBR", cache=False):

```
<p1><strong>df</strong>(Requerido): Dataframe para poder consultar el nivel ingreso proyectado del hogar.</p1>

<p1><strong>df_se</strong>: Dataframe Sisfoh, si no se indica, la función lo consultara por sí misma</p1>

<p1><strong>anio</strong>: Número entero que indica el año base para consultar las proyecciones de ingreso en el año t+1. </p1>

<p1><strong>modalidad</strong>: String que indica la modalidad del servicio educativo </p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>LOG_ING_T_MAS_1_IMP_DIST </strong> y <strong>NA_LOG_ING_T_MAS_1_IMP_DIST</strong>. </p1>

<p1> </p1>

**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import core_helper. helper_terceros_kpi as htk

# df_reg: Dataframe que contiene el nivel ingreso proyectado del hogar
df_reg =  htk.agregar_shock_economico(df_reg,anio=2021)  

```

**<h3>Output :</h3>**

<p1><strong>df</strong>: Retorna un dataframe que contiene las siguientes columnas adicionales: <strong>LOG_ING_T_MAS_1_IMP_DIST</strong>(Valor logarítmico de la proyección de ingreso en el año t+1) y <strong>NA_LOG_ING_T_MAS_1_IMP_DIST</strong>(Dicotómica que indica si la variable fue  missing y posteriormente imputada).</p1>


```Python
# Impresión durante la ejecucion del DataFrame df de prueba
agregar_shock_economico
key_2020
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\shock_economico.h5
NEW : LOG_ING_T_MAS_1_IMP_DIST
NEW : NA_LOG_ING_T_MAS_1_IMP_DIST
(136684, 147)

```

[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
