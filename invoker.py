from flask import Flask, jsonify, request
from redis import Redis
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from cachetools import TTLCache
import requests
import json

app = Flask(__name__)

# Create two levels of cache: TTLCache and Redis
local_cache = TTLCache(maxsize=3, ttl=10)
redis_client = Redis(host='localhost', port=6379)

# URL of generator application 
GENERATOR_APP_URL = 'https://localhost/generate'

# Cascade function to call the generator service
def runcascade(modelnames):
    results = []

    # Creating the tasks for our ThreadPoolExecutor
    def fetch_data(modelname):
        response = requests.post(GENERATOR_APP_URL, json={'modelname': modelname, 'viewerid': '123445'})
        return response.json()

    # Feeding tasks to ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_data, modelname) for modelname in modelnames]

        # Using as.completed to retreive data from the tasks that are already completed, without waiting for the whole pool 
        for future in concurrent.futures.as_completed(futures):
            response = future.result()
            results.append(response)

    return results

# Function to get data from cache
def get_from_cache(key):
    result = local_cache.get(key)
    if result is None:
        result = redis_client.get(key)
        if result is not None:
            result = json.loads(result)
            local_cache[key] = result
    return result

# Function to set data to cache
def set_to_cache(key, value):
    local_cache[key] = value
    redis_client.set(key, json.dumps(value))


@app.route('/recommend', methods=['POST'])
def recommend():
    # getting user_id form the request, and creating a unique caching key
    
    user_id = request.json.get('viewerid')
    cache_key = f"user:{user_id}"

    # checking the cache, and if it is empty, executing runcascade() function
    result = get_from_cache(cache_key)
    if result is None:
        modelnames = ['model1', 'model2', 'model3', 'model4', 'model5']
        cascade_results = runcascade(modelnames)
        merged_result = {'results': cascade_results}
        set_to_cache(cache_key, merged_result)
        result = merged_result
    return jsonify(result)

if __name__ == '__main__':
    app.run()