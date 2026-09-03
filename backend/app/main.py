import time

from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from pydantic import BaseModel


# ==========================================
# Database
# ==========================================

from app.database.database import (
    Base,
    engine,
    get_db
)


# ==========================================
# Models
# ==========================================

from app.models.transaction import (
    Payment,
    Settlement,
    BankTransaction
)

from app.models.reconciliation import (
    Reconciliation
)

from app.models.ai_analysis import (
    AIAnalysis
)

from app.models.ground_truth import (
    GroundTruth
)

from app.models.evaluation import (
    EvaluationRun
)


# ==========================================
# Services
# ==========================================

from app.services.data_generator import (
    generate_data
)

from app.services.reconciliation_engine import (
    reconcile_transactions
)

from app.services.ai_agent import (
    investigate_exception
)

from app.services.finance_assistant import (
    ask_finance_assistant
)

from app.services.evaluation import (
    evaluate_reconciliation,
    evaluate_exception_types
)

from app.services.benchmark import (
    run_scale_benchmark
)


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="LedgerPilot AI",
    description="AI Finance Controller",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================================
# Create Database Tables
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# Request Models
# ==========================================

class FinanceQuestion(BaseModel):

    question: str


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():

    return {
        "application": "LedgerPilot AI",
        "status": "running",
        "message": "AI Finance Controller Backend"
    }


# ==========================================
# PHASE 1
# SYNTHETIC DATA GENERATION
# ==========================================

@app.post("/api/generate-data")
def generate_synthetic_data(
    count: int = 1000,
    db: Session = Depends(get_db)
):

    try:

        result = generate_data(
            db,
            count
        )

        return {
            "success": True,
            "message": "Synthetic finance data generated",
            "records": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Data generation failed: {str(e)}"
        )


# ==========================================
# GET PAYMENTS
# ==========================================

@app.get("/api/payments")
def get_payments(
    db: Session = Depends(get_db)
):

    payments = (
        db.query(Payment)
        .limit(100)
        .all()
    )

    return payments


# ==========================================
# GET SETTLEMENTS
# ==========================================

@app.get("/api/settlements")
def get_settlements(
    db: Session = Depends(get_db)
):

    settlements = (
        db.query(Settlement)
        .limit(100)
        .all()
    )

    return settlements


# ==========================================
# GET BANK TRANSACTIONS
# ==========================================

@app.get("/api/bank-transactions")
def get_bank_transactions(
    db: Session = Depends(get_db)
):

    transactions = (
        db.query(BankTransaction)
        .limit(100)
        .all()
    )

    return transactions


# ==========================================
# DATABASE STATISTICS
# ==========================================

@app.get("/api/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    payment_count = db.query(
        Payment
    ).count()

    settlement_count = db.query(
        Settlement
    ).count()

    bank_count = db.query(
        BankTransaction
    ).count()

    reconciliation_count = db.query(
        Reconciliation
    ).count()

    ai_analysis_count = db.query(
        AIAnalysis
    ).count()

    ground_truth_count = db.query(
        GroundTruth
    ).count()

    return {

        "payments":
            payment_count,

        "settlements":
            settlement_count,

        "bank_transactions":
            bank_count,

        "reconciliations":
            reconciliation_count,

        "ai_analyses":
            ai_analysis_count,

        "ground_truth":
            ground_truth_count
    }


# ==========================================
# PHASE 2
# RUN RECONCILIATION
# ==========================================

@app.post("/api/reconcile")
def run_reconciliation(
    db: Session = Depends(get_db)
):

    try:

        result = reconcile_transactions(
            db
        )

        return {

            "success": True,

            "message":
                "Reconciliation completed",

            "results":
                result
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=(
                f"Reconciliation failed: {str(e)}"
            )
        )


# ==========================================
# GET ALL RECONCILIATION RESULTS
# ==========================================

@app.get("/api/reconciliation")
def get_reconciliation(
    page: int = 1,
    limit: int = 100,
    search: str = "",
    db: Session = Depends(get_db)
):
    # Keep API responses small and fast
    limit = min(max(limit, 10), 200)

    query = db.query(Reconciliation)

    # Server-side search
    if search.strip():
        query = query.filter(
            Reconciliation.payment_id.ilike(
                f"%{search.strip()}%"
            )
        )

    total = query.count()

    pages = (
        (total + limit - 1) // limit
        if total > 0
        else 1
    )

    # Prevent invalid page numbers
    page = max(1, min(page, pages))

    results = (
        query
        .order_by(Reconciliation.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "data": results,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }

# ==========================================
# GET EXCEPTIONS
# ==========================================

@app.get("/api/exceptions")
def get_exceptions(
    db: Session = Depends(get_db)
):

    exceptions = (
        db.query(Reconciliation)
        .filter(
            Reconciliation.status == "EXCEPTION"
        )
        .all()
    )

    return exceptions


# ==========================================
# GET PARTIAL MATCHES
# ==========================================

@app.get("/api/partial")
def get_partial_matches(
    db: Session = Depends(get_db)
):

    partial = (
        db.query(Reconciliation)
        .filter(
            Reconciliation.status == "PARTIAL"
        )
        .all()
    )

    return partial


# ==========================================
# GET MATCHED TRANSACTIONS
# ==========================================

@app.get("/api/matched")
def get_matched_transactions(
    db: Session = Depends(get_db)
):

    matched = (
        db.query(Reconciliation)
        .filter(
            Reconciliation.status == "MATCHED"
        )
        .all()
    )

    return matched


# ==========================================
# RECONCILIATION METRICS
# ==========================================

@app.get("/api/metrics")
def get_metrics(
    db: Session = Depends(get_db)
):

    total = db.query(
        Reconciliation
    ).count()

    matched = (
        db.query(Reconciliation)
        .filter(
            Reconciliation.status == "MATCHED"
        )
        .count()
    )

    partial = (
        db.query(Reconciliation)
        .filter(
            Reconciliation.status == "PARTIAL"
        )
        .count()
    )

    exceptions = (
        db.query(Reconciliation)
        .filter(
            Reconciliation.status == "EXCEPTION"
        )
        .count()
    )

    # --------------------------------------
    # Match Rate
    # --------------------------------------

    match_rate = 0

    if total > 0:

        match_rate = round(
            (matched / total) * 100,
            2
        )

    # --------------------------------------
    # Unreconciled Amount
    # --------------------------------------

    unreconciled_amount = 0.0

    exception_records = (
        db.query(Reconciliation)
        .filter(
            Reconciliation.status == "EXCEPTION"
        )
        .all()
    )

    for record in exception_records:

        if record.amount_difference is not None:

            unreconciled_amount += abs(
                record.amount_difference
            )

        elif record.payment_amount is not None:

            unreconciled_amount += (
                record.payment_amount
            )

    return {

        "total_records":
            total,

        "matched":
            matched,

        "partial":
            partial,

        "exceptions":
            exceptions,

        "match_rate":
            match_rate,

        "unreconciled_amount":
            round(
                unreconciled_amount,
                2
            )
    }


# ==========================================
# PHASE 5.1
# GROUND TRUTH
# ==========================================

@app.get("/api/ground-truth")
def get_ground_truth(
    db: Session = Depends(get_db)
):

    records = (
        db.query(GroundTruth)
        .limit(100)
        .all()
    )

    return records


# ==========================================
# GROUND TRUTH STATISTICS
# ==========================================

@app.get("/api/ground-truth/stats")
def get_ground_truth_stats(
    db: Session = Depends(get_db)
):

    total = db.query(
        GroundTruth
    ).count()

    matched = (
        db.query(GroundTruth)
        .filter(
            GroundTruth.expected_status == "MATCHED"
        )
        .count()
    )

    exceptions = (
        db.query(GroundTruth)
        .filter(
            GroundTruth.expected_status == "EXCEPTION"
        )
        .count()
    )

    partial = (
        db.query(GroundTruth)
        .filter(
            GroundTruth.expected_status == "PARTIAL"
        )
        .count()
    )

    # --------------------------------------
    # Exception Breakdown
    # --------------------------------------

    exception_types = {}

    exception_records = (
        db.query(GroundTruth)
        .filter(
            GroundTruth.expected_exception.isnot(None)
        )
        .all()
    )

    for record in exception_records:

        exception_type = (
            record.expected_exception
        )

        if exception_type:

            exception_types[
                exception_type
            ] = (
                exception_types.get(
                    exception_type,
                    0
                ) + 1
            )

    return {

        "total":
            total,

        "matched":
            matched,

        "partial":
            partial,

        "exceptions":
            exceptions,

        "exception_types":
            exception_types
    }


# ==========================================
# PHASE 3
# AI EXCEPTION INVESTIGATION
# ==========================================

@app.post(
    "/api/ai/investigate/{payment_id}"
)
def investigate_payment(
    payment_id: str,
    db: Session = Depends(get_db)
):

    try:

        result = investigate_exception(
            db,
            payment_id
        )

        return {

            "success": True,

            "analysis":
                result
        }

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)
        )

    except Exception as e:

        print("================================")
        print("AI INVESTIGATION ERROR")
        print(type(e).__name__)
        print(str(e))
        print("================================")

        raise HTTPException(

            status_code=500,

            detail=(
                f"AI analysis failed: {str(e)}"
            )
        )


# ==========================================
# GET ALL AI ANALYSES
# ==========================================

@app.get("/api/ai/analyses")
def get_ai_analyses(
    db: Session = Depends(get_db)
):

    analyses = (
        db.query(AIAnalysis)
        .order_by(
            AIAnalysis.created_at.desc()
        )
        .all()
    )

    return analyses


# ==========================================
# GET AI ANALYSIS FOR PAYMENT
# ==========================================

@app.get(
    "/api/ai/analysis/{payment_id}"
)
def get_ai_analysis(
    payment_id: str,
    db: Session = Depends(get_db)
):

    analysis = (
        db.query(AIAnalysis)
        .filter(
            AIAnalysis.payment_id
            == payment_id
        )
        .order_by(
            AIAnalysis.created_at.desc()
        )
        .first()
    )

    if not analysis:

        raise HTTPException(

            status_code=404,

            detail=(
                "AI analysis not found."
            )
        )

    return analysis


# ==========================================
# AI FINANCE ASSISTANT
# ==========================================

@app.post("/api/ai/ask")
def ask_ai(
    request: FinanceQuestion,
    db: Session = Depends(get_db)
):

    try:

        # ==================================
        # Get reconciliation statistics
        # ==================================

        total = db.query(
            Reconciliation
        ).count()

        matched = (
            db.query(Reconciliation)
            .filter(
                Reconciliation.status
                == "MATCHED"
            )
            .count()
        )

        partial = (
            db.query(Reconciliation)
            .filter(
                Reconciliation.status
                == "PARTIAL"
            )
            .count()
        )

        exceptions = (
            db.query(Reconciliation)
            .filter(
                Reconciliation.status
                == "EXCEPTION"
            )
            .count()
        )

        # ==================================
        # Calculate unreconciled amount
        # ==================================

        unreconciled_amount = 0.0

        exception_records = (
            db.query(Reconciliation)
            .filter(
                Reconciliation.status
                == "EXCEPTION"
            )
            .all()
        )

        for record in exception_records:

            if (
                record.amount_difference
                is not None
            ):

                unreconciled_amount += abs(
                    record.amount_difference
                )

            elif (
                record.payment_amount
                is not None
            ):

                unreconciled_amount += (
                    record.payment_amount
                )

        # ==================================
        # Match rate
        # ==================================

        match_rate = 0

        if total > 0:

            match_rate = round(
                (matched / total) * 100,
                2
            )

        # ==================================
        # Context for Gemini
        # ==================================

        context = {

            "total_records":
                total,

            "matched":
                matched,

            "partial":
                partial,

            "exceptions":
                exceptions,

            "match_rate":
                match_rate,

            "unreconciled_amount":
                round(
                    unreconciled_amount,
                    2
                )
        }

        print("================================")
        print("FINANCE AI REQUEST")

        print(
            "Question:",
            request.question
        )

        print(
            "Context:",
            context
        )

        print("================================")

        # ==================================
        # Ask Gemini
        # ==================================

        answer = ask_finance_assistant(

            request.question,

            context
        )

        return {

            "success": True,

            "question":
                request.question,

            "answer":
                answer
        }

    except Exception as e:

        print("================================")
        print("AI ASK ERROR")
        print(type(e).__name__)
        print(str(e))
        print("================================")

        raise HTTPException(

            status_code=500,

            detail=(
                f"AI assistant failed: {str(e)}"
            )
        )


# ============================================================
# PHASE 5
# EVALUATION RUN
# ============================================================

@app.post("/api/evaluation/run")
def run_evaluation(
    db: Session = Depends(get_db)
):

    try:

        start_time = time.perf_counter()

        # Run reconciliation first
        reconciliation_result = (
            reconcile_transactions(db)
        )

        processing_time = (
            time.perf_counter()
            - start_time
        )

        # Evaluate against ground truth
        evaluation = evaluate_reconciliation(
            db,
            processing_time
        )

        # Per-exception benchmark
        benchmark = evaluate_exception_types(
            db
        )

        return {

            "success": True,

            "message":
                "Evaluation completed",

            "reconciliation":
                reconciliation_result,

            "evaluation": {

                "total_records":
                    evaluation.total_records,

                "correct_status":
                    evaluation.correct_status,

                "incorrect_status":
                    evaluation.incorrect_status,

                "true_positives":
                    evaluation.true_positives,

                "false_positives":
                    evaluation.false_positives,

                "false_negatives":
                    evaluation.false_negatives,

                "accuracy":
                    round(
                        evaluation.accuracy,
                        2
                    ),

                "precision":
                    round(
                        evaluation.precision,
                        2
                    ),

                "recall":
                    round(
                        evaluation.recall,
                        2
                    ),

                "f1_score":
                    round(
                        evaluation.f1_score,
                        2
                    ),

                "exception_detection_rate":
                    round(
                        evaluation.exception_detection_rate,
                        2
                    ),

                "false_match_rate":
                    round(
                        evaluation.false_match_rate,
                        2
                    ),

                "exception_type_accuracy":
                    round(
                        evaluation.exception_type_accuracy,
                        2
                    ),

                "processing_time_seconds":
                    round(
                        evaluation.processing_time_seconds,
                        4
                    ),

                "records_per_second":
                    round(
                        evaluation.records_per_second,
                        2
                    )
            },

            "benchmark":
                benchmark
        }

    except Exception as e:

        print("================================")
        print("EVALUATION ERROR")
        print(type(e).__name__)
        print(str(e))
        print("================================")

        raise HTTPException(

            status_code=500,

            detail=(
                f"Evaluation failed: {str(e)}"
            )
        )


# ============================================================
# GET LATEST EVALUATION METRICS
# ============================================================

@app.get("/api/evaluation/metrics")
def get_evaluation_metrics(
    db: Session = Depends(get_db)
):

    evaluation = (
        db.query(EvaluationRun)
        .order_by(
            EvaluationRun.id.desc()
        )
        .first()
    )

    if not evaluation:

        return {

            "success": False,

            "message":
                "No evaluation has been run yet"
        }

    return {

        "success": True,

        "evaluation": {

            "total_records":
                evaluation.total_records,

            "correct_status":
                evaluation.correct_status,

            "incorrect_status":
                evaluation.incorrect_status,

            "true_positives":
                evaluation.true_positives,

            "false_positives":
                evaluation.false_positives,

            "false_negatives":
                evaluation.false_negatives,

            "accuracy":
                round(
                    evaluation.accuracy,
                    2
                ),

            "precision":
                round(
                    evaluation.precision,
                    2
                ),

            "recall":
                round(
                    evaluation.recall,
                    2
                ),

            "f1_score":
                round(
                    evaluation.f1_score,
                    2
                ),

            "exception_detection_rate":
                round(
                    evaluation.exception_detection_rate,
                    2
                ),

            "false_match_rate":
                round(
                    evaluation.false_match_rate,
                    2
                ),

            "exception_type_accuracy":
                round(
                    evaluation.exception_type_accuracy,
                    2
                ),

            "processing_time_seconds":
                round(
                    evaluation.processing_time_seconds,
                    4
                ),

            "records_per_second":
                round(
                    evaluation.records_per_second,
                    2
                ),

            "evaluated_at":
                evaluation.evaluated_at
        }
    }


# ============================================================
# EXCEPTION TYPE BENCHMARK
# ============================================================

@app.get("/api/evaluation/benchmark")
def get_evaluation_benchmark(
    db: Session = Depends(get_db)
):

    results = evaluate_exception_types(
        db
    )

    return {

        "success": True,

        "benchmark":
            results
    }


# ============================================================
# EVALUATION HISTORY
# ============================================================

@app.get("/api/evaluation/history")
def get_evaluation_history(
    db: Session = Depends(get_db)
):

    evaluations = (
        db.query(EvaluationRun)
        .order_by(
            EvaluationRun.id.desc()
        )
        .limit(20)
        .all()
    )

    return {

        "success": True,

        "count":
            len(evaluations),

        "evaluations": [

            {

                "id":
                    e.id,

                "total_records":
                    e.total_records,

                "accuracy":
                    round(
                        e.accuracy,
                        2
                    ),

                "precision":
                    round(
                        e.precision,
                        2
                    ),

                "recall":
                    round(
                        e.recall,
                        2
                    ),

                "f1_score":
                    round(
                        e.f1_score,
                        2
                    ),

                "exception_detection_rate":
                    round(
                        e.exception_detection_rate,
                        2
                    ),

                "false_match_rate":
                    round(
                        e.false_match_rate,
                        2
                    ),

                "exception_type_accuracy":
                    round(
                        e.exception_type_accuracy,
                        2
                    ),

                "processing_time_seconds":
                    round(
                        e.processing_time_seconds,
                        4
                    ),

                "records_per_second":
                    round(
                        e.records_per_second,
                        2
                    ),

                "evaluated_at":
                    e.evaluated_at
            }

            for e in evaluations
        ]
    }


# ============================================================
# PHASE 5.5
# SCALE BENCHMARK
# ============================================================

@app.post("/api/evaluation/scale-benchmark")
def run_scale_benchmark_api(
    db: Session = Depends(get_db)
):

    try:

        results = run_scale_benchmark(
            db
        )

        return {

            "success": True,

            "message":
                "Scale benchmark completed",

            "benchmark":
                results
        }

    except Exception as e:

        print("================================")
        print("SCALE BENCHMARK ERROR")
        print(type(e).__name__)
        print(str(e))
        print("================================")

        raise HTTPException(

            status_code=500,

            detail=(
                f"Scale benchmark failed: {str(e)}"
            )
        )