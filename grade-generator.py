#!/usr/bin/env python3

"""
Interactive grade calculator that captures assignment data, outputs a formatted
summary, and writes the entries to grades.csv.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, asdict


@dataclass
class Assignment:
    name: str
    category: str  # 'FA' or 'SA'
    grade: float   # 0-100
    weight: float  # > 0

    @property
    def weighted_grade(self) -> float:
        return (self.grade / 100.0) * self.weight


def prompt_non_empty(prompt_text: str) -> str:
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Value cannot be empty.")


def prompt_category() -> str:
    while True:
        category = input("Category (FA/SA): ").strip().upper()
        if category in {"FA", "SA"}:
            return category
        print("Category must be 'FA' or 'SA'")


def prompt_grade() -> float:
    while True:
        raw = input("Grade (0-100): ").strip()
        try:
            grade = float(raw)
        except ValueError:
            print("Grade must be between 0 and 100")
            continue

        if 0 <= grade <= 100:
            return grade
        print("Grade must be between 0 and 100")


def prompt_weight() -> float:
    while True:
        raw = input("Weight (> 0): ").strip()
        try:
            weight = float(raw)
        except ValueError:
            print("Weight must be a positive number")
            continue

        if weight > 0:
            return weight
        print("Weight must be a positive number")


def prompt_continue() -> bool:
    while True:
        response = input("Add another assignment? (y/n): ").strip().lower()
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def collect_assignments() -> list[Assignment]:
    assignments: list[Assignment] = []
    while True:
        print("\nEnter assignment details:")
        name = prompt_non_empty("Assignment Name: ")
        category = prompt_category()
        grade = prompt_grade()
        weight = prompt_weight()

        assignments.append(Assignment(name=name, category=category, grade=grade, weight=weight))

        if not prompt_continue():
            break
    return assignments


def calculate_totals(assignments: list[Assignment]) -> dict[str, float | bool]:
    total_formative = sum(a.weighted_grade for a in assignments if a.category == "FA")
    total_summative = sum(a.weighted_grade for a in assignments if a.category == "SA")
    total_fa_weight = sum(a.weight for a in assignments if a.category == "FA")
    total_sa_weight = sum(a.weight for a in assignments if a.category == "SA")

    final_grade = total_formative + total_summative
    gpa = (final_grade / 100.0) * 5.0

    fa_threshold = total_fa_weight * 0.5
    sa_threshold = total_sa_weight * 0.5
    passes = (total_formative >= fa_threshold if total_fa_weight > 0 else True) and (
        total_summative >= sa_threshold if total_sa_weight > 0 else True
    )

    return {
        "total_formative": total_formative,
        "total_summative": total_summative,
        "total_fa_weight": total_fa_weight,
        "total_sa_weight": total_sa_weight,
        "final_grade": final_grade,
        "gpa": gpa,
        "fa_threshold": fa_threshold,
        "sa_threshold": sa_threshold,
        "passes": passes,
    }


def format_percentage(value: float, total_weight: float) -> float:
    if total_weight <= 0:
        return 0.0
    return (value / total_weight) * 100.0


def print_summary(assignments: list[Assignment], totals: dict[str, float | bool]) -> None:
    total_formative = totals["total_formative"]
    total_summative = totals["total_summative"]
    total_fa_weight = totals["total_fa_weight"]
    total_sa_weight = totals["total_sa_weight"]
    fa_threshold = totals["fa_threshold"]
    sa_threshold = totals["sa_threshold"]
    final_grade = totals["final_grade"]
    gpa = totals["gpa"]
    passes = totals["passes"]

    print("\n=== GRADE SUMMARY ===\n")
    print("Assignments Entered:")
    for idx, assignment in enumerate(assignments, start=1):
        print(
            f"{idx}. {assignment.name} ({assignment.category}): "
            f"{assignment.grade:.2f}% - Weight: {assignment.weight:.2f} - "
            f"Weighted: {assignment.weighted_grade:.2f}"
        )

    print("\nCategory Breakdown:")
    fa_percentage = format_percentage(total_formative, total_fa_weight)
    sa_percentage = format_percentage(total_summative, total_sa_weight)

    print(
        f"- Total Formative (FA): {total_formative:.2f}/{total_fa_weight:.2f} "
        f"({fa_percentage:.2f}%)"
    )
    print(
        f"- Total Summative (SA): {total_summative:.2f}/{total_sa_weight:.2f} "
        f"({sa_percentage:.2f}%)"
    )

    print("\nFinal Results:")
    print(f"- Total Grade: {final_grade:.2f}/100")
    print(f"- GPA: {gpa:.2f}/5.0")
    print(f"- Status: {'PASS' if passes else 'FAIL'}")

    if not passes:
        if total_fa_weight > 0 and total_formative < fa_threshold:
            print(
                f"Failed FA (achieved {total_formative:.2f} / need {fa_threshold:.2f})"
            )
        if total_sa_weight > 0 and total_summative < sa_threshold:
            print(
                f"Failed SA (achieved {total_summative:.2f} / need {sa_threshold:.2f})"
            )


def write_csv(assignments: list[Assignment], filename: str = "grades.csv") -> None:
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Assignment", "Category", "Grade", "Weight"])
        writer.writeheader()
        for assignment in assignments:
            writer.writerow(
                {
                    "Assignment": assignment.name,
                    "Category": assignment.category,
                    "Grade": f"{assignment.grade:.2f}",
                    "Weight": f"{assignment.weight:.2f}",
                }
            )


def main() -> None:
    assignments = collect_assignments()
    if not assignments:
        print("No assignments entered. Exiting without generating summary.")
        return

    totals = calculate_totals(assignments)
    print_summary(assignments, totals)
    write_csv(assignments)
    print("\nData saved to grades.csv")


if __name__ == "__main__":
    main()

