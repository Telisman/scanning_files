import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to calculate statistics about the DataFrame
def calculate_statistics(df, file_type):
    # Get column number
    column_number = len(df.columns)

    # Get data number (number of rows)
    data_number = len(df)

    # Get NaN (missing value) count
    nan_count = df.isna().sum().sum()

    # Get row number
    row_number = df.shape[0]

    # Return the calculated statistics
    return file_type, column_number, data_number, nan_count, row_number

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

        # Calculate statistics about the DataFrame
        file_type, column_number, data_number, nan_count, row_number = calculate_statistics(df, file_type)

        return render_template('display.html',
                               file_type=file_type,
                               column_number=column_number,
                               data_number=data_number,
                               nan_count=nan_count,
                               row_number=row_number,
                               df=df)  # Pass the DataFrame to the template

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
