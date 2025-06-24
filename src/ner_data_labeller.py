# import libraries
import os
import pandas as pd
from typing import List, Dict, Any

class NERDataLabeller:
    def __init__(self, df):
        self.data = df
        self.labels=[]
        self.entity_types = {
            '1': 'B-PRODUCT', # The beginning of a product entity (e.g., "Baby bottle")
            '2': 'I-PRODUCT', # Inside a product entity  (e.g., the word "bottle" in "Baby bottle")
            '3': 'B-PRICE',   # The beginning of a price entity (e.g., "ዋጋ 1000 ብር","በ1000 ብር")
            '4': 'I-PRICE',   # Inside a price entity  (e.g., the word "1000" in “ዋጋ 1000 ብር”)
            '5': 'B-LOC',     # The beginning of a location entity (e.g., "Addis Ababa")
            '6': 'I-LOC',     # Inside a location entity (e.g., The word Ababa in "Addis Ababa")
            '0': 'O'          # Outside of any entity
        }
    def label_tokens(self, tokens):
        for token in tokens:
            label = input(f"Enter label for token '{token}': ")
            if label == "q":
                print("Exiting labeling.")
                self.labels.append((token, "O"))  # Default label for exit
                return self.labels
            self.labels.append((token, label))
        return self.labels

    def retrieve_label_data(self, token_column: str):
        # first divide into rows
        # process only 5 rows for demonstration
        if len(self.data) > 5:
            self.data = self.data.head(5)
        
        for index, row in self.data.iterrows():
            # get the text from the specified column
            tokens = row[token_column]
            tokens = eval(tokens)
            # label the tokens
            labels = self.label_tokens(tokens)
            
            for token, label in labels:
                print(token, label)
            print("")
        #return self.data

   