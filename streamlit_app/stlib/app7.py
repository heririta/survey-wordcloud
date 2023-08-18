description = "Pertanyaan 4"

# Your app goes in the function run()


def run():

    import os
    import streamlit as st
    from st_aggrid import AgGrid, GridUpdateMode
    from st_aggrid.grid_options_builder import GridOptionsBuilder

    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import urllib.parse
    from datetime import datetime
    import pandas as pd
    import glob
    from datetime import date
    import time
    from wordcloud import WordCloud
    import nltk
    from nltk.corpus import stopwords

    import matplotlib.pyplot as plt

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

    # Define the Google News API endpoint
    api_url = "https://news.google.com/rss/search?"

    # Define a function to fetch news articles for a given keyword, language, and date range
    def get_news_articles(keyword, language, start_date=None, end_date=None):
        # Construct the API request URL
        params = {
            "q": keyword,
            "hl": language
        }
        url = api_url + urllib.parse.urlencode(params)
        # Send a GET request to the API
        response = requests.get(url)
        # Parse the XML response
        rss_feed = response.text
        # Create an empty list to store the news data
        news_data = []
        # Extract the relevant information from the XML
        for item in rss_feed.split("<item>")[1:]:
            link = item.split("<link>")[1].split("</link>")[0]
            title = item.split("<title>")[1].split("</title>")[0]
            date = item.split("<pubDate>")[1].split("</pubDate>")[0]
            description = item.split("<description>")[
                1].split("</description>")[0]
            # Convert the date string to a datetime object
            pub_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
            # Check if the article's date is within the specified range
            if start_date and pub_date < start_date:
                continue
            if end_date and pub_date > end_date:
                continue
            # Append the data to the list
            news_data.append((link, title, date, description, keyword))
        # Return the list of news articles
        return news_data

    # # Load the data from the "data_bank.csv" file
    # data_pathsource = './sources'

    # objects_df_all_news_edited = read_csv_files(data_pathsource, delimiter=',')
    # # st.dataframe(objects_df_all_news_edited)

    # Create a function to generate and display the word cloud

    def generate_wordcloud(text, bank):

        # Create a WordCloud object
        wordcloud = WordCloud(width=800, height=400,
                              background_color='white').generate(text)

        # Display the WordCloud
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Word Cloud - {bank}')
        plt.axis('off')
        st.pyplot()

    def generate_wordcloudSurvey(column_name):
        # Membaca data dari file Excel
        excel_file_path = './uploads/LPS_@IKN_Survey2023-08-17_21_10_45.xlsx'
        sheet_name = 'Sheet1'
        # Ganti dengan nama kolom yang ingin Anda buat word cloud-nya
        column_name = column_name

        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        # Menggabungkan semua teks dalam kolom menjadi satu teks panjang
        text = ' '.join(df[column_name].dropna().astype(str))

        # Menggunakan stopwords Bahasa Indonesia dari nltk
        nltk.download('stopwords')
        stop_words = set(stopwords.words('indonesian'))

        # Menambahkan stopwords tambahan
        additional_stop_words = ['lingkungan', 'kantor']
        stop_words.update(additional_stop_words)

        # Membersihkan stopwords dari teks
        filtered_words = [
            word for word in text.split() if word.lower() not in stop_words]

        # Menggabungkan kata-kata yang tersaring kembali menjadi satu teks
        cleaned_text = ' '.join(filtered_words)

        # Membuat word cloud
        wordcloud = WordCloud(width=800, height=400,
                              background_color='white').generate(cleaned_text)

        # Menampilkan word cloud menggunakan matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
        st.pyplot()

    def get_filenames(folder_path):
        filenames = []
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                filenames.append(filename)
        return filenames

    import nltk
    nltk.download('punkt')
    nltk.download('wordnet')
    import pandas as pd
    import matplotlib.pyplot as plt
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    def plot_word_count(dataframe, column):
        # Create an empty dictionary to store word counts
        word_counts = {}

        # Initialize the lemmatizer
        lemmatizer = WordNetLemmatizer()

        # Iterate over each row in the dataframe
        for index, row in dataframe.iterrows():
            # Get the text value from the specified column
            text = row[column]

            # Tokenize the text into words
            words = word_tokenize(text)

            # Iterate over each word
            for word in words:
                # Lemmatize the word to its root form
                root_word = lemmatizer.lemmatize(word)

                # Check if the root word is already in the dictionary
                if root_word in word_counts:
                    # Increment the count by 1 if the root word exists
                    word_counts[root_word] += 1
                else:
                    # Initialize the count to 1 if the root word is new
                    word_counts[root_word] = 1

        # Create a new dataframe to store the word counts
        word_counts_df = pd.DataFrame.from_dict(
            word_counts, orient='index', columns=['Count'])

        # Sort the dataframe by count in descending order
        word_counts_df = word_counts_df.sort_values(
            by='Count', ascending=False)

        # Plot the bar graph
        plt.bar(range(len(word_counts_df)), word_counts_df['Count'])

        # Customize the x-axis labels with the words
        plt.xticks(range(len(word_counts_df)),
                   word_counts_df.index, rotation='vertical')

        # Set the labels and title
        plt.xlabel('Count')
        plt.ylabel('Words')
        plt.title('Word Count')

        # Show the plot
        return st.pyplot()  # plt.show()

    # try:
    #     # st.info(get_filenames(data_pathsource))

    #     # # create_wordcloud(objects_df_all_news_edited)
    #     # pivot_df = objects_df_all_news_edited.pivot_table(
    #     #     index='Date', columns='Object', values='Title', aggfunc=' '.join)
    #     # col_opt = st.selectbox(label='Select ',
    #     #                        options=pivot_df.columns)
    #     # # Combine the text from the selected column
    #     # text = ' '.join(pivot_df[col_opt].dropna())
    #     # # generate_wordcloud(text, col_opt)
    #     # # Assuming you already have a dataframe named 'df' and a column named 'text'
    #     # plot_word_count(objects_df_all_news_edited, 'Title')
    #     # # st.dataframe(objects_df_all_news_edited)

    #     # # Filter DataFrame based on user input
    #     # search_term = col_opt
    #     # # filtered_df = objects_df_all_news_edited[objects_df_all_news_edited['Object'].str.contains(col_opt, case=False)]
    #     # filtered_df = objects_df_all_news_edited[objects_df_all_news_edited['Object'] == search_term]

    #     # # Display filtered results with clickable URLs
    #     # for index, row in filtered_df.iterrows():
    #     #     st.write(row['Date'])
    #     #     st.info(row['Title'])
    #     #     st.write(row['Link'], unsafe_allow_html=True)

    #     # Contoh penggunaan
    #     directory_path = './uploads'
    #     excel_file_name = 'LPS_@IKN_Survey2023-08-17_21_10_45.xlsx'
    #     sheet_name = 'Sheet1'

    #     objectdata_frame = read_excel_files(
    #         directory_path, excel_file_name, sheet_name)
    #     st.dataframe(objectdata_frame)
    #     st.columns(objectdata_frame)

    # except:
    #     st.info("No Generate")

    # Contoh penggunaan
    directory_path = './uploads'
    excel_file_name = 'LPS_@IKN_Survey2023-08-17_21_10_45.xlsx'
    sheet_name = 'Sheet1'

    objectdata_frame = read_excel_files(
        directory_path, excel_file_name, sheet_name)

    # st.write(list(objectdata_frame.columns))
    # st.dataframe(objectdata_frame)

    # st.info('1. Apakah tema yang sesuai untuk Kantor LPS di IKN ?')
    # generate_wordcloudSurvey(
    #     column_name='1. Apakah tema yang sesuai untuk Kantor LPS di IKN ?')
    # plot_word_count(objectdata_frame,
    #                 '1. Apakah tema yang sesuai untuk Kantor LPS di IKN ?')
    st.info('4. Berikan pendapat dan saran Anda untuk pembangunan kantor LPS di IKN')
    generate_wordcloudSurvey(
        column_name='4. Berikan pendapat dan saran Anda untuk pembangunan kantor LPS di IKN')
    # plot_word_count(objectdata_frame,
    #                 '4. Berikan pendapat dan saran Anda untuk pembangunan kantor LPS di IKN')

    # gd = GridOptionsBuilder().from_dataframe(objects_df_all_news_edited)
    # gd.configure_pagination(enabled=True)
    # gd.configure_default_column(editable=True, groupable=True)

    # # gd.configure_selection(selection_mode='single', use_checkbox=True, )
    # gridoptions = gd.build()
    # grid_table = AgGrid(objects_df_all_news_edited, gridOptions=gridoptions,
    #                     update_mode=GridUpdateMode.SELECTION_CHANGED,
    #                     height=500, allow_unsafe_jscode=True, enable_quicksearch=True)

    # sel_row = grid_table["selected_rows"]
    # st.write(sel_row)

    # st.dataframe(objects_df_all_news_edited)


# end of app
# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
