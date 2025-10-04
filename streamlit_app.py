import streamlit as st
import random
from typing import List, Dict
from event_cards_data import get_event_cards

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Spirit Island Event Deck (Shared)",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Event Deck Logic ---
class EventDeck:
    def __init__(self, cards: List[Dict]):
        self.original_cards = cards.copy()
        self.deck = cards.copy()
        self.discard_pile = []
        self.current_card = None

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.deck)

    def draw_card(self) -> Dict:
        """Draw a card from the deck"""
        if not self.deck:
            self.reshuffle_discard()

        if self.deck:
            self.current_card = self.deck.pop(0)
            return self.current_card
        return None

    def discard_current_card(self):
        """Discard the current card"""
        if self.current_card:
            self.discard_pile.append(self.current_card)
            self.current_card = None

    def reshuffle_discard(self):
        """Reshuffle discard pile back into deck"""
        self.deck = self.discard_pile.copy()
        self.discard_pile = []
        self.shuffle()

    def reset_deck(self):
        """Reset deck to original state"""
        self.deck = self.original_cards.copy()
        self.discard_pile = []
        self.current_card = None
        self.shuffle()

    def get_deck_stats(self) -> Dict:
        """Get deck statistics"""
        return {
            "cards_in_deck": len(self.deck),
            "cards_discarded": len(self.discard_pile),
            "total_cards": len(self.original_cards)
        }

# --- Shared Deck for All Users ---
@st.cache_resource
def get_shared_deck():
    """Create one shared EventDeck instance for all users"""
    cards = [card for card in get_event_cards() if card['status'] == 'Active']
    deck = EventDeck(cards)
    deck.shuffle()
    return deck

# --- Main App ---
def main():
    st.title("🌿 Spirit Island Event Deck (with Images?)")
    st.markdown("Manage and draw shared event cards from the official Spirit Island deck.")
    st.markdown("---")

    deck = get_shared_deck()

    # Sidebar Controls
    st.sidebar.header("🎮 Deck Controls")

    if st.sidebar.button("🔀 Shuffle Deck", use_container_width=True):
        deck.shuffle()
        st.sidebar.success("Deck shuffled!")

    if st.sidebar.button("🔄 Reset Deck", use_container_width=True):
        deck.reset_deck()
        st.sidebar.success("Deck reset!")

    # Deck Stats
    stats = deck.get_deck_stats()
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Deck Statistics")
    st.sidebar.metric("Cards in Deck", stats["cards_in_deck"])
    st.sidebar.metric("Cards Discarded", stats["cards_discarded"])
    st.sidebar.metric("Total Cards", stats["total_cards"])

    st.sidebar.markdown("---")
    if st.sidebar.button("🔁 Refresh View", use_container_width=True):
        st.rerun()

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎴 Current Event Card")

        # --- Draw Button (main area) ---
        draw_col1, draw_col2 = st.columns([1, 3])
        with draw_col1:
            if st.button("🎯 Draw & Discard Card", use_container_width=True):
                card = deck.draw_card()
                if card:
                    deck.discard_current_card()
                    st.success(f"Drew and discarded: {card['name']}")
                    st.rerun()
                else:
                    st.error("No cards left in deck!")

        # --- Show last drawn card ---
        if deck.discard_pile:
            card = deck.discard_pile[-1]
            st.markdown(f"### {card['name']}")

            if card.get('image'):
                st.image(card['image'], use_column_width=True)
                
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.markdown(f"**Box:** {card['box']}")
            with info_col2:
                st.markdown(f"**Status:** {card['status']}")

            if card.get('replacement'):
                st.markdown(f"**Replaced by:** {card['replacement']}")

            st.markdown(f"[View on Wiki]({card['url']})")
        else:
            st.info("Click 'Draw & Discard Card' to draw the first event card!")

    with col2:
        st.subheader("📋 Recent Cards")
        if deck.discard_pile:
            st.write("Recently drawn cards:")
            recent_cards = deck.discard_pile[-5:]
            for c in reversed(recent_cards):
                st.write(f"• {c['name']} ({c['box']})")
        else:
            st.write("No cards drawn yet.")

if __name__ == "__main__":
    main()
