from flask import Flask, jsonify, request  # Import the request module
from elasticsearch import Elasticsearch
import pandas as pd;
app = Flask(__name__)

es_host = 'localhost'
es_port = 9200
es = Elasticsearch(hosts=[{'host': es_host, 'port': es_port}])

@app.route('/get_data/<index_name>', methods=['GET'])  # Add index_name parameter
def get_data(index_name):  # Add index_name parameter to the function
    try:
        # Perform an Elasticsearch query to get data based on the index name
        query = {
            "query": {
                "match_all": {}
            },
        "size": 30,
        }
        resp = es.search(index=index_name, body=query)
        
        # Extract the source data from the search response
        hits = resp['hits']['hits']
        data = [hit['_source'] for hit in hits]
        df = pd.DataFrame(data)
        df['price'] = df['price'].str.replace('PKR', '').str.replace('lacs', '').str.replace(',', '').astype(float)
        
        # Filter and sort data
        engine_capacity_filter = "660 cc"  # Set the engine capacity filter
        filtered_df = df[df['engine-capacity'] == engine_capacity_filter]
        sorted_df = filtered_df.sort_values(by='price', ascending=True)
        
        # Convert the sorted DataFrame to JSON
        sorted_json = sorted_df.to_json(orient='records', default_handler=str)
        
        return sorted_json, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
