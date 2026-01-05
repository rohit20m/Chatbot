import pandas as pd  
import sys

try:
    csv_data = pd.read_csv("cases.csv")

except FileNotFoundError:
    print("Error: 'cases.csv' not found. Place it next to this script and retry.")
    sys.exit(1)

except pd.errors.EmptyDataError:
    print("Error: 'cases.csv' is empty.")
    sys.exit(1)

except pd.errors.ParserError:
    print("Error: 'cases.csv' is malformed or cannot be parsed.")
    sys.exit(1)

except Exception as e:
    print(f"Unexpected error reading 'cases.csv': {e}")
    sys.exit(1)

print("-------------------------------------------------------------------------------------")

print("Welcome to the dummy CSV data")

print("-------------------------------------------------------------------------------------")

# Prints whole CVS File Data

print(csv_data.to_string(index=False))

print("-------------------------------------------------------------------------------------")

# Prints Total number of cases

total_status = len(csv_data)

print(f"Total number of cases are: {total_status}")

print("-------------------------------------------------------------------------------------")

while True:
    user_input = input("Use the following inputs to explore more :- \n To view Case Status Summary please Type - 'status' \n To view Case Status subject Summary please Type - 'subject' \n To exit , please type - 'exit' \n Enter your Input here: ").lower()

    # Exit Logic
    if user_input == "exit":
        print("Bot: Thanks you for Visiting and Good bye!!!")
        break

    # Case Status Summary Logic

    elif user_input == "status":
        print("Case Status Summary: ")
        if "Status" not in csv_data.columns:
            print("Bot: 'Status' column not found in CSV.")
        else:
            status_count = csv_data["Status"].value_counts()
            print("-------------------------------------------------------------------------------------")
            for status, count in status_count.items():
                print(f"The total Number of case status {status} are: {count}")
                print("-------------------------------------------------------------------------------------")

    # Case Subject Summary Logic

    elif user_input == "subject":
        total_subjects = len(csv_data)
        print(f"The Total number of subjects are: {total_subjects}")

    # elif user_input == "status":

    # User invalid Logic

    else:
        print("Bot: This feature is not available right now.")
        print("Bot: You can try 'count' or 'status'.")