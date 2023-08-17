Función **SET_MACRO_REGION**
==============================
<p1>Función con la se puede definir el universo de Macro Regiones, en este caso el archivo tiene que tener la siguiente estructura, ubicado en la carpeta *config*:</p1>

```JSON

{
"lima": ["DRE LIMA PROVINCIAS", "DRE LIMA METROPOLITANA", "DRE CALLAO"],
"norte": ["DRE ANCASH", "DRE CAJAMARCA", "DRE LA LIBERTAD", "DRE LAMBAYEQUE", "DRE PIURA", "DRE TUMBES", "DRE AMAZONAS"],
"sur": ["DRE AREQUIPA", "DRE CUSCO", "DRE MADRE DE DIOS", "DRE MOQUEGUA", "DRE PUNO", "DRE TACNA"],
"centro": ["DRE APURIMAC", "DRE AYACUCHO", "DRE HUANCAVELICA", "DRE HUANUCO", "DRE JUNIN", "DRE PASCO", "DRE ICA"]
}

```

**<h2>Parámetros</h2>**
<p>Esta función requiere de un parámetro que se define a continuación:</p>

```Python

helper_acces_db.set_macro_region( filename )

```
<p1><strong>filename</strong> (Requerido): Nombre del archivo de Macro Regiones que se desea establecer.</p1>


**<h2>Retornos</h2>**

<p1><strong>None</strong> : No retorna ningun valor.</p1>
<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import pandas as pd
from med_data_science_helper import helper_acces_db as hadb

hadb.set_macro_region("macroregionesprueba.txt")

MACRO_REGIONES = hadb.get_macro_regiones()
print(MACRO_REGIONES)

```


**<h3>Output :</h3>**

```Python

{
    'lima': ['DRE LIMA PROVINCIAS', 'DRE LIMA METROPOLITANA', 'DRE CALLAO'],
    'norte': ['DRE ANCASH', 'DRE CAJAMARCA', 'DRE LA LIBERTAD', 'DRE LAMBAYEQUE', 'DRE PIURA', 'DRE TUMBES', 'DRE AMAZONAS'],
    'sur': ['DRE AREQUIPA', 'DRE CUSCO', 'DRE MADRE DE DIOS', 'DRE MOQUEGUA', 'DRE PUNO', 'DRE TACNA'],
    'centro': ['DRE APURIMAC', 'DRE AYACUCHO', 'DRE HUANCAVELICA', 'DRE HUANUCO', 'DRE JUNIN', 'DRE PASCO', 'DRE ICA']
}

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ [Ir al siguiente](../helperaccesdb/HELPER_ACCES_DB_get_macro_region.md)
