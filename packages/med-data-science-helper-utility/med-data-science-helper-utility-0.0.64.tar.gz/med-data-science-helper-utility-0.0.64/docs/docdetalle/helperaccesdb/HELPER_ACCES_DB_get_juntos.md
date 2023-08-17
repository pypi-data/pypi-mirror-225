Función **GET_JUNTOS**
==============================
<p1>Función que retorna un Dataframe de la base de *JUNTOS* para el cual se requiere los parámetros de AÑO y CACHE, se requiere que previamente se haya definido la ruta principal en la carpeta *config* archivo *config.txt* dependiendo donde se encuentre la arquitectura del Data Ware House.</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con dos parámetros principales, los cuales se detallan a continuación</p>

```Python

helper_acces_db.get_juntos(anio=2022, cache=False)

```

<p1><strong>anio</strong> (Requerido): Año de procesamiento de la base de JUNTOS.</p1>

<p1><strong>cache</strong> : Flag para cargar la información guardada en CACHE.</p1>



**<h2>Retornos</h2>**

<p1><strong>df_juntos</strong> : Dataframe que contiene información de JUNTOS para el año definido como input.</p1>
<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import pandas as pd
from med_data_science_helper import helper_acces_db as hadb

BD_JUNTOS = hadb.get_juntos(anio=2022, cache=False)

print(f"Shape del DataFrame de prueba JUNTOS: \n * {BD_JUNTOS.shape}")

```


**<h3>Output :</h3>**

```Python

Shape del DataFrame de prueba JUNTOS: 
 * (233671, 16)

```



[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ [Ir al siguiente](../helperaccesdb/HELPER_ACCES_DB_set_macro_region.md)
