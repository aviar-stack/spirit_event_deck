def main():
    st.title("🌿 Spirit Island Event Card Deck (Shared Game)")
    st.markdown("Everyone connected to this app shares the same deck and discard pile.")
    st.markdown("---")

    # Auto-refresh every 5 seconds so all players see updates
    st_autorefresh = st.experimental_rerun  # fallback if Streamlit < 1.31
    try:
        st_autorefresh = st.experimental_data_editor  # dummy fallback
    except Exception:
        pass
    st_autorefresh_interval = st.experimental_rerun if False else None
    st_autorefresh = st.autorefresh if hasattr(st, "autorefresh") else None
    if st_autorefresh:
        st_autorefresh(interval=5000, key="refresh")

    # Load event cards
    with st.spinner("Loading event cards..."):
        event_cards = load_event_cards()

    if not event_cards:
        st.error("Failed to load event cards. Please try again.")
        return

    filtered_cards = [card for card in event_cards if card['status'] == 'Active']

    # Shared deck stored globally across all users
    @st.cache_resource
    def get_shared_deck(cards):
        deck = EventDeck(cards)
        deck.shuffle()
        return deck

    deck = get_shared_deck(filtered_cards)

    # Sidebar controls
    st.sidebar.header("🎮 Deck Controls")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔀 Shuffle Deck", use_container_width=True):
            deck.shuffle()
            st.success("Deck shuffled!")
            st.experimental_rerun()

    with col2:
        if st.button("🎯 Draw & Discard Card", use_container_width=True):
            card = deck.draw_card()
            if card:
                deck.discard_current_card()
                st.success(f"Drew and discarded: {card['name']}")
            else:
                st.error("No cards left in deck!")
            st.experimental_rerun()

    if st.sidebar.button("🔄 Reset Deck", use_container_width=True):
        st.cache_resource.clear()  # clear shared cache
        deck = get_shared_deck(filtered_cards)
        st.success("Deck reset!")
        st.experimental_rerun()

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
            card = deck.discard_pile[-1]
            with st.container():
                st.markdown(f"### {card['name']}")
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.markdown(f"**Box:** {card['box']}")
                with info_col2:
                    st.markdown(f"**Status:** {card['status']}")
                if card.get('replacement'):
                    st.markdown(f"**Replaced by:** {card['replacement']}")
                st.markdown(f"[View on Wiki]({card['url']})")
        else:
            st.info("Click 'Draw Card' to draw an event card from the deck!")

    with col2:
        st.subheader("📋 Recent Cards")

        if deck.discard_pile:
            st.write("Recently drawn cards:")
            recent_cards = deck.discard_pile[-5:-1] if len(deck.discard_pile) > 1 else deck.discard_pile[:-1]
            for card in reversed(recent_cards):
                st.write(f"• {card['name']} ({card['box']})")
        else:
            st.write("No cards drawn yet.")
