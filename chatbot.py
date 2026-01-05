import pandas as pd  
import sys

try:
    csv_data = pd.read_csv("cases.csv")
    # csv_data = pd.read_csv("casefeed.csv")

except FileNotFoundError:
    print("Error: File not found!!!!!!. Please check the file name again.")
    sys.exit(1)

except pd.errors.EmptyDataError:
    print("Error: file is empty.")
    sys.exit(1)

except pd.errors.ParserError:
    print("Error: File is malformed or cannot be parsed.")
    sys.exit(1)

except Exception as e:
    print(f"Unexpected error reading the File: {e}")
    sys.exit(1)

print("-------------------------------------------------------------------------------------")

print("Welcome to the dummy CSV data")

print("-------------------------------------------------------------------------------------")

# Prints whole CVS File Data

print(csv_data.to_string(index=False))

print("-------------------------------------------------------------------------------------")

# Prints Total number of cases

total_cases = len(csv_data)
print(f"Total number of cases are: {total_cases}")

print("-------------------------------------------------------------------------------------")

while True:
    user_input = input("Use the following inputs to explore more :- \n To view Case Status Summary please Type - 'status' \n To view Case Priority Summary please Type - 'priority' \n To exit , please type - 'exit' \n Enter your Input here: \n").lower()

    # Exit Logic
    if user_input == "exit":
        print("Bot: Thanks you for Visiting and Good bye!!!")
        break

    # Case Status Summary Logic
    elif user_input == "status":
        print("Case Status Summary Details:- \n")
        if "Status" not in csv_data.columns:
            print("Bot: 'Status' column not found in CSV.")
        else:
            status_count = csv_data["Status"].value_counts()
            print("-------------------------------------------------------------------------------------")
            for status, count in status_count.items():
                print(f"The total Number of case status {status} are: {count}")
                print("-------------------------------------------------------------------------------------")

    # Case Priority Summary Logic
    elif user_input == "priority":
        print("Case Priority Summary Details:- \n")
        priority_count = csv_data['Priority'].value_counts()
        
        for priority, count in priority_count.items():
            print(f"The total Number of Priority {priority} are: {count}")
            print("-------------------------------------------------------------------------------------")
            
    # User Invalid Input Logic
    else:
        print("Bot: This feature is not available right now.")
        print("Bot: You can try 'count' or 'status'.")