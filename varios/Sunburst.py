# import plotly.graph_objects as go

# fig =go.Figure(go.Sunburst(
#     labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
#     parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
#     values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
# ))
# # Update layout for tight margin
# # See https://plotly.com/python/creating-and-updating-figures/
# fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

# fig.show()


import plotly.graph_objects as go

fig = go.Figure(
    go.Sunburst(
        ids=[
            "North America",
            "Europe",
            "Australia",
            "North America - Football",
            "Soccer",
            "North America - Rugby",
            "Europe - Football",
            "Rugby",
            "Europe - American Football",
            "Australia - Football",
            "Association",
            "Australian Rules",
            "Autstralia - American Football",
            "Australia - Rugby",
            "Rugby League",
            "Rugby Union",
        ],
        labels=[
            "North<br>America",
            "Europe",
            "Australia",
            "Football",
            "Soccer",
            "Rugby",
            "Football",
            "Rugby",
            "American<br>Football",
            "Football",
            "Association",
            "Australian<br>Rules",
            "American<br>Football",
            "Rugby",
            "Rugby<br>League",
            "Rugby<br>Union",
        ],
        parents=[
            "",
            "",
            "",
            "North America",
            "North America",
            "North America",
            "Europe",
            "Europe",
            "Europe",
            "Australia",
            "Australia - Football",
            "Australia - Football",
            "Australia - Football",
            "Australia - Football",
            "Australia - Rugby",
            "Australia - Rugby",
        ],
    )
)
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

fig.show()
