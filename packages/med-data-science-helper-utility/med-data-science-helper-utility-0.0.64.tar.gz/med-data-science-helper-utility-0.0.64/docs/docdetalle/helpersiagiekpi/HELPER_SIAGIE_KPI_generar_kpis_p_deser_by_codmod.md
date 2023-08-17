Función **GENERAR_KPIS_P_DESER_BY_CODMOD**
==============================
<p1>Función que genera indicador de deserción escolar en porcentaje a nivel de código modular para cada periodo que se establece en la entrada de la función.</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con seis parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.generar_kpis_p_deser_by_codmod(df_reg_temp, anio_df=anio, anio_h=anio_h_1, t_anios=4,decimals=2, cache=True)

```

<p1><strong>df</strong> (Requerido): Dataframe el cual recibe los nuevos indicadores para los codigos mudlares "COD_MOD" que coincidan.</p1>

<p1><strong>anio_df</strong> (Requerido): Año de referencia a partir del cual se desea calcular. ejemplo: 2020.</p1>

<p1><strong>anio_h</strong> (Requerido): Número entero que indica el año desde el cual se tomará en cuenta para calcular un histórico.</p1>

<p1><strong>t_anios</strong>: Número entero que indica la cantidad de años que se tomará en cuenta.</p1>

<p1><strong>decimals</strong>: Número entero que indica la cantidad de decimales que mostrará en los cálculos.</p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces.</p1>


**<h2>Retornos</h2>**

<p1><strong>df</strong> : Dataframe que contiene los indicadores de deserción a nivel de código modular.</p1>

<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk

anio=2020  
anio_h_2 = anio-2
anio_h_1 = anio-1
#df_reg_temp: Dataframe que contiene los datos de los estudiantes
df_reg_temp = hsk.generar_kpis_p_deser_by_codmod(df_reg_temp,anio_df=anio , anio_h = anio_h_1 ,t_anios=4,decimals=2  ,cache=True)
```


**<h3>Output :</h3>**

<p1><strong>df</strong> : Dataframe que contiene los indicadores de deserción por distrito.</p1>

```Python
df # dataframe de salida

# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 4 años de histórico: 
-  2019  - 
agregar_kpi_p_desercion_by_cod_mod
key_2019_COD_MOD
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\p_desercion_by_cod_mod.h5
 -  2018  - 
agregar_kpi_p_desercion_by_cod_mod
key_2018_COD_MOD
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\p_desercion_by_cod_mod.h5
 -  2017  - 
agregar_kpi_p_desercion_by_cod_mod
key_2017_COD_MOD
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\p_desercion_by_cod_mod.h5
 -  2016  - 
agregar_kpi_p_desercion_by_cod_mod
key_2016_COD_MOD
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\p_desercion_by_cod_mod.h5
NEW : P_DESERCION_COD_MOD_T_MENOS_1
NEW : P_DESERCION_COD_MOD_T_MENOS_2
NEW : P_DESERCION_COD_MOD_T_MENOS_3
NEW : P_DESERCION_COD_MOD_T_MENOS_4
NEW : P_DESERCION_COD_MOD_SLOPE
NEW : P_DESERCION_COD_MOD_INTERCEPT
NEW : P_DESERCION_COD_MOD_R2

```



[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
