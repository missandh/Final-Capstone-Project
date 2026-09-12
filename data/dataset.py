import json
import random

SEED = 42
TOTAL_RECORDS = 50

CATEGORIES = [
    "General Medicine", "Cardiology", "Dermatology", "Pediatrics", "Orthopedics"
]
STATUSES = [
    "Scheduled", "Completed", "Cancelled", "No-Show", "Rescheduled"
]

FEE_RANGES = {
    "General Medicine": (400, 700),
    "Pediatrics": (500, 800),
    "Dermatology": (700, 1200),
    "Cardiology": (1000, 1600),
    "Orthopedics": (800, 1400),
}


def generate_appointments(seed=SEED, count=TOTAL_RECORDS):
    random.seed(seed)
    records = []

    for cat in CATEGORIES:
        for _ in range(3):
            records.append({"category": cat})
    for st in STATUSES:
        if not any(r.get("status") == st for r in records):
            records.append({"status": st})

    while len(records) < count:
        records.append({})

    final_dataset = []
    follow_up_count = 0

    for idx, r in enumerate(records):
        cat = r.get("category", random.choice(CATEGORIES))
        st = r.get("status", random.choices(STATUSES, weights=[0.4, 0.3, 0.1, 0.1, 0.1])[0])
        fee_min, fee_max = FEE_RANGES[cat]
        fee = round(random.randint(fee_min, fee_max) / 50) * 50
        days = random.randint(0, 30)

        if st == "Completed" and days > 3:
            follow_up = random.random() < 0.38
        else:
            follow_up = random.random() < 0.10

        if follow_up:
            follow_up_count += 1

        final_dataset.append({
            "record_id": f"PRAC-{1000 + idx}",
            "category": cat,
            "status": st,
            "consultation_fee_inr": fee,
            "days_since_created": days,
            "follow_up_required": follow_up,
        })

    return final_dataset


if __name__ == "__main__":
    data = generate_appointments()
    with open("data/appointments.json", "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)

    cat_counts = {c: sum(1 for d in data if d["category"] == c) for c in CATEGORIES}
    st_counts = {s: sum(1 for d in data if d["status"] == s) for s in STATUSES}
    fu_pct = (sum(1 for d in data if d["follow_up_required"]) / len(data)) * 100

    print(f"Total: {len(data)}")
    print(f"Category counts: {cat_counts}")
    print(f"Status counts: {st_counts}")
    print(f"Follow-up Required: {fu_pct:.2f}% (Within 10-30% boundary: {10 <= fu_pct <= 30})")
