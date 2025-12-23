"""Helper script to exercise DB actions from the CLI."""

import sys
from pathlib import Path

# Ensure project root is on sys.path when running the file directly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from db.client import get_supabase_client


class Db_action:
    def __init__(self):
        self.supabase = get_supabase_client()

    def create_problem(self, problem):
        response = (
            self.supabase.table("testing")
            .insert(problem)
            .execute()
        )
        print(response)
