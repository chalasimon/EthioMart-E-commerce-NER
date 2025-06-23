#import libraries
import os
import pandas as pd

class DataLoader:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = None

    def load_data(self):
        """Loads data from a CSV file into a pandas DataFrame."""
        if os.path.exists(self.csv_file):
            self.data = pd.read_csv(self.csv_file)
            print(f"Data loaded successfully from {self.csv_file}.")
        else:
            print(f"File {self.csv_file} does not exist.")
            self.data = pd.DataFrame()  # Return an empty DataFrame if file does not exist

    def get_data(self):
        """Returns the loaded data."""
        return self.data