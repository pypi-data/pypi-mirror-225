"""AutoViz module of official Python client for Driverless AI."""
import time
import types
from typing import Any, Dict, List, Optional
from typing import Sequence

from driverlessai import _core
from driverlessai import _datasets
from driverlessai import _utils


class AutoViz:
    """Interact with dataset visualizations on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._patch_autoviz_client(self._client._backend.autoviz)

    @staticmethod
    def _patch_autoviz_client(autoviz_client: Any) -> None:
        # Patch AutovizClient._wait_for_job to return the whole job object.
        def _wait_for_job(self, key: str) -> dict:  # type: ignore
            """Long polling to wait for async job to finish"""
            while True:
                job = self.client.get_vega_plot_job(key)
                if job.status >= 0:  # done
                    if job.status > 0:  # canceled or failed
                        raise RuntimeError(self.client._format_server_error(job.error))
                    return job  # return the whole job object
                time.sleep(1)

        autoviz_client._wait_for_job = types.MethodType(_wait_for_job, autoviz_client)

    def create(self, dataset: _datasets.Dataset) -> "Visualization":
        """Create a dataset visualization on the Driverless AI server.

        Args:
            dataset: Dataset object
        """
        return self.create_async(dataset).result()

    def create_async(self, dataset: _datasets.Dataset) -> "VisualizationJob":
        """Launch creation of a dataset visualization on the Driverless AI server.

        Args:
            dataset: Dataset object
        """
        key = self._client._backend.get_autoviz(dataset.key, maximum_number_of_plots=50)
        return VisualizationJob(self._client, key)

    def get(self, key: str) -> "Visualization":
        """Get a Visualization object corresponding to a dataset visualization
        on the Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the visualization
        """
        return Visualization(self._client, key)

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the AutoViz page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}visualizations"
        )

    def list(
        self, start_index: int = 0, count: int = None
    ) -> Sequence["Visualization"]:
        """Return list of dataset Visualization objects.

        Args:
            start_index: index on Driverless AI server of first visualization in list
            count: number of visualizations to request from the Driverless AI server
        """
        if count:
            data = self._client._backend.list_visualizations(start_index, count).items
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._client._backend.list_visualizations(
                    page_position, page_size
                ).items
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return _utils.ServerObjectList(
            data=data, get_method=self.get, item_class_name=Visualization.__name__
        )


class CustomPlot(_utils.ServerObject):
    """
    Interact with a custom plot added into a visualization on the Driverless AI server.
    """

    def __init__(self, client: "_core.Client", raw_info: Any) -> None:
        super().__init__(client=client, key=raw_info.key)
        self._set_raw_info(raw_info)
        self._set_name(raw_info.description)
        self._visualization_key = raw_info.dataset.key

    @property
    def plot_data(self) -> Dict[str, Any]:
        """Plot in Vega Lite (v3) format."""
        return self._get_raw_info().entity

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_vega_plot_job(self.key))
        self._set_name(self._get_raw_info().description)


class Visualization(_utils.ServerObject):
    """Interact with a dataset visualization on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)
        self._box_plots: Optional[Dict[str, List[Dict[str, Any]]]] = None
        self._dataset: Optional[_datasets.Dataset] = None
        self._custom_plots: Optional[List[CustomPlot]] = None

    @property
    def box_plots(self) -> Dict[str, List[Dict[str, Any]]]:
        """Disparate box plots and heteroscedastic box plots of this visualization."""
        if not self._box_plots:
            plots_info = self._get_raw_info().entity.boxplots
            self._box_plots = {
                "disparate": [
                    self._get_vega_grouped_boxplot(vn, gvn, False).entity
                    for gvn, vn in _utils.get_or_default(plots_info, "disparate", [])
                ],
                "heteroscedastic": [
                    self._get_vega_grouped_boxplot(vn, gvn, False).entity
                    for gvn, vn in _utils.get_or_default(
                        plots_info, "heteroscedastic", []
                    )
                ],
            }
        return self._box_plots

    @property
    def custom_plots(self) -> List[CustomPlot]:
        """Custom plots added to this visualization."""
        self._check_custom_plots_support()
        if not self._custom_plots:
            self._update()
        return self._custom_plots

    @property
    def dataset(self) -> _datasets.Dataset:
        """Dataset that was visualized."""
        if self._dataset is None:
            try:
                self._dataset = self._client.datasets.get(self._get_dataset_key())
            except self._client._server_module.protocol.RemoteError:
                # assuming a key error means deleted dataset, if not the error
                # will still propagate to the user else where
                self._dataset = self._get_raw_info().dataset.dump()
        return self._dataset

    @property
    def histograms(self) -> Dict[str, List[Dict[str, Any]]]:
        """Spikes, skewed, and gaps histograms of this visualization."""
        histograms_info = self._get_raw_info().entity.histograms
        categorized_plots = {
            "spikes": [
                self._get_vega_histogram(col, 0, "none", "bar").entity
                for col in _utils.get_or_default(histograms_info, "spikes", [])
            ],
            "skewed": [
                self._get_vega_histogram(col, 0, "none", "bar").entity
                for col in _utils.get_or_default(histograms_info, "skewed", [])
            ],
            "gaps": [
                self._get_vega_histogram(col, 0, "none", "bar").entity
                for col in _utils.get_or_default(histograms_info, "gaps", [])
            ],
        }
        return categorized_plots

    @property
    def is_deprecated(self) -> Optional[bool]:
        """``True`` if visualization was created by an old version of
        Driverless AI and is no longer fully compatible with the current
        server version."""
        return getattr(self._get_raw_info(), "deprecated", None)

    @property
    def parallel_coordinates_plot(self) -> Dict[str, Any]:
        """Parallel coordinates plot of this visualization."""
        column_names = self._get_stats().column_names
        return self._get_vega_parallel_coordinates_plot(
            column_names,
            False,
            False,
            False,
        ).entity

    @property
    def recommendations(self) -> Optional[Dict[str, Dict[str, str]]]:
        """Recommended feature transformations and deletions by this visualization."""
        recommendations_info = _utils.get_or_default(
            self._get_raw_info().entity, "transformations", None
        )
        if recommendations_info is None:
            return None
        return {
            "transforms": _utils.get_or_default(recommendations_info, "transforms", {}),
            "deletions": _utils.get_or_default(recommendations_info, "deletions", {}),
        }

    @property
    def scatter_plot(self) -> Optional[Dict[str, Any]]:
        """Scatter plot of this visualization."""
        scatter_plot_info = self._get_raw_info().entity.scatterplots
        if scatter_plot_info.correlated and len(scatter_plot_info.correlated) > 0:
            return self._get_vega_scatter_plot(
                scatter_plot_info.correlated[0][0],
                scatter_plot_info.correlated[0][1],
                "point",
            ).entity

        return None

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _add_custom_plot(self, vega_plot_job: Any) -> CustomPlot:
        custom_plot = CustomPlot(self._client, vega_plot_job)
        self._client._backend.add_autoviz_custom_plot(
            autoviz_key=self.key, vega_plot_key=custom_plot.key
        )
        self._custom_plots = None  # next time we will fetch all from the server
        return custom_plot

    def _check_custom_plots_support(self) -> None:
        _utils.check_server_support(self._client, "1.9.0.6", "custom_plots")

    def _get_dataset_key(self) -> str:
        return self._get_raw_info().dataset.key

    def _get_stats(self) -> "VisualizationStats":
        key = self._client._backend.get_vis_stats(self._get_dataset_key())
        return VisualizationStatsJob(self._client, key).result()

    def _get_vega_grouped_boxplot(
        self, variable_name: str, group_variable_name: str, transpose: bool
    ) -> Any:
        return self._client._backend.autoviz.get_boxplot(
            dataset_key=self._get_dataset_key(),
            variable_name=variable_name,
            group_variable_name=group_variable_name,
            transpose=transpose,
        )

    def _get_vega_histogram(
        self, variable_name: str, number_of_bars: int, transformation: str, mark: str
    ) -> Any:
        return self._client._backend.autoviz.get_histogram(
            dataset_key=self._get_dataset_key(),
            variable_name=variable_name,
            number_of_bars=number_of_bars,
            transformation=transformation,
            mark=mark,
        )

    def _get_vega_parallel_coordinates_plot(
        self, variable_names: List[str], permute: bool, transpose: bool, cluster: bool
    ) -> Any:
        return self._client._backend.autoviz.get_parallel_coordinates_plot(
            dataset_key=self._get_dataset_key(),
            variable_names=variable_names,
            permute=permute,
            transpose=transpose,
            cluster=cluster,
        )

    def _get_vega_scatter_plot(
        self, x_variable_name: str, y_variable_name: str, mark: str
    ) -> Any:
        return self._client._backend.autoviz.get_scatterplot(
            dataset_key=self._get_dataset_key(),
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            mark=mark,
        )

    def _set_custom_plots(self, custom_plots: List[Any]) -> None:
        self._custom_plots = [
            CustomPlot(self._client, plot_info) for plot_info in custom_plots
        ]

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_autoviz_job(self.key))
        self._set_custom_plots(
            _utils.get_or_default(self._get_raw_info().entity, "custom_plots", [])
        )
        self._set_name(self._get_raw_info().name)

    def add_bar_chart(
        self,
        x_variable_name: str,
        y_variable_name: str = "",
        transpose: bool = False,
        mark: str = "bar",
    ) -> CustomPlot:
        """
        Adds a custom bar chart to this visualization and returns it.

        Args:
            x_variable_name: column for the X axis
            y_variable_name: column for the Y axis,
                            if omitted then number of occurrences is considered
            transpose: set to ``True`` to flip axes
            mark: mark type used for the chart,
                use ``"point"`` to get a Cleveland dot plot

        Returns:
            a bar chart in Vega Lite (v3) format
        """

        vega_plot_job = self._client._backend.autoviz.get_bar_chart(
            dataset_key=self._get_dataset_key(),
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            transpose=transpose,
            mark=mark,
        )
        return self._add_custom_plot(vega_plot_job)

    def add_box_plot(self, variable_name: str, transpose: bool = False) -> CustomPlot:
        """
        Adds a custom box plot to this visualization and returns it.

        Args:
            variable_name: column for the plot
            transpose: set to ``True`` to flip axes

        Returns:
            a box plot in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        kwargs = dict(variable_name=variable_name, transpose=transpose)
        job_key = self._client._backend.get_1d_vega_plot(
            self._get_dataset_key(), "boxplot", variable_name, kwargs
        )
        vega_plot_job = self._client._backend.autoviz._wait_for_job(job_key)
        return self._add_custom_plot(vega_plot_job)

    def add_dot_plot(self, variable_name: str, mark: str = "point") -> CustomPlot:
        """
        Adds a custom dot plot to this visualization and returns it.

        Args:
            variable_name: column for the plot
            mark: mark type used for the plot,
                  possible values are ``"point"``, ``"square"`` or ``"bar"``

        Returns:
            a dot plot in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        vega_plot_job = self._client._backend.autoviz.get_dotplot(
            dataset_key=self._get_dataset_key(), variable_name=variable_name, mark=mark
        )
        return self._add_custom_plot(vega_plot_job)

    def add_grouped_box_plot(
        self, variable_name: str, group_variable_name: str, transpose: bool = False
    ) -> CustomPlot:
        """
        Adds a custom grouped box plot to this visualization and returns it.

        Args:
            variable_name: column for the plot
            group_variable_name: grouping column
            transpose: set to ``True`` to flip axes

        Returns:
            a grouped box plot  in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        vega_plot_job = self._get_vega_grouped_boxplot(
            variable_name, group_variable_name, transpose
        )
        return self._add_custom_plot(vega_plot_job)

    def add_heatmap(
        self,
        variable_names: Optional[List[str]] = None,
        permute: bool = False,
        transpose: bool = False,
        matrix_type: str = "rectangular",
    ) -> CustomPlot:
        """
        Adds a custom heatmap to this visualization and returns it.

        Args:
            variable_names: columns for the Heatmap,
                            if omitted then all columns are used
            permute: set to ``True`` to permute rows and columns
                    using singular value decomposition (SVD)
            transpose: set to ``True`` to flip axes
            matrix_type: matrix type,
                        possible values are ``"rectangular"`` or ``"symmetric"``

        Returns:
            a heatmap in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        vega_plot_job = self._client._backend.autoviz.get_heatmap(
            dataset_key=self._get_dataset_key(),
            variable_names=variable_names or [],
            permute=permute,
            transpose=transpose,
            matrix_type=matrix_type,
        )
        return self._add_custom_plot(vega_plot_job)

    def add_histogram(
        self,
        variable_name: str,
        number_of_bars: int = 0,
        transformation: str = "none",
        mark: str = "bar",
    ) -> CustomPlot:
        """
        Adds a custom histogram to this visualization and returns it.

        Args:
            variable_name: column for the histogram
            number_of_bars: number of bars in the histogram
            transformation: a transformation applied to the column,
                        possible values are ``"none"``, ``"log"`` or ``"square_root"``
            mark: mark type used for the histogram, possible values are
                ``"bar"`` or ``"area"``. Use ``"area"`` to get a density polygon.

        Return:
            a histogram in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        vega_plot_job = self._get_vega_histogram(
            variable_name, number_of_bars, transformation, mark
        )
        return self._add_custom_plot(vega_plot_job)

    def add_linear_regression(
        self,
        x_variable_name: str,
        y_variable_name: str,
        mark: str = "point",
    ) -> CustomPlot:
        """
        Adds a custom linear regression to this visualization and returns it.

        Args:
            x_variable_name: column for the X axis
            y_variable_name: column for the Y axis
            mark: mark type used for the plot,
                possible values are ``"point"`` or ``"square"``

        Return:
            a linear regression in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        vega_plot_job = self._client._backend.autoviz.get_linear_regression(
            dataset_key=self._get_dataset_key(),
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            mark=mark,
        )
        return self._add_custom_plot(vega_plot_job)

    def add_loess_regression(
        self,
        x_variable_name: str,
        y_variable_name: str,
        mark: str = "point",
        bandwidth: float = 0.5,
    ) -> CustomPlot:
        """
        Adds a custom loess regression to this visualization and returns it.

        Args:
            x_variable_name: column for the X axis
            y_variable_name: column for the Y axis,
                            if omitted then number of occurrences is considered
            mark: mark type used for the plot,
                possible values are ``"point"`` or ``"square"``
            bandwidth: interval denoting proportion of cases in smoothing window

        Return:
            a loess regression in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        vega_plot_job = self._client._backend.autoviz.get_loess_regression(
            dataset_key=self._get_dataset_key(),
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            mark=mark,
            bandwidth=bandwidth,
        )
        return self._add_custom_plot(vega_plot_job)

    def add_parallel_coordinates_plot(
        self,
        variable_names: List[str] = None,
        permute: bool = False,
        transpose: bool = False,
        cluster: bool = False,
    ) -> CustomPlot:
        """
        Adds a custom parallel coordinates plot to this visualization and returns it.

        Args:
            variable_names: columns for the plot,
                            if omitted then all columns will be used
            permute: set to ``True`` to permute rows and columns
                    using singular value decomposition (SVD)
            transpose: set to ``True`` to flip axes
            cluster: set to ``True`` to k-means cluster variables and
                    color plot by cluster IDs

        Return:
            a parallel coordinates plot in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        vega_plot_job = self._get_vega_parallel_coordinates_plot(
            variable_names or [],
            permute,
            transpose,
            cluster,
        )
        return self._add_custom_plot(vega_plot_job)

    def add_probability_plot(
        self,
        x_variable_name: str,
        distribution: str = "normal",
        mark: str = "point",
        transpose: bool = False,
    ) -> CustomPlot:
        """
        Adds a custom probability plot to this visualization and returns it.

        Args:
            x_variable_name: column for the X axis
            distribution: type of distribution,
                        possible values are ``"normal"`` or ``"uniform"``
            mark: mark type used for the plot,
                possible values are ``"point"`` or ``"square"``
            transpose: set to ``True`` to flip axes

        Return:
            a probability plot in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        kwargs = dict(
            x_variable_name=x_variable_name,
            subtype="probability_plot",
            distribution=distribution,
            mark=mark,
            transpose=transpose,
        )
        job_key = self._client._backend.get_1d_vega_plot(
            self._get_dataset_key(), "probability_plot", x_variable_name, kwargs
        )
        vega_plot_job = self._client._backend.autoviz._wait_for_job(job_key)
        return self._add_custom_plot(vega_plot_job)

    def add_quantile_plot(
        self,
        x_variable_name: str,
        y_variable_name: str,
        distribution: str = "normal",
        mark: str = "point",
        transpose: bool = False,
    ) -> CustomPlot:
        """
        Adds a custom quantile plot to this visualization and returns it.

        Args:
            x_variable_name: column for the X axis
            y_variable_name: column for the Y axis
            distribution: type of distribution,
                        possible values are ``"normal"`` or ``"uniform"``
            mark: mark type used for the plot,
                possible values are ``"point"`` or ``"square"``
            transpose: set to ``True`` to flip axes

        Return:
            a quantile plot in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        kwargs = dict(
            x_variable_name=x_variable_name,
            y_variable_name=y_variable_name,
            subtype="quantile_plot",
            distribution=distribution,
            mark=mark,
            transpose=transpose,
        )
        job_key = self._client._backend.get_2d_vega_plot(
            self._get_dataset_key(),
            "quantile_plot",
            x_variable_name,
            y_variable_name,
            kwargs,
        )
        vega_plot_job = self._client._backend.autoviz._wait_for_job(job_key)
        return self._add_custom_plot(vega_plot_job)

    def add_scatter_plot(
        self,
        x_variable_name: str,
        y_variable_name: str,
        mark: str = "point",
    ) -> CustomPlot:
        """
        Adds a custom scatter plot to this visualization and returns it.

        Args:
            x_variable_name: column for the X axis
            y_variable_name: column for the Y axis,
                            if omitted then number of occurrences is considered
            mark: mark type used for the plot,
                possible values are ``"point"`` or ``"square"``

        Return:
            a scatter plot in Vega Lite (v3) format
        """

        self._check_custom_plots_support()

        vega_plot_job = self._get_vega_scatter_plot(
            x_variable_name, y_variable_name, mark
        )
        return self._add_custom_plot(vega_plot_job)

    def delete(self) -> None:
        """Permanently delete visualization from the Driverless AI server."""
        key = self.key
        self._client._backend.delete_autoviz_job(key)
        print(f"Driverless AI Server reported visualization {key} deleted.")

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the visualization's page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}"
            f"auto_viz?&datasetKey={self._get_dataset_key()}"
            f"&dataset_name={self._get_raw_info().dataset.display_name}"
        )

    def remove_custom_plot(self, custom_plot: CustomPlot) -> None:
        """
        Removes a previously added custom plot from this visualization.

        Args:
            custom_plot: custom plot to be removed & deleted
        """

        self._check_custom_plots_support()

        if self.key != custom_plot._visualization_key:
            raise ValueError(
                f"Custom plot {custom_plot} does not belong to this visualization."
            )

        self._client._backend.remove_autoviz_custom_plot(self.key, custom_plot.key)
        self._custom_plots = None  # next time we will fetch all from the server


class VisualizationJob(_utils.ServerJob):
    """Monitor creation of a visualization on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_autoviz_job(self.key))

    def result(self, silent: bool = False) -> Visualization:
        """Wait for job to complete, then return a Visualization object.

        Args:
            silent: if True, don't display status updates
        """

        self._wait(silent)
        return Visualization(self._client, self.key)


class VisualizationStats(_utils.ServerObject):
    """Interact with a visualization stats on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str, raw_info: Any) -> None:
        super().__init__(client=client, key=key)
        self._set_raw_info(raw_info)

    @property
    def column_names(self) -> List[str]:
        column_names = self._get_raw_info().entity.column_names
        return [name for name in column_names if name != "members_count"]

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_autoviz_job(self.key))


class VisualizationStatsJob(_utils.ServerJob):
    """Monitor creation of a visualization stats on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_vis_stats_job(self.key))

    def result(self, silent: bool = False) -> VisualizationStats:
        """Wait for job to complete, then return a VisualizationStats object.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return VisualizationStats(self._client, self.key, self._get_raw_info())
