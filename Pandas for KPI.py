import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Function to load CSV files from a folder
def load_csv_files_from_folder(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    dataframes = {}
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        try:
            df = pd.read_csv(file_path, delimiter=',')
            df.columns = df.columns.str.strip()
            df.dropna(inplace=True)
            dataframes[csv_file] = df
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
    return dataframes

# Initialize the Dash app
# app = Dash(__name__, external_stylesheets=[r"C:\Users\user\DTS Dropbox\Ehsan Nawaz\Old Dropbox files\Post Processing\Hassan_Raza\WebScraping\style.css"])

# Function to create the plot
def create_plot(data, plot_type, x_axis, y_axis):
    if plot_type == 'Scatter':
        return px.scatter(data, x=x_axis, y=y_axis, color='Cell ID (0)', title=f'{y_axis} vs {x_axis}', labels={x_axis: x_axis, y_axis: y_axis})
    elif plot_type == 'Line':
        return px.line(data, x=x_axis, y=y_axis, color='Cell ID (0)', title=f'{y_axis} vs {x_axis}', labels={x_axis: x_axis, y_axis: y_axis})
    elif plot_type == 'Bar':
        return px.bar(data, x=x_axis, y=y_axis, color='Cell ID (0)', title=f'{y_axis} vs {x_axis}', labels={x_axis: x_axis, y_axis: y_axis})

# Function to calculate percentages
def calculate_percentages(df, rsrp_threshold, cinr_threshold, rsrp_filter, cinr_filter):
    total_count = len(df)
    if total_count == 0:
        return {}, 0, 0

    percentages = {}
    if 'Enable' in rsrp_filter:
        filtered_df_rsrp = df[df['R0 RSRP (0)'] > rsrp_threshold]
        rsrp_percentage = (len(filtered_df_rsrp) / total_count) * 100
    else:
        filtered_df_rsrp = df
        rsrp_percentage = 0

    if 'Enable' in cinr_filter:
        filtered_df_cinr = df[df['R0 RS CINR (0)'] > cinr_threshold]
        cinr_percentage = (len(filtered_df_cinr) / total_count) * 100
    else:
        filtered_df_cinr = df
        cinr_percentage = 0

    cell_id_percentages = {}
    for cell_id in df['Cell ID (0)'].unique():
        cell_df = df[df['Cell ID (0)'] == cell_id]
        cell_total_count = len(cell_df)
        if cell_total_count == 0:
            continue
        if 'Enable' in rsrp_filter:
            cell_filtered_df_rsrp = cell_df[cell_df['R0 RSRP (0)'] > rsrp_threshold]
            cell_rsrp_percentage = (len(cell_filtered_df_rsrp) / cell_total_count) * 100
        else:
            cell_rsrp_percentage = 0

        if 'Enable' in cinr_filter:
            cell_filtered_df_cinr = cell_df[cell_df['R0 RS CINR (0)'] > cinr_threshold]
            cell_cinr_percentage = (len(cell_filtered_df_cinr) / cell_total_count) * 100
        else:
            cell_cinr_percentage = 0

        cell_id_percentages[cell_id] = {
            'RSRP': cell_rsrp_percentage,
            'CINR': cell_cinr_percentage
        }

    return cell_id_percentages, rsrp_percentage, cinr_percentage

# App layout
app.layout = html.Div(children=[
    html.Div(className='input', children=[
        html.Label('Select Folder:', className='label'),
        dcc.Input(id='folder-path', type='text', value=r"C:\Users\user\DTS Dropbox\Ehsan Nawaz\Old Dropbox files\Post Processing")
    ]),
    html.Div(className='input', children=[
        html.Label('Select CSV File:', className='label'),
        dcc.Dropdown(id='csv-file-dropdown', options=[], value=None)
    ]),
    html.Div(className='input', children=[
        html.Label('Select Plot Type:', className='label'),
        dcc.Dropdown(
            id='plot-type-dropdown',
            options=[
                {'label': 'Scatter', 'value': 'Scatter'},
                {'label': 'Line', 'value': 'Line'},
                {'label': 'Bar', 'value': 'Bar'}
            ],
            value='Scatter'
        ),
    ]),
    html.Div(className='input', children=[
        html.Label('X Axis:', className='label'),
        dcc.Dropdown(id='x-axis-dropdown', options=[], value='Time')
    ]),
    html.Div(className='input', children=[
        html.Label('Y Axis:', className='label'),
        dcc.Dropdown(id='y-axis-dropdown', options=[], value='R0 RSRP (0)')
    ]),
    html.Div(className='input', children=[
        html.Label('Apply RSRP Threshold Filter:', className='label'),
        dcc.Checklist(
            id='apply-rsrp-filter',
            options=[{'label': 'Enable', 'value': 'Enable'}],
            value=['Enable']
        ),
        html.Label('RSRP Threshold:', className='label'),
        dcc.Input(id='rsrp-threshold', type='number', value=-100)
    ]),
    html.Div(className='input', children=[
        html.Label('Apply CINR Threshold Filter:', className='label'),
        dcc.Checklist(
            id='apply-cinr-filter',
            options=[{'label': 'Enable', 'value': 'Enable'}],
            value=['Enable']
        ),
        html.Label('CINR Threshold:', className='label'),
        dcc.Input(id='cinr-threshold', type='number', value=4)
    ]),
    html.Div(className='input', children=[
        html.Label('Select Cell ID:', className='label'),
        dcc.Dropdown(id='cell-id-dropdown', options=[], value=None)
    ]),
    html.Div(className='graph', children=[
        dcc.Graph(id='plot')
    ]),
    html.Div(className='graph', children=[
        dcc.Graph(id='rsrp-over-time')
    ]),
    html.Div(className='graph', children=[
        dcc.Graph(id='cinr-over-time')
    ]),
    html.Div(className='graph', children=[
        dcc.Graph(id='percentage-plot')
    ]),
])

# Callback to update the CSV file dropdown based on the selected folder
@app.callback(
    Output('csv-file-dropdown', 'options'),
    [Input('folder-path', 'value')]
)
def update_csv_dropdown(folder_path):
    global dataframes
    dataframes = load_csv_files_from_folder(folder_path)
    return [{'label': f, 'value': f} for f in dataframes.keys()]

# Callback to update the Cell ID dropdown and axis options based on the selected CSV file
@app.callback(
    [Output('cell-id-dropdown', 'options'),
     Output('x-axis-dropdown', 'options'),
     Output('y-axis-dropdown', 'options')],
    [Input('csv-file-dropdown', 'value')]
)
def update_options(csv_file):
    if csv_file and csv_file in dataframes:
        df = dataframes[csv_file]
        cell_ids = [{'label': cid, 'value': cid} for cid in df['Cell ID (0)'].unique()]
        columns = [{'label': col, 'value': col} for col in df.columns if col not in ['Cell ID (0)']]
        return cell_ids, columns, columns
    return [], [], []

# Callback to update the plot based on selected inputs
@app.callback(
    [Output('plot', 'figure'),
     Output('rsrp-over-time', 'figure'),
     Output('cinr-over-time', 'figure'),
     Output('percentage-plot', 'figure')],
    [Input('csv-file-dropdown', 'value'),
     Input('plot-type-dropdown', 'value'),
     Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value'),
     Input('rsrp-threshold', 'value'),
     Input('cinr-threshold', 'value'),
     Input('apply-rsrp-filter', 'value'),
     Input('apply-cinr-filter', 'value')]
)
def update_graphs(csv_file, plot_type, x_axis, y_axis, rsrp_threshold, cinr_threshold, rsrp_filter, cinr_filter):
    if csv_file and csv_file in dataframes:
        df = dataframes[csv_file]
        
        # Main plot (CINR vs. RSRP)
        main_fig = create_plot(df, plot_type, 'R0 RSRP (0)', 'R0 RS CINR (0)')
        
        # RSRP over time
        rsrp_time_fig = create_plot(df, 'Line', 'Time', 'R0 RSRP (0)')
        
        # CINR over time
        cinr_time_fig = create_plot(df, 'Line', 'Time', 'R0 RS CINR (0)')
        
        # Percentage plot
        cell_id_percentages, rsrp_percentage, cinr_percentage = calculate_percentages(df, rsrp_threshold, cinr_threshold, rsrp_filter, cinr_filter)
        
        percentage_data = {
            'Cell ID': list(cell_id_percentages.keys()),
            'RSRP %': [percentages['RSRP'] for percentages in cell_id_percentages.values()],
            'CINR %': [percentages['CINR'] for percentages in cell_id_percentages.values()]
        }
        percentage_df = pd.DataFrame(percentage_data)
        percentage_fig = px.bar(percentage_df, x='Cell ID', y=['RSRP %', 'CINR %'], barmode='group', title='Percentage of Values Above Threshold')
        
        return main_fig, rsrp_time_fig, cinr_time_fig, percentage_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
