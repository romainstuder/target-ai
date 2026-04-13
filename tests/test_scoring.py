from unittest.mock import patch

from open_targets_client import get_association, score_clinical

PSORIASIS = "EFO_0000676"
RA = "EFO_0003965"


# ── Fixtures ─────────────────────────────────────────────────────────────────


def assoc_new(genetic_score=0.8):
    """New-shape assoc response: target → associatedDiseases."""
    return {
        "data": {
            "target": {
                "associatedDiseases": {
                    "rows": [
                        {
                            "disease": {"id": PSORIASIS, "name": "psoriasis"},
                            "score": 0.74,
                            "datatypeScores": [
                                {"id": "genetic_association", "score": genetic_score},
                                {"id": "clinical", "score": 0.98},
                            ],
                            "datasourceScores": [],
                        }
                    ]
                }
            }
        }
    }


def drugs_for(efo_id, drug_name="testdrug", stage="Approved"):
    return {
        "data": {
            "target": {
                "approvedSymbol": "TEST",
                "drugAndClinicalCandidates": {
                    "count": 1,
                    "rows": [
                        {
                            "id": "CHEMBL1",
                            "maxClinicalStage": stage,
                            "drug": {"id": "CHEMBL1", "name": drug_name, "drugType": "Antibody"},
                            "diseases": [{"disease": {"id": efo_id, "name": "test disease"}}],
                        }
                    ],
                },
            }
        }
    }


EMPTY_DRUGS = {
    "data": {
        "target": {
            "approvedSymbol": "X",
            "drugAndClinicalCandidates": {"count": 0, "rows": []},
        }
    }
}
EMPTY_ASSOC = {"data": {"target": {"associatedDiseases": {"rows": []}}}}


# ── Tests: score_clinical ─────────────────────────────────────────────────────


def test_approved_for_target_indication_scores_5():
    score, reason = score_clinical(EMPTY_ASSOC, drugs_for(PSORIASIS, "secukinumab"), PSORIASIS)
    assert score == 5
    assert "this indication" in reason


def test_approved_for_other_indication_is_capped():
    score, reason = score_clinical(EMPTY_ASSOC, drugs_for(RA, "baricitinib"), PSORIASIS)
    assert score <= 3
    assert "other indication" in reason


def test_no_drugs_no_genetics_scores_zero():
    score, _ = score_clinical(EMPTY_ASSOC, EMPTY_DRUGS, PSORIASIS)
    assert score == 0


def test_strong_genetic_association_scores_four():
    score, _ = score_clinical(assoc_new(genetic_score=0.8), EMPTY_DRUGS, PSORIASIS)
    assert score == 4


def test_approved_for_indication_plus_genetics_scores_five():
    score, _ = score_clinical(assoc_new(0.8), drugs_for(PSORIASIS, "secukinumab"), PSORIASIS)
    assert score == 5


def test_phase3_drug_for_indication_scores_four():
    score, _ = score_clinical(EMPTY_ASSOC, drugs_for(PSORIASIS, "candidate", "Phase III"), PSORIASIS)
    assert score == 4


# ── Tests: get_association ────────────────────────────────────────────────────


def test_get_association_uses_target_side_query():
    mock_resp = {"data": {"target": {"associatedDiseases": {"rows": []}}}}
    with patch("open_targets_client.graphql_query", return_value=mock_resp) as mock_gql:
        get_association("ENSG00000112115", PSORIASIS)
        query_str = mock_gql.call_args[0][0]
        assert "associatedDiseases" in query_str
        assert "Bs" not in query_str
        assert "efoId" in query_str


def test_get_association_passes_both_ids():
    mock_resp = {"data": {"target": {"associatedDiseases": {"rows": []}}}}
    with patch("open_targets_client.graphql_query", return_value=mock_resp) as mock_gql:
        get_association("ENSG00000112115", PSORIASIS)
        variables = mock_gql.call_args[0][1]
        assert variables["ensemblId"] == "ENSG00000112115"
        assert variables["efoId"] == PSORIASIS
