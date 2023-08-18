description = "Upload file"

# Your app goes in the function run()


def run():

    import streamlit as st

    # st.header("Example app 2")
    import os
    import streamlit as st

    def delete_files_in_folder(folder):
        file_list = os.listdir(folder)
        for file_name in file_list:
            file_path = os.path.join(folder, file_name)
            os.remove(file_path)

    def save_uploaded_files(uploaded_files, target_folder):
        allowed_extensions = [".docx", ".doc", ".csv", ".pdf", ".txt",".xlsx"]

        for file in uploaded_files:
            file_name = file.name
            file_ext = os.path.splitext(file_name)[1].lower()

            if file_ext in allowed_extensions:
                file_path = os.path.join(target_folder, file_name)

                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

                # st.write(f"Saved file: {file_name}")
            else:
                st.write(f"File {file_name} is not allowed. Skipping.")

    # target_folder = st.text_input("Target Folder", "uploads")
    target_folder = "./uploads"
    os.makedirs(target_folder, exist_ok=True)

    uploaded_files = st.file_uploader(
        "Upload files", accept_multiple_files=True)
    # st.write("File upload .docx, .doc, .csv, .pdf, .txt")

    if uploaded_files:
        delete_files_in_folder(target_folder)
        if st.button("Save Files"):
            save_uploaded_files(uploaded_files, target_folder)
            st.success("Upload completed!")

        # list_files_in_folder(target_folder)


# end of app


# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
