import pandas as pd

def generate_js_from_excel(file_path, bfw_item_code, output_file):
    """
    Generate JavaScript code from an Excel file for a given BFW item code.

    Parameters:
        file_path (str): Path to the Excel file.
        bfw_item_code (str): BFW item code to filter the data.
        output_file (str): Path to save the generated JavaScript code.
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
            print(f"No data found for BFW item code: {bfw_item_code}")
            return

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

            # Debugging: Print prices to check values
            print(f"Prices for {colors_type} {imprint}: {prices}")

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

        # Save the generated JavaScript code to a file
        with open(output_file, 'w') as js_file:
            js_file.write(js_code)

        print(f"JavaScript code successfully written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
file_path = "./files.xlsx"  # Replace with your actual file path
bfw_item_code = "CM7102"  # Replace with your desired code
output_file = "app.js"  # Desired output JavaScript file

generate_js_from_excel(file_path, bfw_item_code, output_file)
