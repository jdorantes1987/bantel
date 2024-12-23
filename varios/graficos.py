# https://deybimorales.gitlab.io/plotly_python_barra.html
import plotly.graph_objs as go
from plotly.offline import plot

x = [
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "Ene-20",
    "Feb-20",
    "Mar-20",
]
y = [119.3, 50.0, 139.8, 152.1, 165.8, 181.7, 198.5, 199.5, 200.5, 201.5]

fig = go.Figure(
    data=[
        go.Bar(
            x=x,
            y=y,
            text=y,
            textposition="auto",
            marker={"color": list(range(2, 15)), "colorscale": "blugrn"},
        )
    ]
)


fig.update_layout(
    barmode="stack",
    xaxis_type="category",
    title="<b></b><b>Recursos del Fondo de Garantía de Depósitos FOGADE</b><br><i>Saldo en millones de dólares</i>",
    # "",
    paper_bgcolor="rgb(206, 220, 227)",
    plot_bgcolor="rgb(206, 220, 227)",
    font=dict(family="Courier New, monospace", size=18, color="#000000"),
    annotations=[
        dict(
            x=0.5,
            y=-0.15,
            showarrow=False,
            text="Fuente: FOGADE",
            xref="paper",
            yref="paper",
        )
    ],
)

plot(fig, auto_open=True)
