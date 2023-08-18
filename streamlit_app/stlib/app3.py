description = "List Survey"

# Your app goes in the function run()


def run():

    import os
    import streamlit as st
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import urllib.parse
    from datetime import datetime
    import pandas as pd
    import glob
    from datetime import date
    import time

    from st_aggrid import AgGrid, GridUpdateMode
    from st_aggrid.grid_options_builder import GridOptionsBuilder

    def delete_files_in_folder(folder):
        file_list = os.listdir(folder)
        for file_name in file_list:
            file_path = os.path.join(folder, file_name)
            os.remove(file_path)

    def read_csv_files(directory, delimiter):
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
        try:
            # Combine all DataFrames into a single DataFrame
            combined_df = pd.concat(data_frames, ignore_index=True)
            return combined_df
        except:
            pass

    def read_excel_files(directory, file_name, sheet_name='Sheet1'):
        try:
            file_path = f'{directory}/{file_name}'
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print("Data loaded successfully!")
            return df
        except Exception as e:
            print("Error:", e)
            return None
    # # Define the Google News API endpoint
    # api_url = "https://news.google.com/rss/search?"

    # # Define a function to fetch news articles for a given keyword, language, and date range
    # def get_news_articles(keyword, language, start_date=None, end_date=None):
    #     # Construct the API request URL
    #     params = {
    #         "q": keyword,
    #         "hl": language
    #     }
    #     url = api_url + urllib.parse.urlencode(params)
    #     # Send a GET request to the API
    #     response = requests.get(url)
    #     # Parse the XML response
    #     rss_feed = response.text
    #     # Create an empty list to store the news data
    #     news_data = []
    #     # Extract the relevant information from the XML
    #     for item in rss_feed.split("<item>")[1:]:
    #         link = item.split("<link>")[1].split("</link>")[0]
    #         title = item.split("<title>")[1].split("</title>")[0]
    #         date = item.split("<pubDate>")[1].split("</pubDate>")[0]
    #         description = item.split("<description>")[
    #             1].split("</description>")[0]
    #         # Convert the date string to a datetime object
    #         pub_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
    #         # Check if the article's date is within the specified range
    #         if start_date and pub_date < start_date:
    #             continue
    #         if end_date and pub_date > end_date:
    #             continue
    #         # Append the data to the list
    #         news_data.append((link, title, date, description, keyword))
    #     # Return the list of news articles
    #     return news_data

    # def get_object_from_new_articles(objects_df, start_date, end_date):
    #     # Loop through each row in the dataframe
    #     for _, row in objects_df.iterrows():
    #         # Get the object and keyword from the row
    #         obj = row["Object"]
    #         keyword = row["Keyword"]
    #         # Fetch news articles for the keyword and language within the specified date range
    #         news_data = get_news_articles(
    #             keyword, language="id", start_date=start_date, end_date=end_date)
    #         # Extend the list with the new news data
    #         all_news_data.extend([(link, title, date, description, keyword, obj)
    #                               for link, title, date, description, keyword in news_data])

    #     # Convert the list of tuples into a pandas dataframe
    #     all_news_df = pd.DataFrame(all_news_data, columns=[
    #         "Link", "Title", "Date", "Description", "Keyword", "Object"])

    #     # Set display options for better readability
    #     pd.set_option('display.max_colwidth', 50)
    #     pd.set_option('display.max_columns', None)

    #     # Display the dataframe
    #     # st.dataframe(all_news_df)

    #     # Save the dataframe as a CSV file
    #     # buat folder Indo_hasil dulu, kalao belum error
    #     # save_path = './sources/all_news.csv'
    #     # all_news_df.to_csv(save_path, index=False)

    #     return all_news_df

    # def get_object_from_new_articles_edited(all_news_df, startdate, enddate):
    #     all_news_edited = all_news_df.copy()

    #     # Clean the last word from the 'Title' column in the new DataFrame
    #     all_news_edited['Title'] = all_news_edited['Title'].str.rsplit(
    #         n=1).str[0]
    #     # Create a new column 'date_edited' with the converted date format
    #     # matiin dulu
    #     # all_news_edited['date_edited'] = pd.to_datetime(all_news_edited['Date']).dt.strftime('%d/%m/%Y')

    #     # buat folder Indo_hasil dulu, kalao belum error
    #     save_path = f'./sources/news_{startdate}_{enddate}.csv'
    #     all_news_edited.to_csv(save_path, index=False)

    #     return all_news_edited

    # Load the data from the "data_bank.csv" file
    data_path = './uploads'

    # Contoh penggunaan
    directory_path = './uploads'
    excel_file_name = 'LPS_@IKN_Survey2023-08-17_21_10_45.xlsx'
    sheet_name = 'Sheet1'

    objectdata_frame = read_excel_files(
        directory_path, excel_file_name, sheet_name)

    st.info('Survei singkat mengenai persiapan pembangunan kantor LPS di IKN')
    st.write(list(objectdata_frame.columns))

    gd = GridOptionsBuilder().from_dataframe(objectdata_frame)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True, groupable=True)

    # gd.configure_selection(selection_mode='single', use_checkbox=True, )
    gridoptions = gd.build()
    grid_table = AgGrid(objectdata_frame, gridOptions=gridoptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        height=500, allow_unsafe_jscode=True, enable_quicksearch=True)

    sel_row = grid_table["selected_rows"]
    st.write(sel_row)

    # st.dataframe(objectdata_frame)

    # Specify the desired date range --> ini bedanya kalau mau pakai tanggal tertentu

    # Initialize an empty list to store all the news data for all objects and keywords
    # all_news_data = []

    # # st.dataframe(objects_df)
    # col1, col2 = st.columns(2)

    # with col1:
    #     start_date = st.date_input("Start Date", date.today())
    #     # Convert the selected date to a datetime.datetime object
    #     start_date_obj = datetime.combine(start_date, datetime.min.time())
    # with col2:
    #     end_date = st.date_input("End Date", date.today())
    #     # Convert the selected date to a datetime.datetime object
    #     end_date_obj = datetime.combine(end_date, datetime.min.time())
    # if start_date > end_date:
    #     st.error("Error: Start Date must be before End Date.")
    # else:
    #     st.info("Date range is valid.")

    # # start_date1 = datetime(2023, 4, 1)
    # # end_date1 = datetime(2023, 5, 24)

    # # st.info(start_date1)
    # # st.info(end_date1)
    # # st.info(type(end_date1))

    # # st.info(start_date_obj)
    # # st.info(type(start_date_obj))
    # # st.info(end_date)
    # # st.info(type(end_date))

    # # Initialize progress bar
    # progress_bar = st.progress(0)

    # # Button to start progress
    # start_button = st.button("Generate")

    # if start_button:
    #     # Start a loop for the progress bar
    #     with st.spinner("In progress..."):
    #         obj = get_object_from_new_articles(
    #             objects_df, start_date_obj, end_date_obj)
    #         get_object_from_new_articles_edited(
    #             obj, start_date, end_date)
    #     for i in range(100):
    #         # Update progress bar value
    #         progress_bar.progress(i + 1)

    #         # Delay to simulate some work
    #         time.sleep(0.1)

    #     st.success("Generate completed!")

    # delete_button = st.button("Delete Files")

    # if delete_button:
    #     folder_all_news = "./sources"
    #     # Start a loop for the progress bar
    #     delete_files_in_folder(folder_all_news)

    #
    # st.info("Dataframe saved successfully.")
    # Load the data from the "data_bank.csv" file

    # objects_df_all_news_edited = read_csv_files(data_pathsource, delimiter=',')
    # st.dataframe(objects_df_all_news_edited)


# end of app

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
