from mcp.server.fastmcp import FastMCP
from typing import TypedDict
from datetime import datetime, date
import calendar
import re

mcp = FastMCP("my_mcp_server")


# @mcp.tool()
# async def get_current_time() -> str:
#     """Get the current time as a string."""
#     return datetime.now().isoformat()


class DateDiff(TypedDict):
    years: int
    months: int
    days: int


@mcp.tool()
async def date_diff(start_date: str, end_date: str) -> DateDiff:
    """Get calendar difference between two dates.

    Inputs:
      - start_date: ISO-8601 date or datetime string (e.g. "2024-01-31", "2024-01-31T23:45:00Z").
      - end_date: ISO-8601 date or datetime string (same accepted formats). Also supports common
        alternatives like "YYYY/MM/DD", "MM/DD/YYYY", or "DD-MM-YYYY".

    Behavior:
      - Returns a human calendar difference in years, months, and days (absolute; order-insensitive).
      - If end_date is earlier than start_date, dates are swapped and the positive difference is returned.

    Returns:
      - {"years": int, "months": int, "days": int}
    """

    def _parse_to_date(value: str) -> date:
        v = value.strip()
        # Normalize Zulu timezone to RFC 3339 offset for fromisoformat
        v = v.replace("Z", "+00:00")

        # Try date-only ISO first
        try:
            return date.fromisoformat(v)
        except Exception:
            pass

        # Try full ISO datetime
        try:
            dt = datetime.fromisoformat(v)
            return dt.date()
        except Exception:
            pass

        # Try common alternative formats
        for fmt in ("%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y", "%d-%m-%Y", "%m-%d-%Y"):
            try:
                return datetime.strptime(v, fmt).date()
            except Exception:
                continue

        # Fallback: extract a YYYY-MM-DD substring if present
        m = re.search(r"\d{4}-\d{2}-\d{2}", v)
        if m:
            return date.fromisoformat(m.group(0))

        raise ValueError(f"Unrecognized date format: {value}")

    d1 = _parse_to_date(start_date)
    d2 = _parse_to_date(end_date)

    # Ensure d1 <= d2 for absolute difference
    if d2 < d1:
        d1, d2 = d2, d1

    years = d2.year - d1.year
    months = d2.month - d1.month
    days = d2.day - d1.day

    if days < 0:
        # Borrow from months; use the number of days in the month preceding d2
        months -= 1
        prev_month = d2.month - 1
        prev_year = d2.year
        if prev_month == 0:
            prev_month = 12
            prev_year -= 1
        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month

    if months < 0:
        months += 12
        years -= 1

    return {"years": years, "months": months, "days": days}

if __name__ == "__main__":
    mcp.run(transport='stdio')
