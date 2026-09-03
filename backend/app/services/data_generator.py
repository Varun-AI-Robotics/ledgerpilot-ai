import random
from datetime import datetime, timedelta

from app.models.transaction import (
    Payment,
    Settlement,
    BankTransaction
)

from app.models.ground_truth import GroundTruth


# ============================================================
# Exception Types
# ============================================================

EXCEPTION_TYPES = [
    "FEE_MISMATCH",
    "AMOUNT_MISMATCH",
    "MISSING_SETTLEMENT",
    "MISSING_BANK_TRANSACTION",
    "DELAYED_SETTLEMENT",
    "DUPLICATE_SETTLEMENT",
    "BANK_REFERENCE_MISMATCH",
]


# ============================================================
# Data Generator
# ============================================================

def generate_data(db, count=1000):

    # -----------------------------------------
    # Clear old data
    # -----------------------------------------

    db.query(GroundTruth).delete()
    db.query(BankTransaction).delete()
    db.query(Settlement).delete()
    db.query(Payment).delete()

    db.commit()

    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    generated = {
        "payments": 0,
        "settlements": 0,
        "bank_transactions": 0,
        "ground_truth": 0,
        "exceptions": 0,
        "partial": 0,
    }

    # -----------------------------------------
    # Generate payments
    # -----------------------------------------

    for i in range(1, count + 1):

        payment_id = f"pay_{i:05d}"

        order_id = f"order_{i:05d}"

        amount = round(
            random.uniform(100, 50000),
            2
        )

        created_at = (
            datetime.utcnow()
            - timedelta(
                minutes=random.randint(0, 10000)
            )
        )

        # -----------------------------------------
        # Payment
        # -----------------------------------------

        payment = Payment(
            payment_id=payment_id,
            order_id=order_id,
            amount=amount,
            currency="INR",
            payment_method=random.choice(
                [
                    "card",
                    "upi",
                    "netbanking",
                    "wallet"
                ]
            ),
            payment_status="captured",
            created_at=created_at
        )

        db.add(payment)

        generated["payments"] += 1

        # -----------------------------------------
        # Decide ground-truth scenario
        # -----------------------------------------

        scenario_roll = random.random()

        if scenario_roll < 0.04:

            scenario = "FEE_MISMATCH"

        elif scenario_roll < 0.07:

            scenario = "AMOUNT_MISMATCH"

        elif scenario_roll < 0.11:

            scenario = "MISSING_SETTLEMENT"

        elif scenario_roll < 0.14:

            scenario = "MISSING_BANK_TRANSACTION"

        elif scenario_roll < 0.17:

            scenario = "DELAYED_SETTLEMENT"

        elif scenario_roll < 0.19:

            scenario = "DUPLICATE_SETTLEMENT"

        elif scenario_roll < 0.22:

            scenario = "BANK_REFERENCE_MISMATCH"

        else:

            scenario = "MATCHED"

        # =====================================================
        # MATCHED
        # =====================================================

        if scenario == "MATCHED":

            fee = round(
                amount * 0.02,
                2
            )

            tax = round(
                fee * 0.18,
                2
            )

            net_amount = round(
                amount - fee - tax,
                2
            )

            settlement_id = (
                f"set_{i:05d}"
            )

            settlement = Settlement(
                settlement_id=settlement_id,
                payment_id=payment_id,
                gross_amount=amount,
                fee=fee,
                tax=tax,
                net_amount=net_amount,
                settlement_status="processed",
                settlement_date=created_at + timedelta(
                    days=2
                )
            )

            db.add(settlement)

            generated["settlements"] += 1

            bank = BankTransaction(
                bank_transaction_id=f"bank_{i:05d}",
                payment_id=payment_id,
                reference=payment_id,
                amount=net_amount,
                transaction_type="credit",
                transaction_date=created_at + timedelta(
                    days=2
                )
            )

            db.add(bank)

            generated["bank_transactions"] += 1

            ground_truth = GroundTruth(
                payment_id=payment_id,
                expected_status="MATCHED",
                expected_exception=None,
                expected_amount=net_amount,
                description="Payment, settlement and bank transaction match."
            )

        # =====================================================
        # FEE MISMATCH
        # =====================================================

        elif scenario == "FEE_MISMATCH":

            correct_fee = round(
                amount * 0.02,
                2
            )

            wrong_fee = round(
                amount * 0.05,
                2
            )

            tax = round(
                correct_fee * 0.18,
                2
            )

            net_amount = round(
                amount - wrong_fee - tax,
                2
            )

            settlement = Settlement(
                settlement_id=f"set_{i:05d}",
                payment_id=payment_id,
                gross_amount=amount,
                fee=wrong_fee,
                tax=tax,
                net_amount=net_amount,
                settlement_status="processed",
                settlement_date=created_at + timedelta(
                    days=2
                )
            )

            db.add(settlement)

            generated["settlements"] += 1

            bank = BankTransaction(
                bank_transaction_id=f"bank_{i:05d}",
                payment_id=payment_id,
                reference=payment_id,
                amount=net_amount,
                transaction_type="credit",
                transaction_date=created_at + timedelta(
                    days=2
                )
            )

            db.add(bank)

            generated["bank_transactions"] += 1

            ground_truth = GroundTruth(
                payment_id=payment_id,
                expected_status="EXCEPTION",
                expected_exception="FEE_MISMATCH",
                expected_amount=net_amount,
                description="Settlement fee differs from expected fee."
            )

            generated["exceptions"] += 1

        # =====================================================
        # AMOUNT MISMATCH
        # =====================================================

        elif scenario == "AMOUNT_MISMATCH":

            fee = round(
                amount * 0.02,
                2
            )

            tax = round(
                fee * 0.18,
                2
            )

            expected_net = round(
                amount - fee - tax,
                2
            )

            settlement_amount = round(
                expected_net - random.uniform(50, 500),
                2
            )

            settlement = Settlement(
                settlement_id=f"set_{i:05d}",
                payment_id=payment_id,
                gross_amount=amount,
                fee=fee,
                tax=tax,
                net_amount=settlement_amount,
                settlement_status="processed",
                settlement_date=created_at + timedelta(
                    days=2
                )
            )

            db.add(settlement)

            generated["settlements"] += 1

            bank = BankTransaction(
                bank_transaction_id=f"bank_{i:05d}",
                payment_id=payment_id,
                reference=payment_id,
                amount=settlement_amount,
                transaction_type="credit",
                transaction_date=created_at + timedelta(
                    days=2
                )
            )

            db.add(bank)

            generated["bank_transactions"] += 1

            ground_truth = GroundTruth(
                payment_id=payment_id,
                expected_status="EXCEPTION",
                expected_exception="AMOUNT_MISMATCH",
                expected_amount=expected_net,
                description="Settlement net amount differs from expected amount."
            )

            generated["exceptions"] += 1

        # =====================================================
        # MISSING SETTLEMENT
        # =====================================================

        elif scenario == "MISSING_SETTLEMENT":

            ground_truth = GroundTruth(
                payment_id=payment_id,
                expected_status="EXCEPTION",
                expected_exception="MISSING_SETTLEMENT",
                expected_amount=amount,
                description="No settlement exists for this payment."
            )

            generated["exceptions"] += 1

        # =====================================================
        # MISSING BANK TRANSACTION
        # =====================================================

        elif scenario == "MISSING_BANK_TRANSACTION":

            fee = round(
                amount * 0.02,
                2
            )

            tax = round(
                fee * 0.18,
                2
            )

            net_amount = round(
                amount - fee - tax,
                2
            )

            settlement_date = (
                created_at + timedelta(days=2)
            )

            # Settlement exists
            settlement = Settlement(
                settlement_id=f"set_{i:05d}",
                payment_id=payment_id,
                gross_amount=amount,
                fee=fee,
                tax=tax,
                net_amount=net_amount,
                settlement_status="processed",
                settlement_date=settlement_date
            )

            db.add(settlement)

            generated["settlements"] += 1

            # IMPORTANT:
            # No bank transaction is created.
            # This creates the PARTIAL scenario.

            ground_truth = GroundTruth(
                payment_id=payment_id,
                expected_status="PARTIAL",
                expected_exception="MISSING_BANK_TRANSACTION",
                expected_amount=net_amount,
                description="Settlement exists but bank transaction is missing."
            )

            generated["partial"] += 1

        # =====================================================
        # DELAYED SETTLEMENT
        # =====================================================

        elif scenario == "DELAYED_SETTLEMENT":

            fee = round(
                amount * 0.02,
                2
            )

            tax = round(
                fee * 0.18,
                2
            )

            net_amount = round(
                amount - fee - tax,
                2
            )

            settlement_date = (
                created_at + timedelta(days=7)
            )

            settlement = Settlement(
                settlement_id=f"set_{i:05d}",
                payment_id=payment_id,
                gross_amount=amount,
                fee=fee,
                tax=tax,
                net_amount=net_amount,
                settlement_status="processed",
                settlement_date=settlement_date
            )

            db.add(settlement)

            generated["settlements"] += 1

            bank = BankTransaction(
                bank_transaction_id=f"bank_{i:05d}",
                payment_id=payment_id,
                reference=payment_id,
                amount=net_amount,
                transaction_type="credit",
                transaction_date=settlement_date
            )

            db.add(bank)

            generated["bank_transactions"] += 1

            ground_truth = GroundTruth(
                payment_id=payment_id,
                expected_status="EXCEPTION",
                expected_exception="DELAYED_SETTLEMENT",
                expected_amount=net_amount,
                description="Settlement occurred significantly later than expected."
            )

            generated["exceptions"] += 1

        # =====================================================
        # DUPLICATE SETTLEMENT
        # =====================================================

        elif scenario == "DUPLICATE_SETTLEMENT":

            fee = round(
                amount * 0.02,
                2
            )

            tax = round(
                fee * 0.18,
                2
            )

            net_amount = round(
                amount - fee - tax,
                2
            )

            settlement_date = (
                created_at + timedelta(days=2)
            )

            settlement1 = Settlement(
                settlement_id=f"set_{i:05d}_A",
                payment_id=payment_id,
                gross_amount=amount,
                fee=fee,
                tax=tax,
                net_amount=net_amount,
                settlement_status="processed",
                settlement_date=settlement_date
            )

            settlement2 = Settlement(
                settlement_id=f"set_{i:05d}_B",
                payment_id=payment_id,
                gross_amount=amount,
                fee=fee,
                tax=tax,
                net_amount=net_amount,
                settlement_status="processed",
                settlement_date=settlement_date
            )

            db.add(settlement1)
            db.add(settlement2)

            generated["settlements"] += 2

            bank = BankTransaction(
                bank_transaction_id=f"bank_{i:05d}",
                payment_id=payment_id,
                reference=payment_id,
                amount=net_amount,
                transaction_type="credit",
                transaction_date=settlement_date
            )

            db.add(bank)

            generated["bank_transactions"] += 1

            ground_truth = GroundTruth(
                payment_id=payment_id,
                expected_status="EXCEPTION",
                expected_exception="DUPLICATE_SETTLEMENT",
                expected_amount=net_amount,
                description="Multiple settlement records exist for one payment."
            )

            generated["exceptions"] += 1

        # =====================================================
        # BANK REFERENCE MISMATCH
        # =====================================================

        elif scenario == "BANK_REFERENCE_MISMATCH":

            fee = round(
                amount * 0.02,
                2
            )

            tax = round(
                fee * 0.18,
                2
            )

            net_amount = round(
                amount - fee - tax,
                2
            )

            settlement_date = (
                created_at + timedelta(days=2)
            )

            settlement = Settlement(
                settlement_id=f"set_{i:05d}",
                payment_id=payment_id,
                gross_amount=amount,
                fee=fee,
                tax=tax,
                net_amount=net_amount,
                settlement_status="processed",
                settlement_date=settlement_date
            )

            db.add(settlement)

            generated["settlements"] += 1

            bank = BankTransaction(
                bank_transaction_id=f"bank_{i:05d}",
                payment_id=payment_id,
                reference=f"WRONG_REF_{i:05d}",
                amount=net_amount,
                transaction_type="credit",
                transaction_date=settlement_date
            )

            db.add(bank)

            generated["bank_transactions"] += 1

            ground_truth = GroundTruth(
                payment_id=payment_id,
                expected_status="EXCEPTION",
                expected_exception="BANK_REFERENCE_MISMATCH",
                expected_amount=net_amount,
                description="Bank transaction reference does not match payment."
            )

            generated["exceptions"] += 1

        else:

            continue

        # -----------------------------------------
        # Save ground truth
        # -----------------------------------------

        db.add(ground_truth)

        generated["ground_truth"] += 1

    # -----------------------------------------
    # Commit all generated records
    # -----------------------------------------

    db.commit()

    return generated