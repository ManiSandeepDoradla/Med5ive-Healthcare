import re
from typing import List, Tuple, Optional
import random
GREETING_KEYWORDS = {
    "hi", "hello", "hey", "good morning", "good afternoon", "good evening",
    "how are you", "how r u", "hru"
}
SMALL_TALK_KEYWORDS = {
    "thank you", "thanks", "ty", "bye", "goodbye", "see you", "nice to meet you"
}
OFF_TOPIC_MESSAGE = (
    "This assistant is only for medical-related queries. "
    "Please ask about symptoms, medications, appointments, or general health information."
)
HEALTH_KEYWORDS = {
    # general care
    "doctor", "clinic", "hospital", "medicine", "medication", "dose", "dosage",
    "symptom", "symptoms", "diagnosis", "treatment", "prescription", "appointment",
    "health", "wellness", "care", "nurse",
    # body parts / systems
    "chest", "heart", "lung", "throat", "nose", "ear", "eye", "stomach", "abdomen",
    "skin", "head", "brain", "back", "leg", "arm", "knee", "shoulder",
    # conditions / signs
    "fever", "cough", "cold", "rash", "pain", "headache", "migraine", "sore", "vomit",
    "diarrhea", "breath", "shortness", "difficulty breathing", "bleeding",
    "pressure", "tightness", "dizziness", "fatigue",
    # tests / procedures
    "test", "blood", "xray", "x-ray", "scan", "ecg", "mri",
    # OTC/common terms
    "paracetamol", "ibuprofen", "antibiotic", "antacid",
    # wellness
    "diet", "exercise"
}
NEGATION_WORDS = {"no", "not", "without", "denies", "deny", "nil", "absent"}
RED_FLAG_PHRASES = {
    # Cardiac/respiratory red flags
    "severe chest pain", "chest pain", "pressure in chest", "tightness in chest",
    "shortness of breath", "difficulty breathing", "breathlessness",
    # Neuro red flags / stroke signs
    "fainting", "passed out", "unconscious", "confusion", "disoriented",
    "stroke", "weakness on one side", "face droop", "slurred speech",
    # Bleeding/GI red flags
    "severe bleeding", "vomiting blood", "black stool"
}
RED_FLAG_TOKENS = {"chest", "sob", "dyspnea", "bleeding", "suicidal"}
MODERATE_RESPONSE = (
    "It may be advisable to consult a clinician within 24–48 hours. "
    "If symptoms worsen or new red-flag signs appear, seek urgent care."
)
SYMPTOM_GROUPS = {
    "gastroenterology": {
        "synonyms": {"stomach pain", "abdominal pain", "stomach ache", "gastric pain", "tummy pain", "belly pain", "cramps"},
        "specialist": "Consult a Gastroenterologist.",
        "mild": (
            "For mild stomach pain, try rest, hydration, and a bland diet. Avoid spicy/oily foods. "
            "An OTC antacid may help. Seek care if it persists or worsens."
        ),
        "moderate": MODERATE_RESPONSE,
        "urgent_phrases": {"rigid abdomen", "vomiting blood", "black stool", "severe sudden abdominal pain"}
    },
    "ent": {
        "synonyms": {"nose pain", "nasal pain", "sinus pain", "sinus pressure", "sore throat", "throat pain", "ear pain", "earache", "congestion", "blocked nose"},
        "specialist": "Consult an ENT specialist.",
        "mild": (
            "For mild nose or sinus pain, try saline rinse, steam inhalation, rest, and OTC pain relief if appropriate. "
            "Monitor and seek care if it persists."
        ),
        "moderate": MODERATE_RESPONSE,
        "urgent_phrases": {"orbital pain with vision change", "facial swelling with high fever"}
    },
    "cardiology": {
        "synonyms": {"chest pain", "chest tightness", "pressure in chest", "angina"},
        "specialist": "Consult a Cardiologist.",
        "mild": (
            "If chest discomfort is brief and non-exertional with no red flags, rest and monitor closely. "
            "Seek care if it recurs."
        ),
        "moderate": MODERATE_RESPONSE,
        "urgent_phrases": {"radiating to left arm", "jaw pain", "sweating with chest pain", "nausea with chest pain"}
    },
    "orthopedics": {
        "synonyms": {"joint pain", "back pain", "knee pain", "shoulder pain", "sprain", "strain", "muscle pain"},
        "specialist": "Consult an Orthopedician.",
        "mild": (
            "For mild musculoskeletal pain, try rest, ice, compression, elevation (RICE), and OTC pain relief if appropriate."
        ),
        "moderate": MODERATE_RESPONSE,
        "urgent_phrases": {"visible deformity", "inability to bear weight after injury", "severe swelling after trauma"}
    },
    "neurology": {
        "synonyms": {"headache", "migraine", "dizziness", "seizure", "weakness on one side"},
        "specialist": "Consult a Neurologist.",
        "mild": (
            "For a mild headache, try rest, hydration, and over-the-counter pain relief (e.g., paracetamol) if appropriate. "
            "Reduce screen time and consider a short nap. If the headache persists, worsens, or new concerning symptoms appear "
            "(stiff neck, confusion, fever ≥ 39°C, sudden severe pain), seek medical attention."
        ),
        "moderate": MODERATE_RESPONSE,
        "urgent_phrases": {"worst headache of my life", "thunderclap", "sudden severe headache", "stiff neck", "neck rigidity",
                           "confusion", "disoriented", "after head injury", "post trauma", "vision loss", "double vision",
                           "face droop", "slurred speech"}
    }
}
def has_negation_before(text: str, start_idx: int, window: int = 40) -> bool:
    span = text[max(0, start_idx - window):start_idx]
    return any(re.search(rf"\b{w}\b", span) for w in NEGATION_WORDS)
 
def is_greeting(text: str) -> bool:
    t = text.lower().strip()
    return any(t.startswith(k) or k in t for k in GREETING_KEYWORDS)
def greeting_response() -> str:
    return random.choice([
        "Hello! 👋 How can I assist you today?",
        "Hi there! 😊 What health info can I help with?",
        "Hey! I’m here to support you. Tell me your concern."
    ])
def is_small_talk(text: str) -> bool:
    t = text.lower().strip()
    return any(k in t for k in SMALL_TALK_KEYWORDS)
def small_talk_response() -> str:
    return random.choice([
        "You’re welcome! 🙏",
        "Glad to help! ✨",
        "Take care! 👋"
    ])
def is_off_topic(text: str) -> bool:
    t = text.lower().strip()
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t)          
    t = re.sub(r"[^a-z0-9\s-]", " ", t)                  
    t = re.sub(r"\s+", " ", t)
    return not any(k in t for k in HEALTH_KEYWORDS)
def red_flag_score(text: str) -> int:
    norm = normalize_for_rules(text)
    score = 0
    # Phrase-level (strong signals FIRST)
    for p in RED_FLAG_PHRASES:
        idx = norm.find(p)
        if idx != -1 and not has_negation_before(norm, idx):
            score += 2
    # Token-level (weaker signals; pain REMOVED)
    for token in RED_FLAG_TOKENS:
        for m in re.finditer(rf"\b{re.escape(token)}\b", norm):
            if not has_negation_before(norm, m.start()):
                score += 1
    # Numeric cues
    temp_c, _ = extract_temp_duration(norm)
    if temp_c >= 39.0:
        score += 1
    return score
def has_red_flags(text: str) -> bool:
    return red_flag_score(text) > 0
def detect_group(text: str) -> Optional[str]:
    t = normalize_for_rules(text)
    for group, info in SYMPTOM_GROUPS.items():
        for syn in info["synonyms"]:
            if syn in t:
                return group
    return None
def assess_group_severity(text: str, group: str) -> str:
    """
    Returns 'urgent' | 'moderate' | 'mild' based on group-specific phrases and generic cues.
    """
    norm = normalize_for_rules(text)
    temp_c, duration_days = extract_temp_duration(norm)
 
    # Urgent: any global red flags or group-specific urgent phrases
    if has_red_flags(text):
        return "urgent"
    for p in SYMPTOM_GROUPS[group].get("urgent_phrases", set()):
        if p in norm:
            return "urgent"
 
    # Moderate: persistence (>=3 days), explicit 'persistent'/'not improving',
    # exertional chest discomfort (cardio), repeated vomiting (gastro), limited movement (ortho),
    # fever + sinus pain >3 days (ent)
    if duration_days >= 3 or "persistent" in norm or "not improving" in norm:
        return "moderate"
 
    if group == "cardiology" and ("exertion" in norm or "on exertion" in norm or "while walking" in norm):
        return "moderate"
 
    if group == "gastroenterology" and ("repeated vomiting" in norm or "vomiting for" in norm):
        return "moderate"
 
    if group == "orthopedics" and ("limited movement" in norm or "restricted movement" in norm):
        return "moderate"
 
    if group == "ent" and ("fever" in norm and duration_days >= 3):
        return "moderate"
 
    # Default
    return "mild"
def extract_temp_duration(text: str) -> Tuple[float, int]:
    temp_c = -1.0
    m_f = re.search(r"(\d{2,3}(?:\.\d)?)\s*°?\s*f", text)
    if m_f:
        f = float(m_f.group(1))
        temp_c = round((f - 32) * 5 / 9, 1)
    m_c = re.search(r"(\d{2,3}(?:\.\d)?)\s*°?\s*c", text)
    if m_c:
        temp_c = float(m_c.group(1))
    m_bare = re.search(r"fever.*?(\d{2,3}(?:\.\d)?)", text)
    if temp_c < 0 and m_bare:
        val = float(m_bare.group(1))
        temp_c = val if val <= 50 else -1.0
    duration_days = -1
    m_days = re.search(r"(\d{1,2})\s*day", text)
    if m_days:
        duration_days = int(m_days.group(1))
    return temp_c, duration_days
def normalize_for_rules(text: str) -> str:
    t = text.lower().strip()
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t)            # split camelCase
    t = re.sub(r"[^a-z0-9\s°.%-]", " ", t)                # simplify punctuation
    t = re.sub(r"\s+", " ", t)
    t = t.replace("sob", " shortness of breath ")
    t = t.replace("dyspnea", " shortness of breath ")
    return t