import streamlit as st
import random
from typing import List, Dict
from event_cards_data import get_event_cards
import time

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
        self.last_modified = time.time()  # Track last modification

    def shuffle(self):
        random.shuffle(self.deck)
        self.last_modified = time.time()

    def draw_card(self) -> Dict:
        if not self.deck:
            self.reshuffle_discard()
        if self.deck:
            self.current_card = self.deck.pop(0)
            self.last_modified = time.time()
            return self.current_card
        return None

    def discard_current_card(self):
        if self.current_card:
            self.discard_pile.append(self.current_card)
            self.current_card = None
            self.last_modified = time.time()

    def reshuffle_discard(self):
        self.deck = self.discard_pile.copy()
        self.discard_pile = []
        self.shuffle()
        self.last_modified = time.time()

    def reset_deck(self):
        self.deck = self.original_cards.copy()
        self.discard_pile = []
        self.current_card = None
        self.shuffle()
        self.last_modified = time.time()

    def get_deck_stats(self) -> Dict:
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
    # Ensure last_modified exists for backwards compatibility
    if not hasattr(deck, 'last_modified'):
        deck.last_modified = time.time()
    return deck

# --- Main App ---
def main():
    st.title("🌿 Spirit Island Event Deck (with Images)")
    st.markdown("Draw and manage shared event cards from the official Spirit Island deck.")
    st.markdown("---")

    deck = get_shared_deck()

    # Initialize session state for tracking last known modification
    if 'last_seen_modification' not in st.session_state:
        st.session_state.last_seen_modification = deck.last_modified

    # Check if deck was modified by another user and trigger auto-refresh
    if deck.last_modified > st.session_state.last_seen_modification:
        st.session_state.last_seen_modification = deck.last_modified
        st.rerun()

    # Auto-refresh every 2 seconds using fragment
    @st.fragment(run_every=2)
    def check_for_updates():
        if deck.last_modified > st.session_state.last_seen_modification:
            st.session_state.last_seen_modification = deck.last_modified
            st.rerun()
    
    check_for_updates()

    # --- Sidebar Controls ---
    st.sidebar.header("🎮 Deck Controls")

    if st.sidebar.button("🔀 Shuffle Deck", use_container_width=True):
        deck.shuffle()
        st.session_state.last_seen_modification = deck.last_modified
        st.sidebar.success("Deck shuffled!")
        st.rerun()

    if st.sidebar.button("🔄 Reset Deck", use_container_width=True):
        deck.reset_deck()
        st.session_state.last_seen_modification = deck.last_modified
        st.sidebar.success("Deck reset!")
        st.rerun()

    # Deck Stats
    stats = deck.get_deck_stats()
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Deck Statistics")
    st.sidebar.metric("Cards in Deck", stats["cards_in_deck"])
    st.sidebar.metric("Cards Discarded", stats["cards_discarded"])
    st.sidebar.metric("Total Cards", stats["total_cards"])

    # Main Content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎴 Current Event Card")

        # Draw Button in Main Area
        if st.button("🎯 Draw & Discard Card", use_container_width=True):
            card = deck.draw_card()
            if card:
                deck.discard_current_card()
                st.session_state.last_seen_modification = deck.last_modified
                st.success(f"Drew and discarded: {card['name']}")
                st.rerun()
            else:
                st.error("No cards left in deck!")

        # Show most recent card
        if deck.discard_pile:
            card = deck.discard_pile[-1]
            st.markdown(f"### {card['name']}")
            if card.get('image'):
                st.image(card['image'], use_container_width=True)
            else:
                st.info("No image available for this card.")
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
            # Last 5 cards, excluding most recent
            recent_cards = deck.discard_pile[-6:-1] if len(deck.discard_pile) > 1 else []
            for c in reversed(recent_cards):
                st.write(f"• {c['name']} ({c['box']})")
        else:
            st.write("No cards drawn yet.")

if __name__ == "__main__":
    main()