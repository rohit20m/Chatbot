import pandas as pd
import sys
import webbrowser
import os
import numpy as np

print("-------------------------------------------------------------------------------------")
print("Starting the AI-Enhanced data analysis script...")

try:
    # --- Step 1: Load and Clean the Data ---
    # Using your current cleaning logic
    df_raw = pd.read_excel("casefeed.csv", sheet_name=0, header=18)
    df_raw.columns = df_raw.columns.str.strip()
    final_columns = ["Case Number", "Subject", "Description", "Status"]
    identifier_cols = ["Case Number", "Subject", "Status"]
    df_raw[identifier_cols] = df_raw[identifier_cols].ffill()
    df_raw.dropna(subset=["Case Number"], inplace=True)
    df_raw['Description'] = df_raw['Description'].astype(str).fillna('')
    df_grouped = df_raw.groupby("Case Number").agg({
        'Subject': 'first',
        'Description': ' '.join,
        'Status': 'first'
    })
    df_grouped['Case Number'] = df_grouped['Case Number'].astype(int)
    df_final = df_grouped[final_columns]

    # --- Step 1.5: NumPy Analysis Layer ---
    # Converting Pandas columns to NumPy arrays for high-speed analysis
    status_array = df_final['Status'].to_numpy()
    desc_array = df_final['Description'].to_numpy().astype(str)

    # Concept: Vectorization to find 'Urgent' cases
    is_urgent = np.char.find(np.char.lower(desc_array), 'urgent') != -1
    urgent_count = np.sum(is_urgent)

    # Concept: Using NumPy attributes (.size) and math for efficiency
    total_cases = status_array.size
    closed_count = np.sum(status_array == 'Closed')
    efficiency_rate = np.round((closed_count / total_cases) * 100, 2) if total_cases > 0 else 0

    # --- Step 2: Generate Tables ---
    main_html_table = df_final.to_html(index=False, justify='left', classes='table table-striped table-hover')
    status_summary_df = df_final.groupby("Status").size().reset_index(name='Total Cases')
    summary_html_table = status_summary_df.to_html(index=False, justify='left', classes='table table-bordered mt-3')

    # --- Step 3: Create HTML Document ---
    # Note: data-bs-theme="light" is set on the html tag for the switcher to work
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en" data-bs-theme="light">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Support AI Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div class="container-fluid">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Support Case AI Dashboard</h1>
                <button id="theme-toggle" class="btn btn-outline-secondary">🌓 Switch Theme</button>
            </div>

            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="dashboard-card">
                        <div class="text-muted">Team Efficiency</div>
                        <div class="metric-val text-primary">{efficiency_rate}%</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="dashboard-card">
                        <div class="text-muted">Urgent Alerts</div>
                        <div class="metric-val text-danger">{urgent_count}</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="dashboard-card">
                        <div class="text-muted">Total Load</div>
                        <div class="metric-val">{total_cases}</div>
                    </div>
                </div>
            </div>

            <button id="toggle-summary-btn" class="btn btn-primary mb-3">Toggle Case Summary View</button>
            <div id="summary-container" style="display: none;">{summary_html_table}</div>

            <hr>
            <div class="table-responsive">
                {main_html_table}
            </div>
        </div>

        <script>
            // Logic 1: Summary Table Toggle
            const toggleBtn = document.getElementById('toggle-summary-btn');
            const summaryContainer = document.getElementById('summary-container');
            toggleBtn.addEventListener('click', () => {{
                if (summaryContainer.style.display === 'none') {{
                    summaryContainer.style.display = 'block';
                    toggleBtn.textContent = 'Hide Summary';
                }} else {{
                    summaryContainer.style.display = 'none';
                    toggleBtn.textContent = 'Show Summary';
                }}
            }});

            // Logic 2: Bootstrap Dark Mode Switcher
            const themeToggleBtn = document.getElementById('theme-toggle');
            themeToggleBtn.addEventListener('click', () => {{
                const htmlElement = document.documentElement;
                if (htmlElement.getAttribute('data-bs-theme') === 'light') {{
                    htmlElement.setAttribute('data-bs-theme', 'dark');
                }} else {{
                    htmlElement.setAttribute('data-bs-theme', 'light');
                }}
            }});
        </script>
    </body>
    </html>
    """

    # --- Step 4: Save and Open ---
    filename = 'case_report.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_template)

    full_path = os.path.abspath(filename)
    webbrowser.open_new_tab('file://' + full_path)
    print("Success! Dashboard generated and opened.")

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
