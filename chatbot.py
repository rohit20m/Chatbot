# --- FINAL REFACTORED VERSION WITH BROWSER AND CONSOLE OUTPUT ---
import pandas as pd
import sys
import webbrowser
import os

# --- Part 1: Define the HTML Template ---
# This remains separate for clarity.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Case Data Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ padding: 2rem; }}
        h1 {{ margin-bottom: 1.5rem; }}
        .table {{ table-layout: fixed; width: 100%; }}
        th {{ white-space: nowrap; }}
        td {{ word-break: break-word; }}
        #summary-container {{ max-width: 600px; }}
        .table th:nth-child(1), .table td:nth-child(1) {{ width: 10%; }}
        .table th:nth-child(2), .table td:nth-child(2) {{ width: 25%; }}
        .table th:nth-child(3), .table td:nth-child(3) {{ width: 50%; }}
        .table th:nth-child(4), .table td:nth-child(4) {{ width: 15%; }}
    </style>
</head>
<body>
    <div class="container-fluid">
        <h1>Case Data Report</h1>
        <p>Total cases found: {total_cases}</p>
        <button id="toggle-summary-btn" class="btn btn-primary mb-3">Show Case Status Summary</button>
        <div id="summary-container" style="display: none;">
            <h2>Case Status Summary</h2>
            {summary_html_table}
        </div>
        <hr>
        <div class="table-responsive">{main_html_table}</div>
    </div>
    <script>
        const toggleBtn = document.getElementById('toggle-summary-btn');
        const summaryContainer = document.getElementById('summary-container');
        toggleBtn.addEventListener('click', () => {{
            const isHidden = summaryContainer.style.display === 'none';
            summaryContainer.style.display = isHidden ? 'block' : 'none';
            toggleBtn.textContent = isHidden ? 'Hide Case Status Summary' : 'Show Case Status Summary';
        }});
    </script>
</body>
</html>
"""

# --- Part 2: Create clear, single-purpose functions ---

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """Loads and cleans the raw Excel file."""
    print("Step 1: Loading and cleaning the Excel file...")
    df = pd.read_excel(filepath, sheet_name=0, header=18)
    df.columns = df.columns.str.strip()
    df[["Case Number", "Subject", "Status"]] = df[["Case Number", "Subject", "Status"]].ffill()
    df.dropna(subset=["Case Number"], inplace=True)
    df['Description'] = df['Description'].astype(str).fillna('').str.replace('nan', '', case=False)
    df_grouped = df.groupby("Case Number", as_index=False).agg({
        'Subject': 'first',
        'Description': ' '.join,
        'Status': 'first'
    })
    df_grouped['Case Number'] = df_grouped['Case Number'].astype(int)
    print("Data cleaning complete.")
    return df_grouped[["Case Number", "Subject", "Description", "Status"]]

def generate_html_report(df: pd.DataFrame) -> str:
    """Generates the full HTML content for the browser report."""
    print("Step 2: Generating HTML report...")
    main_table = df.to_html(index=False, justify='left', classes='table table-striped table-hover')
    summary_df = df.groupby("Status").size().reset_index(name='Total Cases')
    summary_table = summary_df.to_html(index=False, justify='left', classes='table table-bordered mt-3')
    return HTML_TEMPLATE.format(
        total_cases=len(df),
        summary_html_table=summary_table,
        main_html_table=main_table
    )

def save_and_open_in_browser(html_content: str, filename: str):
    """Saves the HTML and opens it in a browser tab."""
    print(f"Step 3: Saving the report to '{filename}'...")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Step 4: Opening the report in your default web browser...")
    full_path = os.path.abspath(filename)
    webbrowser.open_new_tab(f'file://{full_path}')

# --- NEW: Function to print summary to the console ---
def print_console_summary(df: pd.DataFrame):
    """Calculates and prints the status summary to the console."""
    print("-------------------------------------------------------------------------------------")
    print("Case Status Summary (Console Output):")
    summary_df = df.groupby("Status").size().reset_index(name='Total Cases')
    # Using .to_string() gives a nice table format in the console
    print(summary_df.to_string(index=False))
    print("-------------------------------------------------------------------------------------")

# --- Part 3: Main function to orchestrate the script ---

def main():
    """Main function to run the entire data processing pipeline."""
    print("-------------------------------------------------------------------------------------")
    print("Starting the data analysis script...")
    
    input_file = "casefeed.csv"
    output_file = "case_report.html"

    try:
        # The main workflow
        clean_data = load_and_clean_data(input_file)
        html_report = generate_html_report(clean_data)
        save_and_open_in_browser(html_report, output_file)
        
        # --- ADDED BACK: Print the summary to the console ---
        print_console_summary(clean_data)
        
        print("Script finished successfully!")
        print("Your interactive report is open in your browser, and the summary is shown above.")
        print("-------------------------------------------------------------------------------------")

    except Exception as e:
        print("-------------------------------------------------------------------------------------")
        print(f"AN UNEXPECTED ERROR OCCURRED: {e}")
        print("The program will exit.")
        print("-------------------------------------------------------------------------------------")
        sys.exit(1)

# --- Part 4: Run the main function ---
if __name__ == "__main__":
    main()