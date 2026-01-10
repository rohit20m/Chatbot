# --- RUNNING THE LATEST VERSION OF THE SCRIPT ---
import pandas as pd
import sys

try:
    # --- Step 1: Load the raw Excel data ---
    # We know the real headers start on row 19 (index 18)
    df_raw = pd.read_excel("casefeed.csv", sheet_name=0, header=18)

    # --- Step 2: The Advanced Data Cleaning Process ---

    # First, clean the column names to remove any hidden spaces
    df_raw.columns = df_raw.columns.str.strip()
    
    # Define the columns you want in your final table.
    final_columns = ["Case Number", "Subject", "Description", "Status"]

    # Forward-fill the main case identifiers. This copies 'Case Number', 'Subject', etc.,
    # down into the otherwise empty rows that are part of the same case.
    identifier_cols = ["Case Number", "Subject", "Status"]
    df_raw[identifier_cols] = df_raw[identifier_cols].ffill()

    # Now that all rows are properly tagged, we can safely remove any true blank rows
    # that might exist between cases.
    df_raw.dropna(subset=["Case Number"], inplace=True)
    
    # Ensure the 'Description' column is treated as text to prevent errors.
    df_raw['Description'] = df_raw['Description'].astype(str).fillna('')

    # This is the key step: We group everything by 'Case Number' and then "stitch" together
    # all the broken pieces of the 'Description' from multiple rows into one single, clean text block.
    df_grouped = df_raw.groupby("Case Number").agg({
        'Subject': 'first',
        'Description': lambda x: ' '.join(x).replace('nan', '').strip(), # This joins and cleans the text.
        'Status': 'first'
    }).reset_index()

    # Make the 'Case Number' a clean number (e.g., 24413250 instead of 24413250.0)
    df_grouped['Case Number'] = df_grouped['Case Number'].astype(int)
    
    # This is our final, perfect, clean table.
    df_final = df_grouped[final_columns]

except FileNotFoundError:
    print("-------------------------------------------------------------------------------------")
    print("Error: 'casefeed.csv' not found. Please ensure the file is in the same directory.")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)
except KeyError:
    print("-------------------------------------------------------------------------------------")
    print(f"FATAL Error: A required column was not found after loading the file.")
    print("Please check your Excel file's headers (around row 19).")
    print(f"The script was looking for: {final_columns}")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)
except Exception as e:
    print("-------------------------------------------------------------------------------------")
    print(f"An unexpected error occurred during file reading or cleaning: {e}")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)

# --- Main Program Starts Here ---

print("-------------------------------------------------------------------------------------")
print("Welcome to the case data analyzer")
print("-------------------------------------------------------------------------------------")

# This will now print the clean, properly formatted table.
print(df_final.to_string(index=False))

print("-------------------------------------------------------------------------------------")

# The rest of the program continues as before.
total_cases = len(df_final)
print(f"Total number of cases found: {total_cases}")

print("-------------------------------------------------------------------------------------")

while True:
    user_input = input(
        "Use the following inputs to explore more :- \n"
        " To view Case Status Summary please Type - 'status' \n"
        " To exit , please type - 'exit' \n"
        " Enter your Input here: \n"
    ).lower()

    if user_input == "exit":
        print("-------------------------------------------------------------------------------------")
        print("Bot: Thank you for visiting. Good bye!")
        print("-------------------------------------------------------------------------------------")
        break

    elif user_input == "status":
        print("-------------------------------------------------------------------------------------")
        print("\nCase Status Summary Details:- \n")
        print("-------------------------------------------------------------------------------------")
        status_count = df_final.groupby("Status").size()
        for status, count in status_count.items():
            print(f"The total number of cases with status '{status}' are: {count}")
        print("-------------------------------------------------------------------------------------")
    
    else:
        print("-------------------------------------------------------------------------------------")
        print("Bot: This feature is not available right now.")
        print("Bot: You can try 'status'.")
        print("-------------------------------------------------------------------------------------")
