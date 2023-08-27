import pandas as pd
from flask import Flask, render_template, request,send_file

app = Flask(__name__)


# Function to calculate statistics about the DataFrame
def calculate_statistics(df, file_type):
    # Get column number
    column_number = len(df.columns)
    # Get column name
    column_names = df.columns.tolist()
    # Get column data type
    data_types = df.dtypes.to_dict()
    # Get column numeric stats
    numeric_stats = df.describe().transpose()
    # Get column unique values
    unique_values = df.nunique()
    # Get column data preview
    data_preview = df.head()
    # Get data number (number of rows)
    data_number = len(df)
    # Get NaN (missing value) count
    nan_count = df.isna().sum().sum()
    # Get row number
    row_number = df.shape[0]

    # Create a formatted summary text
    summary = f"File Type: {file_type}\n"
    summary += f"Number of Columns: {column_number}\n"
    summary += f"Number of Rows: {row_number}\n"
    summary += f"Number of Data Points: {data_number}\n"
    summary += f"Number of Missing Values: {nan_count}\n"

    summary += "\nData Types:\n"
    for column_name, data_type in data_types.items():
        summary += f"{column_name}: {data_type}\n"

    summary += "\nUnique Values for Non-Numeric Columns:\n"
    for column_name, unique_value_count in unique_values.items():
        summary += f"{column_name}: {unique_value_count}\n"

    return file_type, column_number, data_number, nan_count, row_number, data_preview, unique_values, numeric_stats, data_types, column_names, summary


# HTML form for file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file_type = request.form['file_type']
        file = request.files['file']

        if file_type == "csv":
            df = pd.read_csv(file)
        elif file_type == "excel":
            df = pd.read_excel(file)
        elif file_type == "txt":
            delimiter = request.form['delimiter']
            df = pd.read_csv(file, delimiter=delimiter)
        else:
            return "Invalid file type. Please choose from CSV, Excel, or TXT."

        # Calculate statistics about the DataFrame and get the summary
        file_type, column_number, data_number, nan_count, row_number, data_preview, unique_values, numeric_stats, data_types, column_names, summary = calculate_statistics(
            df, file_type)

        # Store the summary in a text file
        with open("data_summary.txt", "w") as text_file:
            text_file.write(summary)

        return render_template('display.html',
                               file_type=file_type,
                               column_number=column_number,
                               data_number=data_number,
                               nan_count=nan_count,
                               row_number=row_number,
                               data_types=data_types,
                               numeric_stats=numeric_stats,
                               unique_values=unique_values,
                               data_preview=data_preview,
                               df=df)  # Pass the DataFrame to the template

    return render_template('upload.html')

@app.route('/download_summary')
def download_summary():
    return send_file("data_summary.txt", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
