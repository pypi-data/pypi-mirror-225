Función **GET_PATH_BD_SIAGIE_SIN_PROCESAR**
==============================
<p1>Función que retorna la ruta de la base de datos o fuente de datos del *SIAGIE SIN PROCESAR*, se requiere que previamente se haya definido la ruta principal en la carpeta *config* archivo *config.txt* dependiendo donde se encuentre la arquitectura del Data Ware House.</p1>

**<h2>Parámetros</h2>**
<p>Esta función no requiere de parámetros.</p>

```Python

helper_acces_db.get_path_BD_siagie_sin_procesar( )

```

**<h2>Retornos</h2>**

<p1><strong>path_file</strong> : Retorna la ruta de la base de datos o la fuente de datos del SIAGIE SIN PROCESAR.</p1>
<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import pandas as pd
from med_data_science_helper import helper_acces_db as hadb

BD_PATH = hadb.get_path_BD_siagie_sin_procesar()

print(f"Ruta de la Base de datos o Fuente de datos GIAGIE: \n * {BD_PATH}")

```


**<h3>Output :</h3>**

```Python

Ruta de la Base de datos o Fuente de datos GIAGIE: 
 * E:\PROYECTOS\med-data-warehouse-structure\src\01.SIAGIE\_data_\sin_procesar

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ [Ir al siguiente](../helperaccesdb/HELPER_ACCES_DB_get_juntos.md)


