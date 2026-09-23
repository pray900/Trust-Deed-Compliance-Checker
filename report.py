# report.py
from fpdf import FPDF
 
def export_report(results, output_path="compliance_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Trust Deed Compliance Report", ln=True, align='C')
 
    for r in results:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 8, txt=f"{r['status']} | Score: {r['score']}")
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(0, 6, txt=f"Regulation: {r['regulation']}")
        pdf.multi_cell(0, 6, txt=f"Matched Clause: {r['best_matching_clause'][:300]}")
 
    pdf.output(output_path)