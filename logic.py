def generate_study_plan(subjects, marks, hours):
    plan = []

    for sub, mark in zip(subjects, marks):

        # Weakness analysis
        if mark < 50:
            priority = "High"
            time = hours * 0.4
        elif mark < 75:
            priority = "Medium"
            time = hours * 0.3
        else:
            priority = "Low"
            time = hours * 0.2

        plan.append({
            "subject": sub,
            "marks": mark,
            "priority": priority,
            "time": round(time, 2)
        })

    # Sort by priority
    plan = sorted(plan, key=lambda x: x["marks"])

    return plan 