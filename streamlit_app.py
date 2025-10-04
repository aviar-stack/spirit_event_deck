import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

st.set_page_config(page_title="Spirit Island Event Deck", layout="wide")
st.title("Spirit Island — Event Deck Simulator")

# --- Scrape Active Event Cards from wiki ---
@st.cache_data
def get_active_event_cards():
    url = "https://spiritislandwiki.com/index.php?title=List_of_Event_Cards"
    base = "https://spiritislandwiki.com"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    
    cards = []
    # Find Active Event Cards section
    active_header = soup.find("span", {"id": "Active_Event_Cards"})
    if not active_header:
        return []
    table = active_header.parent.find_next_sibling("table")
    if not table:
        return []
    
    for row in table.find_all("tr")[1:]:  # skip header
        cols = row.find_all("td")
        if len(cols) >= 2:
            img_tag = cols[0].find("img")
            name_tag = cols[1].find("a")
            if img_tag and name_tag:
                img_url = base + img_tag["src"]
                name = name_tag.text.strip()
                cards.append({"title": name, "img": img_url})
    return cards

cards = get_active_event_cards()

if not cards:
    st.error("Could not fetch active event cards from the wiki.")
    st.stop()

# --- Session State ---
if "deck" not in st.session_state:
    st.session_state.deck = cards.copy()
if "discard" not in st.session_state:
    st.session_state.discard = []
if "revealed" not in st.session_state:
    st.session_state.revealed = None

# --- Actions ---
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

# --- Layout ---
col1, col2 = st.columns([2,1])

with col1:
    st.subheader(f"Deck ({len(st.session_state.deck)})")
    for card in st.session_state.deck[:6]:
        st.image(card["img"], width=100)
        st.write(card["title"])
    st.button("Shuffle Deck", on_click=shuffle_deck)
    st.button("Draw Top", on_click=draw_top)
    st.button("Draw Random", on_click=draw_random)

with col2:
    st.subheader("Revealed")
    if st.session_state.revealed:
        st.image(st.session_state.revealed["img"], use_column_width=True)
        st.write(st.session_state.revealed["title"])
        st.button("Discard", on_click=discard_revealed)

    st.subheader(f"Discard ({len(st.session_state.discard)})")
    for c in st.session_state.discard[:5]:
        st.image(c["img"], width=80)
        st.write(c["title"])
