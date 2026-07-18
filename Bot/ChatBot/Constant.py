DISCLAIMER = (
    "⚠️ This chatbot provides general information only and does not replace medical advice. "
    "For emergencies, call 108 or visit the nearest hospital."
)
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
NEGATION_WORDS = {"no", "not", "without", "denies", "deny", "nil", "absent"}
 
URGENT_RESPONSE = (
    "Your symptoms may be urgent. Please call emergency services (108) "
    "or visit the nearest hospital immediately."
)
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