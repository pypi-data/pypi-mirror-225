Función **GENERAR_KPIS_HISTORICOS**
==============================
<p1>Función que permite generar nuevos indicadores a partir de los valores de las variables categóricas o dicotómicas del SIAGIE. Los indicadores generados están conformados en 2 grupos. Para un determinado rango de años, se calcula el Max, Min, Mean y Std para cada valor de las variables categóricas o dicotómicas especificadas. Asimismo, se generan nuevas variables a partir de los valores de cada variable categórica o dicotómica por cada año del periodo de tiempo especificado.</p1> 

**<h2>Parámetros</h2>**
<p> Esta función cuenta con ocho parámetros, los cuales se detallan a continuación</p>

```Python

helper_siagie_kpi.generar_kpis_historicos(df,key_df="", anio_df=None, anio_h=None, cls_json=None,
                                        t_anios=0, cache=False,retornar=True):

```

<p1><strong>df</strong> (Requerido): Dataframe de estudiantes que tenga un campo identificador, ejemplo: ID_PERSONA.</p1>

<p1><strong>key_df</strong>: String, usado para generar una clave en caso se desee guardar la información en un archivo cache.</p1>

<p1><strong>anio_df</strong>: Número entero que representa el año de los datos del dataframe <strong>df</strong>.</p1>

<p1><strong>anio_h</strong>: Número entero que indica el año desde el cual se tomará en cuenta para calcular un histórico.</p1>

<p1><strong>cls_json</strong>: Parámetro en formato json para indicar las variables por los cuales se calculará los indicadores historicos.</p1>

<p1><strong>t_anios</strong>: Número entero que indica la cantidad de años que se tomará en cuenta para el histórico.</p1>

<p1><strong>cache</strong>: Flag para almacenar la información guardada en CACHE de manera temporal. es importante en caso se desea ejecutar la función repetidas veces.</p1>


**<h2>Retornos</h2>**

<p1><strong>df</strong> : Retorna un dataframe como valores históricos y acumulados en múltiples años a partir de lo especificado a partir del parámetro <strong>cls_json</strong> y <strong>t_anios</strong>.</p1>

<p1> </p1>

**<h2>Ejemplo de uso</h2>**
<p1> A continuación, se muestra un código de ejemplo sobre el uso de la función.</p1>

**<h3>Código :</h3>**
```Python

import med_data_science_helper.helper_siagie_kpi as hsk

anio=2020 
anio_h_1 = anio-3
kpis_hist = 3
cls_json = {}
cls_json['SITUACION_FINAL']=["APROBADO","DESAPROBADO"]
cls_json['SF_RECUPERACION']=["APROBADO","DESAPROBADO"]
cls_json['SITUACION_MATRICULA']=["PROMOVIDO","REPITE","INGRESANTE","REENTRANTE"]

# df_reg_temp: Dataframe que contiene los datos de los estudiantes
df_reg = hsk.generar_kpis_historicos(df_reg_temp,key_df="{}_{}".format(key_grupo_grados,macro_region),
                                    anio_df=anio, anio_h=anio_h_1, cls_json=cls_json, t_anios=kpis_hist, cache=True)

```


**<h3>Output :</h3>**

<p1><strong>df</strong> : Retornará un Dataframe basado en el valor del parámetro "cls_json".</p1>

```Python
#df: 
print(df.shape)

# Impresión durante la ejecucion del DataFrame df de prueba para el periodo 2020 y 3 años de histórico: 
generar_kpis_historicos
key_2020_2019_3_SI_AP_DE_SF_AP_DE_SI_PR_RE_IN_RE__EBR_B0_9_centro
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_historicos.h5
No hay cache disponible para los parametros ingresados
NEW : SITUACION_FINAL_APROBADO_T_MENOS_1
NEW : SITUACION_FINAL_DESAPROBADO_T_MENOS_1
NEW : SF_RECUPERACION_APROBADO_T_MENOS_1
NEW : SF_RECUPERACION_DESAPROBADO_T_MENOS_1
NEW : SITUACION_MATRICULA_PROMOVIDO_T_MENOS_1
NEW : SITUACION_MATRICULA_REPITE_T_MENOS_1
NEW : SITUACION_MATRICULA_INGRESANTE_T_MENOS_1
NEW : SITUACION_MATRICULA_REENTRANTE_T_MENOS_1
NEW : SITUACION_FINAL_APROBADO_T_MENOS_2
NEW : SITUACION_FINAL_DESAPROBADO_T_MENOS_2
NEW : SF_RECUPERACION_APROBADO_T_MENOS_2
NEW : SF_RECUPERACION_DESAPROBADO_T_MENOS_2
NEW : SITUACION_MATRICULA_PROMOVIDO_T_MENOS_2
NEW : SITUACION_MATRICULA_REPITE_T_MENOS_2
NEW : SITUACION_MATRICULA_INGRESANTE_T_MENOS_2
NEW : SITUACION_MATRICULA_REENTRANTE_T_MENOS_2
NEW : SITUACION_FINAL_APROBADO_T_MENOS_3
NEW : SITUACION_FINAL_DESAPROBADO_T_MENOS_3
NEW : SF_RECUPERACION_APROBADO_T_MENOS_3
NEW : SF_RECUPERACION_DESAPROBADO_T_MENOS_3
NEW : SITUACION_MATRICULA_PROMOVIDO_T_MENOS_3
NEW : SITUACION_MATRICULA_REPITE_T_MENOS_3
NEW : SITUACION_MATRICULA_INGRESANTE_T_MENOS_3
NEW : SITUACION_MATRICULA_REENTRANTE_T_MENOS_3
NEW : TOTAL_SITUACION_FINAL_APROBADO
NEW : MEAN_SITUACION_FINAL_APROBADO
NEW : STD_SITUACION_FINAL_APROBADO
NEW : MIN_SITUACION_FINAL_APROBADO
NEW : MAX_SITUACION_FINAL_APROBADO
NEW : TOTAL_SITUACION_FINAL_DESAPROBADO
NEW : MEAN_SITUACION_FINAL_DESAPROBADO
NEW : STD_SITUACION_FINAL_DESAPROBADO
NEW : MIN_SITUACION_FINAL_DESAPROBADO
NEW : MAX_SITUACION_FINAL_DESAPROBADO
NEW : TOTAL_SF_RECUPERACION_APROBADO
NEW : MEAN_SF_RECUPERACION_APROBADO
NEW : STD_SF_RECUPERACION_APROBADO
NEW : MIN_SF_RECUPERACION_APROBADO
NEW : MAX_SF_RECUPERACION_APROBADO
NEW : TOTAL_SF_RECUPERACION_DESAPROBADO
NEW : MEAN_SF_RECUPERACION_DESAPROBADO
NEW : STD_SF_RECUPERACION_DESAPROBADO
NEW : MIN_SF_RECUPERACION_DESAPROBADO
NEW : MAX_SF_RECUPERACION_DESAPROBADO
NEW : TOTAL_SITUACION_MATRICULA_PROMOVIDO
NEW : MEAN_SITUACION_MATRICULA_PROMOVIDO
NEW : STD_SITUACION_MATRICULA_PROMOVIDO
NEW : MIN_SITUACION_MATRICULA_PROMOVIDO
NEW : MAX_SITUACION_MATRICULA_PROMOVIDO
NEW : TOTAL_SITUACION_MATRICULA_REPITE
NEW : MEAN_SITUACION_MATRICULA_REPITE
NEW : STD_SITUACION_MATRICULA_REPITE
NEW : MIN_SITUACION_MATRICULA_REPITE
NEW : MAX_SITUACION_MATRICULA_REPITE
NEW : TOTAL_SITUACION_MATRICULA_INGRESANTE
NEW : MEAN_SITUACION_MATRICULA_INGRESANTE
NEW : STD_SITUACION_MATRICULA_INGRESANTE
NEW : MIN_SITUACION_MATRICULA_INGRESANTE
NEW : MAX_SITUACION_MATRICULA_INGRESANTE
NEW : TOTAL_SITUACION_MATRICULA_REENTRANTE
NEW : MEAN_SITUACION_MATRICULA_REENTRANTE
NEW : STD_SITUACION_MATRICULA_REENTRANTE
NEW : MIN_SITUACION_MATRICULA_REENTRANTE
NEW : MAX_SITUACION_MATRICULA_REENTRANTE
guardando cache
path_cache : e:\PROYECTOS\med-student-dropout-prediction\cache\kpis_historicos.h5
(128114, 129)

```



[Volver a índice](../../docsPrincipal.md ) $~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~$ 
