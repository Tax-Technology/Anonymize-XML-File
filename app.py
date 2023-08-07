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
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = faker_instance.text()
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    value[index] = faker_instance.text()

        anonymized_xml = xmltodict.unparse(data)
        return anonymized_xml
    except Exception as e:
        st.error(e)

def get_download_link(file_name, data):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/xml;base64,{b64}" download="{file_name}">Click here to download {file_name}</a>'
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
