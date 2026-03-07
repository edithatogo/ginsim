import bibtexparser
import streamlit as st
import yaml

st.set_page_config(page_title="Evidence Explorer", layout="wide")

st.title("🔎 Live Evidence Explorer")
st.markdown("""
This page provides **Diamond-Standard Traceability** for all model inputs.
Every parameter in the model is grounded in empirical evidence and specific assumptions.
""")


def load_data():
    with open("context/assumptions_registry.yaml") as f:
        assumptions = yaml.safe_load(f)["assumptions"]
    with open("context/references.bib") as f:
        bib_db = bibtexparser.load(f)
        bib_dict = {entry["ID"]: entry for entry in bib_db.entries}
    return assumptions, bib_dict


assumptions, bib = load_data()

# Sidebar: Filter by Assumption
selected_aid = st.sidebar.selectbox("Select Assumption", list(assumptions.keys()))
a_data = assumptions[selected_aid]

st.header(f"Assumption {selected_aid}: {a_data['category']}")
st.subheader(a_data["statement"])

col1, col2 = st.columns(2)

with col1:
    st.info("**Rationale**")
    st.write(a_data["rationale"])
    st.write(f"**Jurisdiction:** {a_data['jurisdiction']}")
    st.write(f"**Status:** `{a_data['status']}`")

with col2:
    st.success("**Evidence Basis**")
    for ref_id in a_data.get("evidence_basis", []):
        if ref_id in bib:
            entry = bib[ref_id]
            st.markdown(f"- **{entry.get('author', 'Unknown')} ({entry.get('year', 'N/A')})**")
            st.markdown(f"  *{entry.get('title', 'Untitled')}*")
            if "doi" in entry:
                st.caption(f"DOI: {entry['doi']}")
        else:
            st.warning(f"Reference '{ref_id}' not found in bibliography.")

st.divider()

st.subheader("📈 Parameter Sensitivity Impact")
st.write("This assumption directly influences the following code paths and surfaces:")
for surface in a_data.get("active_surfaces", []):
    st.code(surface, language="text")
