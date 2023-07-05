PHONEPE PULSE  DATA VISUALIZATION
=================================
ABOUT:
    *   PhonePe Pulse is a repository or dataset that contains transaction and user-related data from the PhonePe digital payments platform. PhonePe is a popular digital payments app in India that allows users to make various transactions, such as money transfers, bill payments, mobile recharges, and online purchases, using their smartphones.

    *  The PhonePe Pulse dataset is a valuable resource for analyzing the trends, patterns, and performance of the digital payments ecosystem in India. It provides insights into the usage patterns, transaction volumes, and user behavior on the PhonePe platform.

    *   The dataset likely includes various data points, such as transaction amounts, transaction types, user demographics, timestamps, locations (states and districts), and app usage metrics (such as app openings and registrations).

WORKFLOW:

This project aims to visualize and analyze data from the PhonePe Pulse repository using Python, Streamlit, and MySQL. The workflow involves the following steps:

1. Data Retrieval: The data is fetched from the PhonePe Pulse repository using Git Clone.

2. Data Preprocessing: The retrieved data is read and stored in DataFrames using the os module. Multiple DataFrames are created to hold aggregated transaction data, aggregated user data, mapped transaction data, mapped user data, top transaction data, and top user data.

3. Data Storage: A connection is established with MySQL using the MySQL Connector, and the DataFrames are converted into tables stored in the MySQL database.

4. Streamlit Web App: The data is extracted from MySQL and displayed in an interactive web app built with Streamlit.

   - Option 1: The app shows the total transaction count, transaction amount, registered users, and app openings through an India map for a specific year and quarter. Users can use a slider to change the year and quarter to view the data accordingly.

   - Option 2: Provides an overall analysis for years 2018 to 2022, showing transaction count, transaction amount, registered users, and app openings.

   - Option 3: Transaction Analysis -Explore transaction count and amount by selecting transaction type and district. Gain insights into transaction patterns and regional preferences.

   - Option 4: User Analysis - Visualize registered users and app openings for states and districts. Understand user adoption and app engagement at a regional level.

   - Option 5: Top Charts - Displays the top 3 states for the transaction amount, transaction count, registered users, and app openings for a chosen year and quarter. The year and quarter can be adjusted using a slider.

The Streamlit web app provides an easy-to-use interface for users to explore and gain insights from the PhonePe Pulse data. By following this workflow, others can understand how to collect, preprocess, store, and visualize data from the PhonePe Pulse repository for various analyses.

       

