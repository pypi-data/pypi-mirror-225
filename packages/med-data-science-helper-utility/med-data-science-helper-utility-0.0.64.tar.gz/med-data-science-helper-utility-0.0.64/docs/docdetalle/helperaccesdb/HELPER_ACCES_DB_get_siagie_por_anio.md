Función **get_siagie_por_anio**
==============================
<p1>Función que retorna un Dataframe de la base de *JUNTOS* para el cual se requiere los parámetros de AÑO y CACHE, se requiere que previamente se haya definido la ruta principal en la carpeta *config* archivo *config.txt* dependiendo donde se encuentre la arquitectura del Data Ware House.</p1>

**<h2>Parámetros</h2>**
<p> Esta función cuenta con dos parámetros principales, los cuales se detallan a continuación</p>

```Python

helper_acces_db.get_siagie_por_anio(anio=2022)

```

<p1><strong>anio</strong> (Requerido): Año de procesamiento de la base de JUNTOS.</p1>

<p1><strong>id_grado</strong> : <strong>*int, default None*</strong></p1>

- Se emplea para retornar los registros cuyo identificador de grado coincidan únicamente con  id_grado. 
- No se realiza ningún filtro cuando es id_grado None.

<p1><strong>id_grado_list</strong> : <strong>*[], default None*</strong></p1>

- Se emplea para retornar los registros cuyo identificador de grado se encuentra presente en la lista id_grado_list.
- No se realiza ningún filtro cuando es id_grado_list es None.

<p1><strong>modalidad</strong> : <strong>*str, default None*</strong></p1>

- Se emplea para retornar los registros cuyo código de modalidad coincida únicamente con modalidad.
- No se realiza ningún filtro cuando es modalidad es None.

<p1><strong>modalidad_list</strong> : <strong>*[], default None*</strong> </p1>

- Se emplea para retornar los registros cuyo código de modalidad se encuentra presente en la lista modalidad_list.
- No se realiza ningún filtro cuando es modalidad_list es None.

<p1><strong>dtypes_columns</strong> : <strong>*Type name or dict of column</strong> </p1>

- Se emplea para retornar los registros cuyo código de modalidad se encuentra presente en la lista modalidad_list.
- Si dtypes_columns es None entonces se asignara la siguiente typado a las siguientes variabñes: 
```javascript
{'COD_MOD': str, 
'ID_PERSONA':int,
'UBIGEO_NACIMIENTO_RENIEC':str,
'N_DOC':str,
'CODIGO_ESTUDIANTE':str,
'NUMERO_DOCUMENTO':str,
'N_DOC_APOD':str,
'CODOOII':str,
'ID_GRADO':'uint32',
'ESTADO_MAT':str,
'DSC_SECCION':str,
'ID_SECCION':str,
'SITUACION_MATRICULA':str,
'ID_NIVEL':str,
'SEXO':str,
'ANEXO': 'uint8'}
```
<p1><strong>columns_n</strong> : <strong>*[], default ['ID_PERSONA','ID_GRADO','ID_NIVEL','COD_MOD','ANEXO']*</strong> .</p1>

- Limita las columnas o variables que retornara la función 

<p1><strong>id_persona_df</strong> : <strong>*DataFrame, debe contener la variable ID_PERSONA*</strong></p1>

- Mediante id_persona_df que contiene la variable ID_PERSONA se filtraran los registros cuyo identificador de persona coinciden con ID_PERSONA

<p1><strong>id_nivel</strong> : <strong>*str, default None*</strong></p1>

- Se emplea para retornar los registros cuyo identificador de grado coincidan únicamente con  id_grado. 
- No se realiza ningún filtro cuando es id_nivel None.

<p1><strong>id_nivel_list</strong> : <strong>*[], default None*</strong></p1>

- Se emplea para retornar los registros cuyo identificador de grado se encuentra presente en la lista id_grado_list.
- No se realiza ningún filtro cuando es id_nivel_list es None.

<p1><strong>macro_region</strong> : Flag para cargar la información guardada en CACHE.</p1>

- Se emplea para retornar los registros cuyo código de modalidad coincida únicamente con modalidad.
- No se realiza ningún filtro cuando es modalidad es None.

<p1><strong>desercion</strong> : <strong>*bool, default False*</strong></p1>

 - Flag incorporar información de deserción al momento de retornar los datos.

<p1><strong>servicios</strong> : <strong>*bool, default False*</strong></p1>

 - Flag incorporar información de servicios educativos al momento de retornar los datos.
 - Las variables adicionales son: ["COD_MOD","ANEXO","GESTION","DAREACENSO",'D_TIPSSEXO','D_REGION',"CODGEO"]

<p1><strong>geo</strong> : <strong>*bool, default False*</strong></p1>

 - Flag incorporar información geografica de servicios educativos al momento de retornar los datos.
 - Las variables adicionales son: ['CODOOII','NLAT_IE', 'NLONG_IE']

<p1><strong>ser_anio_menos_1</strong> : <strong>*bool, default False*</strong></p1>

- Flag para habilitar que el cruce de registros con los del servicios educativos tambien incluya el corte de información de servicios educativos del año pasado.

<p1><strong>reduce_mem_usage</strong> : <strong>*bool, default False*</strong></p1>

 - Flag para realizar una conversión optima de todos los tipos de datos






**<h2>Retornos</h2>**

<p1><strong>df_juntos</strong> : Dataframe que contiene información de JUNTOS para el año definido como input.</p1>
<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import pandas as pd
from med_data_science_helper import helper_acces_db as hadb

ANIO_T = 2023
df_siagie_t = hadb.get_siagie_por_anio(ANIO_T=2022)

print(f"Shape del DataFrame de prueba df_siagie_t: \n * {df_siagie_t.shape}")

```


**<h3>Output :</h3>**

```Python

Shape del DataFrame de prueba get_siagie_por_anio: 
 * (X, Y)

```



[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ [Ir al siguiente](../helperaccesdb/HELPER_ACCES_DB_set_macro_region.md)
