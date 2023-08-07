import streamlit as st
import faker
import xmltodict

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
            try:
                anonymized_data = anonymize_xml(xml_file)
                st.progress(50)

                st.download_button("Download Anonymized XML", data=anonymized_data, file_name="anonymized.xml")

                st.progress(100)
            except Exception as e:
                st.error(e)

if __name__ == "__main__":
    main()
