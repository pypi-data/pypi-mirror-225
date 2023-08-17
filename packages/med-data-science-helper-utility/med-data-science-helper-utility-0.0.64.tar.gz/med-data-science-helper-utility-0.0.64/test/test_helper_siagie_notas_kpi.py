
import pandas as pd
import numpy as np
import med_data_science_helper.helper_acces_db as hadb
import med_data_science_helper.helper_siagie_kpi as hsk
import med_data_science_helper.helper_siagie_notas_kpi as hsnk
import med_data_science_helper.helper_terceros_kpi as htk
from scipy.stats import zscore


ANIO_T = 2022
ANIO_T_MENOS_1 = ANIO_T-1
modalidad = "EBR"
df_siagie_t = hadb.get_siagie_por_anio(ANIO_T,  modalidad=modalidad, id_nivel="B0",  id_grado=5,
                                       columns_n= ['ID_PERSONA',"ID_NIVEL" , "ID_GRADO",
                                                   'COD_MOD','ANEXO'],macro_region="norte")


print(df_siagie_t.shape)



df_reg = hsnk.agregar_notas(df_siagie_t,key_df="{}_{}_".format("4","Peru"), liker=True,
                            anio_df=ANIO_T,anio_notas=ANIO_T_MENOS_1, notas_group="CM", 
                            cls_group=["ZSCORE","RANK"],cache=False,cache_db_notas=True) 

print(df_reg.shape)


print(df_reg.columns)
df_reg.RANK_CODMOD_ID_GR_T_MENOS_1.isna().value_counts()


df_reg.Z_NOTA_C_T_MENOS_1.isna().value_counts()
df_reg.IMP_Z_NOTA_C_T_MENOS_1.value_counts()
df_reg.NA_Z_NOTA_C_T_MENOS_1.value_counts()


df_reg.Z_NOTA_C_T_MENOS_1.hist()

df_reg.columns

hadb.get_list_area_letter("B0")


notas = hadb.get_df_notas(2020,liker=True,notas_group="B0",cache=True,rt=False)
notas.shape
#(16282625, 5) 

df_notas = hadb.get_df_notas(2019,liker=True,notas_group="B0",cache=True,rt=True)
df_notas.head()
df_notas.NOTA_AREA_REGULAR.value_counts()
df_notas.ID_PERSONA.min()
url_liker = hadb.get_path_BD_siagie_procesado()+"\\NOTAS_POR_ALUMNO_LIKERT_2021.csv"
dtype = {'COD_MOD':str,'ANEXO':np.int8,'DA':str} 
df_liker = pd.read_csv(url_liker,nrows=1000,encoding='utf-8', dtype=dtype)
df_liker.columns


