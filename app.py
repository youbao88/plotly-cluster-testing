import dash
import dash_core_components as doc
import dash_html_components as html
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import numpy as np
import pickle


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

with open('sankey_node_link_data.pickle', 'rb') as file:
    output = pickle.load(file)

sns_colors = sns.color_palette("husl", 7)
plotly_colors = ['rgba(%s,%s,%s,1)'%(x[0], x[1], x[2]) for x in sns_colors]
plotly_colors_link = ['rgba(%s,%s,%s,0.5)'%(x[0], x[1], x[2]) for x in sns_colors]

node_x_position = [0.01]*7+[0.5]*7+[0.99]*7
node_y_position = [0.05, 0.21, 0.37, 0.53,0.69,0.85, 0.95]*3
node_color = plotly_colors*7
link_color = []
for i in plotly_colors_link:
    link_color = link_color + [i]*7
link_color = link_color *2

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label = ['%s-%s'%(x,str(y)) for x in ['Bas', '10y', '20y'] for y in range(1,8)],
      color = node_color,
      x = node_x_position,
      y = node_y_position,
    ),
    link = dict(
      source = [x[0] for x in output], 
      target = [x[1] for x in output],
      value = [x[2] for x in output],
      color = link_color
  ))])

fig.update_layout(font_size=13, width = 1000, height = 900)

app.layout = html.Div(children=[
    html.H1(children='Sankey plot for SDPP in three different time points'),

    html.Div(children='''
        2021-06-30 Created by Minhao Zhou
    '''),

    doc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)