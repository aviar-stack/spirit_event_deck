"""
Simple Spirit Island Event Deck — Streamlit app
- Single-file Streamlit app (save as app.py)
- Features: deck (shuffle/draw top/draw random), reveal with image, discard pile, add events by URL/title/text, import/export JSON, session_state persistence
- Run: `pip install streamlit` then `streamlit run app.py`
"""
import streamlit as st
import random
import json
import uuid
from io import BytesIO

st.set_page_config(page_title="Spirit Island — Event Deck", layout="wide")

# Helpers
def uid():
    return uuid.uuid4().hex[:8]

SAMPLE = [
    {"id": uid(), "title": "Wild Storm", "img": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800&q=60", "text": "A sudden storm lashes the coast."},
    {"id": uid(), "title": "Lost Shrine", "img": "https://images.unsplash.com/photo-1508766206392-8bd5cf550d1d?w=800&q=60", "text": "A shrine appears where none stood before."},
    {"id": uid(), "title": "Merchant Caravan", "img": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800&q=60", "text": "Caravans bring strange goods — and trouble."},
]

if "deck" not in st.session_state:
    st.session_state.deck = SAMPLE.copy()
if "discard" not in st.session_state:
    st.session_state.discard = []
if "revealed" not in st.session_state:
    st.session_state.revealed = None

# Actions
def shuffle_deck():
    random.shuffle(st.session_state.deck)

def draw_top():
    if st.session_state.deck:
        st.session_state.revealed = st.session_state.deck.pop(0)

def draw_random():
    if st.session_state.deck:
        i = random.randrange(len(st.session_state.deck))
        st.session_state.revealed = st.session_state.deck.pop(i)

def discard_revealed():
    if st.session_state.revealed:
        st.session_state.discard.insert(0, st.session_state.revealed)
        st.session_state.revealed = None

def put_revealed_bottom():
    if st.session_state.revealed:
        st.session_state.deck.append(st.session_state.revealed)
        st.session_state.revealed = None

def add_event_top(title, img, text):
    if not title:
        return
    ev = {"id": uid(), "title": title, "img": img or "", "text": text or ""}
    st.session_state.deck.insert(0, ev)

def add_event_bottom(title, img, text):
    if not title:
        return
    ev = {"id": uid(), "title": title, "img": img or "", "text": text or ""}
    st.session_state.deck.append(ev)

def clear_discard():
    st.session_state.discard = []

def restore_sample():
    st.session_state.deck = [dict(x, id=uid()) for x in SAMPLE]
    st.session_state.discard = []
    st.session_state.revealed = None

def export_state():
    payload = json.dumps({"deck": st.session_state.deck, "discard": st.session_state.discard}, indent=2)
    return payload

def import_state(uploaded_file):
    if not uploaded_file:
        return
    try:
        raw = uploaded_file.read()
        parsed = json.loads(raw)
        if isinstance(parsed.get("deck"), list):
            st.session_state.deck = parsed["deck"]
        if isinstance(parsed.get("discard"), list):
            st.session_state.discard = parsed["discard"]
        st.success("Imported state")
    except Exception as e:
        st.error(f"Failed to import: {e}")

# Layout
st.title("Spirit Island — Event Deck (Streamlit)")

with st.sidebar:
    st.header("Controls")
    st.button("Shuffle deck", on_click=shuffle_deck)
    st.button("Draw top", on_click=draw_top)
    st.button("Draw random", on_click=draw_random)
    st.button("Discard revealed", on_click=discard_revealed)
    st.button("Put revealed to bottom", on_click=put_revealed_bottom)
    st.button("Restore sample deck", on_click=restore_sample)
    st.markdown("---")
    uploaded = st.file_uploader("Import JSON (deck+discard)", type=["json"])
    if uploaded is not None:
        import_state(uploaded)
    st.download_button("Export state (JSON)", data=export_state(), file_name="spirit_island_events.json", mime="application/json")

# Main columns: Deck + Add form, Revealed & Discard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Deck ({len(st.session_state.deck)})")
    # Preview first 6
    for i, card in enumerate(st.session_state.deck[:6]):
        cols = st.columns([1, 4, 1])
        with cols[0]:
            if card.get("img"):
                st.image(card.get("img"), width=100)
            else:
                st.write("")
        with cols[1]:
            st.markdown(f"**{card.get('title')}**")
            st.write(card.get("text"))
        with cols[2]:
            if st.button(f"Reveal {i}", key=f"reveal_{card['id']}"):
                st.session_state.revealed = st.session_state.deck.pop(i)
    if len(st.session_state.deck) > 6:
        st.write(f"... +{len(st.session_state.deck)-6} more")

    st.markdown("---")
    st.subheader("Add event")
    with st.form("add_form"):
        t = st.text_input("Title")
        img = st.text_input("Image URL (optional)")
        txt = st.text_area("Short text (optional)")
        col_a, col_b = st.columns(2)
        with col_a:
            add_top = st.form_submit_button("Add to top")
        with col_b:
            add_bottom = st.form_submit_button("Add to bottom")
        if add_top:
            add_event_top(t, img, txt)
            st.experimental_rerun()
        if add_bottom:
            add_event_bottom(t, img, txt)
            st.experimental_rerun()

    st.markdown("---")
    st.subheader("Full deck list")
    for card in st.session_state.deck:
        c1, c2, c3 = st.columns([1, 6, 1])
        with c1:
            if card.get("img"):
                st.image(card.get("img"), width=80)
        with c2:
            st.markdown(f"**{card.get('title')}**")
            st.write(card.get("text"))
        with c3:
            if st.button(f"Reveal-{card['id']}", key=f"r_{card['id']}"):
                # remove the specific card
                st.session_state.deck = [c for c in st.session_state.deck if c['id'] != card['id']]
                st.session_state.revealed = card
                st.experimental_rerun()

with col2:
    st.subheader("Revealed")
    if st.session_state.revealed:
        card = st.session_state.revealed
        if card.get("img"):
            st.image(card.get("img"), use_column_width=True)
        st.markdown(f"### {card.get('title')}")
        st.write(card.get("text"))
        st.button("Discard", on_click=discard_revealed)
        st.button("Put to bottom", on_click=put_revealed_bottom)
        st.button("Close", on_click=lambda: st.session_state.__setitem__('revealed', None))
    else:
        st.info("No card revealed. Draw a card or reveal from the deck list.")

    st.markdown("---")
    st.subheader(f"Discard ({len(st.session_state.discard)})")
    for card in st.session_state.discard:
        c1, c2, c3 = st.columns([1, 6, 1])
        with c1:
            if card.get("img"):
                st.image(card.get("img"), width=64)
        with c2:
            st.markdown(f"**{card.get('title')}**")
            st.write(card.get("text"))
        with c3:
            if st.button(f"Return-{card['id']}", key=f"ret_{card['id']}"):
                st.session_state.deck.insert(0, card)
                st.session_state.discard = [c for c in st.session_state.discard if c['id'] != card['id']]
                st.experimental_rerun()
            if st.button(f"Remove-{card['id']}", key=f"rm_{card['id']}"):
                st.session_state.discard = [c for c in st.session_state.discard if c['id'] != card['id']]
                st.experimental_rerun()

    st.markdown("---")
    if st.button("Shuffle discard into bottom"):
        st.session_state.deck.extend(list(reversed(st.session_state.discard)))
        st.session_state.discard = []
        st.experimental_rerun()
    if st.button("Clear discard"):
        clear_discard()
        st.experimental_rerun()

# Footer
st.caption("Local-only: state lives in Streamlit session. Use Export to save a JSON backup.")
