import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from collections import Counter
from typing import Any, Callable, List, Sequence



class PieChart:
    def _autopct_format(
        self, 
        values: List[float],
    ) -> Callable[[float], str]:
        def my_format(pct):
            total = sum(values)
            count = int(round(pct * total / 100))
            return f'{pct:.1f}%\n({count})'
        return my_format
    
    def from_two_list(
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
    
    def from_one_list(
        self,
        values: Sequence[Any],
        title_text: str,
        midle_text: str = "",
    ) -> None:
        counter = Counter(values)

        labels = list(counter.keys())
        sizes = list(counter.values())

        self.from_two_list(
            labels=labels, 
            sizes=sizes, 
            title_text=title_text,
            midle_text=midle_text,
        )


