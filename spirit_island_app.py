import streamlit as st
import json
import random
from typing import List, Dict
import os
from event_cards_data import get_event_cards

# Page configuration
st.set_page_config(
    page_title="Spirit Island Event Cards",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_event_cards() -> List[Dict]:
    """Load event cards from static data"""
    return get_event_cards()


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

def main():
    st.title("🌿 Spirit Island Event Card Deck")
    st.markdown("Draw and manage event cards from the official Spirit Island deck")
    st.markdown("---")
    
    # Load event cards
    with st.spinner("Loading event cards..."):
        event_cards = load_event_cards()
    
    if not event_cards:
        st.error("Failed to load event cards. Please try again.")
        return
    
    # Initialize deck with all active cards by default
    filtered_cards = [card for card in event_cards if card['status'] == 'Active']
    
    # Initialize session state
    if 'deck' not in st.session_state:
        st.session_state.deck = EventDeck(filtered_cards)
        st.session_state.deck.shuffle()
    
    deck = st.session_state.deck
    
    # Sidebar controls
    st.sidebar.header("🎮 Deck Controls")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔀 Shuffle Deck", use_container_width=True):
            deck.shuffle()
            st.success("Deck shuffled!")
    
    with col2:
        if st.button("🎯 Draw & Discard Card", use_container_width=True):
            card = deck.draw_card()
            if card:
                st.session_state.current_card = card
                # Immediately discard the drawn card
                deck.discard_current_card()
                st.session_state.current_card = None
                st.success(f"Drew and discarded: {card['name']}")
            else:
                st.error("No cards left in deck!")
    
    if st.sidebar.button("🔄 Reset Deck", use_container_width=True):
        deck.reset_deck()
        st.session_state.current_card = None
        st.success("Deck reset!")
    
    # Deck statistics
    stats = deck.get_deck_stats()
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Deck Statistics")
    st.sidebar.metric("Cards in Deck", stats["cards_in_deck"])
    st.sidebar.metric("Cards Discarded", stats["cards_discarded"])
    st.sidebar.metric("Total Cards", stats["total_cards"])
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎴 Most Recent Event Card")
        
        if deck.discard_pile:
            card = deck.discard_pile[-1]  # Most recently discarded card
            
            # Create card display
            with st.container():
                st.markdown(f"### {card['name']}")
                
                # Card info
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.markdown(f"**Box:** {card['box']}")
                with info_col2:
                    st.markdown(f"**Status:** {card['status']}")
                
                if card.get('replacement'):
                    st.markdown(f"**Replaced by:** {card['replacement']}")
                
                # Link to wiki
                st.markdown(f"[View on Wiki]({card['url']})")
                
        else:
            st.info("Click 'Draw Card' to draw an event card from the deck!")
    
    with col2:
        st.subheader("📋 Recent Cards")
        
        if deck.discard_pile:
            st.write("Recently drawn cards:")
            # Show last 4 cards (excluding the most recent which is shown above)
            recent_cards = deck.discard_pile[-5:-1] if len(deck.discard_pile) > 1 else deck.discard_pile[:-1]
            for card in reversed(recent_cards):  # Show in reverse order (oldest first)
                st.write(f"• {card['name']} ({card['box']})")
        else:
            st.write("No cards drawn yet.")
    

if __name__ == "__main__":
    main()

