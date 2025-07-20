texts = {
    "en": {
        "start": "👋 Welcome to the OSINT Bot!",
        "profile": "👤 Your Profile\nCoins: {coins}\nReferrals: {refs}\nCredits: {credits}",
        "redeem_success": "✅ Redeemed successfully!",
    },
    "hi": {
        "start": "👋 आपका स्वागत है OSINT बॉट में!",
        "profile": "👤 आपकी प्रोफ़ाइल\nसिक्के: {coins}\nरेफरल: {refs}\nक्रेडिट: {credits}",
        "redeem_success": "✅ सफलतापूर्वक रिडीम किया गया!",
    }
}

def get_text(key, lang="en"):
    return texts.get(lang, texts["en"]).get(key, "")