from .Constant import (
    DISCLAIMER,
    OFF_TOPIC_MESSAGE,
)
 
# greetings & small talk
from .Rules import (
    is_greeting,
    greeting_response,
    is_small_talk,
    small_talk_response,
    is_off_topic,
)
 
# red flag & medical rules
from .Rules import (
    has_red_flags,
    detect_group,
    assess_group_severity,
)
 
# ML chatbot
from .Model import AIPoweredChatbot
from .PreProcessing import TextProcessing
 
 
# ===============================
# SINGLETONS (NO RETRAIN PER REQUEST)
# ===============================
 
_processor = None
_bot = None
 
 
def _get_bot():
    """
    Creates your ML chatbot ONCE.
    Your original model, unchanged.
    """
    global _processor, _bot
 
    if _processor is None:
        _processor = TextProcessing()
 
    if _bot is None:
        _bot = AIPoweredChatbot(_processor)
 
    return _bot
 
 
# ===============================
# MAIN ENTRY POINT (SAME FLOW AS YOUR FILE)
# ===============================
 
def get_bot_response(user_text: str) -> str:
    """
    This function follows THE SAME ORDER
    as your original chatbot script.
    """
 
    text = user_text.strip()
 
    # 1️⃣ Greeting
    if is_greeting(text):
        return greeting_response()
 
    # 2️⃣ Small talk
    if is_small_talk(text):
        return small_talk_response()
 
    # 3️⃣ Off-topic (non medical)
    if is_off_topic(text):
        return OFF_TOPIC_MESSAGE
 
    # 4️⃣ Emergency red flags
    if has_red_flags(text):
        return (
            "🚨 Your symptoms may be urgent.\n"
            "Please call emergency services (108) "
            "or visit the nearest hospital immediately."
        )
 
    # 5️⃣ Symptom group detection
    group = detect_group(text)
 
    if group:
        severity = assess_group_severity(text, group)
 
        if severity == "urgent":
            return (
                "⚠️ Your symptoms indicate a potentially serious condition.\n"
                "Please seek urgent medical care immediately.\n\n"
                + DISCLAIMER
            )
 
        if severity == "moderate":
            return (
                "⚠️ It is advisable to consult a clinician within 24–48 hours.\n\n"
                + DISCLAIMER
            )
 
        # mild
        return (
            DISCLAIMER
            + "\n\n"
            + "Your symptoms appear mild. Monitor them and seek care if they worsen."
        )
 
    # 6️⃣ ML fallback (UNCHANGED)
    bot = _get_bot()
    return bot.predict(text)