import streamlit as st
import random
from typing import List, Dict
from event_cards_data import get_event_cards

# -------------------------
# Streamlit page settings
# -------------------------
st.set_page_config(page_title="Spirit Island Event Deck", page_icon="🌿", layout="wide")

# -------------------------
# Event Deck Class
# -------------------------
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
            card = self.deck.pop(0)
            self.discard_pile.append(card)
            self.current_card = card
            return card
        return None

    def reshuffle_discard(self):
        self.deck = self.discard_pile.copy()
        self.discard_pile = []
        self.shuffle()

    def reset(self):
        self.deck = self.original_cards.copy()
        self.discard_pile = []
        self.current_card = None
        self.shuffle()

    def stats(self):
        return {
            "Cards in Deck": len(self.deck),
            "Discarded": len(self.discard_pile),
            "Total": len(self.original_cards),
        }

# -------------------------
# Load and setup deck
# -------------------------
@st.cache_resource
def get_shared_deck():
    cards = [c for c in get_event_cards() if c["status"] == "Active"]
    deck = EventDeck(cards)
    deck.shuffle()
    return deck

deck = get_shared_deck()

# -------------------------
# UI
# -------------------------
st.title("🌿 Spirit Island Event Deck")
st.markdown("Draw and view event cards with images from the official Spirit Island wiki.")
st.markdown("---")

# --- Draw button ---
if st.button("🎴 Draw a Card", use_container_width=True):
    card = deck.draw_card()
    if card:
        st.success(f"Drew: {card['name']}")
    else:
        st.error("No cards left — reshuffling discard pile.")
        deck.reshuffle_discard()

# --- Show current card ---
if deck.discard_pile:
    card = deck.discard_pile[-1]
    st.header(card["name"])
    if card.get("image"):
        st.image(card["image"], use_column_width=True)
    else:
        st.info("No image available.")
    st.write(f"**Box:** {card['box']}")
    st.write(f"**Status:** {card['status']}")
    st.markdown(f"[View on Wiki]({card['url']})")

# --- Deck stats ---
st.markdown("---")
stats = deck.stats()
cols = st.columns(len(stats))
for i, (k, v) in enumerate(stats.items()):
    cols[i].metric(k, v)

# --- Recent cards ---
if len(deck.discard_pile) > 1:
    st.subheader("📋 Recently Drawn")
    recent = deck.discard_pile[-5:-1]
    for c in reversed(recent):
        st.write(f"• {c['name']} ({c['box']})")

# --- Reset button ---
if st.button("🔄 Reset Deck", use_container_width=True):
    deck.reset()
    st.success("Deck reset.")
