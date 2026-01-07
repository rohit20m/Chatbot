import pandas as pd
import sys

try:
    csv_data = pd.read_csv("cases.csv")

except FileNotFoundError:
    print("-------------------------------------------------------------------------------------")
    print("Error: File not found!!!!!!. Please check the file name again.")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)

except pd.errors.EmptyDataError:
    print("-------------------------------------------------------------------------------------")
    print("Error: file is empty.")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)

except pd.errors.ParserError:
    print("-------------------------------------------------------------------------------------")
    print("Error: File is malformed or cannot be parsed.")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)

except Exception as e:
    print("-------------------------------------------------------------------------------------")
    print(f"Unexpected error reading the File: {e}")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)


# --------- GLOBAL VALIDATION LOGIC AT START ---------

required_columns = ["CaseId", "Subject", "Description", "Priority", "Status"]

missing = [col for col in required_columns if col not in csv_data.columns]

if missing:
    print("-------------------------------------------------------------------------------------")
    print(f"Error: The following required columns are missing in CSV: {missing}")
    print("Please correct the CSV file and restart the program.")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)

# ----------------------------------------------------


print("-------------------------------------------------------------------------------------")
print("Welcome to the dummy CSV data")
print("-------------------------------------------------------------------------------------")

# Prints whole CSV File Data without index
print(csv_data.to_string(index=False))

print("-------------------------------------------------------------------------------------")

# Prints Total number of cases
total_cases = len(csv_data)
print(f"Total number of cases are: {total_cases}")

print("-------------------------------------------------------------------------------------")

while True:
    user_input = input(
        "Use the following inputs to explore more :- \n"
        " To view Case Status Summary please Type - 'status' \n"
        " To view Case Priority Summary please Type - 'priority' \n"
        " To exit , please type - 'exit' \n"
        " Enter your Input here: \n"
    ).lower()

    # Exit Logic
    if user_input == "exit":
        print("-------------------------------------------------------------------------------------")
        print("Bot: Thanks you for Visiting and Good bye!!!")
        print("-------------------------------------------------------------------------------------")
        break

    # Case Status Summary Logic
    elif user_input == "status":
        print("-------------------------------------------------------------------------------------")
        print("\nCase Status Summary Details:- \n")
        print("-------------------------------------------------------------------------------------")

        status_count = csv_data.groupby("Status").size()

        for status, count in status_count.items():
            print(f"The total number of cases with status '{status}' are: {count}")

        print("-------------------------------------------------------------------------------------")

    # Case Priority Summary Logic
    elif user_input == "priority":
        print("-------------------------------------------------------------------------------------")
        print("\nPriority - wise Open and Closed Case Summary:- \n")
        print("-------------------------------------------------------------------------------------")

        # Group by Priority and Status to get counts in pivot-table format
        priority_status_summary = csv_data.groupby(["Priority", "Status"]).size().unstack(fill_value=0)

        print(priority_status_summary)

        print("-------------------------------------------------------------------------------------\n")

    # User Invalid Input Logic
    else:
        print("-------------------------------------------------------------------------------------")
        print("Bot: This feature is not available right now.")
        print("Bot: You can try 'status' or 'priority'.")
        print("-------------------------------------------------------------------------------------")
