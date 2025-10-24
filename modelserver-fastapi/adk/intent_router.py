def classify_intent(text: str) -> str:
    """Classify intent into one of: 'qa', 'recommend', 'conversational'.

    This is a lightweight rule-based classifier. Replace with an ML classifier
    for production workloads.
    """
    if not text or not isinstance(text, str):
        return 'qa'

    t = text.lower()
    rec_keywords = ['recommend', 'suggest', 'similar', 'like', 'more like']
    conv_keywords = ['hello', 'hi', 'how are you', 'tell me a story', 'chat']

    if any(k in t for k in rec_keywords):
        return 'recommend'
    if any(k in t for k in conv_keywords):
        return 'conversational'

    return 'qa'
