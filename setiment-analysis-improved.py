#%%
import pandas as pd
import re

df = pd.read_csv('final_df.csv')

def check_preprocessing_status(df):
    # Check for missing values
    print("## Missing Values")
    print(df['Consumer complaint narrative'].isnull().sum(), "missing values in raw narrative")
    print(df['Processed Narrative'].isnull().sum(), "missing values in processed narrative")
    
    # Sample comparison between raw and processed text
    print("\n## Sample Text Comparison")
    sample_idx = 0
    print("Raw text:")
    print(df['Consumer complaint narrative'].iloc[sample_idx])
    print("\nProcessed text:")
    print(df['Processed Narrative'].iloc[sample_idx])
    
    # Check for special characters and numbers in processed text
    special_chars = df['Processed Narrative'].str.contains('[^a-zA-Z\s]').sum()
    print(f"\n## Special Characters")
    print(f"{special_chars} rows contain special characters in processed text")
    
    # Check for uppercase letters in processed text
    uppercase = df['Processed Narrative'].str.contains('[A-Z]').sum()
    print(f"\n## Uppercase Letters")
    print(f"{uppercase} rows contain uppercase letters in processed text")
    
    # Check word count consistency
    word_count_mismatch = (df['Processed Narrative'].str.split().str.len() != df['word_count']).sum()
    print(f"\n## Word Count Consistency")
    print(f"{word_count_mismatch} rows have word count mismatches")
    
    # Check stopwords presence
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    sample_processed = df['Processed Narrative'].iloc[0].split()
    stopwords_present = sum(1 for word in sample_processed if word.lower() in stop_words)
    print(f"\n## Stopwords in Sample")
    print(f"{stopwords_present} stopwords found in first processed text")

# Execute the check
check_preprocessing_status(df)
# %%
# Fix word count and verify text data consistency
def verify_text_data(df):
    # Recalculate word counts
    df['new_word_count'] = df['Processed Narrative'].str.split().str.len()
    
    # Compare with existing word count
    print("Word Count Statistics:")
    print("Original word count mean:", df['word_count'].mean())
    print("New word count mean:", df['new_word_count'].mean())
    print("\nMismatch Analysis:")
    print("Number of mismatches:", (df['word_count'] != df['new_word_count']).sum())
    
    # Sample verification
    print("\nSample Comparison (First 3 rows):")
    comparison_df = pd.DataFrame({
        'Processed_Text': df['Processed Narrative'].head(3),
        'Original_Count': df['word_count'].head(3),
        'New_Count': df['new_word_count'].head(3)
    })
    print(comparison_df)
    
    return df

# Execute verification
df = verify_text_data(df)
# %%
# import torch
# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, accuracy_score
# from transformers import (
#     BertTokenizer, BertForSequenceClassification,
#     RobertaTokenizer, RobertaForSequenceClassification,
#     DistilBertTokenizer, DistilBertForSequenceClassification,
#     T5Tokenizer, T5ForSequenceClassification,
#     AdamW, get_linear_schedule_with_warmup
# )
# import nltk
# from nltk.sentiment import SentimentIntensityAnalyzer

# # Download necessary NLTK resources
# nltk.download('vader_lexicon')

# # Sentiment Label Function
# def get_sentiment_label(text):
#     analyzer = SentimentIntensityAnalyzer()
#     sentiment_score = analyzer.polarity_scores(text)
    
#     if sentiment_score['compound'] >= 0.05:
#         return 2  # Positive
#     elif sentiment_score['compound'] <= -0.05:
#         return 0  # Negative
#     else:
#         return 1  # Neutral

# # Custom PyTorch Dataset
# class ComplaintDataset(torch.utils.data.Dataset):
#     def __init__(self, texts, labels, tokenizer, max_len):
#         self.texts = texts.tolist()
#         self.labels = labels.tolist()
#         self.tokenizer = tokenizer
#         self.max_len = max_len
    
#     def __len__(self):
#         return len(self.texts)
    
#     def __getitem__(self, idx):
#         text = str(self.texts[idx])
#         label = self.labels[idx]
        
#         inputs = self.tokenizer.encode_plus(
#             text,
#             None,
#             add_special_tokens=True,
#             max_length=self.max_len,
#             padding='max_length',
#             truncation=True,
#             return_tensors='pt'
#         )
        
#         return {
#             'input_ids': inputs['input_ids'].flatten(),
#             'attention_mask': inputs['attention_mask'].flatten(),
#             'labels': torch.tensor(label, dtype=torch.long)
#         }

# # Training Function
# def train_model(model, train_loader, val_loader, device, learning_rate=2e-5, epochs=5):
#     optimizer = AdamW(model.parameters(), lr=learning_rate)
#     total_steps = len(train_loader) * epochs
#     scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)
    
#     model.to(device)
    
#     for epoch in range(epochs):
#         model.train()
#         total_train_loss = 0
        
#         for batch in train_loader:
#             optimizer.zero_grad()
            
#             input_ids = batch['input_ids'].to(device)
#             attention_mask = batch['attention_mask'].to(device)
#             labels = batch['labels'].to(device)
            
#             outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
#             loss = outputs.loss
#             total_train_loss += loss.item()
            
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
#             optimizer.step()
#             scheduler.step()
        
#         # Validation
#         model.eval()
#         total_val_loss = 0
#         with torch.no_grad():
#             for batch in val_loader:
#                 input_ids = batch['input_ids'].to(device)
#                 attention_mask = batch['attention_mask'].to(device)
#                 labels = batch['labels'].to(device)
                
#                 outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
#                 loss = outputs.loss
#                 total_val_loss += loss.item()
        
#         print(f"Epoch {epoch+1}/{epochs}")
#         print(f"Average training loss: {total_train_loss/len(train_loader):.4f}")
#         print(f"Average validation loss: {total_val_loss/len(val_loader):.4f}")
    
#     return model

# # Evaluation Function
# def evaluate_model(model, test_loader, device):
#     model.eval()
#     predictions, true_labels = [], []
    
#     with torch.no_grad():
#         for batch in test_loader:
#             input_ids = batch['input_ids'].to(device)
#             attention_mask = batch['attention_mask'].to(device)
#             labels = batch['labels']
            
#             outputs = model(input_ids, attention_mask=attention_mask)
#             _, preds = torch.max(outputs.logits, dim=1)
            
#             predictions.extend(preds.cpu().numpy())
#             true_labels.extend(labels.numpy())
    
#     print(classification_report(true_labels, predictions))
#     return accuracy_score(true_labels, predictions)

# # Main Workflow
# def sentiment_analysis_workflow(df):
#     # Add sentiment labels
#     df['target'] = df['Processed Narrative'].apply(get_sentiment_label)
    
#     # Prepare data for transformer models
#     X = df['Processed Narrative']
#     y = df['target']
    
#     # Three-way split: train, validation, test
#     X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=42)
    
#     # Model configurations
#     models_config = [
#         ('bert-base-uncased', BertTokenizer, BertForSequenceClassification),
#         ('roberta-base', RobertaTokenizer, RobertaForSequenceClassification),
#         ('distilbert-base-uncased', DistilBertTokenizer, DistilBertForSequenceClassification),
#         ('t5-base', T5Tokenizer, T5ForSequenceClassification)
#     ]
    
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
#     results = {}
    
#     for model_name, TokenizerClass, ModelClass in models_config:
#         tokenizer = TokenizerClass.from_pretrained(model_name)
#         model = ModelClass.from_pretrained(model_name, num_labels=3)  # 3 sentiment classes
        
#         train_dataset = ComplaintDataset(X_train, y_train, tokenizer, max_len=128)
#         val_dataset = ComplaintDataset(X_val, y_val, tokenizer, max_len=128)
#         test_dataset = ComplaintDataset(X_test, y_test, tokenizer, max_len=128)
        
#         train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)
#         val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=32, shuffle=False)
#         test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=32, shuffle=False)
        
#         # Train and fine-tune the model
#         trained_model = train_model(model, train_loader, val_loader, device)
        
#         # Evaluate on test set
#         accuracy = evaluate_model(trained_model, test_loader, device)
        
#         results[model_name] = accuracy
    
#     # Compare results
#     best_model = max(results, key=results.get)
#     print("Best Model:", best_model)
#     print("Accuracy Scores:", results)
    
#     return results

# # Execute workflow
# results = sentiment_analysis_workflow(df)
# %%
df.columns
# %%
df.head()
# %%
import torch
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
from transformers import (
    BertTokenizer, 
    BertForSequenceClassification, 
    AdamW, 
    get_linear_schedule_with_warmup
)
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self, model_name='bert-base-uncased', max_len=128, batch_size=32):
        self.model_name = model_name
        self.max_len = max_len
        self.batch_size = batch_size
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Download VADER lexicon
        nltk.download('vader_lexicon', quiet=True)
        
    def _get_sentiment_label(self, text):
        """
        Assign sentiment labels using VADER
        0: Negative, 1: Neutral, 2: Positive
        """
        analyzer = SentimentIntensityAnalyzer()
        sentiment_score = analyzer.polarity_scores(str(text))
        
        if sentiment_score['compound'] >= 0.05:
            return 2  # Positive
        elif sentiment_score['compound'] <= -0.05:
            return 0  # Negative
        else:
            return 1  # Neutral

    class SentimentDataset(Dataset):
        def __init__(self, texts, labels, tokenizer, max_len):
            self.texts = texts
            self.labels = labels
            self.tokenizer = tokenizer
            self.max_len = max_len
        
        def __len__(self):
            return len(self.texts)
        
        def __getitem__(self, idx):
            text = str(self.texts.iloc[idx])
            label = self.labels.iloc[idx]
            
            encoding = self.tokenizer.encode_plus(
                text,
                add_special_tokens=True,
                max_length=self.max_len,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            return {
                'input_ids': encoding['input_ids'].flatten(),
                'attention_mask': encoding['attention_mask'].flatten(),
                'labels': torch.tensor(label, dtype=torch.long)
            }

    def prepare_data(self, df):
        """
        Prepare data with sentiment labels and stratified split
        """
        # Add sentiment labels
        df['sentiment'] = df['Processed Narrative'].apply(self._get_sentiment_label)
        
        # Log sentiment distribution
        sentiment_dist = df['sentiment'].value_counts(normalize=True)
        logger.info("Sentiment Distribution:\n%s", sentiment_dist)
        
        return df

    def train_model(self, df, epochs=5):
        # Prepare data
        df = self.prepare_data(df)
        
        # Tokenizer and model
        tokenizer = BertTokenizer.from_pretrained(self.model_name)
        model = BertForSequenceClassification.from_pretrained(
            self.model_name, 
            num_labels=3,
            output_attentions=False,
            output_hidden_states=False
        )
        model.to(self.device)
        
        # Stratified K-Fold Cross Validation
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        all_predictions, all_true_labels = [], []
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(df['Processed Narrative'], df['sentiment']), 1):
            logger.info(f"Training Fold {fold}")
            
            # Split data
            X_train, X_val = df['Processed Narrative'].iloc[train_idx], df['Processed Narrative'].iloc[val_idx]
            y_train, y_val = df['sentiment'].iloc[train_idx], df['sentiment'].iloc[val_idx]
            
            # Datasets and Loaders
            train_dataset = self.SentimentDataset(X_train, y_train, tokenizer, self.max_len)
            val_dataset = self.SentimentDataset(X_val, y_val, tokenizer, self.max_len)
            
            # Handle class imbalance with weighted sampling
            class_weights = 1.0 / np.unique(y_train, return_counts=True)[1]
            sample_weights = [class_weights[t] for t in y_train]
            sampler = WeightedRandomSampler(sample_weights, len(sample_weights))
            
            train_loader = DataLoader(train_dataset, batch_size=self.batch_size, sampler=sampler)
            val_loader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=False)
            
            # Optimizer and scheduler
            optimizer = AdamW(model.parameters(), lr=2e-5)
            scheduler = get_linear_schedule_with_warmup(
                optimizer, 
                num_warmup_steps=0, 
                num_training_steps=len(train_loader) * epochs
            )
            
            # Training loop
            model.train()
            for epoch in range(epochs):
                total_loss = 0
                for batch in train_loader:
                    optimizer.zero_grad()
                    
                    input_ids = batch['input_ids'].to(self.device)
                    attention_mask = batch['attention_mask'].to(self.device)
                    labels = batch['labels'].to(self.device)
                    
                    outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
                    loss = outputs.loss
                    
                    loss.backward()
                    optimizer.step()
                    scheduler.step()
                    
                    total_loss += loss.item()
                
                logger.info(f"Fold {fold}, Epoch {epoch+1}, Loss: {total_loss/len(train_loader)}")
            
            # Validation
            model.eval()
            fold_predictions, fold_true_labels = [], []
            with torch.no_grad():
                for batch in val_loader:
                    input_ids = batch['input_ids'].to(self.device)
                    attention_mask = batch['attention_mask'].to(self.device)
                    labels = batch['labels']
                    
                    outputs = model(input_ids, attention_mask=attention_mask)
                    _, preds = torch.max(outputs.logits, dim=1)
                    
                    fold_predictions.extend(preds.cpu().numpy())
                    fold_true_labels.extend(labels.numpy())
            
            # Log fold results
            logger.info(f"Fold {fold} Classification Report:\n{classification_report(fold_true_labels, fold_predictions)}")
            
            all_predictions.extend(fold_predictions)
            all_true_labels.extend(fold_true_labels)
        
        # Final model evaluation
        logger.info("Overall Classification Report:\n%s", 
                    classification_report(all_true_labels, all_predictions))
        
        # Visualize confusion matrix
        cm = confusion_matrix(all_true_labels, all_predictions)
        plt.figure(figsize=(10,7))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('confusion_matrix.png')
        
        # Save model
        model.save_pretrained('sentiment_model')
        tokenizer.save_pretrained('sentiment_tokenizer')
        
        return model, tokenizer

# Usage
sentiment_analyzer = SentimentAnalyzer()
model, tokenizer = sentiment_analyzer.train_model(df)
# %%
