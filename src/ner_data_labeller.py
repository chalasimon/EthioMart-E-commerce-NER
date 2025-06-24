# import libraries
import os
import re
import pandas as pd
from typing import List, Tuple
import ast  # Safer than eval for parsing strings

class NERDataLabeller:
    def __init__(self, df: pd.DataFrame):
        self.data = df
        self.labels: List[Tuple[str, str]] = []
        
        # Entity type mappings
        self.entity_types = {
            '1': 'B-PRODUCT',
            '2': 'I-PRODUCT',
            '3': 'B-PRICE',
            '4': 'I-PRICE',
            '5': 'B-LOC',
            '6': 'I-LOC',
            '0': 'O'
        }

        # Indicators
        self.price_indicators = ['ዋጋ', 'ብር', 'በብር', 'በዋጋ', 'ቅናሽ', 'በቅናሽ', 'price', 'Price']
        self.location_indicators = [
            'አዲስአበባ', 'ገርጂ', 'አዲስ', 'ብስራተ', 'ከተማ', 'ገጽ', 'Addisababa', 'Addis', 'Gergi',
            'Bole', 'ቦሌ', 'መገናኛ', 'ሜክሲኮ', 'ድሬዳዋ', 'አሸዋ', 'ሚና', 'ህንፃ', 'ፎቅ','መዳህኒአለም', 'መርካቶ','ቤተክርስቲያን','ቁ','ቁ1','ቁ2','ቁ3',
            'ማራቶን', 'ገበያ', 'ማእከል', 'መግቢያ', 'መሬት', 'ላይ', 'ግራውንድ', 'በስተቀኝ',
            'በመጀመሪያው', 'ሱቅቁ', 'ቁጥር', 'አበባ'
        ]
        self.product_indicators = [
            'ምርት', 'እቃ', 'አምራች', 'አምራች እቃ', 'Juicer', 'ጁስ', 'ማሽን', 'portable',
            'ብርጭቆ', 'dispenser', 'Mop', 'Slicer', 'Gloves', 'Humidifier', 'Phone',
            'Smart', 'ስልክ', 'ስማርት', 'አውቶሞቢል'
        ]

        self.price_pattern = re.compile(r'(?:ዋጋ[:：]?\s*)?(\d+)(?:\s*(?:ብር|birr))?', re.IGNORECASE)

    def auto_label(self, tokens: List[str]) -> List[str]:
        labels = []
        inside_product = False
        inside_price = False
        inside_loc = False

        for token in tokens:
            label = 'O'

            # Price
            if any(ind in token for ind in self.price_indicators) or self.price_pattern.match(token):
                if not inside_price:
                    label = 'B-PRICE'
                    inside_price, inside_product, inside_loc = True, False, False
                else:
                    label = 'I-PRICE'

            # Location
            elif any(ind in token for ind in self.location_indicators):
                if not inside_loc:
                    label = 'B-LOC'
                    inside_loc, inside_price, inside_product = True, False, False
                else:
                    label = 'I-LOC'

            # Product
            elif any(ind in token for ind in self.product_indicators):
                if not inside_product:
                    label = 'B-PRODUCT'
                    inside_product, inside_loc, inside_price = True, False, False
                else:
                    label = 'I-PRODUCT'

            else:
                inside_product = inside_price = inside_loc = False

            labels.append(label)

        return labels

    def label_tokens(self, tokens: List[str]) -> List[Tuple[str, str]]:
        self.labels = []  # reset for each call
        for token in tokens:
            label = input(f"Enter label for token '{token}': ")
            if label.lower() == "q":
                print("Exiting manual labeling.")
                self.labels.append((token, "O"))
                return self.labels
            self.labels.append((token, label))
        return self.labels

    def retrieve_label_data(self, token_column: str, mode: str = "auto"):
        if len(self.data) > 5:
            self.data = self.data.head(5)

        for index, row in self.data.iterrows():
            # Safely parse token list from column
            tokens = ast.literal_eval(row[token_column])

            if mode == "manual":
                labels = self.label_tokens(tokens)
            else:  # "auto"
                labels = list(zip(tokens, self.auto_label(tokens)))

            for token, label in labels:
                print(f"{token}\t{label}")
            print("")
