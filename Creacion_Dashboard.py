# Instalación de módulos
import pip
pip.main(["install","plotly-express"])
pip.main(["install","openpyxl"])


# 1° Ingreso de módulos
import os
import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.subplots as sp
import openpyxl

# 2° Ingreso de valores
title_page_web='Recloser' #Título del Dashboard
title_portada='🖥️ Recloser|Respuesta|Comunicación' #Título del Dashboard
name_empresa='Consorcio CASCADE' #Título del Dashboard

ancho_tabla_datos="1000px"
alto_tabla_datos="400px"

n_fig_AMT=6 # Número de figuras para la figura: recloser por alimentador.
n_row_AMT=3 # Número de filas de la figura: recloser por alimentador.
n_column_AMT=2 # Número de columnas de la figura: recloser por alimentador.
Ancho_AMT,height_AMT=8000,8000 # Dimensiones del ancho y la altura de los subplots de la figura: recloser por alimentador.

name_excel='Registros.xlsx' #Ingrese el nombre del excel con extensión.
# hoja_excel = '25-10-2023' #Hoja de excel que contendrá la base de datos.

#********************************************************************************************************
# 3° Nombres de la página web.
st.set_page_config(page_title = title_page_web, #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = '\u26A1', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

st.title(title_portada)
st.subheader(name_empresa)
st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown


# 4° Abre el libro de Excel "Registros.xlsx"
direc_actual = os.path.dirname(os.path.abspath(__file__))# Ruta del directorio actual del script  
direc=direc_actual+f'\\{name_excel}'

workbook = openpyxl.load_workbook(direc)
sheet_names = []# Lista que almacenará los nombres de las hojas
for sheet in workbook.sheetnames:# Recorre todas las hojas del libro
    if sheet != "SELECTORES":
        sheet_names.append(sheet)
workbook.close()# Cierra el libro
print(sheet_names) #Lista que almacena el nombre de las hojas del excel

# Usamos el widget selectbox para seleccionar una hoja
hoja_excel = st.sidebar.selectbox("Fecha:", sheet_names)



# 5° Lectura de los datos de la hoja excel seleccionada.
df = pd.read_excel(direc,sheet_name = hoja_excel)

# 5° Creación de tablas
#5.1 Creación de filtros
st.sidebar.header("Opciones a filtrar:") #5.1.1 sidebar => Crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
select_all = st.sidebar.checkbox("Seleccionar todo los filtros")# 5.1.2 Casilla de verificación para seleccionar todos los filtros

# Filtro de Departamento
dpto = st.sidebar.multiselect(
    "Seleccione el Departamento:",
    options=['Seleccionar todo'] + df['DEPARTAMENTO'].unique().tolist(),
    default=[],
)

if 'Seleccionar todo' in dpto:
    dpto = df['DEPARTAMENTO'].unique().tolist()

# Filtro de Unidad de Negocio (se habilita en función de la selección de Departamento)
unidad_negocio_options = df[df['DEPARTAMENTO'].isin(dpto)]['UNIDAD DE NEGOCIO'].unique()
unidad_negocio = st.sidebar.multiselect(
    "Seleccione la Unidad de Negocio:",
    options=['Seleccionar todo'] + unidad_negocio_options.tolist(),
    default=[],
)

if 'Seleccionar todo' in unidad_negocio:
    unidad_negocio = unidad_negocio_options.tolist()

# Filtro de Subestación (se habilita en función de la selección de Unidad de Negocio)
se_options = df[
    (df['DEPARTAMENTO'].isin(dpto)) &
    (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio))
]['SUBESTACION'].unique()
se = st.sidebar.multiselect(
    "Seleccione la Subestación:",
    options=['Seleccionar todo'] + se_options.tolist(),
    default=[],
)

if 'Seleccionar todo' in se:
    se = se_options.tolist()

# Filtro de Operador (se habilita en función de la selección de Subestación)
operador_options = df[
    (df['DEPARTAMENTO'].isin(dpto)) &
    (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
    (df['SUBESTACION'].isin(se))
]['OPERADOR INSTALADO'].unique()
operador = st.sidebar.multiselect(
    "Seleccione el Operador:",
    options=['Seleccionar todo'] + operador_options.tolist(),
    default=[],
)

if 'Seleccionar todo' in operador:
    operador = operador_options.tolist()

# Filtro de Alimentador (AMT) - Filtrado en base a todas las selecciones anteriores
amt_options = df[
    (df['DEPARTAMENTO'].isin(dpto)) &
    (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
    (df['SUBESTACION'].isin(se)) &
    (df['OPERADOR INSTALADO'].isin(operador))
]['AMT'].unique()
amt = st.sidebar.multiselect(
    "Seleccione el Alimentador (AMT):",
    options=['Seleccionar todo'] + amt_options.tolist(),
    default=[],
)

if 'Seleccionar todo' in amt:
    amt = amt_options.tolist()

# 5.3° Seleccionar todos los filtros
if select_all:
    dpto = df['DEPARTAMENTO'].unique()
    unidad_negocio_options = df['UNIDAD DE NEGOCIO'].unique()
    unidad_negocio = unidad_negocio_options
    se_options = df['SUBESTACION'].unique()
    se = se_options
    operador_options = df['OPERADOR INSTALADO'].unique()
    operador = operador_options
    amt_options = df['AMT'].unique()
    amt = amt_options


# 5.4 Filtra el DataFrame en función de las selecciones:
filtered_df_UN = df[
    (df['DEPARTAMENTO'].isin(dpto)) &
    (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio))
]

filtered_df_SE = df[
    (df['DEPARTAMENTO'].isin(dpto)) &
    (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
    (df['SUBESTACION'].isin(se))
]

filtered_df = df[
    (df['DEPARTAMENTO'].isin(dpto)) &
    (df['UNIDAD DE NEGOCIO'].isin(unidad_negocio)) &
    (df['SUBESTACION'].isin(se)) &
    (df['OPERADOR INSTALADO'].isin(operador)) &
    (df['AMT'].isin(amt))
]

# 5.5 Muestra la tabla con los datos filtrados
st.markdown(f"<p style='font-size: 20px; text-align: center; font-weight: bold;'>TABLA DE DATOS </p>", unsafe_allow_html=True)
filtered_df_reinicio = filtered_df.reset_index()  # Reiniciar el índice del DataFrame
del filtered_df_reinicio["index"]

# Ordenar las filas del dataframe:

filtered_df_reinicio = filtered_df_reinicio.sort_values(by=filtered_df_reinicio.columns.tolist())

# Filtro de los campos
selected_columns = st.multiselect(
    "Seleccione el(los) campo(s) a mostrar:",
    options=['Seleccionar todo'] + filtered_df_reinicio.columns[4:-2].tolist(),
    default=[],
)

if 'Seleccionar todo' in selected_columns: 
    selected_columns = filtered_df_reinicio.columns[4:-2].tolist() 

#Mostrar las 4 primeras columnas y las dos últimas
selected_columns = filtered_df_reinicio.columns[:4].tolist() + selected_columns + filtered_df_reinicio.columns[-2:].tolist()

# Reorganizar las columnas del DataFrame según el orden de selección
filtered_df_reinicio = filtered_df_reinicio[selected_columns]

column_names = filtered_df_reinicio.columns.tolist()# Lista de las columnas de la tabla de datos "filtered_df_reinicio"
filtered_df_reinicio = filtered_df_reinicio[df.columns.intersection(column_names)]# Ordenar las columnas en base al orden del "df => Excel"

filtered_df_reinicio = filtered_df_reinicio.reset_index(drop=True)# Reiniciar la enumeración del DataFrame
filtered_df_reinicio.index = filtered_df_reinicio.index + 1 #Hacer que primera fila no sea "0"

#Mostar el dataframe como una tabla:
container = st.empty()

container.markdown(
    f'<div style="overflow: auto; width: {ancho_tabla_datos}; height: {alto_tabla_datos}; scrollbar-width: auto;">'
    f'{filtered_df_reinicio.style.set_properties(**{"width": "auto", "text-align": "center"}).to_html(escape=False)}</div>',
    unsafe_allow_html=True,
)

# 6° Impresión de datos generales:
st.markdown("---") #separador
# Cuenta el número de "Si" y "No" en la columna "Rpta actual"
si_rpta = filtered_df['Rpta actual'].value_counts().get('Si', 0)
no_rpta = filtered_df['Rpta actual'].value_counts().get('No', 0)

# Cuenta el número de "Si" y "No" en la columna "Comunicación actual"
si_comunicacion = filtered_df['Comunicación actual'].value_counts().get('Si', 0)
no_comunicacion = filtered_df['Comunicación actual'].value_counts().get('No', 0)

# Calcula el total de elementos en cada columna
total_rpta = len(filtered_df)
total_comunicacion = len(filtered_df)

# Impresión de KPIs
st.markdown(f"<p style='font-size: 24px; text-align: center; font-weight: bold;'>Recloser instalados: {total_rpta}</p>", unsafe_allow_html=True)

left_column, right_column = st.columns(2)

with left_column:
    st.markdown(f"<p style='font-size: 22px'>Tienen respuesta: {si_rpta}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px'>     - Tienen comunicación: {si_comunicacion}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px'>     - No tienen comunicación: {no_comunicacion}</p>", unsafe_allow_html=True)

with right_column:
    st.markdown(f"<p style='font-size: 22px;  text-align: Right'>No tienen respuesta: {no_rpta}</p>", unsafe_allow_html=True)            

# 6° Guardar el gráfico de barras en la siguiente variable
try:

# 6.2° Agrupar por 'UNIDAD DE NEGOCIO' => "Nro de recloser instalados"----------------->DIAGRAMA DE PASTEL
    st.markdown("---") #separador
    st.markdown(f"<p style='font-size: 20px; text-align: center; font-weight: bold;'>Porcentaje de recloser instalados por Unidad de Negocio</p>\n", unsafe_allow_html=True)
    # Agregar una nueva columna 'Contador de "Si"'
    filtered_df_UN['Recloser con respuesta'] = filtered_df_UN['Rpta actual'].apply(lambda x: x.count('Si'))
    filtered_df_UN['Recloser sin respuesta'] = filtered_df_UN['Rpta actual'].apply(lambda x: x.count('No'))
    filtered_df_UN['Recloser con comunicación'] = filtered_df_UN['Comunicación actual'].apply(lambda x: x.count('Si'))
    filtered_df_UN['Recloser sin comunicación'] = filtered_df_UN['Comunicación actual'].apply(lambda x: x.count('No'))

    # Agrupar y sumar los valores
    grouped_2 = filtered_df_UN.groupby('UNIDAD DE NEGOCIO').agg({
        'UNIDAD DE NEGOCIO': 'first',  # Añadir la primera columna
        'Recloser con respuesta': 'sum',
        'Recloser sin respuesta': 'sum',
        'Recloser con comunicación': 'sum',
        'Recloser sin comunicación': 'sum'
    })

    # Calcular el número de Recloser instalados en cada UNIDAD DE NEGOCIO
    grouped_2['Recloser instalados'] = filtered_df_UN['UNIDAD DE NEGOCIO'].value_counts().reindex(grouped_2.index)
    
    # Crear el diagrama de pastel
    fig, ax = plt.subplots(figsize=(4, 4))

    grouped_2 = grouped_2.sort_values(by='Recloser instalados', ascending=False) # Ordenar en base al número de recloser con respuesta.

    ax.pie(
        grouped_2['Recloser instalados'],
        labels=None,  # No mostrar etiquetas
        startangle=90,
        rotatelabels=False,
        pctdistance=0.65
    )

    ax.axis('equal')

    # Crear una leyenda personalizada
    total_valores =  grouped_2['Recloser instalados'].sum()
    encabezados = grouped_2.columns.tolist()
    legend_labels = [f'{label} ({value/total_valores*100:.1f}%)' for label, value in zip(grouped_2['UNIDAD DE NEGOCIO'], grouped_2['Recloser instalados'])]
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='C{}'.format(i), markersize=10) for i in range(len(legend_labels))]
    ax.legend(legend_handles, legend_labels, title="Porcentaje (%)", loc="center left", bbox_to_anchor=(1, 0.5))

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # 6.1.4° Imprimir tabla
    grouped_2.reset_index(drop=True, inplace=True)
    grouped_2.index=grouped_2.index + 1 #Hacer que primera fila no sea "0"
    st.dataframe(grouped_2, use_container_width=True)  # Muestra la tabla debajo del gráfico

    #******************************************************************************************************************************************************************************************************************
    #******************************************************************************************************************************************************************************************************************

    # 6.2° Agrupar por 'SUBESTACIÓN' => "Nro de respuestas y comunicación de los recloser"----------------->DIAGRAMA DE BARRAS EN HORIZONTAL
    st.markdown("---") #separador
    # Agregar una nueva columna 'Contador de "Si"'
    grouped_1 = pd.DataFrame()

    filtered_df_SE['Recloser con respuesta'] = filtered_df_SE['Rpta actual'].apply(lambda x: x.count('Si'))
    filtered_df_SE['Sin Respuesta actual'] = filtered_df_SE['Rpta actual'].apply(lambda x: x.count('No'))
    filtered_df_SE['Recloser con comunicación'] = filtered_df_SE['Comunicación actual'].apply(lambda x: x.count('Si'))
    filtered_df_SE['Sin Comunicación actual'] = filtered_df_SE['Comunicación actual'].apply(lambda x: x.count('No'))

    # Agrupar y sumar los valores
    grouped_1 = filtered_df_SE.groupby('SUBESTACION').agg({
        'Recloser con respuesta': 'sum',
        'Sin Respuesta actual': 'sum',
        'Recloser con comunicación': 'sum',
        'Sin Comunicación actual': 'sum'
    })
    grouped_1['Recloser instalados'] = filtered_df_SE['SUBESTACION'].value_counts().reindex(grouped_1.index) # Conteo de recloser por SE.

    # 6.1.4° Imprimir tabla
    grouped_1 = grouped_1.sort_values(by='Recloser con respuesta', ascending=False) # Ordenar en base al número de recloser instalados.

    fig_rpta_SE = px.bar(grouped_1, x=['Recloser con respuesta','Sin Respuesta actual'],  y=grouped_1.index,
                            orientation= "h", #horizontal bar chart
                            color_discrete_sequence=["blue", "red"],
                            #color_discrete_sequence=px.colors.qualitative.Set3,  # Colores diferentes
                            template='plotly_white')  # Ajustar el ancho
    
    fig_com_SE = px.bar(grouped_1, x=['Recloser con comunicación','Sin Comunicación actual'],  y=grouped_1.index,
                        orientation= "h", #horizontal bar chart
                        color_discrete_sequence=["blue", "green"],
                        #color_discrete_sequence=px.colors.qualitative.Set3,  # Colores diferentes
                        template='plotly_white')  # Ajustar el ancho

    fig_rpta_SE.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title='Subestaciones',  # Nombre del eje y
        xaxis_title='Cantidad de recloser',  # Nombre del eje x
        title_text="<b>Respuesta de recloser por Subestación</b>",
        title_x=0,  # Alinear a la izquierda
        autosize=True,  # Ajustar automáticamente al ancho disponible
        height=1200  # Aumenta la altura a 600 píxeles (ajusta este valor según tus necesidades)

    )

    fig_com_SE.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title='Subestaciones',  # Nombre del eje y
        xaxis_title='Cantidad de recloser',  # Nombre del eje x
        title_text="<b>Comunicación de recloser por Subestación</b>",
        title_x=0,  # Alinear a la izquierda
        autosize=True,  # Ajustar automáticamente al ancho disponible
        height=1200  # Aumenta la altura a 600 píxeles (ajusta este valor según tus necesidades)

    )
    # st.plotly_chart(fig_rpta_SE)# Mostrar el gráfico en Streamlit

    # 6.1.3° Colocar las gráficas con arreglo ( 1 x 2 )

    left_column, right_column = st.columns(2)

    left_column.plotly_chart(fig_rpta_SE, use_container_width = True) #esta va al lado izquierdo
    right_column.plotly_chart(fig_com_SE, use_container_width = True)



    # Imprimir la numeración de las filas y el DataFrame
    summary_df1 = grouped_1.reset_index()  # Reiniciar el índice del DataFrame
    # summary_df1 = summary_df1.drop(["Sin Comunicación actual"], axis=1) #Eliminamos las filas del dataframe a mostrar.
    summary_df1.index = summary_df1.index + 1  # Hacer que la primera fila sea "1" en lugar de "0"
    st.dataframe(summary_df1, use_container_width=True)  # Muestra la tabla debajo del gráfico

    #******************************************************************************************************************************************************************************************************************
    #******************************************************************************************************************************************************************************************************************
    st.markdown("---") #separador
    # 6.1° Agrupar por 'AMT' => El 'Nro de respuestas' y 'Nro de intermitencias'
    grouped = filtered_df.groupby('AMT')[['Nro de respuestas', 'Nro de intermitencias','Nro de muestras']].sum()
    grouped['Recloser instalados'] = filtered_df['AMT'].value_counts().reindex(grouped.index) # Nro de recloser en cada AMT
    grouped = grouped.sort_values(by='Recloser instalados', ascending=False) # Ordenar en orden: (True)-Ascendente ; (False)-Descendente

    # 6.1.1° Crear el gráfico de barras con subcolumnas y ajustar el ancho
    # fig_rpta_interm = sp.make_subplots(rows=4, cols=2, column_widths=[8000, 8000], row_heights=[8000, 8000, 8000, 8000], vertical_spacing=0.2, horizontal_spacing=0.2)#, subplot_titles=['Subplot 1', 'Subplot 2', ...])

    l_column_widths_AMT=[Ancho_AMT]*n_column_AMT
    l_row_heights_AMT=[Ancho_AMT]*n_row_AMT
    
    fig_rpta_interm = sp.make_subplots(rows=n_row_AMT, cols=n_column_AMT, column_widths=l_column_widths_AMT, row_heights=l_row_heights_AMT, vertical_spacing=0.2, horizontal_spacing=0.2)#, subplot_titles=['Subplot 1', 'Subplot 2', ...])


    # Agregar los gráficos a cada subsubplot
    grouped_aux = grouped.sort_values(by='Nro de respuestas', ascending=True).copy()
    total_filas_grouped_aux = len(grouped_aux)
    division_entera, residuo = divmod(total_filas_grouped_aux, n_fig_AMT)    
    #Obtener el nuevo residuo cuando el cociente se incrementa en 1
    division_entera+=1
    residuo=total_filas_grouped_aux-division_entera*n_fig_AMT
    
    #Creación de la lista donde se mostrarán las figuras
    lista_valores = [division_entera] * n_fig_AMT
    lista_valores[-1] += residuo


    indice_inicial = 0
    for i in range(n_fig_AMT):
        col_idx = i % 2 + 1
        row_idx = i // 2 + 1
        
        # Obtiene el límite superior del bloque actual
        limite_superior = indice_inicial + lista_valores[i]
        
        # Crea un nuevo DataFrame copiando las filas correspondientes
        df_aux = grouped.iloc[indice_inicial:limite_superior].copy()
        df_aux = df_aux.sort_values(by='Nro de intermitencias', ascending=True) # Ordenar en orden: (True)-Ascendente ; (False)-Descendente
        # Puedes imprimir df_aux o realizar cualquier otra operación con él aquí
        
        # Actualiza el índice inicial para el próximo ciclo
        indice_inicial = limite_superior
            
        
        subfig = go.Figure(data=[
            go.Bar(x=df_aux.index, y=df_aux['Nro de respuestas'], name='Nro de respuestas'),
            go.Bar(x=df_aux.index, y=df_aux['Nro de intermitencias'], name='Nro de intermitencias')
        ])
        subfig.update_layout(showlegend=True)

        fig_rpta_interm.add_trace(subfig.data[0], row=row_idx, col=col_idx)
        fig_rpta_interm.add_trace(subfig.data[1], row=row_idx, col=col_idx)

    # 6.1.2° Configuración de diseño
    fig_rpta_interm.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False), #tickangle=-45),
        xaxis_title='AMT',
        title_x=0.5,
        autosize=False  # Desactivar el ajuste automático al ancho disponible
    )

    fig_rpta_interm.update_layout(title_text="<b>Respuesta por Alimentador (AMT)</b>", title_x=0, title_y=0.97, title_font_size=20)

    st.plotly_chart(fig_rpta_interm)

    
    # 6.1.3° Mostrar la tabla de resumen
    summary_df = grouped.reset_index()  # Reiniciar el índice del DataFrame
    summary_df.index = summary_df.index + 1  # Hacer que la primera fila sea "1" en lugar de "0"
    st.dataframe(summary_df, use_container_width=True)  # Muestra la tabla debajo del gráfico

    
    # **************************************
    st.markdown("---") #separador
    # Estilo del "Streamlit"
    hide_st_style = """
            <style>
   
            footer {visibility: hidden;}

            </style>
            """

    st.markdown(hide_st_style, unsafe_allow_html= True)

except Exception as e:
    st.markdown(f"....(Espera)")