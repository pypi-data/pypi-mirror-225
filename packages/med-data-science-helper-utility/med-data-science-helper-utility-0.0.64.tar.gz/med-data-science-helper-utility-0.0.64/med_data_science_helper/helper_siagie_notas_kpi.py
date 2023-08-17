
import numpy as np
import pandas as pd
from functools import reduce
import data_science_helper.helper_output as ho
import data_science_helper.helper_cache as hch
import med_data_science_helper.helper_acces_db as hadb
from data_science_helper import helper_dataframe as hdf
import data_science_helper.helper_general as hg
import data_science_helper.helper_clean as hc
from scipy.stats import zscore

def agregar_notas(df,key_df="",anio_df=None,anio_notas=None,df_notas=None,
                  min_alumn_zscore=10, liker=True,
                  cls_group=["NOTA","ZSCORE","AGG_CODMOD_GR","AGG_NOTA_ALUM"],notas_group="CM",
                  cache=False, cache_db_notas=False):
    
    ho.print_message('agregar_notas')

    if df is None:
        msg = "ERROR: Debe proporcionar el DF de alumnos"
        raise Exception(msg)
    
    if 'ID_PERSONA' not in df.columns:
        msg = "ERROR: El dataframe df no tiene la columna ID_PERSONA"
        raise Exception(msg)
        
    filename = 'kpis_notas'
    key_cache = hch.get_key_cache([anio_df,anio_notas,min_alumn_zscore,notas_group]+cls_group+[key_df] )
    print(key_cache)
    if cache:
        df_alum_nota = hch.get_cache(filename,key_cache)
        if df_alum_nota is not None:
            ho.print_items(df_alum_nota.columns)   

            df_join_model = pd.merge(df , df_alum_nota, left_on=['ID_PERSONA'],  right_on=['ID_PERSONA'], how='left',suffixes=('','_x'))
            return df_join_model         
        
        
        
    
    if anio_df is None:
        msg = "ERROR: Debe especificar el año del df de alumnos"
        raise Exception(msg)
    
    if anio_notas is None:
        msg = "ERROR: Debe especificar el año de las notas"
        raise Exception(msg)
    
    if anio_notas>anio_df:
        print("ERROR: El anio de notas no puede ser mayor al anio del df de alumnos")
        raise Exception(msg)
    
    if df_notas is None:
        df_notas_nacional = hadb.get_df_notas(anio_notas,liker=liker,notas_group=notas_group,cache=cache_db_notas)
    else:
        df_notas_nacional = df_notas
        #Si las notas estan por competencia, la agrupamos por area curricular

    
    postfix = ""    
    if anio_df== anio_notas:
        postfix ="T"  
    else:
        resta = anio_df - anio_notas
        postfix ="T_MENOS_{}".format(resta)  

    #df = hadb.get_siagie_por_anio(id_persona_df =df[['ID_PERSONA']], anio=anio_df,  columns_n= ['ID_PERSONA',"ID_NIVEL" , "ID_GRADO"])

    #notas del anio t_menos_n de los alumnos del anio n
    #df_notas_filtrado = pd.merge(df_notas , df['ID_PERSONA'], left_on='ID_PERSONA', right_on='ID_PERSONA', how='inner')
    print("df_notas_nacional")
    print(df_notas_nacional.columns)
    df_notas_presente = pd.merge(df_notas_nacional , df['ID_PERSONA'], left_on='ID_PERSONA', right_on='ID_PERSONA', how='inner')
    #print("df_notas_presente")
    #print(df_notas_presente.columns)
    df_ser_presente=df_notas_presente.groupby(['COD_MOD', 'ANEXO']).size().reset_index()[['COD_MOD', 'ANEXO']]
    #hay que optener el listado total de alumnos del anio pasado para hacer los group_by respectivos con la data total de n-1.
    #estos alumnos deben pertenecer a los mismos servicios que los alumnos del anio n
    df_notas_alum_completo = pd.merge(df_notas_nacional , df_ser_presente, left_on=['COD_MOD','ANEXO'], 
                          right_on=['COD_MOD','ANEXO'], how='inner')

    df_id_persona_total = df_notas_alum_completo[['ID_PERSONA']].drop_duplicates()
    df_temp = hadb.get_siagie_por_anio(anio=anio_notas,  id_persona_df =df_id_persona_total,  columns_n= ['ID_PERSONA',"ID_NIVEL" , "ID_GRADO"])

    df_notas_alum_completo = pd.merge(df_notas_alum_completo , df_temp, left_on=['ID_PERSONA'], right_on=['ID_PERSONA'], how='inner')
     
    df_notas_alum_completo = hdf.reduce_mem_usage(df_notas_alum_completo)
    #df_notas_presente = hdf.reduce_mem_usage(df_notas_presente)
    
    df_alum_nota = get_df_final_notas_alumn(df[['ID_PERSONA']],df_notas_alum_completo,postfix,min_alumn_zscore,cls_group,notas_group)

    df_alum_nota = hdf.reduce_mem_usage(df_alum_nota)
 
 
    column_j_alum_not = ['ID_PERSONA']   
    
    list_area_letter = hadb.get_list_area_letter(notas_group)
    for a_l in list_area_letter:       
        df_alum_nota.rename(columns={get_NC(a_l): get_NC(a_l,postfix)}, inplace=True)
        df_alum_nota.rename(columns={get_MN(a_l): get_MN(a_l,postfix)}, inplace=True)
        df_alum_nota.rename(columns={get_SN(a_l): get_SN(a_l,postfix)}, inplace=True)
        
    df_alum_nota.rename(columns={'TOTAL_CURSOS_X_ALUMNO': 'TOTAL_CURSOS_X_ALUMNO_'+postfix}, inplace=True)                  
    df_alum_nota.rename(columns={'TOTAL_CURSOS_VALIDOS_X_ALUMNO': 'TOTAL_CURSOS_VALIDOS_X_ALUMNO_'+postfix}, inplace=True)                  
    df_alum_nota.rename(columns={'TOTAL_CURSOS_APROBADOS_X_ALUMNO': 'TOTAL_CURSOS_APROBADOS_X_ALUMNO_'+postfix}, inplace=True)                  
    df_alum_nota.rename(columns={'MEAN_CURSOS_X_ALUMNO': 'MEAN_CURSOS_X_ALUMNO_'+postfix}, inplace=True)                  
    df_alum_nota.rename(columns={'STD_CURSOS_X_ALUMNO': 'STD_CURSOS_X_ALUMNO_'+postfix}, inplace=True)                  
          
    if 'TOTAL_ALUMNOS_X_CODMOD_NVL_GR' in df_alum_nota:
        del df_alum_nota['TOTAL_ALUMNOS_X_CODMOD_NVL_GR']

    notas_selected = list_area_letter
        
    list_cls = []
    #print("**********COLUMNAS GENERADAS****************")
    for group in cls_group:
        if group == "NOTA":
            #print("NOTA")
            list_notas_cls = df_alum_nota.loc[:,df_alum_nota.columns.str.startswith('NOTA_')].columns
            notas_selected_ = get_notas_prefix_by_gp("NOTA_",notas_selected)         
            sub_list = [sa for sa in list_notas_cls if any(sb in sa for sb in notas_selected_)]
            #print(sub_list)
            list_cls.append(sub_list)
            #print("*******************************************************")
        if group == "ZSCORE":
            #print("ZSCORE")
            list_zscore_cls = df_alum_nota.loc[:,df_alum_nota.columns.str.contains('Z_NOTA')].columns    
            notas_selected_ = get_notas_prefix_by_gp("Z_NOTA_",notas_selected) 
            sub_list = [sa for sa in list_zscore_cls if any(sb in sa for sb in notas_selected_)]
            #print(sub_list)
            list_cls.append(sub_list)
            #print("********************************************************")
        if group == "AGG_CODMOD_GR":
            #print("AGG_CODMOD_GR")
            list_agg_codmod_cls = df_alum_nota.loc[:,df_alum_nota.columns.str.contains('CODMOD_NVL_GR')].columns 
            notas_selected_ = [ s + '_X_CODMOD_NVL_GR' for s in notas_selected ]             
            sub_list = [sa for sa in list_agg_codmod_cls if any(sb in sa for sb in notas_selected_)]
            #print(sub_list)
            list_cls.append(sub_list)
            #print("*********************************************************")
        if group == "AGG_NOTA_ALUM":
            #print("AGG_NOTA_ALUM")
            sub_list = df_alum_nota.loc[:,df_alum_nota.columns.str.contains('CURSOS')].columns
            #print(sub_list)
            list_cls.append(sub_list)
        if group == "RANK":
            #print("AGG_NOTA_ALUM")
            sub_list = df_alum_nota.loc[:,df_alum_nota.columns.str.contains('RANK')].columns
            #print(sub_list)
            list_cls.append(sub_list)
            #print("*********************************************************")
            
             
    
    list_cls = hg.flat_list(list_cls) 
    #print("----------final--------------")
    #print(list_cls)
    #print("----------final--------------")
    
    ho.print_items(list_cls,excepto=[])
 
    
    list_cls.append('ID_PERSONA')   
    
    hch.save_cache(df_alum_nota[list_cls],filename,key_cache)
    
    
    df_join_model = pd.merge(df , df_alum_nota[list_cls], left_on=['ID_PERSONA'], 
                             right_on=column_j_alum_not, how='left',suffixes=('','_x'))

    df_join_model = hdf.reduce_mem_usage(df_join_model)
    
    #creando dummy que indica si el zscore esta nullo o no
    list_area_letter = notas_selected
    for a_l in list_area_letter:
        if ("ZSCORE" in cls_group): 
            hc.agregar_na_cls(df_join_model,get_ZN(a_l,postfix))
        
    return df_join_model


    
def get_notas_prefix_by_gp(prefix,notas_selected):

    notas_con_prefijo = [prefix + s for s in notas_selected ] 
    return notas_con_prefijo


    '''
    cm_notas = ["C","M"]
    short_notas = cm_notas + ["F","R"]
    B0_notas = ["P","T","Y","S","L"]
    F0_notas = ["E","D","G","I","A","H","B"]
    full_notas = short_notas+B0_notas+F0_notas
    B0_notas = short_notas + B0_notas
    F0_notas = short_notas + F0_notas   
    
    if notas_cls=="SHORT":
        common_zscore = [prefix + s for s in short_notas ] 
    elif notas_cls=="FULL":
        common_zscore = [prefix + s for s in full_notas ] 
    elif notas_cls=="B0":
        common_zscore = [prefix + s for s in B0_notas ] 
    elif notas_cls=="F0":
        common_zscore = [prefix + s for s in F0_notas ] 
    elif notas_cls=="CM":
        common_zscore = [prefix + s for s in cm_notas ] 
    
    return common_zscore
    '''


def get_notas_by_gp(notas_gp):
    cm_notas = ["C","M"]
    short_notas = cm_notas + ["F","R"]
    B0_notas = ["P","T","Y","S","L"]
    F0_notas = ["E","D","G","I","A","H","B"]
    full_notas = short_notas+B0_notas+F0_notas
    B0_notas = short_notas + B0_notas
    F0_notas = short_notas + F0_notas  
    
    if notas_gp=="COMMON":
        notas  = short_notas
    elif notas_gp=="FULL":
        notas  = full_notas 
    elif notas_gp=="B0":
        notas  = B0_notas
    elif notas_gp=="F0":
        notas  = F0_notas
    elif notas_gp=="CM":
        notas  = cm_notas
        
    return notas




def get_df_final_notas_alumn(df_alumnos,df_notas_alum_n_mes_1,postfix,min_alumn,cls_group,notas_group):

    def zscore_with_rounding(x, decimals=5):

        if x.notna().any():  # Verificar si al menos un valor no es NaN en el grupo           
            z_scores = zscore(x.dropna())
            z_scores_rounded = np.round(z_scores, decimals=decimals)
            result = pd.Series(np.nan, index=x.index)  # Crear un Series con NaN en todos los índices
            result.loc[x.index] = z_scores_rounded  # Asignar los valores del z-score en los índices correspondientes
            return result
        else:
            return x
    
    #get_df_por_alum(df_notas_f,notas_group="",cls_group=[],group_by=['COD_MOD','ANEXO','ID_PERSONA']):

    #df_a = get_df_por_alum(df_notas_f=df_notas_f,notas_group = notas_group,cls_group=cls_group,group_by=['COD_MOD','ANEXO','ID_GRADO','ID_PERSONA'])
    df_a = get_df_por_alum(df_notas_f=df_notas_alum_n_mes_1,notas_group = notas_group,cls_group=cls_group,group_by=['COD_MOD','ANEXO','ID_GRADO','ID_PERSONA'])
    
    df_a.reset_index(inplace=True)
    df_a['COD_MOD']=df_a['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    df_a['ANEXO']=df_a['ANEXO'].astype('int')

    if ("ZSCORE"  in cls_group or "AGG_CODMOD_GR"  in cls_group or "AGG_NOTA_ALUM"  in cls_group):

        list_area_letter = hadb.get_list_area_letter(notas_group)
        
        var_ranking = f'RANK_CODMOD_ID_GR_{postfix}'
        df_a[var_ranking] = df_a.groupby(["COD_MOD","ANEXO","ID_GRADO"])["MEAN_CURSOS_X_ALUMNO"].rank(ascending=False, method='dense')
        #df['sub_group_rank'] = df.groupby('type')['AvgBill'].rank(ascending=False,method = "dense")
        #calculamos el z score por alumno a nivel de grado servicio
        for a_l in list_area_letter:
     
            df_a[get_ZN_I(a_l,postfix)] = 1

            # Calcular el número de estudiantes por cada "codigo de aula" y establecer NaN para aquellos con menos de 3 estudiantes
            VAR_TOTAL_CURSO = 'TOTAL_'+get_NC(a_l)
            df_a[VAR_TOTAL_CURSO] = df_a.groupby(["COD_MOD","ANEXO","ID_GRADO"])[get_NC(a_l)].transform(lambda x: x.dropna().count())
 
            df_a.loc[df_a[VAR_TOTAL_CURSO] < min_alumn, VAR_TOTAL_CURSO] = np.nan

            # Calcular el Z-score a nivel de "codigo de aula" para los registros correspondientes
            df_a.loc[df_a[VAR_TOTAL_CURSO] >= min_alumn, get_ZN_I(a_l,postfix)] = 0
            print("4444444444444444444444444444444444444444444444444")
            #df_a[get_ZN(a_l,postfix)] = -1
            df_a[get_ZN(a_l,postfix)] = np.where(
                df_a[VAR_TOTAL_CURSO] >= min_alumn,
                df_a.groupby(["COD_MOD","ANEXO","ID_GRADO"])[get_NC(a_l)].transform(zscore_with_rounding),
                np.nan
            )
            print("5555555555555555555555555555555555555555555555555")
            # Calcular el Z-score a nivel de "codigo de colegio" para los registros restantes
            df_a[get_ZN(a_l,postfix)] = np.where(
                df_a[get_ZN_I(a_l,postfix)] == 1,
                df_a.groupby(["ID_GRADO"])[get_NC(a_l)].transform(zscore_with_rounding),
                df_a[get_ZN(a_l,postfix)]
            )
            print("666666666666666666666666666666666666666666666666")

    #nos quedamos con las notas en el ultimo servicio cursado
    df_a.drop_duplicates(subset ="ID_PERSONA", keep = "last", inplace = True)

    df_alumnos = pd.merge(df_alumnos, df_a , left_on="ID_PERSONA", right_on = "ID_PERSONA" , how="left")

    return df_alumnos





def get_df_por_alum(df_notas_f,notas_group="",cls_group=[],group_by=['COD_MOD','ANEXO','ID_PERSONA']):
    
    
    if notas_group == 'CM':
        
        dic_valores = {
         'NOTA_C_X_ALUMNO' : np.where(df_notas_f['DA']=='C',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_M_X_ALUMNO' : np.where(df_notas_f['DA']=='M',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
        } 
        agg_config = {
         'NOTA_C_X_ALUMNO':'mean',
         'NOTA_M_X_ALUMNO':'mean', 
        }  
        
    elif notas_group == 'COMMON':
        
        dic_valores = {
         'NOTA_C_X_ALUMNO' : np.where(df_notas_f['DA']=='C',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_M_X_ALUMNO' : np.where(df_notas_f['DA']=='M',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_F_X_ALUMNO' : np.where(df_notas_f['DA']=='F',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_R_X_ALUMNO' : np.where(df_notas_f['DA']=='R',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
        } 
        agg_config = {
         'NOTA_C_X_ALUMNO':'mean',
         'NOTA_M_X_ALUMNO':'mean', 
         'NOTA_F_X_ALUMNO':'mean',
         'NOTA_R_X_ALUMNO':'mean',
        }
    elif notas_group == 'B0':
        
        dic_valores = {
         'NOTA_C_X_ALUMNO' : np.where(df_notas_f['DA']=='C',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_M_X_ALUMNO' : np.where(df_notas_f['DA']=='M',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_F_X_ALUMNO' : np.where(df_notas_f['DA']=='F',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_R_X_ALUMNO' : np.where(df_notas_f['DA']=='R',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         
         'NOTA_P_X_ALUMNO' : np.where(df_notas_f['DA']=='P',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_T_X_ALUMNO' : np.where(df_notas_f['DA']=='T',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_Y_X_ALUMNO' : np.where(df_notas_f['DA']=='Y',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_S_X_ALUMNO' : np.where(df_notas_f['DA']=='S',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_L_X_ALUMNO' : np.where(df_notas_f['DA']=='L',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
        } 
        agg_config = {
         'NOTA_C_X_ALUMNO':'mean',
         'NOTA_M_X_ALUMNO':'mean', 
         'NOTA_F_X_ALUMNO':'mean',
         'NOTA_R_X_ALUMNO':'mean',
         
         'NOTA_P_X_ALUMNO':'mean',
         'NOTA_T_X_ALUMNO':'mean',
         'NOTA_Y_X_ALUMNO':'mean',
         'NOTA_S_X_ALUMNO':'mean',
         'NOTA_L_X_ALUMNO':'mean',
        }
    elif notas_group == 'F0':
        
        dic_valores = {
         'NOTA_C_X_ALUMNO' : np.where(df_notas_f['DA']=='C',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_M_X_ALUMNO' : np.where(df_notas_f['DA']=='M',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_F_X_ALUMNO' : np.where(df_notas_f['DA']=='F',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_R_X_ALUMNO' : np.where(df_notas_f['DA']=='R',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         
         'NOTA_E_X_ALUMNO' : np.where(df_notas_f['DA']=='E',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_D_X_ALUMNO' : np.where(df_notas_f['DA']=='D',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_G_X_ALUMNO' : np.where(df_notas_f['DA']=='G',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_I_X_ALUMNO' : np.where(df_notas_f['DA']=='I',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_A_X_ALUMNO' : np.where(df_notas_f['DA']=='A',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_H_X_ALUMNO' : np.where(df_notas_f['DA']=='H',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_B_X_ALUMNO' : np.where(df_notas_f['DA']=='B',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  , 
        } 
        agg_config = {
         'NOTA_C_X_ALUMNO':'mean',
         'NOTA_M_X_ALUMNO':'mean', 
         'NOTA_F_X_ALUMNO':'mean',
         'NOTA_R_X_ALUMNO':'mean',
         
         'NOTA_E_X_ALUMNO':'mean',
         'NOTA_D_X_ALUMNO':'mean',
         'NOTA_G_X_ALUMNO':'mean',
         'NOTA_I_X_ALUMNO':'mean',
         'NOTA_A_X_ALUMNO':'mean',
         'NOTA_H_X_ALUMNO':'mean',
         'NOTA_B_X_ALUMNO':'mean',
        }
    else:
        dic_valores = {
         'NOTA_C_X_ALUMNO' : np.where(df_notas_f['DA']=='C',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_M_X_ALUMNO' : np.where(df_notas_f['DA']=='M',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_P_X_ALUMNO' : np.where(df_notas_f['DA']=='P',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_T_X_ALUMNO' : np.where(df_notas_f['DA']=='T',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_Y_X_ALUMNO' : np.where(df_notas_f['DA']=='Y',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_F_X_ALUMNO' : np.where(df_notas_f['DA']=='F',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_R_X_ALUMNO' : np.where(df_notas_f['DA']=='R',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_S_X_ALUMNO' : np.where(df_notas_f['DA']=='S',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_L_X_ALUMNO' : np.where(df_notas_f['DA']=='L',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_E_X_ALUMNO' : np.where(df_notas_f['DA']=='E',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_D_X_ALUMNO' : np.where(df_notas_f['DA']=='D',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_G_X_ALUMNO' : np.where(df_notas_f['DA']=='G',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_I_X_ALUMNO' : np.where(df_notas_f['DA']=='I',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_A_X_ALUMNO' : np.where(df_notas_f['DA']=='A',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_H_X_ALUMNO' : np.where(df_notas_f['DA']=='H',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         'NOTA_B_X_ALUMNO' : np.where(df_notas_f['DA']=='B',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,    
         'NOTA_O_X_ALUMNO' : np.where(df_notas_f['DA']=='O',  df_notas_f['NOTA_AREA_REGULAR'],np.NaN)  ,
         
            
        }
        
        agg_config = {
         'NOTA_C_X_ALUMNO':'mean',
         'NOTA_M_X_ALUMNO':'mean',  
         'NOTA_P_X_ALUMNO':'mean', 
         'NOTA_T_X_ALUMNO':'mean',
         'NOTA_Y_X_ALUMNO':'mean',
         'NOTA_F_X_ALUMNO':'mean',
         'NOTA_R_X_ALUMNO':'mean',
         'NOTA_S_X_ALUMNO':'mean',
         'NOTA_L_X_ALUMNO':'mean',
         
         'NOTA_E_X_ALUMNO':'mean',
         'NOTA_D_X_ALUMNO':'mean',
         'NOTA_G_X_ALUMNO':'mean',
         'NOTA_I_X_ALUMNO':'mean',
         'NOTA_A_X_ALUMNO':'mean',
         'NOTA_H_X_ALUMNO':'mean',
         'NOTA_B_X_ALUMNO':'mean',
         
         'NOTA_O_X_ALUMNO':'mean',         

        }
        
    if "AGG_NOTA_ALUM" in cls_group:

        dic_valores['TOTAL_CURSOS_X_ALUMNO']=1
        dic_valores['TOTAL_CURSOS_VALIDOS_X_ALUMNO']=np.where((df_notas_f['NOTA_AREA_REGULAR']>=0),1,0)
        dic_valores['TOTAL_CURSOS_APROBADOS_X_ALUMNO']=np.where((df_notas_f['NOTA_AREA_REGULAR']>=11),1,0) 

        
        agg_config['TOTAL_CURSOS_X_ALUMNO']='sum'
        agg_config['TOTAL_CURSOS_VALIDOS_X_ALUMNO']='sum'
        agg_config['TOTAL_CURSOS_APROBADOS_X_ALUMNO']='sum'

    dic_valores['MEAN_CURSOS_X_ALUMNO']=np.where((df_notas_f['NOTA_AREA_REGULAR']>=0),df_notas_f['NOTA_AREA_REGULAR'],0)
    dic_valores['STD_CURSOS_X_ALUMNO']=np.where((df_notas_f['NOTA_AREA_REGULAR']>=0),df_notas_f['NOTA_AREA_REGULAR'],0)      
    agg_config['MEAN_CURSOS_X_ALUMNO']='mean'
    agg_config['STD_CURSOS_X_ALUMNO']='std'
          
    dataSet_por_alumno = df_notas_f.assign(
     **dic_valores        
    ).groupby(group_by).agg(agg_config)
    

    return dataSet_por_alumno




def get_NC(area,postfix=None):
    if postfix is None :
        return 'NOTA_{}_X_ALUMNO'.format(area)
    else:
        return 'NOTA_{}_X_ALUMNO_{}'.format(area,postfix)

def get_ZN_I(area,postfix=None):
    return 'IMP_Z_NOTA_{}_{}'.format(area,postfix)

def get_ZN(area,postfix=None):
    return 'Z_NOTA_{}_{}'.format(area,postfix)

def get_MN(area,postfix=None):
    if postfix is None :
        return 'MEAN_NOTA_{}_X_CODMOD_NVL_GR'.format(area)
    else:
        return 'MEAN_NOTA_{}_X_CODMOD_NVL_GR_{}'.format(area,postfix)

def get_SN(area,postfix=None):
    if postfix is None :
        return 'STD_NOTA_{}_X_CODMOD_NVL_GR'.format(area)
    else:
        return 'STD_NOTA_{}_X_CODMOD_NVL_GR_{}'.format(area,postfix)