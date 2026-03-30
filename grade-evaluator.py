import csv
import sys
import os


def load_csv_data():
    filename = "grades.csv"

    if not os.path.exists(filename):
        print("File not found")
        sys.exit()

    assignments = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            assignments.append({
                "assignment": row["assignment"],
                "group": row["group"],
                "score": float(row["score"]),
                "weight": float(row["weight"])
            })

    return assignments



def evaluate_grades(data):
    print("\n--- Processing Grades ---")

    if not data:
        print("Error: CSV file is empty.")
        return

    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    formative_total = 0
    summative_total = 0

    failed_formative = []

    print("\nAssignments and Calculations:")

    for item in data:
        name = item['assignment']
        group = item['group']
        score = item['score']
        weight = item['weight']

        # Grade validation
        if score < 0 or score > 100:
            print(f"Invalid score in {name}")
            return

        weighted_score = score * (weight / 100)

        print(f"{name} | Group: {group} | Score: {score} | Weight: {weight}")
        print(f"Weighted Score = {score} * ({weight}/100) = {weighted_score}\n")

        total_weight += weight

        if group.lower() == "formative":
            formative_weight += weight
            formative_total += weighted_score

            if score < 50:
                failed_formative.append(item)

        elif group.lower() == "summative":
            summative_weight += weight
            summative_total += weighted_score

    print("\n--- Weight Validation ---")
    print("Total Weight:", total_weight)
    print("Formative Weight:", formative_weight)
    print("Summative Weight:", summative_weight)

    if total_weight != 100:
        print("Error: Total weight must equal 100")
        return

    if formative_weight != 60:
        print("Error: Formative weight must equal 60")
        return

    if summative_weight != 40:
        print("Error: Summative weight must equal 40")
        return

    print("\n--- Category Totals ---")
    print("Formative Total:", formative_total)
    print("Summative Total:", summative_total)

    total_grade = formative_total + summative_total
    print("\nFinal Grade:", total_grade)

    gpa = (total_grade / 100) * 5.0
    print("GPA Calculation:")
    print(f"GPA = ({total_grade}/100) * 5 = {gpa}")

    formative_percent = (formative_total / formative_weight) * 100
    summative_percent = (summative_total / summative_weight) * 100

    print("\nFormative Percentage:", formative_percent)
    print("Summative Percentage:", summative_percent)

    print("\n--- Final Decision ---")
    if formative_percent >= 50 and summative_percent >= 50:
        print("Status: PASSED")
    else:
        print("Status: FAILED")

    print("\n--- Resubmission Check ---")
    if failed_formative:
        max_weight = max(a['weight'] for a in failed_formative)
        resubmit = [a for a in failed_formative if a['weight'] == max_weight]

        print("Eligible assignments for resubmission:")
        for a in resubmit:
            print(a['assignment'], "| Weight:", a['weight'])
    else:
        print("No resubmission required.")

if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
