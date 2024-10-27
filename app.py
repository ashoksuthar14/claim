import streamlit as st
from datetime import datetime
from fpdf import FPDF

# Function to generate PDF from filled form details
def generate_pdf(form_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 12)

    # Title
    pdf.cell(200, 10, "Insurance Claim Form", ln=True, align="C")
    pdf.ln(10)

    # Add form details to PDF
    pdf.set_font("Arial", "", 10)
    for section, fields in form_data.items():
        pdf.cell(200, 10, f"{section}", ln=True, align="L")
        for label, value in fields.items():
            pdf.cell(0, 10, f"{label}: {value}", ln=True, align="L")
        pdf.ln(5)

    # Save PDF
    pdf_output = "claim_form.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Streamlit App Layout
st.title("Professional Insurance Claim Form")
st.write("Please fill in the following details to proceed with your insurance claim.")

# Section 1: Insurance Claim Details
st.header("1. Insurance Claim Details")
st.subheader("Client Information")

col1, col2, col3 = st.columns(3)
with col1:
    client_name = st.text_input("Client's Name", placeholder="Last Name, First Name, Middle Initial")
with col2:
    birth_date = st.date_input("Birth Date")
with col3:
    sex = st.radio("Sex", options=["M", "F"])

st.subheader("Insurance Information")
insured_name = st.text_input("Insured's Name", placeholder="Last Name, First Name, Middle Initial")
policy_number = st.text_input("Policy Number", placeholder="Enter Policy or Group Number")
claim_code = st.text_input("Claim Code (Designated by NUCC)", placeholder="Optional")

st.subheader("Address and Contact Details")
client_address = st.text_input("Client's Address", placeholder="Street Address")
city, state, zip_code = st.columns(3)
with city:
    client_city = st.text_input("City")
with state:
    client_state = st.text_input("State")
with zip_code:
    client_zip = st.text_input("ZIP Code")
client_phone = st.text_input("Telephone (Include Area Code)", placeholder="e.g., +1 555-555-5555")

# Section 2: Damage Detection and Cost Estimation
st.header("2. Damage Detection and Cost Estimation")
st.subheader("Damage and Cost Details")
total_repair_cost = st.number_input("Total Estimated Repair Cost ($)", value=473.83, step=0.01)

# Damage Breakdown
st.write("### Cost Breakdown by Damage Type")
medium_deformation = st.number_input("Medium Deformation", value=473.83, step=0.01)

# Section 3: Fraud Detection
st.header("3. Fraud Detection")
fraud_status = st.selectbox("Is the Claim Fraudulent?", options=["No", "Yes", "Pending Investigation"])

# Section 4: Additional Claim Details
st.header("4. Additional Claim Details")
illness_date = st.date_input("Date of Illness, Injury, or Pregnancy (if applicable)")
unable_to_work_from = st.date_input("Unable to Work From (if applicable)")
unable_to_work_to = st.date_input("Unable to Work To (if applicable)")

st.subheader("Hospitalization and Service Details")
hospitalization_from = st.date_input("Hospitalization From")
hospitalization_to = st.date_input("Hospitalization To")
total_charge = st.number_input("Total Charge", value=0.00, step=0.01)
amount_paid = st.number_input("Amount Paid", value=0.00, step=0.01)
balance_due = st.number_input("Balance Due", value=total_charge - amount_paid, step=0.01, format="%.2f")

# Section 5: Signature and Authorization
st.header("5. Signature and Authorization")
st.write("Please review all the information above and sign to authorize this claim.")
signature = st.text_input("Authorized Signature", placeholder="Enter your full name")
claim_date = st.date_input("Date of Claim", value=datetime.today())

# Submit Button
if st.button("Submit Claim"):
    # Collect form data
    form_data = {
        "Client Information": {
            "Client's Name": client_name,
            "Birth Date": birth_date,
            "Sex": sex,
            "Telephone": client_phone,
            "Address": client_address,
            "City": client_city,
            "State": client_state,
            "ZIP Code": client_zip,
        },
        "Insurance Information": {
            "Insured's Name": insured_name,
            "Policy Number": policy_number,
            "Claim Code": claim_code
        },
        "Damage Detection and Cost Estimation": {
            "Total Estimated Repair Cost": total_repair_cost,
            "Medium Deformation": medium_deformation
        },
        "Fraud Detection": {
            "Is Claim Fraudulent": fraud_status
        },
        "Additional Claim Details": {
            "Date of Illness/Injury": illness_date,
            "Unable to Work From": unable_to_work_from,
            "Unable to Work To": unable_to_work_to,
            "Hospitalization From": hospitalization_from,
            "Hospitalization To": hospitalization_to,
            "Total Charge": total_charge,
            "Amount Paid": amount_paid,
            "Balance Due": balance_due
        },
        "Signature and Authorization": {
            "Authorized Signature": signature,
            "Date of Claim": claim_date
        }
    }

    # Generate PDF and provide download link
    pdf_path = generate_pdf(form_data)
    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Download Filled Claim Form as PDF",
            data=pdf_file,
            file_name="insurance_claim_form.pdf",
            mime="application/pdf"
        )

    # Display a thank you message on submission
    st.success("Thank you! Your claim has been submitted successfully.")
    st.write("Our team will review the details and contact you if any further information is needed.")
