import streamlit as st
import faker
import xmltodict
import base64

def anonymize_xml(xml_file):
    if xml_file is None:
        return None

    try:
        xml_data = xml_file.read()  # Read the contents of the uploaded file

        data = xmltodict.parse(xml_data)

        faker_instance = faker.Faker()
        _anonymize_node(data, faker_instance)

        anonymized_xml = xmltodict.unparse(data)
        return anonymized_xml
    except Exception as e:
        st.error(e)

def _anonymize_node(node, faker_instance):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str):
                node[key] = faker_instance.text() if not key.startswith('@') else value
            elif isinstance(value, list):
                for item in value:
                    _anonymize_node(item, faker_instance)
            elif isinstance(value, dict):
                _anonymize_node(value, faker_instance)

def get_download_link(file_name, data):
    b64_encoded_data = base64.b64encode(data).decode()
    href = f'<a href="data:application/xml;charset=utf-8;base64,{b64_encoded_data}" download="{file_name}">Click here to download {file_name}</a>'
    return href

def main():
    st.title("XML Anonymizer")

    xml_file = st.file_uploader("Upload XML file")

    if xml_file is not None:
        with st.spinner("Anonymizing XML..."):
            anonymized_data = anonymize_xml(xml_file)

            if anonymized_data is not None:
                anonymized_data_bytes = anonymized_data.encode("utf-8")

                # Create a link to download the file
                st.markdown(get_download_link(file_name="anonymized.xml", data=anonymized_data_bytes), unsafe_allow_html=True)
    else:
        st.error("Please upload an XML file.")

if __name__ == "__main__":
    main()
