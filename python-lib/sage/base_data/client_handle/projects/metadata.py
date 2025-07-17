import pandas as pd

def main(client):
    # Create a dictionary to hold the data
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 22, 35],
        'City': ['New York', 'London', 'Paris', 'Tokyo']
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    return df