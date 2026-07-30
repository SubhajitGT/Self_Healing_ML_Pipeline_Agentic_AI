"""
===============================================================================
Project : Self-Healing Agentic AI ML Pipeline

File    : history_manager.py

Purpose :
Maintain self-healing execution history.

Author  : ChatGPT
===============================================================================
"""
from  __future__ import annotations

import sys
import json
import sqlite3
import logging

from pathlib import Path
from typing import Dict

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

logger = logging.getLogger("HistoryManager")

logger.setLevel(config.LOG_LEVEL)

formatter = logging.Formatter(config.LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)

# ==============================================================================
# History Manager
# ==============================================================================


class HistoryManager:

    """
    Maintain self-healing execution history.
    """

    # -------------------------------------------------------------------------

    def __init__(self):

        self.database = str(config.SQLITE_DB_PATH)

        self.create_table()

    # -------------------------------------------------------------------------

    def connect(self):

        return sqlite3.connect(

            self.database

        )

    # -------------------------------------------------------------------------

    def create_table(self):

        logger.info(

            "Creating self-healing history table..."

        )

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS self_healing_history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT,

                action TEXT,

                promoted INTEGER,

                old_version INTEGER,

                new_version INTEGER,

                severity TEXT,

                reason TEXT,

                candidate_metrics TEXT,

                production_metrics TEXT

            )
            """
        )

        connection.commit()

        connection.close()

        logger.info(

            "History table ready."

        )

    # -------------------------------------------------------------------------
        
    # -------------------------------------------------------------------------

    def save_execution(
        self,
        execution: Dict
    ):
        """
        Save one self-healing execution into SQLite.
        """

        logger.info(
            "Saving execution history..."
        )

        required_keys = {

    "timestamp",

    "decision",

    "promoted",

    "old_version",

    "new_version"

}

        missing = required_keys - execution.keys()

        if missing:

            raise ValueError(

        f"Execution missing keys: {missing}"

    )
        connection = self.connect()

        cursor = connection.cursor()

        decision = execution.get("decision", {})

        cursor.execute(
            """
            INSERT INTO self_healing_history
            (
                timestamp,
                action,
                promoted,
                old_version,
                new_version,
                severity,
                reason,
                candidate_metrics,
                production_metrics
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                execution.get("timestamp"),

                decision.get("action"),

                int(execution.get("promoted", False)),

                execution.get("old_version"),

                execution.get("new_version"),

                decision.get("severity"),

                decision.get("reason"),

                json.dumps(
                    execution.get("candidate_metrics", {})
                ),

                json.dumps(
                    execution.get("production_metrics", {})
                )
            )
        )

        connection.commit()

        connection.close()

        logger.info(
            "Execution history saved."
        )

    def get_history(self):
        """
        Return complete execution history.
        """

        logger.info(

            "Loading execution history..."

        )

        connection = self.connect()

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM self_healing_history

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        connection.close()

        history = [

            dict(row)

            for row in rows

        ]

        for record in history:

            record["candidate_metrics"] = json.loads(
            record["candidate_metrics"]
    )

            record["production_metrics"] = json.loads(
            record["production_metrics"]
    )
        return history
    
    # -------------------------------------------------------------------------

    def get_latest_execution(self):
        """
        Return latest execution.
        """

        history = self.get_history()

        if len(history) == 0:

            return None

        return history[0]
    
    # -------------------------------------------------------------------------

    def clear_history(self):
        """
        Delete all execution history.
        """

        logger.info(

            "Clearing execution history..."

        )

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(

            "DELETE FROM self_healing_history"

        )

        connection.commit()

        connection.close()

        logger.info(

            "History cleared."

        )

# ==============================================================================
# Standalone Testing
# ==============================================================================

if __name__ == "__main__":

    from datetime import datetime

    print("=" * 70)
    print("HISTORY MANAGER TEST")
    print("=" * 70)

    try:

        manager = HistoryManager()

        sample_execution = {

            "timestamp":

                datetime.now().isoformat(),

            "decision": {

                "action": "RETRAIN",

                "severity": "HIGH",

                "reason": "Gemini recommended retraining."

            },

            "promoted": True,

            "old_version": 1,

            "new_version": 2,

            "candidate_metrics": {

                "mae": 14.3,

                "rmse": 20.8,

                "r2": 0.95

            },

            "production_metrics": {

                "mae": 18.1,

                "rmse": 24.5,

                "r2": 0.90

            }

        }

        # ---------------------------------------------------------
        # Save Execution
        # ---------------------------------------------------------

        manager.save_execution(

            sample_execution

        )

        # ---------------------------------------------------------
        # Latest Execution
        # ---------------------------------------------------------

        latest = manager.get_latest_execution()

        print()

        print("=" * 70)
        print("LATEST EXECUTION")
        print("=" * 70)

        print(

            "Action      :",

            latest["action"]

        )

        print(

            "Severity    :",

            latest["severity"]

        )

        print(

            "Promoted    :",

            bool(latest["promoted"])

        )

        print(

            "Old Version :",

            latest["old_version"]

        )

        print(

            "New Version :",

            latest["new_version"]

        )

        print()

        print("=" * 70)
        print("TOTAL HISTORY")
        print("=" * 70)

        history = manager.get_history()

        print(

            "Total Records :",

            len(history)

        )

        print()

        print("=" * 70)
        print("HISTORY MANAGER TEST PASSED")
        print("=" * 70)

    except Exception as error:

        logger.exception(error)

        print()

        print("=" * 70)
        print("HISTORY MANAGER TEST FAILED")
        print("=" * 70)

        print(error)