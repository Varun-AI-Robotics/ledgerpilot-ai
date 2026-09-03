from datetime import datetime

from sqlalchemy.orm import Session

from app.models.reconciliation import (
    Reconciliation
)

from app.models.ai_analysis import (
    AIAnalysis
)

from app.services.gemini_service import (
    analyze_exception
)


def investigate_exception(
    db: Session,
    payment_id: str
):

    # --------------------------------------
    # Find reconciliation
    # --------------------------------------

    reconciliation = (
        db.query(Reconciliation)
        .filter(
            Reconciliation.payment_id
            == payment_id
        )
        .first()
    )

    if not reconciliation:

        raise ValueError(
            "Reconciliation record not found."
        )

    # --------------------------------------
    # Only investigate exceptions
    # --------------------------------------

    if reconciliation.status == "MATCHED":

        raise ValueError(
            "This transaction is already matched."
        )

    # --------------------------------------
    # Prepare evidence
    # --------------------------------------

    evidence = {

        "payment_id":
            reconciliation.payment_id,

        "payment_amount":
            reconciliation.payment_amount,

        "settlement_amount":
            reconciliation.settlement_amount,

        "bank_amount":
            reconciliation.bank_amount,

        "expected_net_amount":
            reconciliation.expected_net_amount,

        "fee":
            reconciliation.fee,

        "tax":
            reconciliation.tax,

        "amount_difference":
            reconciliation.amount_difference,

        "settlement_found":
            bool(
                reconciliation.settlement_found
            ),

        "bank_transaction_found":
            bool(
                reconciliation.bank_transaction_found
            ),

        "reference_match":
            bool(
                reconciliation.reference_match
            ),

        "deterministic_status":
            reconciliation.status,

        "deterministic_reason":
            reconciliation.reason
    }

    # --------------------------------------
    # Gemini analysis
    # --------------------------------------

    result = analyze_exception(
        evidence
    )

    # --------------------------------------
    # Save result
    # --------------------------------------

    analysis = AIAnalysis(

        payment_id=
            reconciliation.payment_id,

        classification=
            result.classification,

        confidence=
            result.confidence,

        reason=
            result.reason,

        recommended_action=
            result.recommended_action,

        priority=
            result.priority,

        created_at=datetime.now()
    )

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    return {

        "payment_id":
            analysis.payment_id,

        "classification":
            analysis.classification,

        "confidence":
            analysis.confidence,

        "reason":
            analysis.reason,

        "recommended_action":
            analysis.recommended_action,

        "priority":
            analysis.priority
    }