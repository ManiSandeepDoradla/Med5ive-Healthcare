from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from django.conf import settings
import json
import os
 
from .PreProcessing import TextProcessing
from .Rules import is_greeting , greeting_response , is_small_talk,small_talk_response,is_off_topic,detect_group,assess_group_severity,has_red_flags
from .Constant import DISCLAIMER , OFF_TOPIC_MESSAGE , URGENT_RESPONSE ,SYMPTOM_GROUPS
class AIPoweredChatbot:
    """def __init__(self, processor):
        self.processor = processor
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(preprocessor=processor.preprocess_text)),
            ("clf", LogisticRegression(max_iter=1000))
        ])
 
        self._train_model()
 
 
    def _train_model(self):
        # 🔹 absolute path of THIS file (model.py)
        BASE_DIR = settings.BASE_DIR
        #CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
 
        # 🔹 datasets/healthcare_training_dataset.json
        DATASET_PATH = os.path.join(
            BASE_DIR,
            "Bot",
            "ChatBot",
            "datasets",
            "Trained.json"
        )
        DATASET2_PATH = os.path.join(
            BASE_DIR,
            "Bot",
            "ChatBot",
            "datasets",
            "dev.json"
        )
 
        # 🔴 DEBUG (temporary)
        print("Looking for dataset at:", DATASET_PATH)
 
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            train = json.load(f)
 
       
        print("Dataset Loaded samples" , len(train))            
        with open(DATASET2_PATH, "r", encoding="utf-8") as f:
            dev = json.load(f)
        print("deved", len(dev))
        X_train = [r["text"] for r in train]
        y_train = [r["response"] for r in train]
        X_dev = [r["text"] for r in dev]
        y_dev = [r["response"] for r in dev]
 
        self.pipeline.fit(X_train, y_train)
 
        # Dev evaluation (optional)
        y_pred = self.pipeline.predict(X_dev)
        print("Dev set accuracy:", accuracy_score(y_dev, y_pred))
        print("Dev classification report:\n", classification_report(y_dev, y_pred))
 
    def respond(self, user_input: str) -> str:
        # 1) Greetings — normal conversation
        if is_greeting(user_input):
            return greeting_response()
 
        # 2) Small talk — normal conversation
        if is_small_talk(user_input):
            return small_talk_response()
 
        # 3) Off-topic — politely set boundaries
        if is_off_topic(user_input):
            return OFF_TOPIC_MESSAGE
 
        # 4) Symptom group detection + severity + specialist (moderate)
        group = detect_group(user_input)
        if group:
            severity = assess_group_severity(user_input, group)
            group_info = SYMPTOM_GROUPS[group]
            if severity == "urgent":
                return f"{DISCLAIMER}\n\n{URGENT_RESPONSE}"
            elif severity == "moderate":
                # moderate advice + specialist suggestion
                return f"{DISCLAIMER}\n\n{group_info['moderate']}\n\n{group_info['specialist']}"
            else:  # mild
                return f"{DISCLAIMER}\n\n{group_info['mild']}"
 
        # 5) Global red flags — urgent override (only if group not detected)
        # (This stays after group routing to avoid false positives on mild group cases)
        if has_red_flags(user_input):
            return f"{DISCLAIMER}\n\n{URGENT_RESPONSE}"
 
        # 6) ML prediction (+ confidence fallback)
        pred = self.pipeline.predict([user_input])[0]
 
        if hasattr(self.pipeline.named_steps["clf"], "predict_proba"):
            probs = self.pipeline.named_steps["clf"].predict_proba([user_input])[0]
            max_p = float(max(probs))
            token_count = len(self.processor.preprocess_tokens(user_input))
            if max_p < 0.45 or token_count <= 2:
                fallback = (
                    "Please share your main symptoms, how long they’ve been present, your age, and any existing "
                    "health conditions. For mild issues, rest, hydration, and appropriate OTC remedies may help."
                )
                return f"{DISCLAIMER}\n\n{fallback}"
 
        return f"{DISCLAIMER}\n\n{pred}"
"""
    def __init__(self, processor):
        self.processor = processor
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(preprocessor=processor.preprocess_text)),
            ("clf", LogisticRegression(max_iter=1000))
        ])
 
        self._train_model()
 
 
    def _train_model(self):
        # 🔹 absolute path of THIS file (model.py)
        BASE_DIR = settings.BASE_DIR
        #CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
 
        # 🔹 datasets/healthcare_training_dataset.json
        DATASET_PATH = os.path.join(
            BASE_DIR,
            "Bot",
            "ChatBot",
            "datasets",
            "Trained.json"
        )
 
        # 🔴 DEBUG (temporary)
        print("Looking for dataset at:", DATASET_PATH)
 
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
 
        print("DATASET LOADED, SAMPLES:", len(data))
 
        X = [item["text"] for item in data]
        y = [item["response"] for item in data]
 
        self.pipeline.fit(X, y)
 
 
    def predict(self, text: str) -> str:
        return str(self.pipeline.predict([text])[0])