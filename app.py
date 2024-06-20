import streamlit as st
import pandas as pd
import openai
import fitz  # PyMuPDF
import requests
from io import StringIO

# Initialize OpenAI with your API key
openai.api_key = 'Replace with your actual API key'

# Function to extract text from multiple PDFs
def extract_text_from_pdfs(pdf_files):
    extracted_texts = []
    for pdf_file in pdf_files:
        pdf_file.seek(0)
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        extracted_texts.append(text)
    return " ".join(extracted_texts)

# Function to generate risk template using OpenAI API
def generate_risk_template(business_profile, project_profile, tool_profile, extra_comments, standards_text, template_style):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    style_comment = "Generate a longer list of risks (20-30)." if template_style == "Long & Granular" else "Generate a shorter list of risks (<10)."
    prompt = f"""
    Business Profile: {business_profile}
    Project Profile: {project_profile}
    Tool Profile: {tool_profile}
    Extra Comments: {extra_comments}
    Relevant Standards and Regulations: {standards_text}

    Number of risks in template: {style_comment}

    Generate a comprehensive risk assessment template that is based on the above information.

    The template CSV format: 7 columns 1 header row, there should be nothing outside of this format. Header titles: Risk category, Risk, Control, Mitigation, Relevant Vendor Info/Docs, Reference, Risk Explainer. Risks should be mutually exclusive, collectively exhaustive and reference where the information came from.

    The wording should be succinct, short and sharp with examples. This should be easily read by a risk manager who only has basic technical understanding.

    Risk explainer column should have short explainers for a non-technical audience with examples.

    Relevant Vendor Info/Docs column refers to where the inputter could potentially find this information, this should help them look in the right place, quickly.
    """
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response_json = response.json()
    if 'choices' in response_json:
        return response_json['choices'][0]['message']['content'].strip()
    else:
        return "Error in response: " + str(response_json)

# Streamlit app
st.title("Virtual Risk Project Manager")

# Step-by-step user input collection
st.header("Risk Profile")
st.write("Let's start by understanding the context.")

# Initialize session state for input data
if 'business_profile' not in st.session_state:
    st.session_state['business_profile'] = ''
if 'project_profile' not in st.session_state:
    st.session_state['project_profile'] = ''
if 'tool_profile' not in st.session_state:
    st.session_state['tool_profile'] = ''
if 'extra_comments' not in st.session_state:
    st.session_state['extra_comments'] = ''
if 'template_style' not in st.session_state:
    st.session_state['template_style'] = 'Short & Succinct'

# Step 2: User inputs Profile of business
st.session_state['business_profile'] = st.text_input("Profile of Business (industry, size & geography)", value=st.session_state['business_profile'])

# Step 3: User inputs Profile of project
st.session_state['project_profile'] = st.text_input("Profile of Project (R&D or production)", value=st.session_state['project_profile'])

# Step 4: User inputs Profile of tool
st.session_state['tool_profile'] = st.text_input("Profile of Tool (technology components)", value=st.session_state['tool_profile'])

# Step 5: Extra comments from user
st.session_state['extra_comments'] = st.text_area("Extra Comments about your bespoke risk process", value=st.session_state['extra_comments'])

# Step 6: Placeholder for frameworks/regulations selection
st.subheader("Select the relevant frameworks/regulations")
col1, col2, col3 = st.columns(3)
if col1.button("GDPR"):
    pass  # Placeholder
if col2.button("NIST"):
    pass  # Placeholder
if col3.button("ISO"):
    pass  # Placeholder

# Step 7: User uploads relevant standards & regulations
uploaded_files = st.file_uploader("Upload relevant standards & regulations (PDFs)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    standards_text = extract_text_from_pdfs(uploaded_files)
    st.success("Upload complete!")
else:
    standards_text = ""

# Function to display and download the template
def display_and_download_template(template_text, file_name):
    st.write("Generated Risk Template (Raw Text):")
    st.text(template_text)

    csv_string_io = StringIO(template_text)
    try:
        template_df = pd.read_csv(csv_string_io)
        st.write("Generated Risk Template (Table):")
        st.dataframe(template_df.style.set_table_styles(
            [{'selector': 'table', 'props': [('width', '100%'), ('display', 'block'), ('overflow', 'auto')]}]
        ))
        st.download_button("Download Template as CSV", data=template_text, file_name=file_name, mime='text/csv')
    except pd.errors.ParserError as e:
        st.error("There was an error parsing the CSV. Please check the format of the response.")
        st.text(str(e))

# Step 8: Generate Risk Template
st.subheader("Generate Risk Template")
col1, col2 = st.columns(2)
if col1.button("Long & Granular"):
    st.session_state['template_style'] = "Long & Granular"
    template_text = generate_risk_template(
        st.session_state['business_profile'],
        st.session_state['project_profile'],
        st.session_state['tool_profile'],
        st.session_state['extra_comments'],
        standards_text,
        st.session_state['template_style']
    )
    display_and_download_template(template_text, 'risk_template.csv')

if col2.button("Short & Succinct"):
    st.session_state['template_style'] = "Short & Succinct"
    template_text = generate_risk_template(
        st.session_state['business_profile'],
        st.session_state['project_profile'],
        st.session_state['tool_profile'],
        st.session_state['extra_comments'],
        standards_text,
        st.session_state['template_style']
    )
    display_and_download_template(template_text, 'risk_template.csv')

# Step 9: User can add comments to re-edit the current template
st.header("Edit Template")
edit_comments = st.text_area("Add comments to amend the template")

# Button to re-generate template with comments
if st.button("Re-Generate Risk Template with Comments"):
    combined_comments = f"{st.session_state['extra_comments']} {edit_comments}".strip()
    updated_template_text = generate_risk_template(
        st.session_state['business_profile'],
        st.session_state['project_profile'],
        st.session_state['tool_profile'],
        combined_comments,
        standards_text,
        st.session_state['template_style']
    )
    display_and_download_template(updated_template_text, 'updated_risk_template.csv')
