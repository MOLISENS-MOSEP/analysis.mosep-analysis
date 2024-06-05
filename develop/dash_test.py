import dash
from dash import dcc, html

# Initialize the Dash app with URL prefix
app = dash.Dash(__name__, serve_locally=False)

app.layout = html.Div(
    [
        html.H1("Hello Dash"),
        dcc.Graph(
            id="example-graph",
            figure={
                "data": [
                    {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                    {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": "NYC"},
                ],
                "layout": {"title": "Dash Data Visualization"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=False)
