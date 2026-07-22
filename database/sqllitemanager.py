"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : sqlite_manager.py

Purpose :
Generic SQLite Database Manager

Author  : ChatGPT
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
import uuid
import sqlite3
import logging
import sys
from pathlib import Path
from typing import Any, List, Optional

# ==============================================================================
# Add Project Root
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==============================================================================

import config

# ==============================================================================
# Logging
# ==============================================================================

logger = logging.getLogger("SQLiteManager")
logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)


# ==============================================================================
# SQLite Manager
# ==============================================================================


class SQLiteManager:
    """
    Generic SQLite Database Manager.

    Responsibilities

    - Create database
    - Create tables
    - Execute SQL
    - Fetch records

    Business-specific methods will be added in Phase 2B.
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.database_path = (
            config.DATABASE_DIR /
            config.DATABASE_NAME
        )

        self.connection = None

        self.cursor = None

        self.connect()

        self.create_tables()

    # -------------------------------------------------------------------------

    def connect(self):
        """
        Create SQLite connection.
        """

        try:

            self.connection = sqlite3.connect(
                self.database_path
            )

            self.connection.row_factory = sqlite3.Row

            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")

            logger.info(
                "Connected to SQLite database."
            )

        except sqlite3.Error as error:

            logger.exception(error)

            raise

    # -------------------------------------------------------------------------

    def create_tables(self):
        """
        Create required tables.
        """

        self.create_pipeline_runs_table()

        self.create_metrics_table()

        self.create_diagnosis_table()

        self.create_recovery_table()

        self.create_workflow_logs_table()

        self.create_model_registry_table()

    # -------------------------------------------------------------------------

    def create_pipeline_runs_table(self):

        query = """

        CREATE TABLE IF NOT EXISTS pipeline_runs(

            run_id TEXT PRIMARY KEY,

            dataset_name TEXT NOT NULL,

            start_time TEXT,

            end_time TEXT,

            execution_time REAL,

            status TEXT,

            model_version INTEGER

        );

        """

        self.execute(query)

    # -------------------------------------------------------------------------

    def create_metrics_table(self):

        query = """

        CREATE TABLE IF NOT EXISTS metrics(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id TEXT,

            mae REAL,

            rmse REAL,

            r2 REAL,

            psi REAL,

            FOREIGN KEY(run_id)

            REFERENCES pipeline_runs(run_id)

        );

        """

        self.execute(query)

    # -------------------------------------------------------------------------

    def create_diagnosis_table(self):

        query = """

        CREATE TABLE IF NOT EXISTS diagnosis(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            run_id TEXT,

            severity TEXT,

            root_cause TEXT,

            recommendation TEXT,

            gemini_response TEXT,

            FOREIGN KEY(run_id)

            REFERENCES pipeline_runs(run_id)

        );

        """

        self.execute(query)

    # -------------------------------------------------------------------------

    def execute(
        self,
        query: str,
        parameters: tuple = ()
    ):
        """
        Execute INSERT / UPDATE / DELETE.
        """

        try:

            self.cursor.execute(
                query,
                parameters
            )

            self.connection.commit()

        except sqlite3.Error as error:

            logger.exception(error)

            raise

    # -------------------------------------------------------------------------

    def execute_many(
        self,
        query: str,
        parameters: list
    ):
        """
        Execute multiple SQL statements.
        """

        try:

            self.cursor.executemany(
                query,
                parameters
            )

            self.connection.commit()

        except sqlite3.Error as error:

            logger.exception(error)

            raise

    # -------------------------------------------------------------------------

    def fetch_one(
        self,
        query: str,
        parameters: tuple = ()
    ) -> Optional[sqlite3.Row]:
        """
        Fetch single row.
        """

        self.cursor.execute(
            query,
            parameters
        )

        return self.cursor.fetchone()

    # -------------------------------------------------------------------------

    def fetch_all(
        self,
        query: str,
        parameters: tuple = ()
    ) -> List[sqlite3.Row]:
        """
        Fetch multiple rows.
        """

        self.cursor.execute(
            query,
            parameters
        )

        return self.cursor.fetchall()
    
    # -------------------------------------------------------------------------

    def create_recovery_table(self):

        query = """

    CREATE TABLE IF NOT EXISTS recovery(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        run_id TEXT,

        strategy TEXT,

        status TEXT,

        retraining_required INTEGER,

        model_version INTEGER,

        FOREIGN KEY(run_id)

        REFERENCES pipeline_runs(run_id)

    );

    """

        self.execute(query)

    # -------------------------------------------------------------------------

    def create_workflow_logs_table(self):

        query = """

    CREATE TABLE IF NOT EXISTS workflow_logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        run_id TEXT,

        timestamp TEXT,

        step TEXT,

        status TEXT,

        message TEXT,

        FOREIGN KEY(run_id)

        REFERENCES pipeline_runs(run_id)

    );

    """

        self.execute(query)

    # -------------------------------------------------------------------------

    def create_model_registry_table(self):

        query = """

    CREATE TABLE IF NOT EXISTS model_registry(

        model_version INTEGER PRIMARY KEY,

        training_date TEXT,

        dataset_name TEXT,

        mae REAL,

        rmse REAL,

        r2 REAL,

        model_path TEXT

    );

    """

        self.execute(query)

    # -------------------------------------------------------------------------

    def delete(
    self,
    query: str,
    parameters: tuple = ()
    ):
        """
    Delete records.
    """

        self.execute(
        query,
        parameters
    )
    
    # -------------------------------------------------------------------------

    def close(self):
        """
        Close SQLite connection.
        """

        if self.connection:

            self.connection.close()

            logger.info(
            "SQLite connection closed."
        )
    # -------------------------------------------------------------------------

    def start_pipeline_run(
    self,
    dataset_name: str,
    model_version: int = 1
) -> str:
        """
        Start a new pipeline execution.

        Returns
        -------
        str
        Unique Run ID.
        """

        run_id = (
        f"RUN_{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
        f"{uuid.uuid4().hex[:6].upper()}"
        )

        start_time = datetime.now().isoformat()

        query = """
        INSERT INTO pipeline_runs
        (
            run_id,
            dataset_name,
            start_time,
            status,
            model_version
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
    """

        self.execute(

        query,

        (

            run_id,

            dataset_name,

            start_time,

            "Running",

            model_version

        )

    )

        logger.info(f"Pipeline Started : {run_id}")

        return run_id
    
    # -------------------------------------------------------------------------

    def finish_pipeline_run(
    self,
    run_id: str,
    status: str = "Completed"
):
        """
        Finish pipeline execution.
        """

        query = """
        SELECT start_time
        FROM pipeline_runs
        WHERE run_id = ?
    """

        row = self.fetch_one(

        query,

        (

            run_id,

        )

    )

        if row is None:

            raise ValueError(f"Run ID not found : {run_id}")

        start_time = datetime.fromisoformat(

        row["start_time"]

    )

        end_time = datetime.now()

        execution_time = (

        end_time - start_time

    ).total_seconds()

        update_query = """
        UPDATE pipeline_runs
        SET
            end_time = ?,
            execution_time = ?,
            status = ?
        WHERE run_id = ?
    """

        self.execute(

        update_query,

        (

            end_time.isoformat(),

            execution_time,

            status,

            run_id

        )

    )

        logger.info(

        f"Pipeline Finished : {run_id}"

    )
    # -------------------------------------------------------------------------

    def insert_log(
    self,
    run_id: str,
    step: str,
    status: str,
    message: str
    ):
        """
        Insert workflow log.
        """

        timestamp = datetime.now().isoformat()

        query = """
        INSERT INTO workflow_logs
        (
            run_id,
            timestamp,
            step,
            status,
            message
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
    """

        self.execute(

        query,

        (

            run_id,

            timestamp,

            step,

            status,

            message

        )

    )

        logger.info(

        f"[{step}] {status} : {message}"

        )

    # -------------------------------------------------------------------------

    def insert_metrics(
    self,
    run_id: str,
    mae: float,
    rmse: float,
    r2: float,
    psi: float
    ):
        """
        Store model evaluation metrics.
        """

        query = """
        INSERT INTO metrics
        (
            run_id,
            mae,
            rmse,
            r2,
            psi
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
    """

        self.execute(

        query,

        (

            run_id,

            float(mae),

            float(rmse),

            float(r2),

            float(psi)

        )

    )

        logger.info(
        f"Metrics inserted for {run_id}"
        )

    # -------------------------------------------------------------------------

    def insert_diagnosis(
    self,
    run_id: str,
    severity: str,
    root_cause: str,
    recommendation: str,
    gemini_response: str
    ):
        """
        Store Gemini diagnosis.
        """

        query = """
        INSERT INTO diagnosis
        (
            run_id,
            severity,
            root_cause,
            recommendation,
            gemini_response
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
    """

        self.execute(

        query,

        (

            run_id,

            severity,

            root_cause,

            recommendation,

            gemini_response

        )

        )

        logger.info(
        f"Diagnosis inserted for {run_id}"
    )
        
    # -------------------------------------------------------------------------

    def insert_recovery(
    self,
    run_id: str,
    strategy: str,
    status: str,
    retraining_required: bool,
    model_version: int
):
        """
        Store recovery information.
        """

        query = """
        INSERT INTO recovery
        (
            run_id,
            strategy,
            status,
            retraining_required,
            model_version
        )
        VALUES
        (
            ?, ?, ?, ?, ?
        )
    """

        self.execute(

        query,

        (

            run_id,

            strategy,

            status,

            int(retraining_required),

            model_version

        )

    )

        logger.info(
        f"Recovery inserted for {run_id}"
    )
        
    # -------------------------------------------------------------------------

    def register_model(
    self,
    model_version: int,
    training_date: str,
    dataset_name: str,
    mae: float,
    rmse: float,
    r2: float,
    model_path: str
):
        """
        Register a trained model.
        """

        query = """
        INSERT INTO model_registry
        (
            model_version,
            training_date,
            dataset_name,
            mae,
            rmse,
            r2,
            model_path
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?
        )
    """

        self.execute(

        query,

        (

            model_version,

            training_date,

            dataset_name,

            mae,

            rmse,

            r2,

            model_path

        )

    )

        logger.info(
        f"Model Version {model_version} registered."
    )
        
    # -------------------------------------------------------------------------

    def get_pipeline_history(self):
        """
        Return all pipeline runs.
        """

        query = """

        SELECT *

        FROM pipeline_runs

        ORDER BY start_time DESC

        """

        return self.fetch_all(query)
    
    # -------------------------------------------------------------------------

    def get_pipeline_run(
    self,
    run_id: str
):
        """
        Return one pipeline run.
        """

        query = """

        SELECT *

        FROM pipeline_runs

        WHERE run_id = ?

        """

        return self.fetch_one(

        query,

        (

            run_id,

        )

    )

    # -------------------------------------------------------------------------

    def get_metrics(
    self,
    run_id: str
    ):
        """
        Return metrics for one run.
        """

        query = """

        SELECT *

        FROM metrics

        WHERE run_id = ?

        """

        return self.fetch_one(

        query,

        (

            run_id,

        )

    )

    # -------------------------------------------------------------------------

    def get_diagnosis(
    self,
    run_id: str
):
        """
        Return diagnosis.
        """

        query = """

        SELECT *

        FROM diagnosis

        WHERE run_id = ?

        """

        return self.fetch_one(

        query,

        (

            run_id,

        )

    )

    # -------------------------------------------------------------------------

    def get_recovery(
    self,
    run_id: str
    ):
        """
        Return recovery information.
        """

        query = """

        SELECT *

        FROM recovery

        WHERE run_id = ?

        """

        return self.fetch_one(

        query,

        (

            run_id,

        )

    )

    # -------------------------------------------------------------------------

    def get_logs(
    self,
    run_id: str
):
        """
        Return workflow logs.
        """

        query = """

        SELECT *

        FROM workflow_logs

        WHERE run_id = ?

        ORDER BY timestamp

        """

        return self.fetch_all(

        query,

        (

            run_id,

        )

    )
    # -------------------------------------------------------------------------

    def get_latest_model(self):
        """
        Return latest registered model.
        """

        query = """

        SELECT *

        FROM model_registry

        ORDER BY model_version DESC

        LIMIT 1

        """

        return self.fetch_one(query)
    
    # -------------------------------------------------------------------------

    def delete_pipeline_run(
    self,
    run_id: str
    ):
        """
        Delete an entire pipeline run.
        """

        tables = [

        "workflow_logs",

        "recovery",

        "diagnosis",

        "metrics",

        "pipeline_runs"

        ]

        for table in tables:

            query = f"""

            DELETE FROM {table}

            WHERE run_id = ?

            """

            self.execute(

            query,

            (

                run_id,

            )

        )

        logger.info(

        f"Pipeline Run Deleted : {run_id}"

    )
# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from datetime import datetime

    database = SQLiteManager()

    run_id = database.start_pipeline_run(

        "sales_normal.xlsx"

    )

    database.insert_log(

        run_id,

        "Validation",

        "Completed",

        "Validation successful."

    )

    database.insert_metrics(

        run_id,

        11.8,

        15.2,

        0.95,

        0.04

    )

    database.insert_diagnosis(

        run_id,

        "Low",

        "No issue detected.",

        "No action required.",

        "Pipeline healthy."

    )

    database.insert_recovery(

        run_id,

        "None",

        "Completed",

        False,

        1

    )

    database.register_model(

        model_version=1,

        training_date=datetime.now().isoformat(),

        dataset_name="sales_normal.xlsx",

        mae=11.8,

        rmse=15.2,

        r2=0.95,

        model_path="models/saved_models/sales_forecaster.pkl"

    )

    database.finish_pipeline_run(run_id)

    print("\nPipeline History\n")

    history = database.get_pipeline_history()

    for row in history:

        print(dict(row))

    print("\nLatest Model\n")

    latest = database.get_latest_model()

    print(dict(latest))

    print("\nWorkflow Logs\n")

    logs = database.get_logs(run_id)

    for log in logs:

        print(dict(log))

    database.close()