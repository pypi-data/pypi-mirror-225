Función **GET_COEFF**
==============================
<p1>Función que realiza una regresión lineal al arreglo de valores suministrados.</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con dos parámetros principales, los cuales se detallan a continuación</p>

```Python


helper_siagie_kpi.get_coeff(row, min_vars = 3)

```

<p1><strong>row</strong> (Requerido): Un arreglo  valores, puede ser tambien un columna de un dataframe.</p1>

<p1><strong>min_vars</strong> : El arreglo debe tener una cantidad de valores mayor a este parametro para poder realizar la regresión, de lo contrario devuelve un arreglo de nulos.</p1>

**<h2>Retornos</h2>**

<p1>Se la regresión lineal que se obtiene: <strong>Y = a*X + b</strong></p1>

<p1><strong>slope</strong> : Pendiente (a) de la regresión lineal que se obtiene.</p1>

<p1><strong>intercept_</strong> : Intercepto (b) de la regresión lineal con eje principal.</p1>

<p1><strong>r2_score</strong> : Un estadístico que nos indica que tanto se aproxima el modelo obtenido a los datos suministrados. </p1>
<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk

# Los nombres de las columnas son referenciales
df_resultado[["Slope","Intercept","R2_score"]] = df_resultado["Columna_Calcular"].apply(hsk.get_coeff, axis=1)

```


**<h3>Output :</h3>**

```Python
pd.Series([slope , intercept_,r2_score])

# Esos valores se pueden asignas a las columnas de un dataframe
pd.Series([slope , intercept_,r2_score]) = df_resultado[["Slope","Intercept","R2_score"]]

```



[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
