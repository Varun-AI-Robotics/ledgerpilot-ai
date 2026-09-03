from sqlalchemy.orm import Session

from app.models.ground_truth import GroundTruth
from app.models.reconciliation import Reconciliation
from app.models.evaluation import EvaluationRun


EXCEPTION_TYPES = [
    "FEE_MISMATCH",
    "AMOUNT_MISMATCH",
    "MISSING_SETTLEMENT",
    "MISSING_BANK_TRANSACTION",
    "DELAYED_SETTLEMENT",
    "DUPLICATE_SETTLEMENT",
    "BANK_REFERENCE_MISMATCH",
]


def detect_exception_type(reason: str | None):

    if not reason:
        return None

    reason = reason.lower()

    if "missing settlement" in reason:
        return "MISSING_SETTLEMENT"

    if "duplicate settlement" in reason:
        return "DUPLICATE_SETTLEMENT"

    if "delayed settlement" in reason:
        return "DELAYED_SETTLEMENT"

    if "reference mismatch" in reason:
        return "BANK_REFERENCE_MISMATCH"

    if "fee mismatch" in reason:
        return "FEE_MISMATCH"

    if "settlement amount mismatch" in reason:
        return "AMOUNT_MISMATCH"

    if "bank transaction missing" in reason:
        return "MISSING_BANK_TRANSACTION"

    if "bank amount mismatch" in reason:
        return "AMOUNT_MISMATCH"

    return None


# ============================================================
# OVERALL EVALUATION
# ============================================================

def evaluate_reconciliation(
    db: Session,
    processing_time: float = 0.0
):

    ground_truth = db.query(GroundTruth).all()

    reconciliations = db.query(
        Reconciliation
    ).all()

    reconciliation_map = {
        r.payment_id: r
        for r in reconciliations
    }

    total = len(ground_truth)

    correct_status = 0
    incorrect_status = 0

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    correct_exception_type = 0
    total_ground_truth_exceptions = 0

    for truth in ground_truth:

        prediction = reconciliation_map.get(
            truth.payment_id
        )

        if prediction is None:

            incorrect_status += 1

            if truth.expected_exception:
                total_ground_truth_exceptions += 1
                false_negatives += 1

            continue

        predicted_status = prediction.status
        expected_status = truth.expected_status

        if predicted_status == expected_status:
            correct_status += 1
        else:
            incorrect_status += 1

        expected_exception = truth.expected_exception

        predicted_exception = detect_exception_type(
            prediction.reason
        )

        if expected_exception:

            total_ground_truth_exceptions += 1

            if predicted_exception:

                true_positives += 1

                if (
                    predicted_exception
                    == expected_exception
                ):
                    correct_exception_type += 1

            else:

                false_negatives += 1

        else:

            if predicted_exception:
                false_positives += 1

    # ------------------------------------------------
    # METRICS
    # ------------------------------------------------

    accuracy = (
        correct_status / total
        if total
        else 0
    )

    precision = (
        true_positives /
        (true_positives + false_positives)
        if true_positives + false_positives
        else 0
    )

    recall = (
        true_positives /
        (true_positives + false_negatives)
        if true_positives + false_negatives
        else 0
    )

    f1_score = (
        2 * precision * recall /
        (precision + recall)
        if precision + recall
        else 0
    )

    exception_detection_rate = (
        true_positives /
        total_ground_truth_exceptions
        if total_ground_truth_exceptions
        else 0
    )

    # False match = genuine exceptions
    # that were not detected.
    false_match_rate = (
        false_negatives /
        total_ground_truth_exceptions
        if total_ground_truth_exceptions
        else 0
    )

    exception_type_accuracy = (
        correct_exception_type /
        total_ground_truth_exceptions
        if total_ground_truth_exceptions
        else 0
    )

    records_per_second = (
        total / processing_time
        if processing_time > 0
        else 0
    )

    evaluation = EvaluationRun(

        total_records=total,

        correct_status=correct_status,

        incorrect_status=incorrect_status,

        true_positives=true_positives,

        false_positives=false_positives,

        false_negatives=false_negatives,

        accuracy=accuracy * 100,

        precision=precision * 100,

        recall=recall * 100,

        f1_score=f1_score * 100,

        exception_detection_rate=
            exception_detection_rate * 100,

        false_match_rate=
            false_match_rate * 100,

        exception_type_accuracy=
            exception_type_accuracy * 100,

        processing_time_seconds=
            processing_time,

        records_per_second=
            records_per_second
    )

    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    return evaluation


# ============================================================
# EXCEPTION TYPE BENCHMARK
# ============================================================

def evaluate_exception_types(db: Session):

    ground_truth = db.query(GroundTruth).all()

    reconciliations = db.query(
        Reconciliation
    ).all()

    reconciliation_map = {
        r.payment_id: r
        for r in reconciliations
    }

    results = {}

    for exception_type in EXCEPTION_TYPES:

        tp = 0
        fp = 0
        fn = 0
        support = 0

        for truth in ground_truth:

            prediction = reconciliation_map.get(
                truth.payment_id
            )

            expected = truth.expected_exception

            predicted = None

            if prediction:

                predicted = detect_exception_type(
                    prediction.reason
                )

            expected_is_type = (
                expected == exception_type
            )

            predicted_is_type = (
                predicted == exception_type
            )

            if expected_is_type:
                support += 1

            if expected_is_type and predicted_is_type:

                tp += 1

            elif (
                not expected_is_type
                and predicted_is_type
            ):

                fp += 1

            elif (
                expected_is_type
                and not predicted_is_type
            ):

                fn += 1

        precision = (
            tp / (tp + fp)
            if tp + fp
            else 0
        )

        recall = (
            tp / (tp + fn)
            if tp + fn
            else 0
        )

        f1 = (
            2 * precision * recall /
            (precision + recall)
            if precision + recall
            else 0
        )

        results[exception_type] = {

            "support": support,

            "true_positives": tp,

            "false_positives": fp,

            "false_negatives": fn,

            "precision": round(
                precision * 100,
                2
            ),

            "recall": round(
                recall * 100,
                2
            ),

            "f1_score": round(
                f1 * 100,
                2
            )
        }

    return results