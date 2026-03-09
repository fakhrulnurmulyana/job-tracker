import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from typing import Sequence



class CircularChart:
    def pie(
        self,
        labels: Sequence[str],
        sizes: Sequence[float],
        title_text: str,
        midle_text: str = '',
    )->None:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels, 
                    values=sizes, 
                    hole=.4, 
                    marker=dict(
                        colors=px.colors.sequential.Viridis_r
                    )
                )
            ]
        )

        fig.update_layout(
            title_text=title_text,
            annotations=[dict(
                    text=midle_text, 
                    y=0.5,
                    font_size=20, 
                    showarrow=False, 
                    xanchor="center"
                )
            ]
        )

        fig.show()

    def sunburst(
        self, 
        labels: Sequence[str],
        parents: Sequence[str],
        sizes:Sequence[int | float],
        title_text: str,
    ):
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=sizes,
            branchvalues="total",
        ))

        fig.update_traces(
            hovertemplate=
            "<b>%{label}</b><br>" +
            "Jumlah: %{value}<br>" +
            "Persen: %{percentParent:.2%}" +
            "<extra></extra>"
        )

        fig.update_layout(
            margin=dict(t=0, l=0, r=0, b=0),
            title_text=title_text,
        )
        fig.show()