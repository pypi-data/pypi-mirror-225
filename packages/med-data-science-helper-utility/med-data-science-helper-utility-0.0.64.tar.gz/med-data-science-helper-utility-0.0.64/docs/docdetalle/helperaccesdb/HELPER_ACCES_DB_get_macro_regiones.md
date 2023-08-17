Función **GET_MACRO_REGIONES**
==============================
<p1>Función que retorna todas las macro regiones definidas mediante la función *set_macro_region*, esta toma por defecto las definidas en el archivo *base.txt* definidos en configuración.</p1>

**<h2>Parámetros</h2>**
<p>Esta función no requiere de parámetros.</p>

```Python

helper_acces_db.get_macro_regiones( )

```

**<h2>Retornos</h2>**

<p1><strong>data</strong> : Retorna un diccionario con listas de las macro regiones.</p1>
<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import pandas as pd
from med_data_science_helper import helper_acces_db as hadb

MACRO_REGIONES = hadb.get_macro_regiones()

print(MACRO_REGIONES)


```


**<h3>Output :</h3>**

```Python

{
    'lima_provincias': ['DRE LIMA PROVINCIAS'], 
    'lima_metro_callao': ['DRE LIMA METROPOLITANA', 'DRE CALLAO'],
    'norte': ['DRE ANCASH', 'DRE CAJAMARCA', 'DRE LA LIBERTAD', 'DRE LAMBAYEQUE', 'DRE PIURA', 'DRE TUMBES'],
    'sur': ['DRE AREQUIPA', 'DRE CUSCO', 'DRE MADRE DE DIOS', 'DRE MOQUEGUA', 'DRE PUNO', 'DRE TACNA'],
    'centro': ['DRE APURIMAC', 'DRE AYACUCHO', 'DRE HUANCAVELICA', 'DRE HUANUCO', 'DRE JUNIN', 'DRE PASCO', 'DRE ICA'],
    'oriente': ['DRE AMAZONAS', 'DRE LORETO', 'DRE SAN MARTIN', 'DRE UCAYALI']
}

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ [Ir al siguiente](../helperaccesdb/HELPER_ACCES_DB_get_path_BD.md)


