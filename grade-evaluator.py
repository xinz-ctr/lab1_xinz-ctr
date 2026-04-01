# Import required modules
import csv
import sys
import os

#Function to load the grades CSV file
def load_csv_data():
    filename = "grades.csv"
#Check if the file exists if not stop the program
    if not os.path.exists(filename):
        print("File not found")
        sys.exit()
# This list is to store all the assignment grades
    assignments = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)
# Loop through the grades file and turn each low into a dictionary
        for row in reader:
            assignments.append({
                "assignment": row["assignment"],
                "group": row["group"],
                "score": float(row["score"]),
                "weight": float(row["weight"])
            })

    return assignments


# Function to process the grades calculations
def evaluate_grades(data):
    print("\n--- Processing Grades ---")

# Check if file has data
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

# Loop through the assignment list to get the assignment information
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

# Process formative assignments
        if group.lower() == "formative":
            formative_weight += weight
            formative_total += weighted_score
# Look for formatives with below 50
            if score < 50:
                failed_formative.append(item)

# Process the summatives
        elif group.lower() == "summative":
            summative_weight += weight
            summative_total += weighted_score

# Validating the weights
    print("\n--- Weight Validation ---")
    print("Total Weight:", total_weight)
    print("Formative Weight:", formative_weight)
    print("Summative Weight:", summative_weight)

# Checking if the weights match the grading policy
    if total_weight != 100:
        print("Error: Total weight must equal 100")
        return

    if formative_weight != 60:
        print("Error: Formative weight must equal 60")
        return

    if summative_weight != 40:
        print("Error: Summative weight must equal 40")
        return

#Category totals
    print("\n--- Category Totals ---")
    print("Formative Total:", formative_total)
    print("Summative Total:", summative_total)
#Calculating the final grade
    total_grade = formative_total + summative_total
    print("\nFinal Grade:", total_grade)
# Calculating the GPA
    gpa = (total_grade / 100) * 5.0
    print("GPA Calculation:")
    print(f"GPA = ({total_grade}/100) * 5 = {gpa}")
# Calculatinng the percentage in each category
    formative_percent = (formative_total / formative_weight) * 100
    summative_percent = (summative_total / summative_weight) * 100

    print("\nFormative Percentage:", formative_percent)
    print("Summative Percentage:", summative_percent)

# Determine if it is a fail or a pass
    print("\n--- Final Decision ---")
    if formative_percent >= 50 and summative_percent >= 50:
        print("Status: PASSED")
    else:
        print("Status: FAILED")

# Check if the formative assignments are eligible for resubmission
    print("\n--- Resubmission Check ---")
    if failed_formative:
        max_weight = max(a['weight'] for a in failed_formative)
        resubmit = [a for a in failed_formative if a['weight'] == max_weight]

        print("Eligible assignments for resubmission:")
        for a in resubmit:
            print(a['assignment'], "| Weight:", a['weight'])
    else:
        print("No resubmission required.")

# This is the program entry point
# It ensures the code runs only when the script is executed directly
if __name__ == "__main__":
# Load course data from CSV file
    course_data = load_csv_data()
# Evaluate the grades using loaded data
    evaluate_grades(course_data)
