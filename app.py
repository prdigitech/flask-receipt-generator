from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_receipt():
    # Collect form data
    client_name = request.form.get("client_name")
    amount = request.form.get("amount")
    payment_method = request.form.get("payment_method")
    product = request.form.get("product")
    description = request.form.get("description")

    if not client_name or not amount or not payment_method or not product:
        return "Please fill in all required fields.", 400

    # Construct receipt text
    global receipt_text
    receipt_text = (
        f"Receipt\n"
        f"----------------------------\n"
        f"Client Name: {client_name}\n"
        f"Product: {product}\n"
        f"Amount: ${amount}\n"
        f"Payment Method: {payment_method}\n"
        f"Description: {description}\n"
        f"----------------------------\n"
        f"Thank you for your payment!"
    )
    
    return {"receipt_text": receipt_text}

@app.route("/download")
def download_pdf():
    if not receipt_text:
        return "No receipt available. Please generate one first.", 400

    # Create a PDF file in memory
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.drawString(100, 750, "Payment Receipt")
    c.drawString(100, 730, "----------------------------")

    # Split the receipt text by lines and write to the PDF
    y_position = 710
    for line in receipt_text.split("\n"):
        c.drawString(100, y_position, line)
        y_position -= 20

    c.save()
    pdf_buffer.seek(0)

    # Send the PDF as a downloadable file
    return send_file(pdf_buffer, as_attachment=True, download_name="receipt.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
