"""
This is the main Dash Module which is combining get_data + data_viz modules.

"""
# IMPORTS
from get_data import *
from data_viz import *
from dotenv import dotenv_values
import os
import dash
from dash import dcc
from dash import html

# FIGs Creation
dict_df = Getdata()
fig_valorisation, fig_dividende = SunBursts(dict_df["Dividende"])
fig_benefice = Benefice_Evolution(dict_df["Patrimoine"])
fig_patrimoine = Patrimoine_Evolution(dict_df["Patrimoine"])
fig_waterflow = Waterfall_Perso(dict_df["Cash_Flow"])
fig_charge = Pie_Charge(dict_df["Cash_Flow"])
fig_epargne = Epargne_Evolution(dict_df["Patrimoine"])

# DASH app creation
app = dash.Dash(__name__)
server = app.server

# DASH app Layout
app.layout = html.Div(className='row', children=[
    html.H1(children="Dashboard de finances personelles",
        style={
            'textAlign': 'center'
        }),
    html.H2(children="Valorisation et dividendes",
        style={
            'textAlign': 'center'
        }),
    html.Div(children=[
        dcc.Graph(id="graph_valorisation", style={'display': 'inline-block'}, figure=fig_valorisation),
        dcc.Graph(id="graph_dividende", style={'display': 'inline-block'}, figure=fig_dividende)
    ],
        style={
            'textAlign': 'center'
        }
    ),
    html.H2(children="Patrimoine et évolution de bénéfice",
        style={
            'textAlign': 'center'
        }),
    html.Div(children=[
        dcc.Graph(id="graph_benefice", style={'display': 'inline-block'}, figure=fig_benefice),
        dcc.Graph(id="graph_patrimoine", style={'display': 'inline-block'}, figure=fig_patrimoine)
    ],
        style={
            'textAlign': 'center'
        }
    ),
    html.H2(children="Waterflow et évaluation des charges",
        style={
            'textAlign': 'center'
        }),
    html.Div(children=[
        dcc.Graph(id="graph_waterflow", style={'display': 'inline-block'}, figure=fig_waterflow),
        dcc.Graph(id="graph_charge", style={'display': 'inline-block'}, figure=fig_charge)
    ],
        style={
            'textAlign': 'center'
        }
    ),
    html.H2(children="Evolution de l'épargne mensuelle",
        style={
            'textAlign': 'center'
        }),
    html.Div(children=dcc.Graph(id="graph_epargne",
                  style={'display': 'inline-block'},
                  figure=fig_epargne),
        style={
            'textAlign': 'center',
            'width': '90vw',
            'height': '20vh'
        }
    ),

])

# App rendering
if __name__ == '__main__':
    # PROD MOD
    if os.environ.get("ENV") == "PROD":
        app.run_server(debug=False)

    # TEST MOD
    else:
        app.run_server(host='0.0.0.0', port=5001, debug=True)

