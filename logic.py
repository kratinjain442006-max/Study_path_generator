"""Study planning logic for StudyPathAI."""
from datetime import datetime, timedelta


def generate_study_plan(subjects, marks, hours):
    """Allocate available hours according to each subject's need.

    Lower marks receive a higher weight. The final allocation is normalized so
    the sum of planned subject hours equals the user's available daily hours.
    """
    if len(subjects) != len(marks):
        raise ValueError("Subjects and marks must have the same length.")
    if not subjects:
        raise ValueError("At least one subject is required.")
    if hours <= 0:
        raise ValueError("Study hours must be greater than zero.")
    if any(mark < 0 or mark > 100 for mark in marks):
        raise ValueError("Marks must be between 0 and 100.")

    plan = []
    weights = []
    for mark in marks:
        if mark < 50:
            weights.append(3)
        elif mark < 75:
            weights.append(2)
        else:
            weights.append(1)

    total_weight = sum(weights)
    for subject, mark, weight in zip(subjects, marks, weights):
        allocated = round(float(hours) * weight / total_weight, 2)
        if mark < 50:
            priority = "High"
            suggestion = "Focus on core concepts, then solve practice questions."
        elif mark < 75:
            priority = "Medium"
            suggestion = "Practice questions and review mistakes to strengthen understanding."
        else:
            priority = "Low"
            suggestion = "Revise key concepts and solve a short set of exam-style questions."

        plan.append({
            "subject": subject,
            "marks": float(mark),
            "priority": priority,
            "weight": weight,
            "time": allocated,
            "suggestion": suggestion,
        })

    # Adjust rounding difference on the highest-priority subject, so total
    # allocation matches the requested daily hours to two decimal places.
    difference = round(float(hours) - sum(item["time"] for item in plan), 2)
    if plan and difference:
        target = next((item for item in plan if item["priority"] == "High"), plan[0])
        target["time"] = round(target["time"] + difference, 2)

    return sorted(plan, key=lambda item: (item["weight"] * -1, item["marks"]))


def _format_time(total_minutes):
    total_minutes = int(round(total_minutes))
    hour = (total_minutes // 60) % 24
    minute = total_minutes % 60
    return f"{hour:02d}:{minute:02d}"


def build_daily_timetable(plan, start_hour=8):
    """Create a continuous timetable with accurate minute-level durations."""
    current_minutes = int(start_hour) * 60
    timetable = []
    for item in plan:
        duration = max(1, int(round(float(item["time"]) * 60)))
        start = _format_time(current_minutes)
        current_minutes += duration
        end = _format_time(current_minutes)
        timetable.append({
            "subject": item["subject"],
            "start": start,
            "end": end,
            "hours": float(item["time"]),
            "minutes": duration,
        })
    return timetable
