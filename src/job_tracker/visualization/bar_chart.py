import plotly.express as px

from typing import Literal, Sequence

class BarChart:
    def bar_chart(
        self,
        labels:Sequence[str], 
        sizes:Sequence[float],
        title_text:str,
        orientation:Literal["v", "h"]="v",
    )->None:
        fig = px.bar(
            x=labels, 
            y=sizes,
            orientation=orientation,
        )

        fig.update_layout(
            title_text=title_text
        )

        fig.show()