import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO
from faker import Faker

def anonymize_xml_element(element, idx):
    fake = Faker()
    original_text = element.text
    fake_text = fake.text(max_nb_chars=len(original_text))
    element.text = fake_text

def anonymize_xml(xml_content):
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()

    for idx, element in enumerate(root.iter()):
        try:
            anonymize_xml_element(element, idx)
        except Exception as e:
            print(e)

    output = StringIO()
    tree.write(output, encoding="unicode")
    return output.getvalue()

def main():
    st.title("XML Data Anonymizer")
    st.write("Upload an XML file below and click the 'Anonymize' button to remove sensitive data.")
    
    uploaded_file = st.file_uploader("Upload XML File", type=["xml"])

    if uploaded_file is not None:
        xml_content = uploaded_file.read()

        if st.button("Anonymize"):
            try:
                anonymized_xml = anonymize_xml(xml_content)
            except Exception as e:
                st.error(e)

            st.download_button(
                "Download Anonymized XML",
                data=anonymized_xml,
                file_name="anonymized.xml",
                mime="text/xml",
            )

if __name__ == "__main__":
    main()
