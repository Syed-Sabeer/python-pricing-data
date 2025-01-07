from flask import Flask, request, send_from_directory, jsonify
import pandas as pd
import os

app = Flask(__name__)

def generate_js_from_excel(file_path, bfw_item_code):
    """
    Generate JavaScript code from an Excel file for a given BFW item code.
    """
    try:
        # Load the Excel sheet
        df = pd.read_excel(file_path, dtype=str)
        df.columns = df.columns.str.strip()  # Remove whitespace from column headers
        df['BFW item'] = df['BFW item'].str.strip().str.upper()  # Clean up BFW item column

        # Convert the search term to uppercase
        bfw_item_code = bfw_item_code.strip().upper()

        # Filter rows for the given BFW item code
        filtered_df = df[df['BFW item'] == bfw_item_code]
        if filtered_df.empty:
            return "No data found for the provided BFW item code."

        js_code = ""

        # Map conditions to the specified format
        for _, row in filtered_df.iterrows():
            colors_type = row['Colors Type']
            imprint = row['Imprint']

            # Handle price cleaning
            prices = []
            for col in filtered_df.columns[6:15]:  # Assuming price columns are from index 6 to 15
                price = row[col]
                if isinstance(price, str) and price.strip() != "":
                    # Clean price and check if it's a valid number
                    cleaned_price = price.replace('$', '').replace(',', '').strip()  # Remove dollar sign, commas, and spaces
                    try:
                        # Ensure we can convert to a float
                        float_price = float(cleaned_price)
                        prices.append(f"{float_price:.2f}")  # Append the price as a string with 2 decimals
                    except ValueError:
                        # If not a valid number, append 0.00
                        prices.append("0.00")
                else:
                    prices.append("0.00")  # Default to "0.00" if the value is NaN or empty

            # Determine the variable name based on colors type and imprint
            variable_name = f"{'bb' if imprint.lower() == 'blank' else 'pwl'}_{'n' if colors_type.lower() == 'white' else 'c'}"

            # Create the condition format
            js_condition = " : ".join(
                [f"{{qty}} < {threshold} ? {price}" for threshold, price in zip([12, 24, 36, 72, 144, 288, 576, 1008, 2016], prices)]
            ) + f" : {prices[-1]}"  # Use the last price for values >= 2016

            # Add JavaScript code block with the specific format for each color and imprint
            js_code += f"/* {colors_type} {imprint} Start */\n"
            js_code += f"var {variable_name} = {{qty}} < 12 ? {prices[0]} : ({{qty}} < 24 ? {prices[1]} : ({{qty}} < 36 ? {prices[2]} : ({{qty}} < 72 ? {prices[3]} : ({{qty}} < 144 ? {prices[4]} : ({{qty}} < 288 ? {prices[5]} : ({{qty}} < 576 ? {prices[6]} : ({{qty}} < 1008 ? {prices[7]} : ({{qty}} < 2016 ? {prices[8]} : {prices[-1]}))))))));\n"
            js_code += f"/* {colors_type} {imprint} End */\n\n"

        return js_code

    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')  # Serve the index.html directly from the current folder

@app.route('/fetch_data')
def fetch_data():
    bfw_item_code = request.args.get('bfw_item_code', '')
    file_path = "./files.xlsx"  # Replace with your actual file path

    js_code = generate_js_from_excel(file_path, bfw_item_code)

    return jsonify(js_code=js_code)

if __name__ == '__main__':
    app.run(debug=True)
