from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "synthetic_pet_adoption.csv"


@dataclass(frozen=True)
class AdoptionCase:
    case_id: str
    hours_away: int
    activity_level: str
    housing_type: str
    pet_type: str
    pet_energy_level: str
    mismatch_risk: str


def score_case(case: AdoptionCase) -> tuple[int, str, list[str], list[str]]:
    score = 0
    reasons: list[str] = []
    guidance: list[str] = []

    if case.hours_away >= 8:
        score += 3
        reasons.append("The adopter is away from home for long periods.")
        guidance.append("Reduce time away or arrange more daily pet support.")
    elif case.hours_away >= 6:
        score += 1
        reasons.append("Time away is moderately high.")

    if case.pet_energy_level == "high" and case.activity_level == "low":
        score += 4
        reasons.append("A high-energy pet is paired with a low-activity lifestyle.")
        guidance.append("Choose a lower-energy pet or commit to a more active routine.")
    elif case.pet_energy_level == "high" and case.activity_level == "medium":
        score += 2
        reasons.append("A high-energy pet may need more activity than the adopter currently reports.")

    if case.housing_type == "apartment" and case.pet_type == "dog" and case.pet_energy_level == "high":
        score += 3
        reasons.append("A high-energy dog in an apartment increases mismatch risk.")
        guidance.append("Consider a lower-energy pet or a setup with easier outdoor access.")

    if case.pet_type == "dog" and case.hours_away >= 6:
        score += 2
        reasons.append("Dogs usually require more daily interaction and routine care.")

    if case.activity_level == "high" and case.pet_energy_level == "low":
        score -= 1
        reasons.append("The adopter activity level is supportive of routine pet engagement.")

    score = max(score, 0)
    risk = "high" if score >= 5 else "low"

    if not guidance:
        guidance.append("Current lifestyle and pet needs appear reasonably aligned.")

    return score, risk, reasons, deduplicate(guidance)


def deduplicate(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def load_cases() -> list[AdoptionCase]:
    cases: list[AdoptionCase] = []
    with DATA_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cases.append(
                AdoptionCase(
                    case_id=row["case_id"],
                    hours_away=int(row["hours_away"]),
                    activity_level=row["activity_level"],
                    housing_type=row["housing_type"],
                    pet_type=row["pet_type"],
                    pet_energy_level=row["pet_energy_level"],
                    mismatch_risk=row["mismatch_risk"],
                )
            )
    return cases


def evaluate_cases(cases: list[AdoptionCase]) -> dict[str, int]:
    summary = {
        "total": 0,
        "correct": 0,
        "predicted_high": 0,
        "actual_high": 0,
        "true_positive": 0,
        "false_negative": 0,
    }

    for case in cases:
        _, predicted, _, _ = score_case(case)
        actual_high = case.mismatch_risk == "high"
        predicted_high = predicted == "high"

        summary["total"] += 1
        summary["correct"] += int(predicted == case.mismatch_risk)
        summary["predicted_high"] += int(predicted_high)
        summary["actual_high"] += int(actual_high)
        summary["true_positive"] += int(actual_high and predicted_high)
        summary["false_negative"] += int(actual_high and not predicted_high)

    return summary


def print_demo(cases: list[AdoptionCase]) -> None:
    print("Pet Adoption Risk Decision System")
    print("=" * 34)

    summary = evaluate_cases(cases)
    accuracy = summary["correct"] / summary["total"]
    recall = (
        summary["true_positive"] / summary["actual_high"]
        if summary["actual_high"]
        else 0.0
    )

    print(f"Cases evaluated: {summary['total']}")
    print(f"Rule alignment with synthetic labels: {accuracy:.0%}")
    print(f"High-risk recall: {recall:.0%}")
    print(f"False negatives: {summary['false_negative']}")
    print()
    print("Example Cases")
    print("-" * 13)

    for case in cases[:3]:
        score, risk, reasons, guidance = score_case(case)
        print(f"{case.case_id}: score={score}, predicted_risk={risk}, actual_risk={case.mismatch_risk}")
        print(f"  Profile: hours_away={case.hours_away}, activity={case.activity_level}, housing={case.housing_type}, pet={case.pet_type}, pet_energy={case.pet_energy_level}")
        print(f"  Why: {' | '.join(reasons)}")
        print(f"  Guidance: {' | '.join(guidance)}")
        print()


if __name__ == "__main__":
    print_demo(load_cases())
