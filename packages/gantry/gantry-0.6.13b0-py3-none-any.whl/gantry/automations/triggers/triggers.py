import datetime
from abc import ABC
from typing import Dict, List, Optional

from gantry import globals
from gantry.alerts import create_alert
from gantry.alerts.client import AlertsAggregation, AlertsCheck, DiffCheck
from gantry.query.core.dataframe import GantryDataFrame
from gantry.query.time_window import RelativeTimeWindow
from gantry.utils import from_isoformat_duration, to_datetime, to_isoformat_duration


class Trigger(ABC):
    """
    Parent class for all triggers.
    """

    def __init__(self):
        self._application_name = None

    def add_to_application(self, application_name: str):
        self._application_name = application_name

    def remove_from_application(self):
        self._application_name = None

    def to_dict(self):
        pass


class IntervalTrigger(Trigger):
    def __init__(
        self,
        start_on: datetime.datetime,
        interval: datetime.timedelta,
        delay: datetime.timedelta = datetime.timedelta(),
    ):
        """
        Initialize an interval trigger.

        Args:
            start_on (datetime.datetime): the start time of the interval.
            interval (datetime.timedelta): the interval of the trigger.
            delay (datetime.timedelta): the delay of the trigger. Defaults to 0.
        """
        super().__init__()
        self.start_on = start_on
        self.interval = interval
        self.delay = delay or datetime.timedelta()

    def is_triggered(self):
        raise NotImplementedError

    def to_dict(self) -> Dict:
        return {
            "type": "IntervalTrigger",
            "content": {
                "start_on": self.start_on.isoformat(),
                "interval": to_isoformat_duration(self.interval),
                "delay": to_isoformat_duration(self.delay),
            },
        }

    @classmethod
    def from_dict(cls, d) -> "IntervalTrigger":
        return cls(
            start_on=to_datetime(d["start_on"]),
            interval=from_isoformat_duration(d["interval"]),
            delay=from_isoformat_duration(d["delay"]),
        )


class QueriesAggregationTrigger(Trigger):
    def __init__(
        self,
        name: str,
        compare_fields: List[str],
        compare_aggregation: AlertsAggregation,
        trigger_range_type: str,
        queries: List[GantryDataFrame],
        query_aggregation: List[AlertsAggregation],
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
    ):
        """
        Initialize a trigger based on multiple queries.
        As of now, we only support trigger based on 2 queries.

        Example:

        Say I want to setup a trigger that:

        - Calculate max(inputs.latitude) of query1 and query2.

        - Calculate the difference between the 2 max values, as in:

        - max(inputs.latitude) of query1 - max(inputs.latitude) of query2.

        - Trigger an alert if the difference is within a range [0.1, 1.0].

        .. code-block:: python

            first_query = app.get_query("first_query")
            second_query = app.get_query("second_query")

            query_trigger_alert = QueriesAggregationTrigger(
                name = "queries-trigger",
                compare_aggregation = AlertsAggregation.TOTAL_DIFFERENCE,
                compare_fields = ["inputs.latitude"],
                queries = [first_query, second_query],
                query_aggregation=[AlertsAggregation.MAX, AlertsAggregation.MAX],
                lower_bound = 0.1,
                upper_bound = 1.0,
            trigger_range_type="within",
            )

        Args:
            name (str): the name of the trigger.
            compare_fields: (List[str]) The fields to calculate aggregated difference on between
                queries. As of now, we only support 1 field.
            compare_aggregation (AlertsAggregation): the aggregation of the difference between
                aggregated query values.
            lower_bound (float): the lower bound (inclusive) of the aggregated difference.
            upper_bound (float): the upper bound (inclusive) of the aggregated difference.
            trigger_range_type (str): the type of the trigger range. The options are:

                "within": triggered when aggregated difference is within the bounds

                "outside": triggered when aggregated difference is outside the bounds

                "above": triggered when aggregated difference is above the upper bound

                "below": triggered when aggregated difference is below the lower bound
            queries (List[GantryDataFrame]): the list of queries (in order) to compare.
            query_aggregation (List[AlertsAggregation]): the aggregation of the queries.
        """
        if len(compare_fields) > 1:
            raise ValueError("As of now, we only support 1 field for compare_fields")
        if len(queries) > 2:
            raise ValueError("As of now, we only support comparing 2 queries")
        if len(queries) != len(query_aggregation):
            raise ValueError(
                "The number of queries and the number of query aggregations must be the same"
            )
        if trigger_range_type in ["within", "outside"]:
            if not lower_bound and not upper_bound:
                raise ValueError(
                    "lower_bound and upper_bound must be specified for this trigger range type"
                )
        if trigger_range_type == "above" and not upper_bound:
            raise ValueError("upper_bound must be specified for this trigger range type")
        if trigger_range_type == "below" and not lower_bound:
            raise ValueError("lower_bound must be specified for this trigger range type")
        if lower_bound and upper_bound and lower_bound > upper_bound:
            raise ValueError("lower_bound must be less than upper_bound")

        super().__init__()
        self.name = name
        self.aggregation = compare_aggregation
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.trigger_range_type = trigger_range_type
        self.queries = queries
        self.query_aggregation = query_aggregation
        self.fields = compare_fields
        self.api_client = None

    def generate_alert(self) -> str:
        subqueries = self.compile_subqueries()
        for subquery in subqueries:
            subquery.pop("app_name", None)
        alert_diff_check = DiffCheck(
            field_names=self.fields,
            aggregation=self.aggregation,
            trigger_range_type=self.trigger_range_type,
            subqueries=subqueries,
            lower_bound=self.lower_bound,
            upper_bound=self.upper_bound,
        )
        alert_id = create_alert(
            application_name=self._application_name,
            alert_name=self.name,
            alert_checks=[alert_diff_check],
            evaluation_window="P0D",
            evaluation_delay="P0D",
        )
        return alert_id

    def compile_subqueries(self):
        subqueries = []
        for query, aggregation in zip(self.queries, self.query_aggregation):
            self.api_client = query.api_client
            if not query.relative_time_window:
                raise ValueError("Relative time window must be specified for all queries")
            tags_as_filters = []
            if query.tags:
                tags_as_filters = [
                    {
                        "feature_name": tag_key,
                        "category_query": [tag_value],
                        "dtype": "tag",
                    }
                    for tag_key, tag_value in query.tags.items()
                ]
            subquery = {
                "app_name": query.application,
                "field_names": self.fields,
                "aggregation": aggregation.value,
                "filters": query.filters + tags_as_filters,
                "relative_time_window": to_isoformat_duration(query.relative_time_window),
                "relative_time_delay": to_isoformat_duration(query.relative_time_delay)
                if query.relative_time_delay
                else "P0D",
            }
            subqueries.append(subquery)
        return subqueries

    @staticmethod
    def subquery_from_dict(subquery_dict: Dict) -> GantryDataFrame:
        tags = {}
        for filter in subquery_dict["filters"]:
            if filter.get("dtype") and filter["dtype"] == "tag":
                tags[filter["feature_name"]] = filter["category_query"][0]
                subquery_dict["filters"].remove(filter)
        end_time = datetime.datetime.utcnow() - from_isoformat_duration(
            subquery_dict["relative_time_delay"]
        )
        start_time = end_time - from_isoformat_duration(subquery_dict["relative_time_window"])
        return GantryDataFrame(
            application=subquery_dict["app_name"],
            api_client=globals._API_CLIENT,  # type: ignore
            filters=subquery_dict["filters"],
            start_time=start_time,
            end_time=end_time,
            relative_time_window=from_isoformat_duration(subquery_dict["relative_time_window"]),
            relative_time_delay=from_isoformat_duration(subquery_dict["relative_time_delay"]),
            tags=tags,
        )

    def to_dict(self) -> Dict:
        return {
            "type": "QueriesAggregationTrigger",
            "content": {
                "name": self.name,
                "aggregation": self.aggregation.value,
                "lower_bound": self.lower_bound,
                "upper_bound": self.upper_bound,
                "trigger_range_type": self.trigger_range_type,
                "queries": self.compile_subqueries(),
                "query_aggregation": [aggregation.value for aggregation in self.query_aggregation],
                "fields": self.fields,
            },
        }

    @classmethod
    def from_dict(cls, trigger_dict: Dict) -> "QueriesAggregationTrigger":
        return cls(
            name=trigger_dict["name"],
            compare_aggregation=AlertsAggregation(trigger_dict["aggregation"]),
            lower_bound=trigger_dict["lower_bound"],
            upper_bound=trigger_dict["upper_bound"],
            trigger_range_type=trigger_dict["trigger_range_type"],
            queries=[
                cls.subquery_from_dict(subquery_dict=subquery)
                for subquery in trigger_dict["queries"]
            ],
            query_aggregation=[
                AlertsAggregation(aggregation) for aggregation in trigger_dict["query_aggregation"]
            ],
            compare_fields=trigger_dict["fields"],
        )


class AggregationTrigger(Trigger):
    def __init__(
        self,
        name: str,
        aggregation: AlertsAggregation,
        fields: List[str],
        lower_bound: float,
        upper_bound: float,
        evaluation_window: RelativeTimeWindow,
        tags: Optional[Dict] = None,
    ):
        """
        Initialize an aggregation trigger.

        Args:
            name (str): the name of the trigger.
            aggregation (AlertsAggregation): the aggregation of the trigger.
            fields (List[str]): the fields of the trigger.
            lower_bound (float): the lower bound of the field.
            upper_bound (float): the upper bound of the field.
            evaluation_window (:class:`gantry.query.time_window.RelativeTimeWindow`):: the
                evaluation window for the trigger.
            tags (Optional[Dict]): the tags of the trigger. Defaults to None.

        """
        super().__init__()
        self.name = name
        self.aggregation = aggregation
        self.fields = fields
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.evaluation_window = evaluation_window.window_length
        self.delay = evaluation_window.offset
        self.tags = tags

    def generate_alert(self) -> str:
        alert_check = AlertsCheck(
            self.aggregation, self.fields, self.lower_bound, self.upper_bound, "range_check"
        )
        evaluation_window = to_isoformat_duration(self.evaluation_window)
        delay = to_isoformat_duration(datetime.timedelta())
        if self.delay:
            delay = to_isoformat_duration(self.delay)
        alert_id = create_alert(
            self._application_name,
            self.name,
            [alert_check],
            evaluation_window,
            delay,
            self.tags,
        )
        return alert_id

    def to_dict(self) -> Dict:
        return {
            "type": "AggregationTrigger",
            "content": {
                "name": self.name,
                "aggregation": self.aggregation,
                "fields": self.fields,
                "lower_bound": self.lower_bound,
                "upper_bound": self.upper_bound,
                "evaluation_window": to_isoformat_duration(self.evaluation_window),
                "delay": to_isoformat_duration(self.delay)
                if self.delay
                else to_isoformat_duration(datetime.timedelta()),
                "tags": self.tags,
            },
        }

    @classmethod
    def from_dict(cls, d) -> "AggregationTrigger":
        return cls(
            d["name"],
            d["aggregation"],
            d["fields"],
            d["lower_bound"],
            d["upper_bound"],
            RelativeTimeWindow(
                window_length=from_isoformat_duration(d["evaluation_window"]),
                offset=from_isoformat_duration(d["delay"]),
            ),
            d["tags"],
        )
