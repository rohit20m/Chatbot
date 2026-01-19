# Importing tools 
import pandas as pd
import sys

def load_and_clean_data(filepath : str) -> pd.DataFrame:
    '''
    This is the most important function. It reads the messy Excel file
    and performs all the data cleaning to produce a perfect table.
    '''
    
    try:
        # Reading Excel File, starting from the correct row (19)
        df = pd.read_excel(filepath, sheet_name=0, header=18)
        
        # Cleaning the Columna Names by removing extra spaces
        df.columns = df.columns.str.strip()
        
        # Replacing the blank values with columns named "Case Number", "Status" and "Subject" 
        df[["Case Number", "Status", "Subject"]] = df[["Case Number", "Status", "Subject"]].ffill()
        
        # Removing an empty rows only if, the Column 'Case Number' for a row is blank
        df.dropna(subset=["Case Number"], inplace=True)

        # Making sure if the column "Description" is being taken as String or not
        df["Description"] = df["Description"].astype(str).fillna('').str.replace('nan', '', case=False)
        
        # Grouping all the broken pieces by "Case Number" and stitching their Descriptions back together into one paragraph
        df_grouped = df.groupby("Case Number", as_index=False).agg({
            'Subject' : 'first',
            'Description' : ''.join,
            'Status' : 'first'
        })

        # Final Clean up to make the column "Case number" as Whole Number
        df_grouped["Case Number"] = df_grouped["Case Number"].astype(int)

        # Returns the Table with clean and perfect order
        return df_grouped[["Case Number", "Description", "Subject", "Status"]]
    
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found. Please make sure it's in the same folder.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during cleaning: {e}")
        sys.exit(1)

# Main Part of the code

print("\n Starting the Data Cleaning Process")

# Defining the name of the file

input_filename = "casefeed.csv"

# Calling load_and_clean_data function and storing it in variable - cleaned_table v
cleaned_table = load_and_clean_data(input_filename)

# Printing the Final Data
print(cleaned_table.to_string(index=False))

print("\nData Cleaning Complete") 
print("\nBelow is your clean and Final Data:- ") 