# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 12:21:41 2021

@author: User
"""

import numpy as np
import pandas as pd
from functools import reduce

import med_data_science_helper.helper_acces_db as hadb
from data_science_helper import helper_dataframe as hdf
import data_science_helper.helper_general as hg
import data_science_helper.helper_output as ho
import data_science_helper.helper_clean as hc
import data_science_helper.helper_cache as hch
from sklearn.linear_model import LinearRegression
'''
df_siagie = hadb.get_siagie_por_anio(2022,columns_n= ['ID_PERSONA'])
print(df_siagie.shape)
df = hadb.get_juntos(2019)
print(df.PERIODO.unique())
df_siagie2 = agregar_pivot_juntos(df_siagie, anio_df=2022,anio_h=2021,t_anios=3,cache=True)
print(df_siagie2.columns)
print(df_siagie2.VCC_1_T.value_counts())
print(df_siagie2.VCC_1_T_MENOS_1.value_counts())
'''



def get_coeff(row,min_vars = 3):
    

    
    # fit a row assuming points are separated by unit length and return the slope.
    model = LinearRegression()
    row = row.copy().dropna()
    
    X_array = np.arange(len(row)).reshape(-1,1)
    Y_array = row.values.reshape(-1,1)
    
    #print("X_array : ",X_array)
    #print("Y_array : ",Y_array)
    #print("Y_array size: ",len(Y_array))
    total_vars = len(Y_array)
    if total_vars<min_vars:
        return pd.Series([np.nan , np.nan,np.nan])
    else:    
        model.fit(X_array, Y_array)
        slope = model.coef_[0][0]    
        intercept_ = model.intercept_[0]
        r2_score = model.score(X_array, Y_array)
        
        return pd.Series([slope , intercept_,r2_score])
    


def generar_kpis_p_deser_by_dist(df,anio_df=None , anio_h = None,t_anios=0 ,decimals=2 , cache=False):
    
    #anio_df_menos_1 = anio_df-1
    
    ultimo_anio =anio_h- t_anios
    #ultimo_anio_data = ultimo_anio + 1    
    num = anio_df-anio_h
    
    list_df_agg = []
    
    cls_list = []
    
    for anio in range(anio_h,ultimo_anio,-1):
        
        print(" - ",anio," - ")
        

        col_name="P_DESERCION_CODGEO_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            
        df_p_deser = get_p_desercion_by_distrito(anio=anio,macro_region="Peru",cache=cache)
        df_p_deser = df_p_deser.round({"P_DESERCION_CODGEO":decimals })
        df_p_deser.rename({"P_DESERCION_CODGEO": col_name}, axis=1, inplace=True)
        list_df_agg.append(df_p_deser)
        
        cls_list.append(col_name)
        
        num+=1
        
    cls_list_old_new = list(reversed(cls_list))
    
    df_final = reduce(lambda left,right: pd.merge(left,right,on=["CODGEO"]), list_df_agg)
    df_final.fillna(0,inplace=True)
    
  
    df_final[["P_DESERCION_CODGEO_SLOPE","P_DESERCION_CODGEO_INTERCEPT","P_DESERCION_CODGEO_R2"]] = df_final[cls_list_old_new].apply(get_coeff, axis=1)
    df_final = df_final.round({"P_DESERCION_CODGEO_SLOPE":decimals })
    df_final = df_final.round({"P_DESERCION_CODGEO_INTERCEPT":decimals })
    df_final = df_final.round({"P_DESERCION_CODGEO_R2":decimals })
                    
    ho.print_items(df_final.columns, excepto=["CODGEO"])
    
    df = pd.merge(df, df_final ,left_on="CODGEO",  right_on="CODGEO", how='left')
    
    
    
    return df


def get_p_desercion_by_distrito(anio=None, macro_region=None,modalidad=None,id_grado_list=None,cache=False ):
    
    index_column="CODGEO"
    
    filename = 'p_desercion_by_codgeo'
    ho.print_message('agregar_kpi_p_desercion_by_codgeo')
    #key_cache = hch.get_key_cache([anio,index_column,macro_region,modalidad,id_grado_list])
    key_cache = hch.get_key_cache([anio,index_column])
    
    print(key_cache)
    
    if cache:
        df = hch.get_cache(filename,key_cache)
            
        if df is not None:
            return df

    df_siagie = hadb.get_siagie_por_anio(anio,macro_region=macro_region,desercion=True,  modalidad=modalidad , id_grado_list= id_grado_list ,columns_n= ['ID_PERSONA','COD_MOD','ANEXO'])
    anios_str=str(anio)+"_"+str(anio+1)
    original_col = "DESERCION_"+anios_str
    df =  pd.crosstab(index=df_siagie[index_column], columns=df_siagie[original_col], normalize='index')
    new_column = 'P_DESERCION_'+index_column
    df.rename({1: new_column, 0: 'P_SIN_DESERCION'}, axis=1, inplace=True)
    df.reset_index(drop=False,inplace=True)
    df[new_column].fillna(0,inplace=True)
    df.drop(['P_SIN_DESERCION'], axis = 1, inplace=True)
    
    hch.save_cache(df,filename,key_cache)
    
    return df




def generar_kpis_p_deser_by_codmod(df,anio_df=None , anio_h = None,t_anios=0 ,decimals=2 , cache=False):
    
    #anio_df_menos_1 = anio_df-1
    
    ultimo_anio =anio_h- t_anios
    #ultimo_anio_data = ultimo_anio + 1    
    num = anio_df-anio_h
    
    list_df_agg = []
    
    cls_list = []
    
    for anio in range(anio_h,ultimo_anio,-1):
        
        print(" - ",anio," - ")
        

        col_name="P_DESERCION_COD_MOD_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix            
        
        df_p_deser = get_p_desercion_by_codmod(anio=anio,macro_region="Peru",cache=cache)
        
        df_p_deser = df_p_deser.round({"P_DESERCION_COD_MOD":decimals })
        df_p_deser.rename({"P_DESERCION_COD_MOD": col_name}, axis=1, inplace=True)
        list_df_agg.append(df_p_deser)
        
        cls_list.append(col_name)
        
        num+=1
        
    cls_list_old_new = list(reversed(cls_list))
    
    df_final = reduce(lambda left,right: pd.merge(left,right,on=["COD_MOD"]), list_df_agg)
    df_final.fillna(0,inplace=True)
    
    #df_final["P_DESERCION_COD_MOD_SLOPE"] = df_final[cls_list_old_new].apply(get_coeff, axis=1)
    #df_final = df_final.round({"P_DESERCION_COD_MOD_SLOPE":decimals })
    
    df_final[["P_DESERCION_COD_MOD_SLOPE","P_DESERCION_COD_MOD_INTERCEPT","P_DESERCION_COD_MOD_R2"]] = df_final[cls_list_old_new].apply(get_coeff, axis=1)
    df_final = df_final.round({"P_DESERCION_COD_MOD_SLOPE":decimals })
    df_final = df_final.round({"P_DESERCION_COD_MOD_INTERCEPT":decimals })
    df_final = df_final.round({"P_DESERCION_COD_MOD_R2":decimals })
    
        
    ho.print_items(df_final.columns, excepto=["COD_MOD"])
    
    df = pd.merge(df, df_final ,left_on="COD_MOD",  right_on="COD_MOD", how='left')
    
    
    
    return df

'''

def generar_kpis_p_deser_by_codmod(df,anio_df=None ,cache=False):
    
    anio_df_menos_1 = anio_df-1
    
    df_p_deser = get_p_desercion_by_codmod(anio=anio_df_menos_1,macro_region="Peru",cache=cache)
    
    ho.print_items(df_p_deser.columns, excepto=["COD_MOD"])
    
    df = pd.merge(df, df_p_deser ,left_on="COD_MOD",  right_on="COD_MOD", how='left')
    
    df.rename({"P_DESERCION_COD_MOD": "P_DESERCION_COD_MOD_T_MENOS_1"}, axis=1, inplace=True)
    
    return df
'''

def get_p_desercion_by_codmod(anio=None, macro_region=None,modalidad=None,id_grado_list=None,cache=False ):
    
    index_column="COD_MOD"
    
    filename = 'p_desercion_by_cod_mod'
    ho.print_message('agregar_kpi_p_desercion_by_cod_mod')
    #key_cache = hch.get_key_cache([anio,index_column,macro_region,modalidad,id_grado_list])
    key_cache = hch.get_key_cache([anio,index_column])
    
    print(key_cache)
    
    if cache:
        df = hch.get_cache(filename,key_cache)
            
        if df is not None:
            return df

    df_siagie = hadb.get_siagie_por_anio(anio,macro_region=macro_region,desercion=True,  modalidad=modalidad , id_grado_list= id_grado_list,columns_n= ['ID_PERSONA','COD_MOD','ANEXO'])
    anios_str=str(anio)+"_"+str(anio+1)
    original_col = "DESERCION_"+anios_str
    df =  pd.crosstab(index=df_siagie[index_column], columns=df_siagie[original_col], normalize='index')
    new_column = 'P_DESERCION_'+index_column
    df.rename({1: new_column, 0: 'P_SIN_DESERCION'}, axis=1, inplace=True)
    df.reset_index(drop=False,inplace=True)
    df[new_column].fillna(0,inplace=True)
    df.drop(['P_SIN_DESERCION'], axis = 1, inplace=True)
    
    hch.save_cache(df,filename,key_cache)
    
    return df
    




def gestionar_errores_filtro_kpi(anio_df,anio_h,t_anios):
    
    if(t_anios < 1):            
        msg = "ERROR: El numero t_anios debe ser mayor a 0"
        raise Exception(msg)
        
    ultimo_anio =anio_h- t_anios
    ultimo_anio_data = ultimo_anio + 1    
    
    if(ultimo_anio_data<2014):            
        msg = "ERROR: Se pretende consultar hasta el anio "+str(ultimo_anio_data)+", solo se tiene data hasta el 2014"      
        raise Exception(msg)   

    if(anio_h>anio_df):            
        msg = "ERROR: El parametro anio_h no puede ser mayor al parametro anio_h "        
        raise Exception(msg)   
        
    num = anio_df-anio_h
    
    return ultimo_anio , num


def get_kpi_foraneo(df,anio_df=None, anio_h=None ,t_anios=1,cache=False):
    
    filename = 'kpi_foraneo'
    ho.print_message('agregar_kpi_foraneo')
    key_cache = hch.get_key_cache([anio_df,anio_h,t_anios])
    print(key_cache)
    if cache:
        df_final_total = hch.get_cache(filename,key_cache)
        if df_final_total is not None:
            ho.print_items(df_final_total.columns)
            if df is None:
                return 
            else:
                df = pd.merge(df, df_final_total, left_on="ID_PERSONA",  right_on="ID_PERSONA",  how='left')
                return df
    
    ultimo_anio, num = gestionar_errores_filtro_kpi(anio_df,anio_h,t_anios) 
    ultimo_anio_data = ultimo_anio + 1 
    if(ultimo_anio_data<2016):            
        msg = "ERROR: Se pretende consultar hasta el anio "+str(ultimo_anio_data)+", solo se tiene data hasta el 2016"     
        raise Exception(msg) 
    
    #df_id_persona = df[["ID_PERSONA"]].copy()
    df_id_persona = hadb.get_siagie_por_anio(anio_df,columns_n= ['ID_PERSONA'])
    
    
    url = hadb.get_path_BD()+"\\06.ubigeo_peru\\ubigeo_distrito.csv" 

    dtypes_columns = {'reniec':str, 'inei':str }
    df_reniec_ubigeo = pd.read_csv(url,encoding="latin-1",usecols=["reniec","inei"],dtype=dtypes_columns)

    list_df=[]
    
    for anio in range(anio_h,ultimo_anio,-1):
        

        col_name="FORANEO_{}_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            #cols_to_drop_desap.append(col_name.format("TOTAL","DESAPROBADO"))
            #cols_to_drop_reti.append(col_name.format("TOTAL","RETIRADO"))

        #cols_to_sum_desap.append(col_name.format("TOTAL","DESAPROBADO"))
        #cols_to_sum_reti.append(col_name.format("TOTAL","RETIRADO"))
        
    
        df_estudiantes =  hadb.get_siagie_por_anio(anio,
                                                   columns_n=["ID_PERSONA","UBIGEO_NACIMIENTO_RENIEC","COD_MOD","ANEXO"])

        df_merged = pd.merge(df_estudiantes,df_reniec_ubigeo,left_on="UBIGEO_NACIMIENTO_RENIEC",right_on="reniec",how="left")
        
        df_merged = pd.merge(df_id_persona,df_merged,left_on="ID_PERSONA",right_on="ID_PERSONA",how="left")

        df_serv = hadb.get_df_servicios(anio=anio,geo=True)[["COD_MOD","ANEXO","CODGEO"]]
        df_final = pd.merge(df_merged,df_serv,left_on=["COD_MOD","ANEXO"],right_on=["COD_MOD","ANEXO"],how="inner")

        df_final.loc[(df_final['inei'].isna()), col_name.format("DIST")] = np.nan
        df_final.loc[(df_final['inei'].isna()==False) & (df_final['inei']==df_final['CODGEO']), col_name.format("DIST")] = 0
        df_final.loc[(df_final['inei'].isna()==False) & (df_final['inei']!=df_final['CODGEO']), col_name.format("DIST")] = 1

        df_final.loc[(df_final['inei'].isna()), col_name.format("PROV")] = np.nan
        df_final.loc[(df_final['inei'].isna()==False) & (df_final['inei'].str[:4]==df_final['CODGEO'].str[:4]), col_name.format("PROV")] = 0
        df_final.loc[(df_final['inei'].isna()==False) & (df_final['inei'].str[:4]!=df_final['CODGEO'].str[:4]), col_name.format("PROV")] = 1

        df_final.loc[(df_final['inei'].isna()), col_name.format("DEP")] = np.nan
        df_final.loc[(df_final['inei'].isna()==False) & (df_final['inei'].str[:2]==df_final['CODGEO'].str[:2]), col_name.format("DEP")] = 0
        df_final.loc[(df_final['inei'].isna()==False) & (df_final['inei'].str[:2]!=df_final['CODGEO'].str[:2]), col_name.format("DEP")] = 1
        df_final.drop(['UBIGEO_NACIMIENTO_RENIEC', 'COD_MOD', 'ANEXO', 'inei', 'reniec', 'CODGEO'], axis=1,inplace=True)
        list_df.append(df_final)
        
        num+=1
        
    df_final_total = reduce(lambda left,right: pd.merge(left,right,on="ID_PERSONA"), list_df)
    ho.print_items(df_final_total.columns)
    hch.save_cache(df_final_total,filename,key_cache)
    if df is None:
        return 
    else:  
        df = pd.merge(df, df_final_total, left_on="ID_PERSONA",  right_on="ID_PERSONA",  how='left')
        return df



def generar_kpis_agg_servicios(df,anio_df=None , anio_h =None ,t_anios=1,modalidad=None,valor_por_anio=False, cache=False):
    
    filename = 'kpis_agg_servicios'
    ho.print_message('agregar_kpis_agg_servicios')
    key_cache = hch.get_key_cache([anio_df,anio_h,t_anios,modalidad])
    print(key_cache)
    if cache:
        df_final = hch.get_cache(filename,key_cache)
        if df_final is not None:
            ho.print_items(df_final.columns, excepto=["COD_MOD","ANEXO"])            
            if df is None:
                return 
            else:
                df = pd.merge(df, df_final, left_on=["COD_MOD","ANEXO"],  right_on=["COD_MOD","ANEXO"],  how='left')
            return df

    ultimo_anio, num = gestionar_errores_filtro_kpi(anio_df,anio_h,t_anios)

    df_serv = hadb.get_df_servicios(anio=anio_df,columns=["COD_MOD","ANEXO"])
    
    cols_to_sum_desap = []
    cols_to_sum_reti = []
    list_df_agg=[]
    cols_to_drop_desap = []
    cols_to_drop_reti = []
    for anio in range(anio_h,ultimo_anio,-1):

        if(anio<=2013):
                break

        col_name="{}_{}_SERVICIO_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            cols_to_drop_desap.append(col_name.format("TOTAL","DESAPROBADO"))
            cols_to_drop_reti.append(col_name.format("TOTAL","RETIRADO"))

            cols_to_sum_desap.append(col_name.format("TOTAL","DESAPROBADO"))
            cols_to_sum_reti.append(col_name.format("TOTAL","RETIRADO"))

        
        if (num>0):

            df_alum =  hadb.get_siagie_por_anio(anio, columns_n= ['ID_PERSONA','COD_MOD','ANEXO','SITUACION_FINAL'])
            df_alum = hc.trim_category_cls(df_alum)

            dic_valores = {
            'TOTAL_DESAPROBADO' : np.where(df_alum['SITUACION_FINAL']=='DESAPROBADO', 1,0)  ,
            'TOTAL_RETIRADO' : np.where(df_alum['SITUACION_FINAL']=='RETIRADO', 1,0)  ,    
            'TOTAL_ESTUDIANTES':1,
            }

            agg_config = {
            'TOTAL_DESAPROBADO':'sum',
            'TOTAL_RETIRADO':'sum', 
            'TOTAL_ESTUDIANTES':'sum',
            }

            df_agg = df_alum.assign(
            **dic_valores        
            ).groupby(['COD_MOD','ANEXO']).agg(agg_config).reset_index()

            df_agg_serv = pd.merge(df_serv,df_agg, 
                                    left_on=["COD_MOD","ANEXO"], 
                                    right_on = ["COD_MOD","ANEXO"] ,how="left")
        else:
            df_agg_serv = df_serv

        df_serv_anio_n = hadb.get_df_servicios(anio=anio,columns=["COD_MOD","ANEXO",'TALUMNO', 'TDOCENTE', 'TSECCION'])
 
        df_agg_serv = pd.merge(df_agg_serv,df_serv_anio_n, 
                               left_on=["COD_MOD","ANEXO"], 
                               right_on = ["COD_MOD","ANEXO"] ,how="left")


        df_agg_serv['RATIO_ALUMNO_DOCENTE'] = np.round(df_agg_serv['TALUMNO']/df_agg_serv['TDOCENTE'], decimals = 1)
        df_agg_serv['RATIO_SECCION_DOCENTE'] = np.round(df_agg_serv['TSECCION']/df_agg_serv['TDOCENTE'], decimals = 1)
        df_agg_serv.rename(columns={'TALUMNO': col_name.format("TOTAL","ALUMNO")}, inplace=True)
        df_agg_serv.rename(columns={'TDOCENTE': col_name.format("TOTAL","DOCENTE")}, inplace=True)
        df_agg_serv.rename(columns={'TSECCION': col_name.format("TOTAL","SECCION")}, inplace=True)
        
        df_agg_serv.rename(columns={'TALUMNO': col_name.format("TOTAL","ALUMNO")}, inplace=True)
        df_agg_serv.rename(columns={'TDOCENTE': col_name.format("TOTAL","DOCENTE")}, inplace=True)
        df_agg_serv.rename(columns={'TSECCION': col_name.format("TOTAL","SECCION")}, inplace=True)
        
        df_agg_serv.rename(columns={'RATIO_ALUMNO_DOCENTE': col_name.format("RATIO","ALUMNO_DOCENTE")}, inplace=True)
        df_agg_serv.rename(columns={'RATIO_SECCION_DOCENTE': col_name.format("RATIO","SECCION_DOCENTE")}, inplace=True)
        
        if num > 0:                
            df_agg_serv['RATIO_DESAPROBADOS'] = np.round(df_agg_serv['TOTAL_DESAPROBADO']/df_agg_serv['TOTAL_ESTUDIANTES'], decimals = 1)
            df_agg_serv['RATIO_RETIRADO'] = np.round(df_agg_serv['TOTAL_RETIRADO']/df_agg_serv['TOTAL_ESTUDIANTES'], decimals = 1)
            df_agg_serv.drop(['TOTAL_ESTUDIANTES'], axis=1,inplace=True)
        #df_agg_serv.rename(columns={'TOTAL_ESTUDIANTES': col_name.format("TOTAL","ESTUDIANTES")}, inplace=True)
        
        if num > 0: 
            df_agg_serv.rename(columns={'RATIO_DESAPROBADOS': col_name.format("RATIO","DESAPROBADO")}, inplace=True)
            df_agg_serv.rename(columns={'RATIO_RETIRADO': col_name.format("RATIO","RETIRADO")}, inplace=True)
            
            df_agg_serv.rename(columns={'TOTAL_DESAPROBADO': col_name.format("TOTAL","DESAPROBADO")}, inplace=True)
            df_agg_serv.rename(columns={'TOTAL_RETIRADO': col_name.format("TOTAL","RETIRADO")}, inplace=True)


        list_df_agg.append(df_agg_serv)

        num+=1


    df_final = reduce(lambda left,right: pd.merge(left,right,on=["COD_MOD","ANEXO"]), list_df_agg)
   
    ''' 
    #Total de totales no tiene sentido, aqui si aplicaria totales por año
    df_final['TOTAL_DESAPROBADO_SERVICIO'] = df_final[cols_to_sum_desap].sum(axis=1)
    df_final['MEAN_DESAPROBADO_SERVICIO'] = df_final[cols_to_sum_desap].mean(axis=1)
    df_final['STD_DESAPROBADO_SERVICIO'] = df_final[cols_to_sum_desap].std(axis=1)

    df_final['TOTAL_RETIRADO_SERVICIO'] = df_final[cols_to_sum_reti].sum(axis=1)
    df_final['MEAN_RETIRADO_SERVICIO'] = df_final[cols_to_sum_reti].mean(axis=1)
    df_final['STD_RETIRADO_SERVICIO'] = df_final[cols_to_sum_reti].std(axis=1)
    '''
    if valor_por_anio==False:
        print("--------------")
        print(cols_to_sum_desap)
        print(cols_to_sum_reti)
        print("--------------")
        df_final.drop(cols_to_sum_desap, axis = 1,inplace=True) 
        df_final.drop(cols_to_sum_reti, axis = 1,inplace=True) 
           
    hch.save_cache(df_final,filename,key_cache)
    ho.print_items(df_final.columns, excepto=["COD_MOD","ANEXO"])
    if df is None:
        return 
    else:  
        df = pd.merge(df, df_final, left_on=["COD_MOD","ANEXO"],  right_on=["COD_MOD","ANEXO"],  how='left')
        return df

def generar_kpis_traslado(df,anio_df=None , anio_h =None ,modalidad="EBR"  ,t_anios=1,cache=False, por_anio=False):
    ho.print_message('generar_kpis_traslado')     
    filename = 'kpis_traslado'
    
    key_cache = hch.get_key_cache([anio_df,anio_h,t_anios,modalidad,por_anio])
    print(key_cache)
    if cache:
        df_final = hch.get_cache(filename,key_cache)
        if df_final is not None:
            ho.print_items(df_final.columns)
            
            if df is None:
                return  df_final
            else:
                df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='left')
                return df
    
    
    #ID_PERSONA_SERIES = df['ID_PERSONA']
    ID_PERSONA_SERIES = hadb.get_siagie_por_anio(anio_df,columns_n= ['ID_PERSONA'])
    
    #ultimo_anio =ANIO- T_ANIOS
    ultimo_anio, num = gestionar_errores_filtro_kpi(anio_df,anio_h,t_anios)
    #num = anio_df-anio_h
    #ultimo_anio =anio_h - t_anios
    #ultimo_anio_data = ultimo_anio + 1
    #num = 0
    list_df_m_tras = []
    cols_to_sum = []
    cols_to_drop = []
    for anio in range(anio_h,ultimo_anio,-1):
        if(anio<=2013):
            break
        col_name="TOTAL_TRASLADOS_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            cols_to_drop.append(col_name)
        cols_to_sum.append(col_name)
        df_m_t = pd.merge(ID_PERSONA_SERIES, hadb.get_traslados_por_anio(anio),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        df_m_t.fillna({'TOTAL_TRASLADOS':0}, inplace=True)
        df_m_t.rename(columns={'TOTAL_TRASLADOS': col_name}, inplace=True)
        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final['TOTAL_TRASLADOS'] = df_final[cols_to_sum].sum(axis=1)
    df_final['MEAN_TRASLADOS'] = df_final[cols_to_sum].mean(axis=1)
    df_final['STD_TRASLADOS'] = df_final[cols_to_sum].std(axis=1)
    #print()
    if por_anio==False:
        df_final.drop(cols_to_drop, axis = 1,inplace=True)   
    

    ho.print_items(df_final.columns)
    hch.save_cache(df_final,filename,key_cache)
    #print(cols_to_sum)
    if df is None:
        return df_final
    else:    
        df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='left')        
        return df

def generar_kpis_traslado_a_publico(df,anio_df=None, anio_h =None ,t_anios=1,modalidad="EBR",cache=False, por_anio=False):
    ho.print_message('generar_kpis_traslado_a_publico') 
    
    filename = 'kpis_traslado_a_publico'
    key_cache = hch.get_key_cache([anio_df,anio_h,t_anios,modalidad,por_anio])
    print(key_cache)
    if cache:
        df_final = hch.get_cache(filename,key_cache)
        if df_final is not None:
            ho.print_items(df_final.columns) 
            
            if df is None:
                return df_final
            else:          
                df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='left')
                return df    
        
    #if df_servicios is None:
    #    df_servicios = hadb.get_df_servicios()
    
    #ID_PERSONA_SERIES = df['ID_PERSONA']
    ID_PERSONA_SERIES = hadb.get_siagie_por_anio(anio_df,columns_n= ['ID_PERSONA'])
    
    #ultimo_anio =ANIO- T_ANIOS
    ultimo_anio, num = gestionar_errores_filtro_kpi(anio_df,anio_h,t_anios)
    #num = 0
    list_df_m_tras = []
    cols_to_sum = []
    cols_to_drop = []
    for anio in range(anio_h,ultimo_anio,-1):
        if(anio<=2013):
            break
        col_name="TOTAL_TRASLADOS_A_PUBLICO_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            cols_to_drop.append(col_name)
        cols_to_sum.append(col_name)
        df_servicios = hadb.get_df_servicios(anio=anio)
        df_m_t = pd.merge(ID_PERSONA_SERIES, hadb.get_traslados_a_publico(anio,df_servicios),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        df_m_t.fillna({'TOTAL_TRASLADOS':0}, inplace=True)
        df_m_t.rename(columns={'TOTAL_TRASLADOS': col_name}, inplace=True)
        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final['TOTAL_TRASLADOS_A_PUBLICO'] = df_final[cols_to_sum].sum(axis=1)
    df_final['MEAN_TRASLADOS_A_PUBLICO'] = df_final[cols_to_sum].mean(axis=1)
    df_final['STD_TRASLADOS_A_PUBLICO'] = df_final[cols_to_sum].std(axis=1)

    if por_anio==False:
        df_final.drop(cols_to_drop, axis = 1,inplace=True)    
    
    ho.print_items(df_final.columns)  
    hch.save_cache(df_final,filename,key_cache)
    
    if df is None:
        return df_final
    else:    
        df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='left')    
        return df


def generar_kpis_desercion(df,anio_df=None, anio_h=None ,t_anios=1,cache=False):
    
    ho.print_message('generar_kpis_desercion')    
    
    filename = 'kpis_desercion'
    key_cache = hch.get_key_cache([anio_df,anio_h,t_anios])
    print(key_cache)
    if cache:
        df_final = hch.get_cache(filename,key_cache)
        if df_final is not None:
            ho.print_items(df_final.columns)
            if df is None:
                return 
            else:     
                df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='left')
                return df    
    
    #ID_PERSONA_SERIES = df['ID_PERSONA']
    ID_PERSONA_SERIES = hadb.get_siagie_por_anio(anio_df,columns_n= ['ID_PERSONA'])
    
    ultimo_anio, num = gestionar_errores_filtro_kpi(anio_df,anio_h,t_anios)
    #ultimo_anio =ANIO- T_ANIOS       
    #num = 1
    list_df_m_tras = []
    cols_to_sum = []
    cols_to_drop = []
    #ANIO = ANIO-1
    #print("anio_h : ",anio_h," ultimo_anio : ",ultimo_anio)
    for anio in range(anio_h,ultimo_anio,-1):
        #print("anio : ",anio)
        if(anio<=2013):
            break
        col_name="DESERTARA_DESPUES_DE_T"
        if(num>0):
            posfix="_MENOS_{}".format(num)
            col_name = col_name+posfix
            cols_to_drop.append(col_name)
        cols_to_sum.append(col_name)
        df_m_t = pd.merge(ID_PERSONA_SERIES, hadb.get_desertores_por_anio(anio),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        anios_str=str(anio)+"_"+str(anio+1)
        original_col = "DESERCION_"+anios_str

        df_m_t.fillna({original_col:0}, inplace=True)
        df_m_t.rename(columns={original_col: col_name}, inplace=True)

        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final['TOTAL_DESERCIONES'] = df_final[cols_to_sum].sum(axis=1)
    df_final['MEAN_DESERCIONES'] = df_final[cols_to_sum].mean(axis=1)
    df_final['STD_DESERCIONES'] = df_final[cols_to_sum].std(axis=1)
    df_final.drop(cols_to_drop, axis = 1,inplace=True)    
    

    ho.print_items(df_final.columns)
    hch.save_cache(df_final,filename,key_cache)
    if df is None:
        return 
    else:    
        df = pd.merge(df, df_final, left_on=["ID_PERSONA"],  right_on=["ID_PERSONA"],  how='left')    
        return df



def agregar_distancia_prim_sec(df,cache=False):
    

    ho.print_message('agregar_distancia_prim_sec')
    
    filename = 'distancia_prim_sec'
    key_cache = hch.get_key_cache(["distancia_prim_sec"])
    print(key_cache)
    if cache:
        df_dist = hch.get_cache(filename,key_cache)
        if df_dist is not None:
            ho.print_items(df_dist.columns,excepto=["COD_MOD","ANEXO"])
            if df is None:
                return 
            else:   
                df = pd.merge(df,df_dist, left_on=['COD_MOD','ANEXO'],right_on=['COD_MOD','ANEXO'], how='left')  
                return df  
    
    
    df_dist= hadb.get_distancia_prim_sec()    
    
    ho.print_items(df_dist.columns,excepto=["COD_MOD","ANEXO"])
    hch.save_cache(df_dist,filename,key_cache)
    
    if df is None:
        return 
    else:      
        df = pd.merge(df,df_dist, left_on=['COD_MOD','ANEXO'],right_on=['COD_MOD','ANEXO'], how='left')  
        return df

def agregar_distancia_ini_pri(df,cache=False):
    

    ho.print_message('agregar_distancia_ini_prim')
    
    filename = 'distancia_ini_prim'
    key_cache = hch.get_key_cache(["distancia_ini_prim"])
    print(key_cache)
    if cache:
        df_dist = hch.get_cache(filename,key_cache)
        if df_dist is not None:
            ho.print_items(df_dist.columns,excepto=["COD_MOD","ANEXO"])
            if df is None:
                return 
            else:   
                df = pd.merge(df,df_dist, left_on=['COD_MOD','ANEXO'],right_on=['COD_MOD','ANEXO'], how='left')  
                return df  
    
    
    df_dist= hadb.get_distancia_ini_prim()    
    
    ho.print_items(df_dist.columns,excepto=["COD_MOD","ANEXO"])
    hch.save_cache(df_dist,filename,key_cache)
    
    if df is None:
        return 
    else:      
        df = pd.merge(df,df_dist, left_on=['COD_MOD','ANEXO'],right_on=['COD_MOD','ANEXO'], how='left')  
        return df


def generar_kpis_historicos(df,key_df="",anio_df=None,anio_h=None,cls_json=None,t_anios=0,
                            cache=False,valor_por_anio=False,retornar=True):
    
    ho.print_message('generar_kpis_historicos')
    
    json_str = json_to_str(cls_json)
    
    filename = 'kpis_historicos'
    key_cache = hch.get_key_cache([anio_df,anio_h,t_anios,json_str,key_df])
    print(key_cache)
    if cache: 
        df_final = hch.get_cache(filename,key_cache)
        #df_final = hdf.reduce_mem_usage(df_final)
        if df_final is not None:
            ho.print_items(df_final.columns)
            if df is None:
                #return df_final
                return
            else:   
                df_final = pd.merge(df , df_final, left_on=['ID_PERSONA'], right_on=['ID_PERSONA'], how='left',suffixes=('','_repetido')) 
                return df_final    
    
    if(t_anios < 1):            
        msg = "ERROR: El numero t_anios debe ser mayor a 0"
        raise Exception(msg)
        #return False
    
    ultimo_anio =anio_h- t_anios
    ultimo_anio_data = ultimo_anio + 1
    if(ultimo_anio_data<2014):            
        msg = "ERROR: Se pretende consultar hasta el anio "+str(ultimo_anio_data)+", solo se tiene data hasta el 2014"      
        raise Exception(msg)   
    
    
    if(anio_h>anio_df):            
        msg = "ERROR: El parametro anio_h no puede ser mayor al parametro anio_h "        
        raise Exception(msg)  
    
    cls_list = []
    for key, value in cls_json.items():
        cls_list.append(key)  
        
    if 'ID_PERSONA' not in cls_list :
        cls_list.append('ID_PERSONA')
       
    ID_PERSONA_SERIES = df['ID_PERSONA']

    #df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)
    df_final,kpi_final_dic = get_df_final_kpis_historicos(ID_PERSONA_SERIES,anio_df,anio_h,ultimo_anio,cls_list,cls_json)

    kpi_list = []
    for key, cls_anios in kpi_final_dic.items():
        kpi_list.append(key)   
        df_final = set_generic_kpis(df_final,key,cls_anios)
        if valor_por_anio==False:
            df_final.drop(cls_anios, axis = 1,inplace=True) 
       
    df_final.columns = df_final.columns.str.replace(r" ", "_")
    
    #df_final = hdf.reduce_mem_usage(df_final)
    ho.print_items(df_final.columns)
    hch.save_cache(df_final,filename,key_cache)
    
    if df is None:
        return 
    else:     
        df_final = pd.merge(df , df_final, left_on=['ID_PERSONA'], right_on=['ID_PERSONA'], how='left',suffixes=('','_repetido'))    
        return df_final


def json_to_str(cls_json):
    list_value = ""
    for key,value in cls_json.items():   
        list_value=list_value+key[:2]+"_"
        if isinstance(value, list):
            listToStr = '_'.join([str(elem[:2]) for elem in value])
            list_value=list_value+listToStr+"_"
        else:
            list_value=list_value+value[:2]
    return list_value

def get_df_final_kpis_historicos(ID_PERSONA_SERIES,anio_df,anio_h,ultimo_anio,cls_list,cls_json):
    
    
    
    num = anio_df-anio_h
    list_df_m_tras = []
    kpi_final_dic = {}
    
    for anio in range(anio_h,ultimo_anio,-1):
        if(anio<=2013):
            break

        #print("ANIO =================>>>>>>>>>  : ",anio)
        df_m_t = pd.merge(ID_PERSONA_SERIES, hadb.get_siagie_por_anio(anio,columns_n=cls_list),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        
        df_m_t = hc.trim_category_cls(df_m_t)
        
        for key, values in cls_json.items():
            if  isinstance(values, list):
         
                #print("------------------category---------------------")
                for val in values:
                    key_val = key+"_"+val
                    if num ==0:
                        cl_pf = key_val+"_T"               
                    else:
                        cl_pf = key_val+"_T_MENOS_{}".format(num)                        
                    #df_m_t[cl_pf] = np.where((df_m_t[key]==val),1,0)
                    
                    df_m_t[cl_pf] = np.NaN 
                    df_m_t.loc[(df_m_t[key]!="NaN") & (df_m_t[key]==val), cl_pf] = 1
                    df_m_t.loc[(df_m_t[key]!="NaN") & (df_m_t[key]!=val), cl_pf] = 0  
                    
                    #print(cl_pf)
                    if  (key_val in kpi_final_dic) ==False:
                        kpi_final_dic[key_val]=[]                    
                    kpi_final_dic[key_val].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 
            elif values=="dummy":      
                
                #print("-----------------dummy----------------------")
                if num ==0:
                    cl_pf = key+"_T"              
                else:
                    cl_pf = key+"_T_MENOS_{}".format(num)                
                #df_m_t[cl_pf] = np.where((df_m_t[key]==1),1,0)
                
                df_m_t[cl_pf] = np.NaN 
                df_m_t.loc[(df_m_t[key]!="NaN") & (df_m_t[key]==1), cl_pf] = 1
                df_m_t.loc[(df_m_t[key]!="NaN") & (df_m_t[key]==0), cl_pf] = 0   
                
                #print(cl_pf)
                
                if  (key in kpi_final_dic) ==False:
                    kpi_final_dic[key]=[]                    
                kpi_final_dic[key].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 
                
            elif values=="numero":    
                
                #print("-----------------numero----------------------")                
                if num ==0:
                    cl_pf = key+"_T"              
                else:
                    cl_pf = key+"_T_MENOS_{}".format(num)                
                #df_m_t[cl_pf] = df_m_t[key]  
                
                df_m_t[cl_pf] = np.NaN    
                df_m_t.loc[(df_m_t[key]!="NaN"), cl_pf] = df_m_t[key] 
                
                #print(cl_pf)
                if  (key in kpi_final_dic) ==False:
                    kpi_final_dic[key]=[]                    
                kpi_final_dic[key].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 
                
        df_m_t = hdf.reduce_mem_usage(df_m_t)
        list_df_m_tras.append(df_m_t)
        num+=1

    return reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras), kpi_final_dic


def set_generic_kpis(df,cl_name=None,cl_list=[],set_nan=False):

    if(set_nan==False):
        if(len(cl_list)>1):            
            #print("---------------------------------------") 
            t_cl_name = 'TOTAL_'+cl_name
            df[t_cl_name] = df[cl_list].sum(axis=1)
            #print(t_cl_name)
            
            m_cl_name = 'MEAN_'+cl_name
            df[m_cl_name] = df[cl_list].mean(axis=1)
            #print(m_cl_name)
            
            if(len(cl_list)>2):
                st_cl_name = 'STD_'+cl_name 
                df[st_cl_name] = df[cl_list].std(axis=1)
                #print(st_cl_name)
                
            mi_cl_name = 'MIN_'+cl_name    
            df[mi_cl_name] = df[cl_list].min(axis=1)
            #print(mi_cl_name)
            
            ma_cl_name = 'MAX_'+cl_name  
            df[ma_cl_name] = df[cl_list].max(axis=1)
            #print(ma_cl_name)
    else:
        df['TOTAL_'+cl_name] = np.nan
        df['MEAN_'+cl_name] = np.nan
        df['STD_'+cl_name] = np.nan
    return df







def existe_columna(df,cl):
    if cl not in  df:
        raise Exception("No se puede formatear la columna " + cl + ", no existe en el DF")
        
def formatear_TIENE_TRABAJO(df,drop=True):
    existe_columna(df,'HORAS_SEMANALES_TRABAJO') 
    existe_columna(df,'TRABAJA') 
    df['TIENE_TRABAJO'] = np.where((df.TRABAJA==1) | (df.HORAS_SEMANALES_TRABAJO>0) , 1 , 0 )
    print("NEW : {}".format('TIENE_TRABAJO'))
    if(drop):        
        df.drop(['TRABAJA','HORAS_SEMANALES_TRABAJO'], axis = 1,inplace=True) 
        print("drop : {}".format('TRABAJA'))
        print("drop : {}".format('HORAS_SEMANALES_TRABAJO'))
    

def formatear_TIENE_PADRES_COMO_APODERADO(df,drop=True):
    existe_columna(df,'PARENTESCO') 
    df['TIENE_PADRES_COMO_APODERADO'] = np.where((df.PARENTESCO=="MADRE") | (df.PARENTESCO=="PADRE") , 1 , 0 )
    print("NEW : {}".format('TIENE_PADRES_COMO_APODERADO'))
    if drop:
        df.drop(['PARENTESCO'], axis = 1,inplace=True) 
        print("drop : {}".format('PARENTESCO'))

def formatear_NO_VIVE_ALGUN_PADRE(df,drop=True):
    
    existe_columna(df,'PADRE_VIVE') 
    existe_columna(df,'MADRE_VIVE') 
    
    df['NO_VIVE_ALGUN_PADRE'] = np.where((df.PADRE_VIVE=="NO") | (df.MADRE_VIVE=="NO") , 1 , 0 )
    print("NEW : {}".format('NO_VIVE_ALGUN_PADRE'))
    if drop:
        df.drop(['PADRE_VIVE','MADRE_VIVE'], axis = 1,inplace=True) 
        print("drop : {}".format('PADRE_VIVE'))
        print("drop : {}".format('MADRE_VIVE'))

def formatear_TIENE_DISCAPACIDAD(df,drop=True):
    existe_columna(df,'TIENE_CERTIFICADO_DISCAPACIDAD') 
    existe_columna(df,'DSC_DISCAPACIDAD')
     
    df['TIENE_DISCAPACIDAD'] = np.where((df.DSC_DISCAPACIDAD!=0) | (df.TIENE_CERTIFICADO_DISCAPACIDAD=="SI") , 1 , 0 )
    print("NEW : {}".format('TIENE_DISCAPACIDAD'))
    if drop:
        df.drop(['DSC_DISCAPACIDAD','TIENE_CERTIFICADO_DISCAPACIDAD'], axis = 1,inplace=True) 
        print("drop : {}".format('DSC_DISCAPACIDAD'))
        print("drop : {}".format('TIENE_CERTIFICADO_DISCAPACIDAD'))

def formatear_TIENE_DNI(df,drop=True):
    existe_columna(df,'N_DOC')
    df['TIENE_DNI'] = np.where(df.N_DOC==0 , 0 , 1 )
    if(drop):
        df.drop(['N_DOC'], axis = 1,inplace=True)  
        print("drop : {}".format('N_DOC'))
    
    
    #df.drop(['EDAD_EN_DIAS_T','EDAD'], axis = 1,inplace=True)  

'''deprecated: la edad ya vendra en decimales, no sera necesario esta funcion
def formatear_dias_decimales(df):
    existe_columna(df,'EDAD_EN_DIAS_T')
    df['EDAD_EN_DECIMALES_T'] = df.EDAD_EN_DIAS_T/365.25
    df['EDAD_EN_DECIMALES_T'] = df.EDAD_EN_DECIMALES_T.round(2)
    
    if 'EDAD' in df:
        df.drop(['EDAD'], axis = 1,inplace=True)  
    if 'EDAD_EN_DIAS_T' in df:
        df.drop(['EDAD_EN_DIAS_T'], axis = 1,inplace=True)  
'''
        
def formatear_ES_MUJER(df,drop=True):
    existe_columna(df,'SEXO')
    df['ES_MUJER'] = np.where(df.SEXO=="MUJER" , 1 , 0 )
    print("NEW : {}".format('ES_MUJER'))
    if(drop):
        df.drop(['SEXO'], axis = 1,inplace=True)  
        print("drop : {}".format('SEXO'))
    
def formatear_ES_MUJER_APOD(df,drop=True):
    existe_columna(df,'SEXO_APOD')
    df['ES_MUJER_APOD'] = np.where(df.SEXO_APOD=="MUJER" , 1 , 0 )
    print("NEW : {}".format('ES_MUJER_APOD'))
    if(drop):
        df.drop(['SEXO_APOD'], axis = 1,inplace=True) 
        print("drop : {}".format('SEXO_APOD'))

def formatear_lengua_nacionalidad(df,drop=True):
    existe_columna(df,'DSC_LENGUA')
    existe_columna(df,'DSC_PAIS')
    df['ES_LENGUA_CASTELLANA'] = np.where(df.DSC_LENGUA=="CASTELLANO" , 1 , 0 )
    df['ES_PERUANO'] = np.where(df.DSC_PAIS.str.startswith('Per', na=False) , 1 , 0 )  
    
    print("NEW : {}".format('ES_LENGUA_CASTELLANA'))
    print("NEW : {}".format('ES_PERUANO'))
    
    if(drop):
        df.drop(['DSC_LENGUA','DSC_PAIS'], axis = 1,inplace=True) 
        print("drop : {}".format('DSC_LENGUA'))
        print("drop : {}".format('DSC_PAIS'))
    
    
def formatear_anio_escolaridad(df,drop=True):   
    anios_esc = {  'NINGUNO':0,              
                   'OTRO':0,
                   'PRIMARIA INCOMPLETA':4,
                   'PRIMARIA COMPLETA':6,
                   'SECUNDARIA INCOMPLETA':9,
                   'SECUNDARIA COMPLETA':11,
                   'SUPERIOR NO UNIV.INCOMPLETA':14,
                   'SUPERIOR NO UNIV.COMPLETA':16,
                   'SUPERIOR UNIV.INCOMPLETA':14,
                   'SUPERIOR UNIV.COMPLETA':16,
                   'SUPERIOR POST GRADUADO':20
                  }
    
    df['ANIOS_ESCOLARIDAD_APOD'] = df['NIVEL_INSTRUCCION_APOD'].map(anios_esc)
    print("NEW : {}".format('ANIOS_ESCOLARIDAD_APOD'))
    if(drop):
        df.drop(['NIVEL_INSTRUCCION_APOD'], axis = 1,inplace=True) 
        print("drop : {}".format('NIVEL_INSTRUCCION_APOD'))


def formatear_columnas_siaguie(df):
    
    formatear_anio_escolaridad(df)
    #formatear_dias_decimales(df)   
    formatear_ES_MUJER(df)    
    formatear_ES_MUJER_APOD(df)    
    formatear_lengua_nacionalidad(df)    
    formatear_TIENE_DNI(df)    
    formatear_TIENE_DISCAPACIDAD(df)    
    formatear_NO_VIVE_ALGUN_PADRE(df)    
    formatear_TIENE_PADRES_COMO_APODERADO(df)  
    formatear_TIENE_TRABAJO(df)  
    
    return df

'''  
dtypes_columns = {'COD_MOD': str,
                  'ANEXO':int,
                
                  'COD_MOD_T_MENOS_1':str,
                  'ANEXO_T_MENOS_1':int,
                  
                  'UBIGEO_NACIMIENTO_RENIEC':str,
                  'N_DOC':str,
                  'ID_GRADO':int,
                  'ID_PERSONA':int,#nurvo
                  'CODIGO_ESTUDIANTE':str,
                  'NUMERO_DOCUMENTO':str,
                  'NUMERO_DOCUMENTO_APOD':str,
                  'CODOOII':str
                  } 
url = hg.get_base_path()+"\\src\\Prj_Interrupcion_Estudios\\Prj_Desercion\\_02_Preparacion_Datos\\_02_Estructura_Base\\_data_\\nominal\\estructura_base_EBR_{}_{}_delta_1.csv"
url = url.format(5,2017)
df =pd.read_csv(url, dtype=dtypes_columns ,encoding="utf-8")

df=formatear_columnas_siaguie(df)

print(df.shape)
df_ = generar_kpis_desercion(df,anio_df=2019,anio_h=2018,t_anios=4)
print(df_.shape)



cls_json = {}
cls_json['SITUACION_FINAL']=["APROBADO","DESAPROBADO"]
#cls_json['SF_RECUPERACION']=["APROBADO","DESAPROBADO"]
#cls_json['SITUACION_MATRICULA']=["PROMOVIDO","REPITE","INGRESANTE","REENTRANTE"]
cls_json['JUNTOS']="dummy"
df_h = generar_kpis_historicos(df,anio_df=2017,anio_h=2016,cls_json=cls_json,t_anios=0 )
'''


