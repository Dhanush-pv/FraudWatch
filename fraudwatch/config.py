import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    seed: int = int(os.getenv("FRAUDWATCH_SEED", "42"))
    transaction_count: int = int(os.getenv("FRAUDWATCH_TRANSACTIONS", "10000"))
    output_dir: str = os.getenv("FRAUDWATCH_OUTPUT", "data/generated")

settings = Settings()
