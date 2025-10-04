import streamlit as st
import random
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from event_cards_data import get_event_cards  # your static card data

# ----------------------
# Page config
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
# Fetch card image from wiki
# ----------------------
@st.cache_data(show_spinner=False)
def fetch_card_image(wiki_url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(wiki_url, headers=headers, timeout=5)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find("div", class_="cardarticleimage")
        if div:
            img_tag = div.find("img")
            if img_tag:
                src = img_tag.get("src")
                # Make full HTTPS URL
                if src.startswith("//"):
                    return "https:" + src
                elif src.startswith("/"):
                    return "https://spiritislandwiki.com" + src
                else:
                    return src
    except Exception as e:
        st.warning(f"Failed to fetch image from {wiki_url}: {e}")
    return None

# ----------------------
# Load shared deck with images
# ----------------------
@st.cache_resource
def get_shared_deck():
    cards = [c for c in get_event_cards() if c['status'] == 'Active']
    # Fetch images for all cards
    for card in cards:
        if not card.get("image"):
            card["image"] = fetch_card_image(card["url"])
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

# Draw button
if st.button("🎴 Draw Card"):
    card = deck.draw_card()
    if card:
        st.success(f"Drew: {card['name']}")
    else:
        st.error("No cards left!")

# Deck stats
stats = deck.get_stats()
st.markdown("### 📊 Deck Statistics")
st.metric("Cards in Deck", stats["cards_in_deck"])
st.metric("Cards Discarded", stats["cards_discarded"])
st.metric("Total Cards", stats["total_cards"])

# Show most recent card
if deck.discard_pile:
    card = deck.discard_pile[-1]
    st.markdown(f"## {card['name']}")
    if card.get("image"):
        st.image(card["image"], use_column_width=True)
    else:
        st.info("No image available for this card")

    st.write(f"**Box:** {card['box']}")
    st.write(f"**Status:** {card['status']}")
    if card.get("replacement"):
        st.write(f"**Replaced by:** {card['replacement']}")
    st.markdown(f"[View on Wiki]({card['url']})")
else:
    st.info("Draw a card to see it here!")

# Recent cards
if len(deck.discard_pile) > 1:
    st.markdown("### 📋 Recent Cards")
    recent_cards = deck.discard_pile[-5:-1]
    for c in reversed(recent_cards):
        st.write(f"• {c['name']} ({c['box']})")
        if c.get("image"):
            st.image(c["image"], width=120)

# Reset deck
if st.button("🔄 Reset Deck"):
    deck.reset_deck()
    st.success("Deck reset!")
