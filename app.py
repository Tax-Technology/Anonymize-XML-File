import streamlit as st
import faker
import xmltodict
import io

def anonymize_xml(xml_file):
    if xml_file is None:
        return None

    try:
        with open(xml_file, "r") as f:
            xml_data = f.read()

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

def main():
    st.title("XML Anonymizer")

    xml_file = st.file_uploader("Upload XML file")

    if xml_file is not None:
        with st.progress(0):
            anonymized_data = anonymize_xml(xml_file)
            st.progress(50)

            # Encode the string as bytes
            anonymized_data_bytes = anonymized_data.encode("utf-8")

            # Create a link to download the file
            st.markdown(get_download_link(anonymized_data_bytes, "anonymized.xml"), unsafe_allow_html=True)

            st.progress(100)
    else:
        st.error("Please upload an XML file.")

def get_download_link(data, file_name):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{file_name}">Click here to download {file_name}</a>'
    return href

if __name__ == "__main__":
    main()
