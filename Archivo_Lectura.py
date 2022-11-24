import pandas as pd
import sqlite3

'''
Recomendaciones y uso:
    
Este archivo de lectura es capaz de leer y procesar ulrs de los reportes de producción tanto de datos oficiales, como de blind test.
   
Así mismo, el usuario debe ingresar sólo una url para de esta manera obtener un dataframe depurado. 
    -Ejemplo de ejecución del programa: -----> print(archivos("https://github.com/specolombiahackathon/202010/raw/main/Produccion-fiscalizada-crudo-2017.xlsx"))
    
    Repositorios a usar: 
        Blind test: https://github.com/specolombiahackathon/202010/tree/main/Data_BlindTest
        
        Datos oficiales: https://github.com/specolombiahackathon/202010    
                         https://www.anh.gov.co/estadisticas-del-sector/sistemas-integrados-operaciones/estad%C3%ADsticas-producci%C3%B3n
                         
                         Nota: En caso de presentar problemas de conexión remota para extraer los datos oficiales de la página de la ANH, se recomienda usar el repositorio de Github.
                        
Soporte: angelica.gutierrez1910@gmail.com, sntiagopuentes@gmail.com,u20141125137@usco.edu.co
'''
def archivos(url:str):
        
    #Leer archivo excel de la url  
    df1 = pd.read_excel(url,header=None)
    
    #Eliminar columnas y filas vacias que no afectan los datos de producción----------------------------------- 
    df1 = df1.dropna(axis='columns', thresh= 25)
    df1 = df1.dropna(axis='rows')
    df1 = df1.reset_index()
      
    #Asiganción preliminar de los indices de las columnas---------------------
    df1.drop(['index'],axis=1,inplace=True)
    df1 =df1.rename(columns=df1.iloc[0])  
    df1.drop([0],axis=0,inplace=True)
    df1 = df1.drop_duplicates() # eliminar duplicados 
    df1 = df1.reset_index()
    df1.drop(['index'],axis=1,inplace=True)
    
    
    #Extraer las etiquetas de las columnas para estandarizar la estructura del dataframe------------------------------- 
    etiquetas_columns= df1.columns
    
    for etiqueta in etiquetas_columns:
      etiqueta1= etiqueta.upper ()#Asignar etiquetas a mayúsculas
      etiqueta1= etiqueta1.strip()#Eliminar espacios dentro de las etiquetas 
      
         
    # Reasignar nombre de etiqueta
      if etiqueta1 == 'EMPRESA':
        df1.rename(columns=lambda x: x.replace(etiqueta, 'OPERADORA'), inplace=True)
    
      df1.rename(columns=lambda x: x.replace(etiqueta, etiqueta1), inplace=True)
    
    #Organizar de manera descendente los departamentos-----------------------------------
    df1.sort_values(by='DEPARTAMENTO',ascending=True, inplace=True)
    df1 = df1.reset_index()
    df1.drop(['index'],axis=1,inplace=True)
    
    #Organizar y estandarizar índices de las columnas-------------------------------------------------
            
    lista_etiquetas= ['DEPARTAMENTO','MUNICIPIO','CUENCA','OPERADORA','CONTRATO','CAMPO','ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
    
    #Establecer varoles de producción a formato float ----
    
    formato_float= lista_etiquetas[lista_etiquetas.index('ENERO'):len(df1.columns)+1]
    # Colocar la produccion por mes -------
    anhos= int(anho(url))   
    for formato in formato_float:
        lista_pruduccion=[]
        dias_mes= obtener_dias_del_mes(formato,anhos)
        meses= df1[formato].tolist()
        for mes in meses:
            produccion_mes= round(float(mes*dias_mes),2)
            #produccion_mes= float(produccion_mes)
            lista_pruduccion.append(produccion_mes)
        df1[formato]= lista_pruduccion # Reescribir la columna del mes con los valores de produccion por mes 
            
   
    
    
    
    
    #Formato long----------------------------------------------------------------------------------
    
    #seleccion de id_vars ['DEPARTAMENTO','MUNICIPIO','OPERADORA','CONTRATO','CAMPO']
    
    if ('MUNICIPIO' in  df1.columns) and ('CUENCA' in  df1.columns):
      lista_etiquetas
    elif 'MUNICIPIO' in  df1.columns:        
        lista_etiquetas.pop(2)
    elif 'CUENCA' in  df1.columns:
        lista_etiquetas.pop(1)
    
        
    
    df1=pd.melt(df1,id_vars=lista_etiquetas[0:lista_etiquetas.index('ENERO')],
                value_vars= lista_etiquetas[lista_etiquetas.index('ENERO'):len(df1.columns)],
                var_name= 'MES',#Asignar año del respectivo reporte de producción
                value_name='PRODUCCION_MES')
    
    #Agregar etiqueta año al indice---
    
    anhos= anho(url)
    
    anio = "PRODUCCION_" + anho(url)
    try:    
        # CONECTAMOS, AGREGAMOS Y CERRAMOS ESTA BASE DE DATOS A MEDIDA QUE LLAMAMOS NUEVOS URLS
        miConexion = sqlite3.connect("BASE_DATOS_ANH_DATOS_OFICIALES")
        df1.to_sql(anio, miConexion, if_exists="replace")
        miConexion.close()
    except:
        return "POR FAVOR INGRESE URL DIFERENTE O CONFIRME QUE LO INGRESO BIEN."
    
    return df1
    
    
    
def archivos_blind_tests(url:str):
        
    #Leer archivo excel de la url  
    df1 = pd.read_excel(url,header=None)
    
    #Eliminar columnas y filas vacias que no afectan los datos de producción----------------------------------- 
    df1 = df1.dropna(axis='columns', thresh= 25)
    df1 = df1.dropna(axis='rows')
    df1 = df1.reset_index()
      
    #Asiganción preliminar de los indices de las columnas---------------------
    df1.drop(['index'],axis=1,inplace=True)
    df1 =df1.rename(columns=df1.iloc[0])  
    df1.drop([0],axis=0,inplace=True)
    df1 = df1.drop_duplicates() # eliminar duplicados 
    df1 = df1.reset_index()
    df1.drop(['index'],axis=1,inplace=True)
    
    
    #Extraer las etiquetas de las columnas para estandarizar la estructura del dataframe------------------------------- 
    etiquetas_columns= df1.columns
    
    for etiqueta in etiquetas_columns:
      etiqueta1= etiqueta.upper ()#Asignar etiquetas a mayúsculas
      etiqueta1= etiqueta1.strip()#Eliminar espacios dentro de las etiquetas 
      
         
    # Reasignar nombre de etiqueta
      if etiqueta1 == 'EMPRESA':
        df1.rename(columns=lambda x: x.replace(etiqueta, 'OPERADORA'), inplace=True)
    
      df1.rename(columns=lambda x: x.replace(etiqueta, etiqueta1), inplace=True)
    
    #Organizar de manera descendente los departamentos-----------------------------------
    df1.sort_values(by='DEPARTAMENTO',ascending=True, inplace=True)
    df1 = df1.reset_index()
    df1.drop(['index'],axis=1,inplace=True)
    
    #Organizar y estandarizar índices de las columnas-------------------------------------------------
            
    lista_etiquetas= ['DEPARTAMENTO','MUNICIPIO','CUENCA','OPERADORA','CONTRATO','CAMPO','ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
    
    #Establecer varoles de producción a formato float ----
    
    formato_float= lista_etiquetas[lista_etiquetas.index('ENERO'):len(df1.columns)+1]
    # Colocar la produccion por mes -------
    anhos= int(anho(url))   
    for formato in formato_float:
        lista_pruduccion=[]
        dias_mes= obtener_dias_del_mes(formato,anhos)
        meses= df1[formato].tolist()
        for mes in meses:
            produccion_mes= round(float(mes*dias_mes),2)
            #produccion_mes= float(produccion_mes)
            lista_pruduccion.append(produccion_mes)
        df1[formato]= lista_pruduccion # Reescribir la columna del mes con los valores de produccion por mes 
            
   
    
    
    
    
    #Formato long----------------------------------------------------------------------------------
    
    #seleccion de id_vars ['DEPARTAMENTO','MUNICIPIO','OPERADORA','CONTRATO','CAMPO']
    
    if ('MUNICIPIO' in  df1.columns) and ('CUENCA' in  df1.columns):
      lista_etiquetas
    elif 'MUNICIPIO' in  df1.columns:        
        lista_etiquetas.pop(2)
    elif 'CUENCA' in  df1.columns:
        lista_etiquetas.pop(1)
    
        
    
    df1=pd.melt(df1,id_vars=lista_etiquetas[0:lista_etiquetas.index('ENERO')],
                value_vars= lista_etiquetas[lista_etiquetas.index('ENERO'):len(df1.columns)],
                var_name= 'MES',#Asignar año del respectivo reporte de producción
                value_name='PRODUCCION_MES')
    
    #Agregar etiqueta año al indice---
    
    anhos= anho(url)
    
    anio = "PRODUCCION_" + anho(url)
    try:    
        # CONECTAMOS, AGREGAMOS Y CERRAMOS ESTA BASE DE DATOS A MEDIDA QUE LLAMAMOS NUEVOS URLS
        miConexion = sqlite3.connect("BASE_DATOS_ANH_BLIND_TEST")
        df1.to_sql(anio, miConexion, if_exists="replace")
        miConexion.close()
    except:
        return "POR FAVOR INGRESE URL DIFERENTE O CONFIRME QUE LO INGRESO BIEN."
    
    
    return df1

# Determinar el año de la respectiva url-----------------
def anho(url:str )-> str:
    try:
        #
        if 'rudo%2020' in url:        
         anho= url[url.find('rudo%2020')+7:url.find('rudo%2020')+11]
        elif 'rudo_20' in url:    
         anho= url[url.find('rudo_20')+5:url.find('rudo_20')+9]      
        elif 'rudo-20' in url:
         anho= url[url.find('rudo-20')+5:url.find('rudo-20')+9]
        else:    
         anho= url[url.find('%2020')+3:url.find('%2020')+7]
        
        return anho
    except: return 'Por favor ingrese una url con reporte de producción fiscalizada'
    

#Determinar el numero de dias por mes-----------------------------------------------

def es_bisiesto(anho: int) -> bool:
    return anho % 4 == 0 and (anho % 100 != 0 or anho % 400 == 0)


#def obtener_dias_del_mes(mes: int, anho: int) -> int:
def obtener_dias_del_mes(mes: str, anho: int) -> int:
    
    # Abril, junio, septiembre y noviembre tienen 30
    
    if (mes=='ABRIL') or (mes=='JUNIO') or (mes=='SEPTIEMBRE') or (mes == 'NOVIEMBRE'):
        return 30
    # Febrero depende de si es o no bisiesto
    if mes == 'FEBRERO':
        if es_bisiesto(anho):
            return 29
        else:
            return 28
    else:
        # En caso contrario, tiene 31 días
        return 31
seguir = True
while (seguir==True):
    Nueva_url = input("Desea Ingresar nueva URL de datos oficiales, ingrese SI sino NO: ")
    bandera = True
    if (Nueva_url=="SI"):
        seguir=True
    if (Nueva_url== "NO"):
        seguir=False
    else:

        while bandera == True :
            url = input("Ingrese URL : ")
            if (len(url)<2):
            # COLOCAR POSIBLES VALIDACIONES DE LA URL( ESPACIOS, ETC)
                print("LA URL ES INCORRECTA POR FAVOR VUELVA A INGRESAR UNA URL VALIDA")
            else:
                TABLA = archivos(url)
                bandera=False
                
print("PROGRAMA FINALIZADO, POR FAVOR REVISE ARCHIVO DE BASE DE DATOS DE DATOS OFICIALES EN SU CARPETA")              
            # else:
seguir1 = True
while (seguir1==True):
    Nueva_url = input("Desea Ingresar nueva URL de Blind Test, ingrese SI sino NO: ")
    bandera1 = True
    if (Nueva_url=="SI"):
        seguir1=True
    if (Nueva_url== "NO"):
        seguir1=False
    else:

        while bandera1 == True :
            url = input("Ingrese URL : ")
            if (len(url)<2):
            # COLOCAR POSIBLES VALIDACIONES DE LA URL( ESPACIOS, ETC)
                print("LA URL ES INCORRECTA POR FAVOR VUELVA A INGRESAR UNA URL VALIDA")
            else:
                TABLA = archivos_blind_tests(url)
                bandera1=False            
           
print("PROGRAMA FINALIZADO, POR FAVOR REVISE ARCHIVO DE BASE DE DATOS DE BLIND TESTS EN SU CARPETA")    

# ARCHIVOS GITHUB 
# 2013
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Producci%C3%B3n%20fiscalizada%20de%20crudo%20a%C3%B1o%202013.xlsx?raw=true"))
# 2014 
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Producci%C3%B3n%20fiscalizada%20de%20crudo_2014_31122014.xlsx?raw=true"))
# 2015
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Producci%C3%B3n%20Fiscalizada%20Crudo%202015.xlsx?raw=true"))
# 2016 
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Producci%C3%B3n%20fiscalizada%20crudo%202016_18042018.xls?raw=true"))
# 2017 
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Produccion-fiscalizada-crudo-2017.xlsx?raw=true"))
# 2018 
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Producci%C3%B3n%20Fiscalizada%20Crudo%202018.xlsx?raw=true"))
# 2019
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Producci%C3%B3n%20Fiscalizada%20Crudo%202019-DIC.xlsx?raw=true"))
# 2020 
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Producci%C3%B3n%20Fiscalizada%20Crudo%202020%20Agosto.xlsx?raw=true"))
# BLIND TEST 2017
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Data_BlindTest/Producci%C3%B3n%20Fiscalizada%20Crudo%202017.xlsx?raw=true"))
# BLIND TEST 2018
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Data_BlindTest/Producci%C3%B3n%20Fiscalizada%20Crudo_2018_12458.xlsx?raw=true"))
# BLIND TEST 2019
# print(archivos("https://github.com/specolombiahackathon/202010/blob/main/Data_BlindTest/Producci%C3%B3n%20Fiscalizada%20Crudo%20ANH%20Colombia%202019%20-%20final.xlsx?raw=true"))


# ARCHIVOS PAGINA ANH
#2013
#url = "https://www.anh.gov.co/Operaciones-Regal%c3%adas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%c3%b3n%20fiscalizada%20de%20crudo%20a%c3%b1o%202013.xlsx"
#2014
# url ="https://www.anh.gov.co/Operaciones-Regal%c3%adas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%c3%b3n%20fiscalizada%20de%20crudo_2014_31122014.xlsx"
#2015
# url = "https://www.anh.gov.co/Operaciones-Regal%c3%adas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%c3%b3n%20Fiscalizada%20Crudo%202015.xlsx"
#2016
#url = "https://www.anh.gov.co/Operaciones-Regal%c3%adas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%c3%b3n%20fiscalizada%20crudo%202016_18042018.xls"
#2017
#url = "https://www.anh.gov.co/Operaciones-Regal%c3%adas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Produccion-fiscalizada-crudo-2017.xlsx"
#2018
#url = "https://www.anh.gov.co/Operaciones-Regal%c3%adas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%c3%b3n%20Fiscalizada%20Crudo%202018.xlsx"
#2019
# url = "https://www.anh.gov.co/Operaciones-Regal%c3%adas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%c3%b3n%20Fiscalizada%20Crudo%202019-DIC.xlsx"
#2020 Agosto
# url = "https://www.anh.gov.co/Operaciones-Regal%C3%ADas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documentos%20compartidos/Producci%C3%B3n%20Fiscalizada%20Crudo%202020%20Agosto.xlsx"