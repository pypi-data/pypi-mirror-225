import functools
import time
from typing import Any
from .metrics.randomscore import RandomMetric
from .metrics.metric import Metric
from .metrics.bertscore_metric import BertScoreMetric
from .metrics.entailment_metric import EntailmentScoreMetric


def assert_llm_output(
    output: Any, expected_output: Any, metric: Any = "entailment", query: str = "-"
):
    if metric == "exact":
        assert_exact_match(output, expected_output)
    elif metric == "random":
        metric: RandomMetric = RandomMetric()
        metric(output, expected_output, query=query)
    elif metric == "bertscore":
        metric: BertScoreMetric = BertScoreMetric()
        metric(output, expected_output, query=query)
    elif metric == "entailment":
        metric: EntailmentScoreMetric = EntailmentScoreMetric()
        metric(output, expected_output, query=query)
    elif isinstance(metric, Metric):
        metric(output, expected_output, query=query)
    else:
        raise ValueError("Inappropriate metric")
    assert metric.is_successful(), metric.__class__.__name__ + " was unsuccessful."


def assert_factual_consistency(output: str, context: str):
    """Assert that the output is factually consistent with the context."""

    class FactualConsistency(EntailmentScoreMetric):
        def __name__(self):
            return "Factual Consistency"

    metric = FactualConsistency()
    score = metric(context, output)
    assert metric.is_successful(), metric.__class__.__name__ + " was unsuccessful."


def assert_exact_match(text_input, text_output):
    assert text_input == text_output, f"{text_output} != {text_input}"


class TestEvalCase:
    pass


def timing_decorator(func):
    @functools.wraps(func)  # Preserves the original function's metadata
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds to execute.")
        return result

    return wrapper


def tags(tags: list):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # TODO - add logging for tags
            print(f"Tags are: {tags}")
            return result

        return wrapper

    return decorator
