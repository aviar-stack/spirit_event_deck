import streamlit as st
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from event_cards_data import get_event_cards  # your existing static data

# ----------------------
# Streamlit page config
# ----------------------
st.set_page_config(
    page_title="Spirit Island Event Cards",
    page_icon="🌿",
    layout="wide"
)

# ----------------------
# EventDeck class
# ----------------------
class EventDeck:
    def __init__(self, cards: List[Dict]):
        self.original_cards = cards.copy()
        self.deck = cards.copy()
        self.discard_pile = []
        self.current_card = None

    def shuffle(self):
        random.shuffle(self.deck)

    def draw_card(self) -> Dict:
        if not self.deck:
            self.reshuffle_discard()
        if self.deck:
            self.current_card = self.deck.pop(0)
            self.discard_pile.append(self.current_card)
            return self.current_card
        return None

    def reshuffle_discard(self):
        self.deck = self.discard_pile.copy()
        self.discard_pile = []
        self.shuffle()

    def reset_deck(self):
        self.deck = self.original_cards.copy()
        self.discard_pile = []
        self.current_card = None
        self.shuffle()

    def get_stats(self) -> Dict:
        return {
            "cards_in_deck": len(self.deck),
            "cards_discarded": len(self.discard_pile),
            "total_cards": len(self.original_cards)
        }

# ----------------------
# Image fetching with caching
# ----------------------
@st.cache_data(show_spinner=False)
def fetch_card_image(wiki_url: str, card_name: str) -> str:
    """Fetch image URL from wiki and cache in memory"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/140.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(wiki_url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.content, "html.parser")
        div = soup.find("div", class_="cardarticleimage")
        if div and div.find("img"):
            img_tag = div.find("img")
            img_url = "https://spiritislandwiki.com" + img_tag["src"]
            return img_url
    except Exception as e:
        st.warning(f"Failed to fetch image for {card_name}: {e}")
    return None

# ----------------------
# Initialize shared deck
# ----------------------
@st.cache_resource
def get_shared_deck():
    cards = [card for card in get_event_cards() if card['status'] == 'Active']
    for card in cards:
        card["image"] = fetch_card_image(card["url"], card["name"])
    deck = EventDeck(cards)
    deck.shuffle()
    return deck

deck = get_shared_deck()

# ----------------------
# App UI
# ----------------------
st.title("🌿 Spirit Island Event Card Deck")
st.markdown("Draw and manage event cards from the official Spirit Island deck")
st.markdown("---")

# ----------------------
# Draw button (main area)
# ----------------------
if st.button("🎴 Draw Card"):
    card = deck.draw_card()
    if card:
        st.success(f"Drew: {card['name']}")
    else:
        st.error("No cards left!")

# ----------------------
# Deck stats
# ----------------------
stats = deck.get_stats()
st.markdown("### 📊 Deck Statistics")
st.metric("Cards in Deck", stats["cards_in_deck"])
st.metric("Cards Discarded", stats["cards_discarded"])
st.metric("Total Cards", stats["total_cards"])

# ----------------------
# Show most recent card
# ----------------------
if deck.discard_pile:
    card = deck.discard_pile[-1]
    st.markdown(f"## {card['name']}")
    if card.get("image"):
        st.image(card["image"], use_container_width=True)
    # Additional info
    st.write(f"**Box:** {card['box']}")
    st.write(f"**Status:** {card['status']}")
    if card.get("replacement"):
        st.write(f"**Replaced by:** {card['replacement']}")
    st.markdown(f"[View on Wiki]({card['url']})")
else:
    st.info("Draw a card to see it here!")

# ----------------------
# Recent cards list
# ----------------------
if len(deck.discard_pile) > 1:
    st.markdown("### 📋 Recent Cards")
    recent_cards = deck.discard_pile[-5:-1]  # last 4 excluding most recent
    for c in reversed(recent_cards):
        st.write(f"• {c['name']} ({c['box']})")

# ----------------------
# Reset deck button
# ----------------------
if st.button("🔄 Reset Deck"):
    deck.reset_deck()
    st.success("Deck reset!")
