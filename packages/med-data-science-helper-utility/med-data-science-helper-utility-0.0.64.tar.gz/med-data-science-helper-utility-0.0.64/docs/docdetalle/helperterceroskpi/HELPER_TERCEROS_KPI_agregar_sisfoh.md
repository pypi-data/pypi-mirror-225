Función **AGREGAR_SISFOH**
==============================
<p1> Esta función permite obtener información sobre proyección de ingresos a nivel nominal.</p1>

**<h2>Parámetros</h2>**

<p> Esta función cuenta con tres parámetros, los cuales se detallan a continuación</p>

```Python

helper_terceros_kpi.agregar_sisfoh(df, df_sisfoh=None, cache=False ):

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
df_reg_temp = htk.agregar_sisfoh(df_reg_temp,cache=True)

```

**<h3>Output :</h3>**

<p1><strong>df</strong>: Retorna un dataframe que contiene la siguiente columna adicional: <strong>SISFOH_CSE</strong>(contiene los niveles socioeconómicos tales como POBRE_EXTREMO, POBRE).</p1>


```Python
#df: 
print(df_reg_temp.shape)
# Impresión durante la ejecucion del DataFrame df de prueba
agregar_sisfoh
la cache para agregar_sisfoh no es necesario
The default value of regex will change from True to False in a future version.
NEW : SISFOH_CSE
NEW nan_category:  SISFOH_CSE
(128114, 134)

```

[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
