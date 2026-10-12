"""Create reproducible hospitality booking summaries from locally obtained CSV data."""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "datasets"
OUTPUT = ROOT / "outputs"


def load_table(filename: str, required: set[str]) -> pd.DataFrame:
    path = DATA / filename
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing {path.name}. Download the hospitality learning data from the "
            "official Codebasics resource and place the CSV in the local datasets/ folder."
        )
    frame = pd.read_csv(path)
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{filename} is missing required columns: {', '.join(sorted(missing))}")
    return frame


def save_summary(name: str, frame: pd.DataFrame) -> None:
    target = OUTPUT / f"{name}.csv"
    frame.to_csv(target, index=False)
    print(f"\n{name.replace('_', ' ').title()}\n{frame.to_string(index=False)}")


def main() -> int:
    hotels = load_table("dim_hotels.csv", {"property_id", "property_name", "category", "city"})
    rooms = load_table("dim_rooms.csv", {"room_id", "room_class"})
    dates = load_table("dim_date.csv", {"date", "mmm yy", "day_type"})
    occupancy = load_table(
        "fact_aggregated_bookings.csv",
        {"property_id", "check_in_date", "room_category", "successful_bookings", "capacity"},
    )
    bookings = load_table(
        "fact_bookings.csv",
        {"property_id", "check_in_date", "no_guests", "booking_platform", "revenue_realized"},
    )

    OUTPUT.mkdir(exist_ok=True)

    # Keep questionable capacity rows visible as a quality summary, rather than silently dropping them.
    occupancy["capacity"] = pd.to_numeric(occupancy["capacity"], errors="coerce")
    occupancy["successful_bookings"] = pd.to_numeric(occupancy["successful_bookings"], errors="coerce")
    quality = pd.DataFrame(
        [{
            "rows": len(occupancy),
            "missing_capacity": int(occupancy["capacity"].isna().sum()),
            "zero_or_negative_capacity": int(occupancy["capacity"].le(0).sum()),
            "bookings_over_capacity": int((occupancy["successful_bookings"] > occupancy["capacity"]).sum()),
        }]
    )
    save_summary("data_quality", quality)

    usable = occupancy.loc[occupancy["capacity"].gt(0)].copy()
    usable["occupancy_pct"] = 100 * usable["successful_bookings"] / usable["capacity"]
    hotel_occupancy = usable.merge(rooms, left_on="room_category", right_on="room_id", how="left", validate="many_to_one")
    hotel_occupancy = hotel_occupancy.merge(hotels, on="property_id", how="left", validate="many_to_one")

    by_room = hotel_occupancy.groupby("room_class", dropna=False)["occupancy_pct"].mean().reset_index()
    save_summary("occupancy_by_room_class", by_room.sort_values("occupancy_pct", ascending=False))

    by_city = hotel_occupancy.groupby("city", dropna=False)["occupancy_pct"].mean().reset_index()
    save_summary("occupancy_by_city", by_city.sort_values("occupancy_pct", ascending=False))

    date_lookup = dates[["date", "mmm yy", "day_type"]].copy()
    date_lookup["date"] = pd.to_datetime(date_lookup["date"], dayfirst=True, errors="coerce")
    hotel_occupancy["check_in_date"] = pd.to_datetime(hotel_occupancy["check_in_date"], dayfirst=True, errors="coerce")
    with_dates = hotel_occupancy.merge(date_lookup, left_on="check_in_date", right_on="date", how="left")

    by_day_type = with_dates.groupby("day_type", dropna=False)["occupancy_pct"].mean().reset_index()
    save_summary("occupancy_by_day_type", by_day_type)

    june = with_dates.loc[with_dates["check_in_date"].dt.month.eq(6)]
    june_by_city = june.groupby("city", dropna=False)["occupancy_pct"].mean().reset_index()
    save_summary("june_occupancy_by_city", june_by_city.sort_values("occupancy_pct", ascending=False))

    bookings["no_guests"] = pd.to_numeric(bookings["no_guests"], errors="coerce")
    bookings["revenue_realized"] = pd.to_numeric(bookings["revenue_realized"], errors="coerce")
    valid_bookings = bookings.loc[bookings["no_guests"].gt(0)].copy()
    booking_detail = valid_bookings.merge(hotels, on="property_id", how="left", validate="many_to_one")

    revenue_by_city = booking_detail.groupby("city", dropna=False)["revenue_realized"].sum().reset_index()
    save_summary("revenue_by_city", revenue_by_city.sort_values("revenue_realized", ascending=False))

    revenue_by_platform = booking_detail.groupby("booking_platform", dropna=False)["revenue_realized"].sum().reset_index()
    save_summary("revenue_by_booking_platform", revenue_by_platform.sort_values("revenue_realized", ascending=False))

    booking_detail["check_in_date"] = pd.to_datetime(booking_detail["check_in_date"], dayfirst=True, errors="coerce")
    booking_detail["month"] = booking_detail["check_in_date"].dt.to_period("M").astype("string")
    revenue_by_month = booking_detail.groupby("month", dropna=False)["revenue_realized"].sum().reset_index()
    save_summary("revenue_by_month", revenue_by_month.sort_values("month"))

    print(f"\nSaved summary tables in {OUTPUT}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError) as error:
        print(f"Data setup error: {error}", file=sys.stderr)
        raise SystemExit(1)
