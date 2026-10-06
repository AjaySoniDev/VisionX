import numpy as np
import pytest

from vxn_ramnet.evaluation.baselines import dtw_similarity
from vxn_ramnet.evaluation.metrics import ranking_metrics, summarize_decisions, timing_summary


def row(identifier, truth, decision, branch=None, score=0.7):
    return {
        "query_id": identifier,
        "expected_label": truth,
        "decision_kind": decision,
        "branch_id": branch,
        "best_branch_score": score,
    }


def test_errors_abstentions_and_unknowns_have_explicit_denominators():
    metrics = summarize_decisions(
        [
            row("qa", "BRANCH_A", "known_branch", "BRANCH_A"),
            row("qb", "BRANCH_B", "uncertain"),
            row("qc", "UNKNOWN", "known_branch", "BRANCH_A"),
            row("qd", "UNKNOWN", "unknown_route", score=0.1),
        ]
    )
    assert metrics["accepted"] == 2
    assert metrics["accepted_errors"] == 1
    assert metrics["coverage"] == metrics["selective_risk"] == 0.5
    assert metrics["known_decision_accuracy"] == metrics["unknown_false_acceptance_rate"] == 0.5
    assert metrics["confusion_matrix"]["BRANCH_B"]["ABSTAIN"] == 1
    assert metrics["known_macro_f1"] == 0.5


def test_zero_accepted_and_no_unknowns_remain_undefined():
    metrics = summarize_decisions([row("qa", "BRANCH_A", "unknown_route")])
    assert metrics["selective_risk"] is None
    assert metrics["unknown_false_acceptance_rate"] is None
    assert metrics["unknown_auroc"] is None


@pytest.mark.parametrize(
    "truth,scores,auc,ap",
    [
        ([False, True], [0.1, 0.9], 1.0, 1.0),
        ([False, True], [0.9, 0.1], 0.0, 0.5),
        ([False, True], [0.5, 0.5], 0.5, 0.5),
        ([False, False, True, True], [0, 1, 2, 3], 1.0, 1.0),
    ],
)
def test_rank_metrics_handle_ties_exactly(truth, scores, auc, ap):
    result = ranking_metrics(truth, scores)
    assert result["unknown_auroc"] == auc
    assert result["unknown_average_precision"] == ap


def test_dtw_handles_unequal_lengths_and_perfect_matching():
    assert dtw_similarity(np.ones((2, 5))) == 1.0
    assert dtw_similarity(np.eye(4)) == 1.0
    assert dtw_similarity(np.zeros((3, 2))) == 0.0
    with pytest.raises(ValueError):
        dtw_similarity(np.array([[np.nan]]))


def test_duplicate_metrics_records_are_not_double_counted():
    with pytest.raises(ValueError):
        summarize_decisions([row("qa", "UNKNOWN", "uncertain")] * 2)


def test_timing_percentiles_and_invalid_samples():
    assert timing_summary([1, 2, 3])["median_ms"] == 2
    assert timing_summary([1, 2, 3])["samples"] == 3
    with pytest.raises(ValueError):
        timing_summary([float("nan")])
