from datetime import datetime

from app.models.transaction import (
    Payment,
    Settlement,
    BankTransaction
)

from app.models.reconciliation import (
    Reconciliation
)


# ==========================================
# CONSTANTS
# ==========================================

EXPECTED_FEE_RATE = 0.02
EXPECTED_TAX_RATE = 0.18

EXPECTED_SETTLEMENT_DAYS = 2

DELAY_THRESHOLD_DAYS = 5


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def calculate_expected_fee(amount):
    return round(
        amount * EXPECTED_FEE_RATE,
        2
    )


def calculate_expected_tax(fee):
    return round(
        fee * EXPECTED_TAX_RATE,
        2
    )


def calculate_expected_net(amount):
    fee = calculate_expected_fee(amount)

    tax = calculate_expected_tax(fee)

    return round(
        amount - fee - tax,
        2
    )


# ==========================================
# RECONCILIATION ENGINE
# ==========================================

def reconcile_transactions(db):

    # --------------------------------------
    # Remove previous reconciliation results
    # --------------------------------------

    db.query(Reconciliation).delete()

    db.commit()

    # --------------------------------------
    # Get all payments
    # --------------------------------------

    payments = (
        db.query(Payment)
        .all()
    )

    # --------------------------------------
    # Metrics
    # --------------------------------------

    total = 0

    matched = 0

    partial = 0

    exceptions = 0

    unreconciled_amount = 0.0

    # --------------------------------------
    # Process each payment
    # --------------------------------------

    for payment in payments:

        total += 1

        payment_id = payment.payment_id

        payment_amount = float(
            payment.amount or 0
        )

        # ==================================
        # Find ALL settlements
        # ==================================

        settlements = (
            db.query(Settlement)
            .filter(
                Settlement.payment_id
                == payment_id
            )
            .all()
        )

        # ==================================
        # Find ALL bank transactions
        # ==================================

        bank_transactions = (
            db.query(BankTransaction)
            .filter(
                BankTransaction.payment_id
                == payment_id
            )
            .all()
        )

        # ==================================
        # No settlement
        # ==================================

        if len(settlements) == 0:

            record = Reconciliation(

                payment_id=payment_id,

                payment_amount=payment_amount,

                settlement_amount=None,

                bank_amount=None,

                expected_net_amount=calculate_expected_net(
                    payment_amount
                ),

                fee=calculate_expected_fee(
                    payment_amount
                ),

                tax=calculate_expected_tax(
                    calculate_expected_fee(
                        payment_amount
                    )
                ),

                amount_difference=payment_amount,

                reference_match=0,

                settlement_found=0,

                bank_transaction_found=(
                    1
                    if len(bank_transactions) > 0
                    else 0
                ),

                status="EXCEPTION",

                reason="Missing settlement",

                reconciled_at=datetime.utcnow()
            )

            db.add(record)

            exceptions += 1

            unreconciled_amount += payment_amount

            continue

        # ==================================
        # Duplicate settlement
        # ==================================

        if len(settlements) > 1:

            first_settlement = settlements[0]

            settlement_amount = float(
                first_settlement.net_amount or 0
            )

            bank_amount = None

            if len(bank_transactions) > 0:

                bank_amount = float(
                    bank_transactions[0].amount or 0
                )

            expected_net = calculate_expected_net(
                payment_amount
            )

            record = Reconciliation(

                payment_id=payment_id,

                payment_amount=payment_amount,

                settlement_amount=settlement_amount,

                bank_amount=bank_amount,

                expected_net_amount=expected_net,

                fee=float(
                    first_settlement.fee or 0
                ),

                tax=float(
                    first_settlement.tax or 0
                ),

                amount_difference=round(
                    settlement_amount
                    - expected_net,
                    2
                ),

                reference_match=(
                    1
                    if len(bank_transactions) > 0
                    and bank_transactions[0].reference
                    == payment_id
                    else 0
                ),

                settlement_found=1,

                bank_transaction_found=(
                    1
                    if len(bank_transactions) > 0
                    else 0
                ),

                status="EXCEPTION",

                reason=(
                    f"Duplicate settlement detected: "
                    f"{len(settlements)} settlement records"
                ),

                reconciled_at=datetime.utcnow()
            )

            db.add(record)

            exceptions += 1

            unreconciled_amount += abs(
                settlement_amount - expected_net
            )

            continue

        # ==================================
        # Single settlement
        # ==================================

        settlement = settlements[0]

        settlement_amount = float(
            settlement.net_amount or 0
        )

        settlement_fee = float(
            settlement.fee or 0
        )

        settlement_tax = float(
            settlement.tax or 0
        )

        # ==================================
        # Expected values
        # ==================================

        expected_fee = calculate_expected_fee(
            payment_amount
        )

        expected_tax = calculate_expected_tax(
            expected_fee
        )

        expected_net = calculate_expected_net(
            payment_amount
        )

        # ==================================
        # Amount difference
        # ==================================

        amount_difference = round(
            settlement_amount - expected_net,
            2
        )

        # ==================================
        # Fee mismatch
        # ==================================

        fee_difference = round(
            settlement_fee - expected_fee,
            2
        )

        # ==================================
        # Bank transaction
        # ==================================

        bank_amount = None

        reference_match = 0

        if len(bank_transactions) > 0:

            bank_transaction = bank_transactions[0]

            bank_amount = float(
                bank_transaction.amount or 0
            )

            if (
                bank_transaction.reference
                == payment_id
            ):

                reference_match = 1

        # ==================================
        # Missing bank transaction
        # ==================================

        if len(bank_transactions) == 0:

            record = Reconciliation(

                payment_id=payment_id,

                payment_amount=payment_amount,

                settlement_amount=settlement_amount,

                bank_amount=None,

                expected_net_amount=expected_net,

                fee=settlement_fee,

                tax=settlement_tax,

                amount_difference=amount_difference,

                reference_match=0,

                settlement_found=1,

                bank_transaction_found=0,

                status="PARTIAL",

                reason="Bank transaction missing",

                reconciled_at=datetime.utcnow()
            )

            db.add(record)

            partial += 1

            continue

        # ==================================
        # Delayed settlement
        # ==================================

        delayed = False

        if (
            settlement.settlement_date
            and payment.created_at
        ):

            settlement_delay = (
                settlement.settlement_date
                - payment.created_at
            ).days

            if (
                settlement_delay
                > DELAY_THRESHOLD_DAYS
            ):

                delayed = True

        if delayed:

            record = Reconciliation(

                payment_id=payment_id,

                payment_amount=payment_amount,

                settlement_amount=settlement_amount,

                bank_amount=bank_amount,

                expected_net_amount=expected_net,

                fee=settlement_fee,

                tax=settlement_tax,

                amount_difference=amount_difference,

                reference_match=reference_match,

                settlement_found=1,

                bank_transaction_found=1,

                status="EXCEPTION",

                reason=(
                    "Delayed settlement: "
                    f"{settlement_delay} days after payment"
                ),

                reconciled_at=datetime.utcnow()
            )

            db.add(record)

            exceptions += 1

            unreconciled_amount += abs(
                amount_difference
            )

            continue

        # ==================================
        # Bank reference mismatch
        # ==================================

        if reference_match == 0:

            record = Reconciliation(

                payment_id=payment_id,

                payment_amount=payment_amount,

                settlement_amount=settlement_amount,

                bank_amount=bank_amount,

                expected_net_amount=expected_net,

                fee=settlement_fee,

                tax=settlement_tax,

                amount_difference=amount_difference,

                reference_match=0,

                settlement_found=1,

                bank_transaction_found=1,

                status="EXCEPTION",

                reason="Bank transaction reference mismatch",

                reconciled_at=datetime.utcnow()
            )

            db.add(record)

            exceptions += 1

            unreconciled_amount += abs(
                amount_difference
            )

            continue

        # ==================================
        # Fee mismatch
        # ==================================

        if abs(fee_difference) > 0.01:

            record = Reconciliation(

                payment_id=payment_id,

                payment_amount=payment_amount,

                settlement_amount=settlement_amount,

                bank_amount=bank_amount,

                expected_net_amount=expected_net,

                fee=settlement_fee,

                tax=settlement_tax,

                amount_difference=amount_difference,

                reference_match=reference_match,

                settlement_found=1,

                bank_transaction_found=1,

                status="EXCEPTION",

                reason=(
                    "Fee mismatch: "
                    f"expected {expected_fee}, "
                    f"actual {settlement_fee}"
                ),

                reconciled_at=datetime.utcnow()
            )

            db.add(record)

            exceptions += 1

            unreconciled_amount += abs(
                fee_difference
            )

            continue

        # ==================================
        # Amount mismatch
        # ==================================

        if abs(amount_difference) > 0.01:

            record = Reconciliation(

                payment_id=payment_id,

                payment_amount=payment_amount,

                settlement_amount=settlement_amount,

                bank_amount=bank_amount,

                expected_net_amount=expected_net,

                fee=settlement_fee,

                tax=settlement_tax,

                amount_difference=amount_difference,

                reference_match=reference_match,

                settlement_found=1,

                bank_transaction_found=1,

                status="EXCEPTION",

                reason=(
                    "Settlement amount mismatch: "
                    f"difference {amount_difference}"
                ),

                reconciled_at=datetime.utcnow()
            )

            db.add(record)

            exceptions += 1

            unreconciled_amount += abs(
                amount_difference
            )

            continue

        # ==================================
        # Bank amount mismatch
        # ==================================

        bank_amount_difference = round(
            bank_amount - settlement_amount,
            2
        )

        if abs(bank_amount_difference) > 0.01:

            record = Reconciliation(

                payment_id=payment_id,

                payment_amount=payment_amount,

                settlement_amount=settlement_amount,

                bank_amount=bank_amount,

                expected_net_amount=expected_net,

                fee=settlement_fee,

                tax=settlement_tax,

                amount_difference=bank_amount_difference,

                reference_match=reference_match,

                settlement_found=1,

                bank_transaction_found=1,

                status="EXCEPTION",

                reason=(
                    "Bank amount mismatch: "
                    f"difference {bank_amount_difference}"
                ),

                reconciled_at=datetime.utcnow()
            )

            db.add(record)

            exceptions += 1

            unreconciled_amount += abs(
                bank_amount_difference
            )

            continue

        # ==================================
        # MATCHED
        # ==================================

        record = Reconciliation(

            payment_id=payment_id,

            payment_amount=payment_amount,

            settlement_amount=settlement_amount,

            bank_amount=bank_amount,

            expected_net_amount=expected_net,

            fee=settlement_fee,

            tax=settlement_tax,

            amount_difference=0,

            reference_match=1,

            settlement_found=1,

            bank_transaction_found=1,

            status="MATCHED",

            reason="Payment, settlement and bank transaction matched",

            reconciled_at=datetime.utcnow()
        )

        db.add(record)

        matched += 1

    # ==========================================
    # Commit
    # ==========================================

    db.commit()

    # ==========================================
    # Match rate
    # ==========================================

    match_rate = 0

    if total > 0:

        match_rate = round(
            (matched / total) * 100,
            2
        )

    # ==========================================
    # Return metrics
    # ==========================================

    return {

        "total": total,

        "matched": matched,

        "partial": partial,

        "exceptions": exceptions,

        "match_rate": match_rate,

        "unreconciled_amount": round(
            unreconciled_amount,
            2
        )
    }