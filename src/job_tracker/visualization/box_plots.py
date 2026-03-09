import plotly.graph_objects as go

from typing import Any, Literal, Sequence



class BoxPlots:
    def box_plots(
        self, 
        y:Sequence[int | float],
        name: str,
        fig=None,  
        idx:int=0,
        boxpoints: Literal[
            "all", 
            "outliers", 
            "suspectedoutliers", 
            False
        ] = "all",
    )-> go.Figure:
        if fig is None:
            fig = go.Figure()

        fig.add_trace(go.Box(
            y=y,
            name=name,
            boxpoints=boxpoints,
            marker=dict(
                color='rgb(8,81,156)',
                outliercolor='rgba(219, 64, 82, 0.6)',
                line=dict(
                    outliercolor='rgba(219, 64, 82, 0.6)',
                    outlierwidth=idx)),
            line_color='rgb(8,81,156)'
        ))

        return fig

    def batch_box_plots(
        self,
        title_text: str,
        names: Sequence[str],
        data : Sequence[Sequence[int | float | Any]],
        boxpoints: Literal[
            "all", 
            "outliers", 
            "suspectedoutliers", 
            False
        ] = "all",
    )-> go.Figure:
        names = list(names)
        fig = go.Figure()

        for idx, (y, name) in enumerate(zip(data, names)):
            self.box_plots(
                fig=fig,
                y=y,
                name=name,  
                idx=idx,
                boxpoints=boxpoints,
            )

        fig.update_layout(title_text=title_text)
        fig.show()