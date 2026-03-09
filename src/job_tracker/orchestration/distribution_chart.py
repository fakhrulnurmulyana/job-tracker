from typing import Any, Callable, List, Literal, Optional, Sequence, Tuple

import plotly.graph_objects as go

from job_tracker.transform import counter_data
from job_tracker.visualization import BarChart, CircularChart, BoxPlots


ChartType = Literal[
    "pie",
    "bar",
    "batch_box_plot",
]


class DistributionChart:
    """
    High-level chart orchestrator.
    Responsible only for routing and preprocessing.
    """

    def __init__(self) -> None:
        self.circular_chart = CircularChart()
        self.bar_chart = BarChart()
        self.box_plot = BoxPlots()

        self._chart_handlers: dict[ChartType, Callable[..., go.Figure]] = {
            "pie": self._pie_chart,
            "bar": self._bar_chart,
            "batch_box_plot": self._batch_box_plot,
            "sunburst": self._sunburst,
        }

    # PUBLIC API
    def distribution_chart(
        self,
        title_text: str,
        chart_type: ChartType,
        data: Any= None,
        names: Optional[Sequence[str]] = None,
        parents: Optional[Sequence[str]] = None,
        sizes:Sequence[int | float] = None,
        boxpoints: Optional[str] = None,
        midle_text: str = "",
        orientation:Literal["v", "h"]="v",
        reverse: bool = False,
    ) -> go.Figure:

        if chart_type not in self._chart_handlers:
            raise ValueError(f"Unsupported chart_type: {chart_type}")

        return self._chart_handlers[chart_type](
            data=data,
            title_text=title_text,
            names=names,
            parents=parents,
            sizes=sizes,
            boxpoints=boxpoints,
            midle_text=midle_text,
            orientation=orientation,
            reverse=reverse,
        )


    # HANDLERS
    def _prepare_counter(self, data: Any):
        counter = counter_data(data=data)
        labels = list(counter.keys())
        sizes = list(counter.values())
        return labels, sizes
    
    def _list_sorted(
        self,
        labels: Sequence[str],
        sizes: Sequence[int | float],
        reverse: bool = False,
    ) -> Tuple[List[str], List[int | float]]:
        
        sorted_pairs = sorted(
            zip(labels, sizes),
            key=lambda x: x[1],
            reverse=reverse
        )

        labels_sorted, sizes_sorted = zip(*sorted_pairs)

        return list(labels_sorted), list(sizes_sorted)

    def _pie_chart(self, *, data, title_text, midle_text, **_) -> go.Figure:
        labels, sizes = self._prepare_counter(data)

        return self.circular_chart.pie(
            labels=labels,
            sizes=sizes,
            title_text=title_text,
            midle_text=midle_text,
        )

    def _bar_chart(
        self, 
        *, 
        data, 
        title_text, 
        orientation:Literal["v", "h"]="v",
        reverse: bool = False,
        **_,
    ) -> go.Figure:
        labels, sizes = self._prepare_counter(data)

        labels_sorted, sized_sorted = self._list_sorted(
                                            labels=labels,
                                            sizes=sizes,
                                            reverse=reverse,
                                        )

        return self.bar_chart.bar_chart(
            labels=labels_sorted,
            sizes=sized_sorted,
            title_text=title_text,
            orientation=orientation,
        )

    def _batch_box_plot(
        self,
        *,
        data,
        names,
        boxpoints,
        title_text,
        **_,
    ) -> go.Figure:

        return self.box_plot.batch_box_plots(
            names=names,
            data=data,
            boxpoints=boxpoints or "all",
            title_text=title_text,
        )

    def _sunburst(
        self,
        *,
        names: Sequence[str],
        parents: Sequence[str],
        sizes:Sequence[int | float],
        title_text: str,
        **_,
    ) -> go.Figure:
        if all(x is None for x in (names, parents, sizes)):
            raise ValueError("names, parents, and sizes cannot all be None")

        return self.circular_chart.sunburst(
            labels= names,
            parents=parents,
            sizes=sizes,
            title_text=title_text,
        )