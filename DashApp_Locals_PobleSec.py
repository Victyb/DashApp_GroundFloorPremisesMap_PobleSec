import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Cargar datos
df = pd.read_csv(r"C:\Users\victor.bousquet\OneDrive - Barcelona Activa\Documentos\CaP\filtered_poble_sec_data2.csv")

# Inicializar la app
app = dash.Dash(__name__)

# Valores únicos para los filtros
sectors = sorted(df['Nom_Sector_Activitat'].dropna().unique())
groups = sorted(df['Nom_Grup_Activitat'].dropna().unique())
activities = sorted(df['Nom_Activitat'].dropna().unique())

# Determinar el layout
app.layout = html.Div([
    html.H2("Mapa de locals en planta baixa destinats a activitat econòmica al Poble Sec"),

    html.Div([
        html.Label("Filtrar pel sector de l'activitat"),
        dcc.Dropdown(
            options=[{'label': s, 'value': s} for s in sectors],
            value=None,
            id='sector-filter',
            multi=True,
            placeholder="Selecciona un o més sectors"
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Filtrar pel nom del grup d'activitats"),
        dcc.Dropdown(
            options=[{'label': g, 'value': g} for g in groups],
            value=None,
            id='group-filter',
            multi=True,
            placeholder="Selecciona un o més grups"
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Filtrar pel nom de l'activitat"),
        dcc.Dropdown(
            options=[{'label': a, 'value': a} for a in activities],
            value=None,
            id='activity-filter',
            multi=True,
            placeholder="Selecciona una o més activitats"
        ),
    ], style={'width': '30%', 'display': 'inline-block'}),

    dcc.Graph(id='map-graph')
])

# Callback para actualizar el mapa
@app.callback(
    Output('map-graph', 'figure'),
    Input('sector-filter', 'value'),
    Input('group-filter', 'value'),
    Input('activity-filter', 'value')
)
def update_map(selected_sectors, selected_groups, selected_activities):
    filtered_df = df.copy()
    if selected_sectors:
        filtered_df = filtered_df[filtered_df['Nom_Sector_Activitat'].isin(selected_sectors)]
    if selected_groups:
        filtered_df = filtered_df[filtered_df['Nom_Grup_Activitat'].isin(selected_groups)]
    if selected_activities:
        filtered_df = filtered_df[filtered_df['Nom_Activitat'].isin(selected_activities)]

    # Crear columna personalizada para mostrar en el hover
    filtered_df["Info"] = (
        "Nom de l'activitat: " + filtered_df["Nom_Activitat"].astype(str) + "<br>" +
        "Nom del local: " + filtered_df["Nom_Local"].astype(str) + "<br>" +
        "Nom de la via: " + filtered_df["Nom_Via"].astype(str) + "<br>" +
        "Direcció: " + filtered_df["Direccio_Unica"].astype(str)
    )

    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitud",
        lon="Longitud",
        hover_name="Info",
        color_discrete_sequence=["red"],
        zoom=14,
        height=700
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    fig.update_traces(marker=dict(size=8, color="blue"))

    return fig

# Ejecutar la app con manejo de interrupciones (en consola Ctrl+C)
if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("App detenida manualmente. Cerrando de forma segura...")
