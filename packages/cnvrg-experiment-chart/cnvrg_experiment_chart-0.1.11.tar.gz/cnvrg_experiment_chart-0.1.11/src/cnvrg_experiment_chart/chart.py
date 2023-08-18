"""Module to supliment the handling of charts in the cnvrgv2 sdk"""
from cnvrgv2.utils.chart_utils import Chart
from cnvrgv2.modules.workflows.experiment.experiment import Experiment


class ExperimentChart:
    """
    A class used to manage an experiment's chart

    Attributes
    ----------
    experiment : cnvrgv2.Experiment
        A cnvrg Experiment object. If you do not pass in, we assume you want us
        to create this on your behalf.
    key : str
        The title and reference name used for the chart
    chart_type : str
        The type of chart to generate
    chart : LineChart
        The cnvrg Chart object generated after instantiating this object
    Examples
    --------
    >>> chart = ExperimentChart(key="line_chart", chart_type="line")
    >>> chart.add_series(series_name="index")
    >>> chart.create_chart()
    >>> chart.add_metric(series_name="index", data=[1,2,3])
    """

    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        key : str
            The title and reference name used for the chart
        chart_type : str
            The type of chart to generate. Choices are: line todo: bar, heatmap
            and scatter
        group : string
            Not sure
        step : int
            Number of steps?
        x_ticks : list
            List of strings to group together bar charts?
        stops : int
            Not sure
        max_val : int
            Maximum boundary for the Y axis
        min_val : int
            Minimum boundary for the Y axis
        colors : string
            Not sure, not valid with chart_type: line
        experiment: cnvrgv2.Experiment
            A cnvrg Experiment object. If you do not pass in, we assume you
            want us to create this on your behalf.
        """
        valid_types = ["line", "bar", "scatter", "heatmap"]
        if kwargs["chart_type"] not in valid_types:
            raise AttributeError(
                f"""Chart type must be one of the following strings:
                {valid_types}"""
            )
        self.experiment = kwargs.get("experiment", None)
        self.key = kwargs["key"]
        self.chart_type = kwargs["chart_type"]
        if self.chart_type == "line":
            self.chart_type = "none"
        self.chart = Chart(
            key=self.key,
            chart_type=self.chart_type,
            group=kwargs.get("group", None),
            step=kwargs.get("step", None),
            x_ticks=kwargs.get("x_ticks", None),
            stops=kwargs.get("stops", None),
            max_val=kwargs.get("max_val", None),
            min_val=kwargs.get("min_val", None),
            colors=kwargs.get("colors", None),
        )
        if not isinstance(self.experiment, Experiment):
            self.experiment = Experiment()

    def create_chart(self):
        """
        This method will add your chart to the experiment (aka. adds the chart
        to the experiments UI)

        Returns
        -------
        self : ExperimentChart
            Returns the updated ExperimentChart object allowing for method
            chaining
        """
        self.chart = self.experiment.log_metric(self.chart)
        return self

    def add_series(self, series_name, data=None):
        """
        This method adds a data series to the chart as well as the initial data
        point

        Parameters
        ----------
        data : list, default=None
            This is a list of one or more data points that will be added to the
            data series. If not included this will create an empty series.
        series_name : str
            This is the name you would like to give the data series.

        Returns
        -------
        self : ExperimentChart
            Returns the updated ExperimentChart object allowing for method
            chaining
        """
        if data is None:
            data = []
        self.chart.add_series(data, series_name)
        return self

    def add_metric(self, data, series_name):
        """
        This method appends a data point to an existing data series (appears in
        UI in real time)

        Parameters
        ----------
        data : list
            This is a list of one or more data points that will be appended to
            the currently list of datapoints
        series_name : str
            This is the name of the series to add the datapoints to

        Returns
        -------
        self : ExperimentChart
            Returns the updated ExperimentChart object allowing for method
            chaining
        """
        self.chart = self.experiment.update_chart(self.key, data, series_name)
        return self
