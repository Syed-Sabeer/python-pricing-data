from flask import Flask, request, send_from_directory, jsonify
import pandas as pd
import os

app = Flask(__name__)

def generate_js_and_html_from_excel(file_path, bfw_item_code):
    """
    Generate JavaScript and HTML table from an Excel file for a given BFW item code.
    """
    try:
        df = pd.read_excel(file_path, dtype=str)
        df.columns = df.columns.str.strip()
        df['BFW item'] = df['BFW item'].str.strip().str.upper()
        bfw_item_code = bfw_item_code.strip().upper()

        filtered_df = df[df['BFW item'] == bfw_item_code]
        if filtered_df.empty:
            return "No data found for the provided BFW item code.", ""

        js_code = ""
        html_code = """<table style="border-collapse: collapse; width: 509px; border-style: solid; border-color: #cccccc; height: 48px;" border="1" width="445" cellspacing="0" cellpadding="0"><colgroup><col style="mso-width-source: userset; mso-width-alt: 2706; width: 56pt;" span="2" width="74" /> <col style="mso-width-source: userset; mso-width-alt: 2194; width: 45pt;" width="60" /> <col style="mso-width-source: userset; mso-width-alt: 2742; width: 56pt;" width="75" /> <col style="mso-width-source: userset; mso-width-alt: 2706; width: 56pt;" width="74" /> <col style="mso-width-source: userset; mso-width-alt: 2230; width: 46pt;" width="61" /> </colgroup>
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
    </tr>
    """

        for _, row in filtered_df.iterrows():
            colors_type = row['Colors Type']
            imprint = row['Imprint']

            prices = []
            for col in filtered_df.columns[6:15]:
                price = row[col]
                cleaned_price = price.replace('$', '').replace(',', '').strip() if isinstance(price, str) else "0.00"
                try:
                    prices.append(f"{float(cleaned_price):.2f}")
                except ValueError:
                    prices.append("0.00")

            variable_name = f"{'bb' if imprint.lower() == 'blank' else 'pwl'}_{'n' if colors_type.lower() == 'white' else 'c'}"

            js_code += f"/* {colors_type} {imprint} Start */\n"
            js_code += f"var {variable_name} = {{qty}} < 12 ? {prices[0]} : ({{qty}} < 24 ? {prices[1]} : ({{qty}} < 36 ? {prices[2]} : ({{qty}} < 72 ? {prices[3]} : ({{qty}} < 144 ? {prices[4]} : ({{qty}} < 288 ? {prices[5]} : ({{qty}} < 576 ? {prices[6]} : ({{qty}} < 1008 ? {prices[7]} : ({{qty}} < 2016 ? {prices[8]} : {prices[-1]}))))))));\n"
            js_code += f"/* {colors_type} {imprint} End */\n\n"

            html_code += f"<tr><td>{colors_type}</td>" + "".join([f"<td>${price}</td>" for price in prices]) + "</tr>"

        html_code += "</tbody></table>"
        return js_code, html_code

    except Exception as e:
        return f"An error occurred: {e}", ""

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')  # Serve the index.html directly from the current folder

@app.route('/fetch_data')
def fetch_data():
    bfw_item_code = request.args.get('bfw_item_code', '')
    file_path = "./files.xlsx"

    js_code, html_code = generate_js_and_html_from_excel(file_path, bfw_item_code)

    return jsonify(js_code=js_code, html_code=html_code)

if __name__ == '__main__':
    app.run(debug=True)
