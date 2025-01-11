from flask import Flask, request, send_from_directory, jsonify
import pandas as pd
import os

app = Flask(__name__)

def generate_js_and_html_from_excel(file_path, bfw_item_code):
    """
    Generate JavaScript and HTML code from an Excel file for a given BFW item code.
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
            return "No data found for the provided BFW item code.", "", ""

        js_code = ""
        pwl_html_code = """<table style="border-collapse: collapse; width: 509px; border-style: solid; border-color: #cccccc; height: 48px;" border="1" width="445" cellspacing="0" cellpadding="0"><colgroup><col style="mso-width-source: userset; mso-width-alt: 2706; width: 56pt;" span="2" width="74" /> <col style="mso-width-source: userset; mso-width-alt: 2194; width: 45pt;" width="60" /> <col style="mso-width-source: userset; mso-width-alt: 2742; width: 56pt;" width="75" /> <col style="mso-width-source: userset; mso-width-alt: 2706; width: 56pt;" width="74" /> <col style="mso-width-source: userset; mso-width-alt: 2230; width: 46pt;" width="61" /> </colgroup>
    <tbody>
    <tr style="height: 15.0pt;">
    <td class="xl66" style="height: 15px; width: 72.8711px; text-align: center;" height="20"><strong>QTY</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>12</strong></td>
    <td class="xl69" style="border-left: none; width: 58.5156px; text-align: center; height: 15px;" align="right"><strong>24</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>36</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>72</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>144</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>288</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>576</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>1008</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>2016+</strong></td>
    </tr>"""
        bb_html_code = """<table style="border-collapse: collapse; width: 509px; border-style: solid; border-color: #cccccc; height: 48px;" border="1" width="445" cellspacing="0" cellpadding="0"><colgroup><col style="mso-width-source: userset; mso-width-alt: 2706; width: 56pt;" span="2" width="74" /> <col style="mso-width-source: userset; mso-width-alt: 2194; width: 45pt;" width="60" /> <col style="mso-width-source: userset; mso-width-alt: 2742; width: 56pt;" width="75" /> <col style="mso-width-source: userset; mso-width-alt: 2706; width: 56pt;" width="74" /> <col style="mso-width-source: userset; mso-width-alt: 2230; width: 46pt;" width="61" /> </colgroup>
    <tbody>
    <tr style="height: 15.0pt;">
    <td class="xl66" style="height: 15px; width: 72.8711px; text-align: center;" height="20"><strong>QTY</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>12</strong></td>
    <td class="xl69" style="border-left: none; width: 58.5156px; text-align: center; height: 15px;" align="right"><strong>24</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>36</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>72</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>144</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>288</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>576</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>1008</strong></td>
    <td class="xl68" style="border-left: none; width: 72.8906px; text-align: center; height: 15px;" align="right"><strong>2016+</strong></td>
    </tr>"""

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

            # Determine if it's pwl or bb and append to the appropriate table
            if imprint.lower() == 'blank':  # bb
                variable_name = f"bb_{'n' if colors_type.lower() == 'white' else 'c'}"
                bb_html_code += f"<tr><td style='text-align: center;'>{colors_type}</td>" + "".join([f"<td style='text-align: center;'>${price}</td>" for price in prices]) + "</tr>"

                js_condition = " : ".join([f"{{qty}} <= {threshold} ? {price}" for threshold, price in zip([23, 35, 72, 144, 288, 576, 1008, 2016], prices)]) + f" : {prices[-1]}"
                js_code += f"// {colors_type} {imprint} Start\nvar {variable_name} = {{qty}} < 12 ? 0.00 : ({{qty}} < 24 ? {prices[0]} : ({{qty}} < 36 ? {prices[1]} : ({{qty}} < 72 ? {prices[2]} : ({{qty}} < 144 ? {prices[3]} : ({{qty}} < 288 ? {prices[4]} : ({{qty}} < 576 ? {prices[5]} : ({{qty}} < 1008 ? {prices[6]} : ({{qty}} < 2016 ? {prices[7]} : {prices[-1]}))))))));\n// {colors_type} {imprint} End\n\n"
            else:  # pwl
                variable_name = f"pwl_{'n' if colors_type.lower() == 'white' else 'c'}"
                pwl_html_code += f"<tr><td style='text-align: center;'>{colors_type}</td>" + "".join([f"<td style='text-align: center;'>${price}</td>" for price in prices]) + "</tr>"

                js_condition = " : ".join([f"{{qty}} <= {threshold} ? {price}" for threshold, price in zip([23, 35, 72, 144, 288, 576, 1008, 2016], prices)]) + f" : {prices[-1]}"
                js_code += f"// {colors_type} {imprint} Start\nvar {variable_name} = {{qty}} < 12 ? 0.00 : ({{qty}} < 24 ? {prices[0]} : ({{qty}} < 36 ? {prices[1]} : ({{qty}} < 72 ? {prices[2]} : ({{qty}} < 144 ? {prices[3]} : ({{qty}} < 288 ? {prices[4]} : ({{qty}} < 576 ? {prices[5]} : ({{qty}} < 1008 ? {prices[6]} : ({{qty}} < 2016 ? {prices[7]} : {prices[-1]}))))))));\n// {colors_type} {imprint} End\n\n"

        pwl_html_code += "</table>"
        bb_html_code += "</table>"
        
        return js_code, pwl_html_code, bb_html_code

    except Exception as e:
        return f"An error occurred: {e}", "", ""

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')  # Serve the index.html directly from the current folder

@app.route('/fetch_data')
def fetch_data():
    bfw_item_code = request.args.get('bfw_item_code', '')
    file_path = "./files.xlsx"  # Replace with your actual file path

    js_code, pwl_html_code, bb_html_code = generate_js_and_html_from_excel(file_path, bfw_item_code)

    return jsonify(js_code=js_code, pwl_html_code=pwl_html_code, bb_html_code=bb_html_code)

if __name__ == "__main__":
    app.run(debug=True)
