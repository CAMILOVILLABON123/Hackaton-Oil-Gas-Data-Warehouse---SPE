import pandas as pd
import plotly.express as px  # (version 4.7.0)
import dash  # (version 1.12.0) pip install dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sqlite3

# SE CONSULTAN A LA BASE DE DATOS CREADA ANTERIORMENTE EN EL ARCHIVO DE LECTURA
db = sqlite3.connect('BASE_DATOS_ANH_DATOS_OFICIALES')
df_2013 = pd.read_sql_query('SELECT * FROM PRODUCCION_2013 ', db)
df_2014 = pd.read_sql_query('SELECT * FROM PRODUCCION_2014 ', db)
df_2015 = pd.read_sql_query('SELECT * FROM PRODUCCION_2015 ', db)
df_2016 = pd.read_sql_query('SELECT * FROM PRODUCCION_2016 ', db)
df_2017 = pd.read_sql_query('SELECT * FROM PRODUCCION_2017 ', db)
df_2018 = pd.read_sql_query('SELECT * FROM PRODUCCION_2018 ', db)
df_2019 = pd.read_sql_query('SELECT * FROM PRODUCCION_2019 ', db)
df_2020 = pd.read_sql_query('SELECT * FROM PRODUCCION_2020 ', db)
# POR FAVOR ELIJA BASE DE DATOS DESEADA PARA EJECUTAR EN LA INTERFAZ
# DEBIDO A QUE "df" SERA SU BASE DE DATOS A EJECUTAR EN EL AÑO DESEADO
df=df_2014
# SE PREGUNTA AL USUARIO QUE BASE DE DATOS DESEA VISUALIZAR EN LA INTERFAZ


# -------------------------------------------------------------------------------------
app = dash.Dash(__name__, prevent_initial_callbacks=True) # PRESENTA LA VERSION DE DASH
# SE CREA EL DISEÑO DE NUESTRA INTERFAZ
app.layout = html.Div([
    
# SE CREAN NUESTROS RESPECTIVOS COMPONENTES COMO NUESTRA TABLAS Y NUESTRO DESPLEGABLE

      html.Div([
#CREAMOS NUESTRO DESPLEGABLE CON NUESTRAS ETIQUETAS VACIAS 
    html.Div([
        html.Label(['PRODUCCION FISCALIZADA DE CRUDO']),
        dcc.Dropdown(
            id="my_dropdown",
            options=[
                         {'label': 'DEPARTAMENTO', 'value': 'DEPARTAMENTO'},
                         {'label': 'OPERADORA', 'value': 'OPERADORA'},
                         # {'label': 'Age', 'value': 'Age', 'disabled':True},
                         {'label': 'CONTRATO', 'value': 'CONTRATO'},
                         # {'label': 'Borough', 'value': 'Borough'},
                         {'label': 'CAMPO', 'value': 'CAMPO'}
            ],
            value = 'DEPARTAMENTO',
            multi=False,
            clearable=False,
            style={"width":"50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
        
    ]),
    ],className='row'),
# CREAMOS NUESTRA TABLA DINAMICA DONDE EL USUARIO PODRA INTERACTUAR CON DISTINTAS FUNCIONES, ENTRE
# ESAS: FILTRADO DE DATOS, ELIMINAR U OCULTAR COLUMNAS, ETC
    html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            if i == "MUNICIPIO" or i == "CUENCA" 
            else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df.columns
         ],
        data=df.to_dict('records'),  # the contents of the table
        editable=False,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=6,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['index', 'PRODUCCION']
        ],
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),
    html.Br(),
    html.Br(),
    html.Div(id='bar-container'),
    html.Div(id='choromap-container')

    ],className='row'),
          
])
# --------------------------------------------------------------------------------------


# HACEMOS UN LLAMADO A NUESTROS COMPONENTES, EN ESTE CASO NUESTRA TABLA DINAMICA PARA CREAR
# NUESTRO DIAGRAMA DE BARRAS
@app.callback(
     Output(component_id='bar-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells')]
)
# CREAMOS UNA FUNCION QUE CONSTANTEMENTE NOS ACTUALICE NUESTRO DIAGRAMA DE BARRAS
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    print('***************************************************************************')
    print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    print('---------------------------------------------')
    print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
    print('---------------------------------------------')
    print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
    print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
    print("---------------------------------------------")
    print("Complete data of active cell: {}".format(actv_cell))
    print("Complete data of all selected cells: {}".format(slctd_cell))

    dff1 = pd.DataFrame(all_rows_data)

    # used to highlight selected countries on bar chart
    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff1))]
# CREAMOS 4 GRAFICAS SEGUN LOS REQUERIMIENTOS DEL PROBLEMA, PRODUCCION POR CAMPO, POR CONTRATO
# POR OPERADORA Y POR DEPARTAMENTO.
    if "CAMPO" in dff1 and "CONTRATO" in dff1 and "OPERADORA" in dff1 and "DEPARTAMENTO" in dff1 and "PRODUCCION_MES" in dff1 :
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff1,
                          x="CAMPO",
                          y='PRODUCCION_MES',
                          labels={"PRODUCCION_MES": "PRODUCCION MENSUAL DE CRUDO (BBL)"}
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
                      ),
            dcc.Graph(id='bar-chart2',
                      figure=px.bar(
                          data_frame=dff1,
                          x="CONTRATO",
                          y='PRODUCCION_MES',
                          labels={"PRODUCCION_MES": "PRODUCCION MENSUAL DE CRUDO (BBL)"}
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
                      ),
            dcc.Graph(id='bar-chart3',
                      figure=px.bar(
                          data_frame=dff1,
                          x="OPERADORA",
                          y='PRODUCCION_MES',
                          labels={"PRODUCCION_MES": "PRODUCCION MENSUAL DE CRUDO (BBL)"}
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
                      ),
            dcc.Graph(id='bar-chart4',
                      figure=px.bar(
                          data_frame=dff1,
                          x="DEPARTAMENTO",
                          y='PRODUCCION_MES',
                          labels={"PRODUCCION_MES": "PRODUCCION MENSUAL DE CRUDO (BBL)"}
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
                      )
        ]

# ----------------------------------------------------------------------------------
# LLAMAMOS NUESTRO DIAGRAMA DE TORTA 
@app.callback(
    Output(component_id='the_graph',component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]

)        
#CREAMOS NUESTRA FUNCION PARA QUE NOS ACTUALICE NUESTRO DESPLEGABLE Y NUESTRO
#DIAGRAMA DE TORTA 
def update_graph(my_dropdown):
    dff=df
    piechart=px.pie(
            data_frame=dff,
            names= my_dropdown,
            hole=.3,
            )        
    return (piechart)
# ----------------------------------------------------------------------------------
# FINALIZAMOS LA LECTURA DEL CODIGO Y EJECUTAMOS NUESTRA INTERFAZ EN EL SERVIDOR
if __name__ == '__main__':
    app.run_server(debug=True)
# DIRECCIONARSE A LA DIRECCION WEB GENERADA POR EL CODIGO O EN EL DEBIDO CASO COPIAR
# Y PEGAR EL LINK EN SU NAVEGADOR DE PREFERENCIA.
    
# LA INTERFAZ TIENE VARIAS FUNCIONALIDADES PARA INTERACTUAR CON EL USUARIO TALES COMO:
# FILTRADO, SELECCION,ELIMINACION, OCULTAR COLUMNAS, RECORRER LA TABLA ENTRE OTRAS
# LAS GRAFICAS SE PUEDEN DESCARGAR EN FORMATO DE IMAGEN
# EL DIAGRAMA DE BARRAS PERMITE INTERACTUAR Y FILTRAR DATOS DESEADOS A LA PAR CON NUESTRA TABLA
# EL DIAGRAMA DE TORTA PERMITE SELECCIONAR LOS PARAMETROS QUE SE DESEEN VISUALIZAR Y ACTUALIZAR EL DIAGRAMA.

