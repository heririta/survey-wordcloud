description = "Data sources"

# Your app goes in the function run()


def run():

    import streamlit as st

    # st.header("Example app 2")
    import os
    import streamlit as st
    import glob
    import pandas as pd

    def delete_files_in_folder(folder):
        file_list = os.listdir(folder)
        for file_name in file_list:
            file_path = os.path.join(folder, file_name)
            os.remove(file_path)

    def list_files_in_folder(folder_path):
        files = os.listdir(folder_path)
        return files

    def download_file(file_path):
        with open(file_path, "rb") as file:
            file_contents = file.read()
        return file_contents

    def read_csv_files(directory, delimiter=';'):
        # Get all CSV files in the directory
        csv_files = glob.glob(directory + '/*.csv')

        # Initialize an empty list to store the DataFrames
        data_frames = []

        # Read each CSV file and store its DataFrame
        for csv_file in csv_files:
            df = pd.read_csv(csv_file, delimiter=delimiter)
            if not df.empty:
                data_frames.append(df)

        # Check if any DataFrames were read
        if not data_frames:
            # raise ValueError("No data found in CSV files.")
            st.info("No data found in CSV files.")

        # Combine all DataFrames into a single DataFrame
        combined_df = pd.concat(data_frames, ignore_index=True)

        return combined_df

    # st.title("Multifile Uploader to Folder")

    # target_folder = st.text_input("Target Folder", "uploads")
    target_folder = "./uploads"

    # Get folder path from user input
    folder_path = st.text_input("Source Folder", target_folder)
    file_list = list_files_in_folder(folder_path)
    if file_list:
        st.write("Files in the folder:")
        for file_name in file_list:
            col0, col1 = st.columns([15, 3])

            with col0:
                file_path = os.path.join(folder_path, file_name)
                icon = "file" if os.path.isfile(file_path) else "folder"
                st.write(
                    f"<i class='fas fa-{icon}'></i> {file_name}", unsafe_allow_html=True)
            with col1:
                file_path = os.path.join(folder_path, file_name)
                download_button = st.button(
                    f"Download", key=f"download_{file_name}")

            if download_button:
                file_contents = download_file(
                    os.path.join(folder_path, file_name))
                st.download_button(label="Click to Download", data=file_contents,
                                   file_name=file_name, key=f"download_button_{file_name}")
    else:
        st.write("No files found in the folder.")

    delete_button = st.button("Delete Files")
    if delete_button:
        # Start a loop for the progress bar
        delete_files_in_folder(folder_path)
        st.experimental_rerun()

        # Specify the directory containing the CSV files
    csv_directory = './uploads'

    try:
        # Call the function to read all CSV files in the directory and combine them
        result_df = read_csv_files(csv_directory, delimiter=';')

        # Perform operations on the resulting DataFrame
        # For example, you can print the first few rows of the data
        # print(result_df.head())
        st.dataframe(result_df)
        st.info(result_df.shape)
    except ValueError as e:
        print(str(e))

# end of app


# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
