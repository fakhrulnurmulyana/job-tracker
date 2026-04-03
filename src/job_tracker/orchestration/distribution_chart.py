import plotly.graph_objects as go

from collections import Counter
from typing import Any, Callable, List, Literal, Optional, Sequence, Tuple
from job_tracker.visualization import BarChart, CircularChart, BoxPlots


ChartType = Literal[
    "pie",
    "bar",
    "batch_box_plot",
    "sunburst",
]


class DistributionChart:
    """High-level chart orchestrator for distribution visualizations.

    Routes chart-creation requests to the appropriate delegated chart
    implementation based on ``chart_type``. Handles data preprocessing
    (counting, sorting) before delegating to :class:`CircularChart`,
    :class:`BarChart`, or :class:`BoxPlots`.

    Attributes:
        circular_chart (CircularChart): Delegate for pie and sunburst charts.
        bar_chart (BarChart): Delegate for bar charts.
        box_plot (BoxPlots): Delegate for box-plot charts.

    Example:
        >>> chart = DistributionChart()
        >>> fig = chart.distribution_chart(
        ...     title_text="Job Roles",
        ...     chart_type="pie",
        ...     data=["Engineer", "Manager", "Engineer"],
        ... )
    """
    def __init__(self) -> None:
        """Initialize DistributionChart and register all chart handlers.

        Instantiates the three delegate chart objects and maps each
        :data:`ChartType` literal to its corresponding private handler method.
        """
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
        """Build and return a Plotly figure for the requested chart type.

        Validates ``chart_type`` against the registered handlers, then
        dispatches all keyword arguments to the matching private handler.

        Args:
            title_text (str): Title rendered at the top of the chart.
            chart_type (ChartType): One of ``"pie"``, ``"bar"``,
                ``"batch_box_plot"``, or ``"sunburst"``.
            data (Any, optional): Raw iterable used to build a
                :class:`~collections.Counter` for pie and bar charts, or a
                collection of value sequences for box plots.
            names (Sequence[str], optional): Node label sequence for
                sunburst charts and series names for box plots.
            parents (Sequence[str], optional): Parent label sequence for
                sunburst charts.
            sizes (Sequence[int | float], optional): Numeric value sequence
                for sunburst charts.
            boxpoints (str, optional): Plotly ``boxpoints`` argument passed
                to box-plot charts (e.g. ``"all"``, ``"outliers"``).
                Defaults to ``"all"`` when ``None``.
            midle_text (str, optional): Annotation text rendered in the
                centre of pie charts. Defaults to ``""``.
            orientation (Literal["v", "h"], optional): Bar orientation;
                ``"v"`` for vertical, ``"h"`` for horizontal.
                Defaults to ``"v"``.
            reverse (bool, optional): When ``True``, sorts bar chart bars in
                descending order of size. Defaults to ``False``.

        Returns:
            go.Figure: Configured Plotly figure ready for rendering.

        Raises:
            ValueError: If ``chart_type`` is not one of the supported values.

        Example:
            >>> fig = chart.distribution_chart(
            ...     title_text="Skills",
            ...     chart_type="bar",
            ...     data=["Python", "SQL", "Python"],
            ...     reverse=True,
            ... )
        """

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
    def _prepare_counter(self, data: Any) -> Tuple[List[str], List[int]]:
        """Count occurrences of each element in ``data``.

        Wraps :class:`~collections.Counter` and unpacks the result into
        parallel label and size lists.

        Args:
            data (Any): Any iterable whose elements are hashable.

        Returns:
            Tuple[List[str], List[int]]: A ``(labels, sizes)`` pair where
                ``labels`` contains unique elements and ``sizes`` contains
                their respective counts in insertion order.

        Example:
            >>> chart._prepare_counter(["a", "b", "a"])
            (['a', 'b'], [2, 1])
        """
        counter = Counter(data=data)
        labels = list(counter.keys())
        sizes = list(counter.values())
        return labels, sizes
    
    def _list_sorted(
        self,
        labels: Sequence[str],
        sizes: Sequence[int | float],
        reverse: bool = False,
    ) -> Tuple[List[str], List[int | float]]:
        """Sort parallel label and size sequences by size.

        Args:
            labels (Sequence[str]): Category label for each data point.
            sizes (Sequence[int | float]): Numeric value corresponding to
                each label.
            reverse (bool, optional): When ``True``, sorts in descending
                order. Defaults to ``False`` (ascending).

        Returns:
            Tuple[List[str], List[int | float]]: A ``(labels_sorted,
                sizes_sorted)`` pair sorted by ``sizes``.

        Example:
            >>> chart._list_sorted(["a", "b", "c"], [3, 1, 2])
            (['b', 'c', 'a'], [1, 2, 3])
        """
        sorted_pairs = sorted(
            zip(labels, sizes),
            key=lambda x: x[1],
            reverse=reverse
        )

        labels_sorted, sizes_sorted = zip(*sorted_pairs)

        return list(labels_sorted), list(sizes_sorted)

    def _pie_chart(self, *, data, title_text, midle_text, **_) -> go.Figure:
        """Build a pie chart from raw data.

        Counts element frequencies via :pymeth:`_prepare_counter` and
        delegates rendering to :pymeth:`CircularChart.pie`.

        Args:
            data (Any): Raw iterable of categorical values.
            title_text (str): Chart title.
            midle_text (str): Annotation text in the centre of the chart.
            **_: Unused keyword arguments forwarded from
                :pymeth:`distribution_chart`.

        Returns:
            go.Figure: Configured Plotly pie chart figure.
        """
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
        """Build a sorted bar chart from raw data.

        Counts element frequencies via :pymeth:`_prepare_counter`, sorts
        the result via :pymeth:`_list_sorted`, and delegates rendering to
        :pymeth:`BarChart.bar_chart`.

        Args:
            data (Any): Raw iterable of categorical values.
            title_text (str): Chart title.
            orientation (Literal["v", "h"], optional): Bar orientation.
                Defaults to ``"v"``.
            reverse (bool, optional): Sort order; ``True`` for descending.
                Defaults to ``False``.
            **_: Unused keyword arguments forwarded from
                :pymeth:`distribution_chart`.

        Returns:
            go.Figure: Configured Plotly bar chart figure.
        """
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
        """Build a batch of box plots from grouped data.

        Delegates directly to :pymeth:`BoxPlots.batch_box_plots`,
        defaulting ``boxpoints`` to ``"all"`` when not provided.

        Args:
            data (Any): Collection of value sequences, one per series.
            names (Sequence[str]): Series name for each box plot.
            boxpoints (str, optional): Plotly ``boxpoints`` argument.
                Defaults to ``"all"`` when ``None``.
            title_text (str): Chart title.
            **_: Unused keyword arguments forwarded from
                :pymeth:`distribution_chart`.

        Returns:
            go.Figure: Configured Plotly box-plot figure.
        """

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
        """Build a sunburst chart from explicit label, parent, and size data.

        Delegates to :pymeth:`CircularChart.sunburst` after validating that
        at least one of ``names``, ``parents``, or ``sizes`` is not ``None``.

        Args:
            names (Sequence[str]): Node labels for each segment.
            parents (Sequence[str]): Parent label for each node; root nodes
                should have an empty string as their parent.
            sizes (Sequence[int | float]): Numeric value for each node,
                determining arc size.
            title_text (str): Chart title.
            **_: Unused keyword arguments forwarded from
                :pymeth:`distribution_chart`.

        Returns:
            go.Figure: Configured Plotly sunburst figure.

        Raises:
            ValueError: If ``names``, ``parents``, and ``sizes`` are all
                ``None``.
        """
        if all(x is None for x in (names, parents, sizes)):
            raise ValueError("names, parents, and sizes cannot all be None")

        return self.circular_chart.sunburst(
            labels= names,
            parents=parents,
            sizes=sizes,
            title_text=title_text,
        )