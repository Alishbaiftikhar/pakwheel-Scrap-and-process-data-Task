from flask import Flask, render_template
import requests
import pandas as pd
def fetch_data_from_api(index_name):
    api_url = f'http://localhost:5000/get_data/{index_name}'
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            fetched_data = response.json()
            # print(fetched_data)
            # df = pd.DataFrame(fetched_data)
            # print(df)
            return render_template('frontend.html', data=fetched_data)
            # df['price'] = df['price'].str.replace('PKR', '').str.replace('lacs', '').str.replace(',', '').astype(float)
            # sorted_df = df.sort_values(by='price', ascending=True)
            # filtered_df = df.sort_values(by='engine-capacity', ascending=False)
            # ordered_columns = ['title', 'price', 'place', 'engine-capacity', 'Registered In', 'image']
            # sorted_df = sorted_df[ordered_columns]
            # filtered_df=filtered_df[ordered_columns]
            # # print(filtered_df)
            # print(sorted_df)

            # print("Fetched data:", fetched_data)
        else:
            print("Failed to fetch data from the API")
    except Exception as e:
        print("Error fetching data:", e)
fetch_data_from_api("pak-string")