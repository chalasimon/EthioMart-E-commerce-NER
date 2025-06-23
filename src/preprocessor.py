# import libraries
import pandas as pd
import numpy as np
from etnltk.lang.am import (preprocessing,clean_amharic)


class Preprocessor:
    def __init__(self, data):
        self.data = data

    def clean_text(self,column_name='Message'):
        custom_pipeline = [
            preprocessing.remove_emojis,
            ]
        """Cleans the text data in the DataFrame."""
        self.data[column_name] = self.data[column_name].apply(
            lambda text: clean_amharic(text, abbrev=False, pipeline=custom_pipeline)
        )
        return self.data[column_name]