from unittest import TestCase, mock
import pytest

import cnvrg_experiment_chart


__author__ = "Craig Smith"
__copyright__ = "Craig Smith"
__license__ = "MIT"


class TestInit(TestCase):
    @mock.patch("cnvrg_experiment_chart.chart.Experiment.__init__")
    def test_init_experiment_chart_good_wo_obj(self, mock_exp_init):
        mock_exp_init.return_value = None
        test_chart = cnvrg_experiment_chart.ExperimentChart(
            key="test_key", chart_type="line"
        )
        self.assertEqual(test_chart.key, "test_key")
        self.assertEqual(test_chart.chart_type, "none")
        self.assertIsInstance(
            test_chart.experiment, cnvrg_experiment_chart.chart.Experiment
        )
        self.assertIsInstance(test_chart.chart, cnvrg_experiment_chart.chart.Chart)

    @mock.patch("cnvrg_experiment_chart.chart.Experiment.__init__")
    def test_init_experiment_chart_good_w_obj(self, mock_exp_init):
        mock_exp_init.return_value = None
        test_exp = cnvrg_experiment_chart.chart.Experiment()
        test_chart = cnvrg_experiment_chart.ExperimentChart(
            key="test_key", chart_type="line", experiment=test_exp
        )
        self.assertIsInstance(
            test_chart.experiment, cnvrg_experiment_chart.chart.Experiment
        )

    @mock.patch("cnvrg_experiment_chart.chart.Experiment.__init__")
    def test_init_experiment_chart_w_bad_chart_type(self, mock_exp_init):
        mock_exp_init.return_value = None
        with pytest.raises(Exception) as e_info:
            test_chart = cnvrg_experiment_chart.ExperimentChart(
                key="test_key", chart_type="bad"
            )
            del test_chart
            assert e_info is not None

    @mock.patch("cnvrg_experiment_chart.chart.Experiment.__init__")
    def test_init_experiment_chart_good_nonline(self, mock_exp_init):
        mock_exp_init.return_value = None
        test_chart = cnvrg_experiment_chart.ExperimentChart(
            key="test_key", chart_type="bar"
        )
        self.assertEqual(test_chart.key, "test_key")
        self.assertEqual(test_chart.chart_type, "bar")
        self.assertIsInstance(
            test_chart.experiment, cnvrg_experiment_chart.chart.Experiment
        )
        self.assertIsInstance(test_chart.chart, cnvrg_experiment_chart.chart.Chart)


class TestCreateChart(TestCase):
    @mock.patch("cnvrg_experiment_chart.chart.Experiment.__init__")
    def setUp(self, mock_exp_init):
        mock_exp_init.return_value = None
        self.test_exp_chart = cnvrg_experiment_chart.ExperimentChart(
            key="test_key", chart_type="line"
        )
        self.addCleanup(mock.patch.stopall)

    @mock.patch("cnvrg_experiment_chart.chart.Experiment.log_metric")
    def test_create_chart(self, mock_log_metric):
        mock_log_metric.return_value = None
        test_return_obj = self.test_exp_chart.create_chart()
        self.assertIsInstance(test_return_obj, cnvrg_experiment_chart.ExperimentChart)


class TestAddSeries(TestCase):
    @mock.patch("cnvrg_experiment_chart.chart.Experiment.__init__")
    def setUp(self, mock_exp_init):
        mock_exp_init.return_value = None
        self.test_exp_chart = cnvrg_experiment_chart.ExperimentChart(
            key="test_key", chart_type="line"
        )
        self.addCleanup(mock.patch.stopall)

    def test_add_series_no_data(self):
        test_obj = self.test_exp_chart.add_series("test_series")
        self.assertIsInstance(test_obj, cnvrg_experiment_chart.ExperimentChart)

    def test_add_series_data(self):
        test_obj = self.test_exp_chart.add_series(series_name="test_series", data=[1])
        self.assertIsInstance(test_obj, cnvrg_experiment_chart.ExperimentChart)


class TestAddMetric(TestCase):
    @mock.patch("cnvrg_experiment_chart.chart.Experiment.__init__")
    def setUp(self, mock_exp_init):
        mock_exp_init.return_value = None
        self.test_exp_chart = cnvrg_experiment_chart.ExperimentChart(
            key="test_key", chart_type="line"
        )
        self.addCleanup(mock.patch.stopall)

    @mock.patch("cnvrg_experiment_chart.chart.Experiment.update_chart")
    def test_add_metric(self, mock_update_chart):
        mock_update_chart.return_value = None
        test_obj = self.test_exp_chart.add_metric([1], "test_series")
        self.assertIsInstance(test_obj, cnvrg_experiment_chart.ExperimentChart)
