# app.py
import streamlit as st
from pdf_parser import extract_clauses
from embedder import get_embedding, embed_all
from matcher import check_regulation
 
st.title("📋 Trust Deed Compliance Checker")
st.caption("Powered by LegalBERT")
 
pdf_file = st.file_uploader("Upload Trust Deed PDF", type="pdf")
reg_input = st.text_area("Paste Regulatory Changes (one per line)")
 
if pdf_file and reg_input and st.button("Run Compliance Check"):
 
    with st.spinner("Parsing deed and building LegalBERT embeddings..."):
        clauses = extract_clauses(pdf_file)
        clause_embeddings = embed_all(clauses)
        regulations = [r.strip() for r in reg_input.strip().split("\n") if r.strip()]
 
    st.subheader("Compliance Report")
    for reg in regulations:
        result = check_regulation(reg, clauses, clause_embeddings, get_embedding)
        color = "green" if "Covered" in result["status"] and "Partial" not in result["status"] else \
                "orange" if "Partial" in result["status"] else "red"
 
        with st.expander(f"{result['status']} — {reg[:80]}..."):
            st.markdown(f"**Similarity Score:** `{result['score']}`")
            st.markdown(f"**Best Matching Clause:**")
            st.info(result['best_matching_clause'][:500])