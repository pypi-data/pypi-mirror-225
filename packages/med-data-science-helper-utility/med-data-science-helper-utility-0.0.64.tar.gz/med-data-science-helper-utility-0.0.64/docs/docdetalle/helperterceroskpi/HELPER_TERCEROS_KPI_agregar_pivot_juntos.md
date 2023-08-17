Función **agregar_pivot_juntos**
==============================
<p1> Esta función permite obtener información sobre indicadores dicotomicos para conocer si el estudiante participo en el programa juntos asi como sus cumplimientos de corresponsabilidad respectivos.</p1>

**<h2>Parámetros</h2>**

<p> Esta función cuenta con tres parámetros, los cuales se detallan a continuación</p>

```Python

agregar_pivot_juntos(df,anio_df=None, anio_h=None , t_anios=1,delete_juntos_t_vcc=False, cache=False):

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


# df_reg_temp: Dataframe que contiene los niveles socioeconomicos
df_new = htk.agregar_pivot_juntos(df, anio_df=anio,anio_h=anio,t_anios=4,delete_juntos_t_vcc=True,cache=True)

```

**<h3>Output :</h3>**

<p1><strong>df</strong>: Retorna un dataframe que contiene la siguiente columna adicional: <strong>JUNTOS_T_MENOS_{N}</strong>(dicotomica si participo en el programa juntos para un determinado año), <strong>VCC_{a}_T_MENOS_{n}/strong>(dicotomica si cumplio con la corresponsabilidad a para un determinado año), .</p1>


```Python
# Impresión durante la ejecucion del DataFrame df de prueba
agregar_pivot_juntos
key_2020_2020_4
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\agregar_pivot_juntos.h5

NEW : JUNTOS_T
NEW : VCC_1_T_MENOS_1
NEW : VCC_2_T_MENOS_1
NEW : VCC_3_T_MENOS_1
NEW : VCC_4_T_MENOS_1
NEW : VCC_5_T_MENOS_1
NEW : VCC_6_T_MENOS_1
NEW : JUNTOS_T_MENOS_1
NEW : VCC_1_T_MENOS_2
NEW : VCC_2_T_MENOS_2
NEW : VCC_3_T_MENOS_2
NEW : VCC_4_T_MENOS_2
NEW : VCC_5_T_MENOS_2
NEW : VCC_6_T_MENOS_2
NEW : JUNTOS_T_MENOS_2
NEW : VCC_1_T_MENOS_3
NEW : VCC_2_T_MENOS_3
NEW : VCC_3_T_MENOS_3
NEW : VCC_4_T_MENOS_3
NEW : VCC_5_T_MENOS_3
NEW : VCC_6_T_MENOS_3
NEW : JUNTOS_T_MENOS_3
(136684, 212)

```

[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
