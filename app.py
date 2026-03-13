import pandas as pd
from dash import Dash, dash_table, dcc, callback, Output, Input, html
import plotly.express as px

# データ読み込み
df_gdp = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/2014_world_gdp_with_codes.csv"
)

app = Dash()

# レイアウト
app.layout = [
    html.H1("国別GDPのダッシュボード", style={"text-align": "center"}),

    # データテーブル
    dash_table.DataTable(
        data=df_gdp.to_dict("records"),
        page_size=10,
        style_cell={"textAlign": "center"},
        style_table={"overflowX": "auto"}
    ),

    html.Br(),

    # ソートラジオ
    dcc.RadioItems(
        options=[{"label": "GDP大きい順", "value": "大きい順"},
                 {"label": "GDP小さい順", "value": "小さい順"}],
        value="大きい順",
        id="sort_type",
        inline=True,
        style={"textAlign": "center"}
    ),

    html.Br(),

    # グラフ
    dcc.Graph(id="gdp_graph", figure={})
]

# コールバック
@callback(
    Output("gdp_graph", "figure"),
    Input("sort_type", "value")
)
def update_gdp_graph(value):
    if value == "大きい順":
        df_bar = df_gdp.sort_values("GDP (BILLIONS)", ascending=False)[:10]
    else:
        df_bar = df_gdp.sort_values("GDP (BILLIONS)").head(10)

    fig = px.bar(
        df_bar,
        x="COUNTRY",
        y="GDP (BILLIONS)",
        text="GDP (BILLIONS)",
        color="COUNTRY",
        title="国別GDPトップ10" if value == "大きい順" else "国別GDP下位10"
    )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    return fig

if __name__ == "__main__":
    app.run(debug=True)