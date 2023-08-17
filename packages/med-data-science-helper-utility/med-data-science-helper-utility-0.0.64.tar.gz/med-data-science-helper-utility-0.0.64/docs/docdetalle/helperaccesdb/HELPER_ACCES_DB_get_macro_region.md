Función **GET_MACRO_REGION**
==============================
<p1>Función que retorna la macro región requerida mediante el *KEY*, esta toma por defecto las definidas en el archivo *base.txt* definidos en configuración.</p1>

**<h2>Parámetros</h2>**
<p>Esta función requiere de un parámetro que se define a continuación:</p>

```Python

helper_acces_db.get_macro_region( macro )

```
<p1><strong>macro</strong> (Requerido): Nombre de la macro región que se desea obtener como retorno.</p1>


**<h2>Retornos</h2>**

<p1><strong>data</strong> : Retorna una lista con las regiones correspondientes a la *MACRO*.</p1>
<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import pandas as pd
from med_data_science_helper import helper_acces_db as hadb

REGIONES = hadb.get_macro_region("norte")
print(f"Regiones Norte: {REGIONES}")

REGIONES = hadb.get_macro_region("oriente")
print(f"Regiones Oriente: {REGIONES}")

```


**<h3>Output :</h3>**

```Python

Regiones Norte: ['DRE ANCASH', 'DRE CAJAMARCA', 'DRE LA LIBERTAD', 'DRE LAMBAYEQUE', 'DRE PIURA', 'DRE TUMBES']
Regiones Oriente: ['DRE AMAZONAS', 'DRE LORETO', 'DRE SAN MARTIN', 'DRE UCAYALI']

```



[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ [Ir al siguiente](../helperaccesdb/HELPER_ACCES_DB_get_macro_regiones.md)

