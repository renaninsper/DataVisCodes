import plotly.graph_objects as go
from plotly.offline import plot

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 20,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ['A', 'B', 'C', 'D', 'E', 'F'],
      color = ['#52a7f7', '#f569d2', '#f56969', '#6ef569', '#f5b869', '#69f5bd']
    ),
    link = dict(
      source = [0, 1, 0, 2, 3, 3], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = [2, 3, 3, 4, 4, 5],
      value = [8, 4, 2, 8, 4, 2],
      color = ['#52a7f7', '#f569d2', '#52a7f7', '#f56969', '#6ef569', '#6ef569']
  ))])

fig.update_layout(title_text="Diagrama Sankey Básico", font_size=10, font_family='Bahnschrift')
plot(fig, auto_open=True)