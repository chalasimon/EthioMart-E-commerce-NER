# EthioMart E-Commerce NER Pipeline

![Telegram Scraper](https://img.shields.io/badge/Source-Telegram-blue)
![Amharic NLP](https://img.shields.io/badge/Language-Amharic-green)
![CoNLL Format](https://img.shields.io/badge/Format-CoNLL-orange)

A complete data pipeline for Ethiopian Telegram e-commerce channels, featuring:
- Real-time message ingestion
- Amharic text processing
- Named Entity Recognition (NER) labeling
- Fine tuning of NER models with Hugging Face Transformers

## Notebooks files
- `data_ingestion.ipynb`: Scrapes messages from Telegram channels.
- `data_preprocessing.ipynb`: Processes Amharic text and tokenizes the messages.
- `data_labeling.ipynb`: Labels entities in the preprocessed data and saves them in CoNLL format.
- `ner_fine_tuner.ipynb`: Fine-tunes NER models using the labeled data.


