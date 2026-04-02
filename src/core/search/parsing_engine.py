import re
import pandas as pd
from typing import Dict


class ParserEngine:
    def __init__(self, patterns: Dict[str, str]):
        self.patterns = {
            name: re.compile(p, re.MULTILINE)
            for name, p in patterns.items()
        }

    def parse(self, blocks: list[str]) -> pd.DataFrame:
        results = []

        for block in blocks:
            for name, pattern in self.patterns.items():
                if pattern.search(block):
                    results.append({
                        "message": self._extract_main(block),
                        "raw": block
                    })

        return pd.DataFrame(results)

    def _extract_main(self, block: str) -> str:
        return block.splitlines()[0] if block else ""