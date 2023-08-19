import dataclasses
from enum import Enum
from typing import Optional, TypedDict


@dataclasses.dataclass
class AccountBorrowRequest:
    asset: str
    amount: str
    isIsolated: Optional[bool] = False
    symbol: str = ""

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        if self.isIsolated:
            as_dict["isIsolated"] = "TRUE" if self.isIsolated else "FALSE"
        else:
            del as_dict["symbol"]
        return as_dict
