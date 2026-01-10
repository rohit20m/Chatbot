# --- FINAL VERSION WITH INTERACTIVE BROWSER BUTTON ---
import pandas as pd
import sys
import webbrowser
import os

print("-------------------------------------------------------------------------------------")
print("Starting the data analysis script...")

try:
    # --- Step 1: Load and Clean the Data ---
    print("Step 1: Loading and cleaning the Excel file...")
    # (The cleaning logic remains the same)
    df_raw = pd.read_excel("casefeed.csv", sheet_name=0, header=18)
    df_raw.columns = df_raw.columns.str.strip()
    final_columns = ["Case Number", "Subject", "Description", "Status"]
    identifier_cols = ["Case Number", "Subject", "Status"]
    df_raw[identifier_cols] = df_raw[identifier_cols].ffill()
    df_raw.dropna(subset=["Case Number"], inplace=True)
    df_raw['Description'] = df_raw['Description'].astype(str).fillna('')
    df_grouped = df_raw.groupby("Case Number").agg({
        'Subject': 'first',
        'Description': lambda x: ' '.join(x).replace('nan', '').strip(),
        'Status': 'first'
    }).reset_index()
    df_grouped['Case Number'] = df_grouped['Case Number'].astype(int)
    df_final = df_grouped[final_columns]
    print("Data cleaning complete.")

    # --- Step 2: Generate HTML for BOTH tables ---
    print("Step 2: Generating HTML for main report and status summary...")
    # Main table for all cases
    main_html_table = df_final.to_html(index=False, justify='left', classes='table table-striped table-hover')

    # NEW: Create a summary DataFrame and convert it to a simple HTML table
    status_summary_df = df_final.groupby("Status").size().reset_index(name='Total Cases')
    summary_html_table = status_summary_df.to_html(index=False, justify='left', classes='table table-bordered mt-3')

    # --- Step 3: Create the final HTML document with the button and hidden summary ---
    html_template = f"""
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
            #summary-container {{ max-width: 600px; }} /* Limit width of summary table */
            /* Column Widths */
            .table th:nth-child(1), .table td:nth-child(1) {{ width: 10%; }}
            .table th:nth-child(2), .table td:nth-child(2) {{ width: 25%; }}
            .table th:nth-child(3), .table td:nth-child(3) {{ width: 50%; }}
            .table th:nth-child(4), .table td:nth-child(4) {{ width: 15%; }}
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <h1>Case Data Report</h1>
            <p>Total cases found: {len(df_final)}</p>
            
            <!-- NEW: The button to toggle the summary -->
            <button id="toggle-summary-btn" class="btn btn-primary mb-3">Show Case Status Summary</button>
            
            <!-- NEW: The hidden container for the summary table -->
            <div id="summary-container" style="display: none;">
                <h2>Case Status Summary</h2>
                {summary_html_table}
            </div>

            <hr> <!-- A separator line for clarity -->

            <!-- The main table of all cases -->
            <div class="table-responsive">
                {main_html_table}
            </div>
        </div>

        <!-- NEW: JavaScript to make the button work -->
        <script>
            const toggleBtn = document.getElementById('toggle-summary-btn');
            const summaryContainer = document.getElementById('summary-container');

            toggleBtn.addEventListener('click', () => {{
                if (summaryContainer.style.display === 'none') {{
                    summaryContainer.style.display = 'block';
                    toggleBtn.textContent = 'Hide Case Status Summary';
                }} else {{
                    summaryContainer.style.display = 'none';
                    toggleBtn.textContent = 'Show Case Status Summary';
                }}
            }});
        </script>
    </body>
    </html>
    """

    # --- Step 4 & 5: Save and open the file ---
    filename = 'case_report.html'
    print(f"Step 3: Saving the report to '{filename}'...")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print("Step 4: Opening the report in your default web browser...")
    full_path = os.path.abspath(filename)
    webbrowser.open_new_tab('file://' + full_path)

except Exception as e:
    print("-------------------------------------------------------------------------------------")
    print(f"AN UNEXPECTED ERROR OCCURRED: {e}")
    print("The program will exit.")
    print("-------------------------------------------------------------------------------------")
    sys.exit(1)

print("-------------------------------------------------------------------------------------")
print("Script finished successfully!")
print("Your interactive report is now open in your browser.")
print("The console is no longer needed for summaries.")
print("You can close this window or press Ctrl+C to exit.")
print("-------------------------------------------------------------------------------------")
# The interactive console loop is removed as its functionality is now in the browser.