Función **AGREGAR_NOTAS**
==============================
<p1><p align="justify">Función que permite generar nuevos indicadores a partir información sobre indicadores de notas. Los indicadores generados están conformados en 4 grupos (NOTA, ZSCORE, AGG_CODMOD_GR y AGG_NOTA_ALUM). 
- El grupo de NOTA corresponde a las notas de cada curso obtenido por el estudiante. 
- El grupo ZSCORE es similar a los indicadores del grupo NOTA, sin embargo, los valores se encuentran escalado al z-score con relación al promedio obtenido de una determinada nota de un grado escolar de un servicio educativo. 
- El grupo AGG_CODMOD_GR corresponde indicadores sobre Mean y STD de los cursos a nivel de grado escolar de los servicios educativos. 
- Por último, el grupo AGG_NOTA_ALUM corresponde a indicadores estadísticos sobre la cantidad de cursos dispones del estudiante</p></p1> 

**<h2>Parámetros</h2>**
<p> Esta función cuenta con nueve parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.agregar_notas(df, key_df="", anio_df=None, anio_notas=None, df_notas=None,
                  min_alumn_zscore=20, cls_group=["NOTA","ZSCORE","AGG_CODMOD_GR","AGG_NOTA_ALUM"],
                  notas_group="CM", cache=False):

```
<p1><strong>df</strong> (Requerido): Dataframe de estudiantes que tenga un campo identificador, ejemplo: ID_PERSONA.</p1>

<p1><strong>key_df</strong>: String, usado para generar una clave en caso se desee guardar la información en un archivo cache.</p1>

<p1><strong>anio_df</strong>: Número entero que representa el año de los datos del dataframe <strong>df</strong>.</p1>

<p1><strong>anio_notas</strong>: Número entero que representa el año de información de las notas.</p1>

<p1><strong>df_notas</strong>  Dataframe de notas precargado con la funcion get_df_notas( anio_notas ) de helper_acces_db.py. </p1>

<p1><strong>min_alumn_zscore</strong> (Requerido): Número entero que el mínimo de numero estudiantes.</p1>

<p1><strong>cls_group</strong> Dataframe  con columna ID_PERSONA, que sirve para hacer un prefiltro.</p1>

<p1><strong>notas_group</strong> (Requerido): Un arreglo  valores, puede ser tambien un columna de un dataframe.</p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces</p1>

**<h2>Retornos</h2>**

<p1>Dado {i} Є al conjunto de las iniciales de cursos que se muestran a continuación:</p1>
```Python
{
C, #COMUNICACIÓN
M, #MATEMÁTICA
F, #EDUCACIÓN FÍSICA
R, #EDUCACIÓN RELIGIOSA

P, #PERSONAL SOCIAL
T, #CIENCIA Y TECNOLOGÍA
Y, #ARTE Y CULTURA
S, #CASTELLANO COMO SEGUNDA LENGUA
L, #COMUNICACIÓN LENGUA MATERNA

E, #HISTORIA, GEOGRAFÍA Y ECONOMÍA
D, #FORMACIÓN CIUDADANA Y CÍVICA
G, #CIENCIA, TECNOLOGÍA Y AMBIENTE
I, #INGLES
A, #ARTE
H, #PERSONA, FAMILIA Y RELACIONES HUMANAS
B, #EDUCACIÓN PARA EL TRABAJO

O, #OTROS
}
```

<p1>Además, {p} es es un postfijo que Є al siguiente conjunto:</p1>
```Python
{
T,
T_MENOS_1,
T_MENOS_2,
.
.
.
T_MENOS_N,
}
```
Los nuevos indicadores que retornara la funciones se conforman en tres grupos como se muestra a continuación:

<strong>NOTA</strong>
- NOTA_{i}_X_ALUMNO _{p} : Nota de un curso

<strong>ZSCORE</strong>

- Z_NOTA_{i}_{p}:  Z score de la nota de un curso de un alumno
- IMP_Z_NOTA_{i}_{p} : Dummy de Imputación del Z score con la media a nivel nacional de notas cunado la cantidad de alumnos es menor igual a 20 o cuando el STD de la nota de un curso en el grado – servicio es cero, empleando el STD nacional de un curso determinado.

<strong>AGG_CODMOD_GR</strong>
- MEAN_NOTA_{i}_X_CODMOD_NVL_GR_{p} : MEAN de curso en Grado de IE
- STD_NOTA_{i}_X_CODMOD_NVL_GR _{p} : STD de curso en Grado de IE

<strong>AGG_NOTA_ALUM</strong>
- TOTAL_CURSOS_X_ALUMNO_{p} : Total de cursos que tiene un alumno en el anio {p} 
- TOTAL_CURSOS_VALIDOS_X_ALUMNO_{p} : Total de cursos  validos  (con notas >=0) que tiene un alumno en el anio {p} 
- TOTAL_CURSOS_APROBADOS_X_ALUMNO_{p} : Total de cursos  aprobados  (con notas >=11) que tiene un alumno en el anio {p} 
-	MEAN_CURSOS_X_ALUMNO_{p} : Promedio de notas que tiene un alumno en el anio {p} 
-	STD_CURSOS_X_ALUMNO_{p} : Desviación Estándar de notas que tiene un alumno en el anio {p}



<p1>Se la regresión lineal que se obtiene: <strong>Y = a*X + b</strong></p1>


<p1> </p1>


**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>


**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk

anio=2020 
anio_h_1 = anio-3
macro_region="centro"

# df_reg_temp: Dataframe que contiene los datos de los estudiantes
df_reg_temp = hsk.agregar_notas(df_reg_temp,key_df="{}_{}".format(key_grupo_grados,macro_region),
                            anio_df=anio,anio_notas=anio_h_1, cls_group=["ZSCORE"],cache=True)    

```

**<h3>Output :</h3>**

<p1><strong>df</strong> : Retornará un Dataframe que contiene la nota de los estudiantes, zscore(un variable categorica de acuerdo al desempeño), y otros indicadores tales como la cantidad de materias que cursan cierto año, total de cursos aprobados, etc...</p1>

```Python
#df: 
print(df.shape)
# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 3 años de histórico:
agregar_notas
key_2020_2019_20_CM_ZSCORE_EBR_B0_9_centro
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_notas.h5
NEW : Z_NOTA_C_T_MENOS_1
NEW : Z_NOTA_M_T_MENOS_1
NEW : IMP_Z_NOTA_C_T_MENOS_1
NEW : IMP_Z_NOTA_M_T_MENOS_1
(128114, 133)

```


[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
