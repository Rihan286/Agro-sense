import os

file = 'generate_pages.py'

from generate_pages import template

history_content = """
            <div class="history-container card" style="max-width: 1000px; margin: 0 auto;">
                <div id="status-message" class="loading" style="text-align: center; padding: 20px; color: rgba(63, 75, 59, 0.6); font-size: 1.1em;">Loading history...</div>
                <table id="history-table" style="display: none; width: 100%; border-collapse: collapse; margin-top: 10px;">
                    <thead>
                        <tr>
                            <th style="padding: 15px; border-bottom: 1px solid rgba(63, 75, 59, 0.1); background-color: rgba(90, 147, 103, 0.05); color: var(--hunter-green); font-weight: 600; text-align: left; border-top-left-radius: 8px;">Date & Time</th>
                            <th style="padding: 15px; border-bottom: 1px solid rgba(63, 75, 59, 0.1); background-color: rgba(90, 147, 103, 0.05); color: var(--hunter-green); font-weight: 600; text-align: left;">Crop</th>
                            <th style="padding: 15px; border-bottom: 1px solid rgba(63, 75, 59, 0.1); background-color: rgba(90, 147, 103, 0.05); color: var(--hunter-green); font-weight: 600; text-align: left;">Predicted Disease</th>
                            <th style="padding: 15px; border-bottom: 1px solid rgba(63, 75, 59, 0.1); background-color: rgba(90, 147, 103, 0.05); color: var(--hunter-green); font-weight: 600; text-align: left;">Confidence</th>
                            <th style="padding: 15px; border-bottom: 1px solid rgba(63, 75, 59, 0.1); background-color: rgba(90, 147, 103, 0.05); color: var(--hunter-green); font-weight: 600; text-align: left; border-top-right-radius: 8px;">Image Reference</th>
                        </tr>
                    </thead>
                    <tbody id="history-body">
                        <!-- Data will be populated here -->
                    </tbody>
                </table>
                <style>
                    #history-table td { padding: 15px; border-bottom: 1px solid rgba(63, 75, 59, 0.1); }
                    #history-table tr:hover td { background-color: rgba(90, 147, 103, 0.05); }
                    .confidence-high { color: var(--hunter-green); font-weight: 600; }
                    .confidence-med { color: #ff9800; font-weight: 600; }
                    .confidence-low { color: #d32f2f; font-weight: 600; }
                    .error { color: #d32f2f; text-align: center; padding: 15px; background: #ffebee; border-radius: 8px; }
                </style>
            </div>
"""

full_html = template.format(
    title="Detection History",
    content=history_content,
    active_detect="",
    active_weather="",
    active_market="",
    active_assistant="",
    active_history="active"
)

with open('history.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Generated history.html!")
