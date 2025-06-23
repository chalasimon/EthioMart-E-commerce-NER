# import libraries
import pandas as pd
import numpy as np
from etnltk.lang.am import (preprocessing,clean_amharic)
from etnltk.lang.am import normalize


class Preprocessor:
    def __init__(self, data):
        self.data = data
    def remove_duplicates(self, column_name='Message'):
        self.data = self.data.drop_duplicates(subset=[column_name])
    def clean_text(self,column_name='Message'):
        custom_pipeline = [
            preprocessing.remove_emojis,
            ]
        if not pd.api.types.is_string_dtype(self.data[column_name]):
            self.data[column_name] = self.data[column_name].astype(str).replace('nan', '')
            print(f"Column '{column_name}' must be of string type for text cleaning.")
        # Cleans the text data in the DataFrame
        self.data[column_name] = self.data[column_name].apply(
            lambda text: clean_amharic(text, abbrev=False, pipeline=custom_pipeline)
        )
        return self.data[column_name]
    def normalize_text(self, column_name='Message'):
        # Normalizes the text data in the DataFrame
        self.data[column_name] = self.data[column_name].apply(
            lambda text: normalize(text)
        )
        return self.data[column_name]