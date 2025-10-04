import streamlit as st
import random

st.set_page_config(page_title="Spirit Island Event Deck", layout="wide")

# --- Active Event Cards with image URLs ---
cards = [
    {"title": "Cultural Assimilation", "img": "https://spiritislandwiki.com/images/c/c3/Cultural_Assimilation.png"},
    {"title": "Distant Exploration", "img": "https://spiritislandwiki.com/images/c/c3/Distant_Exploration.png"},
    {"title": "Farmers Seek the Dahan for Aid", "img": "https://spiritislandwiki.com/images/c/c3/Farmers_Seek_the_Dahan_for_Aid.png"},
    {"title": "Heavy Farming", "img": "https://spiritislandwiki.com/images/c/c3/Heavy_Farming.png"},
    {"title": "Interesting Discoveries", "img": "https://spiritislandwiki.com/images/c/c3/Interesting_Discoveries.png"},
    {"title": "Invaders Surge Inland", "img": "https://spiritislandwiki.com/images/c/c3/Invaders_Surge_Inland.png"},
    {"title": "Investigation of Dangers", "img": "https://spiritislandwiki.com/images/c/c3/Investigation_of_Dangers.png"},
    {"title": "Missionaries Arrive", "img": "https://spiritislandwiki.com/images/c/c3/Missionaries_Arrive.png"},
    {"title": "New Species Spread", "img": "https://spiritislandwiki.com/images/c/c3/New_Species_Spread.png"},
    {"title": "Population Rises", "img": "https://spiritislandwiki.com/images/c/c3/Population_Rises.png"},
    {"title": "Promising Farmland", "img": "https://spiritislandwiki.com/images/c/c3/Promising_Farmland.png"},
    {"title": "Putting Down Roots", "img": "https://spiritislandwiki.com/images/c/c3/Putting_Down_Roots.png"},
    {"title": "Rising Interest in the Island", "img": "https://spiritislandwiki.com/images/c/c3/Rising_Interest_in_the_Island.png"},
    {"title": "Sacred Sites Under Threat", "img": "https://spiritislandwiki.com/images/c/c3/Sacred_Sites_Under_Threat.png"},
    {"title": "Search for New Lands", "img": "https://spiritislandwiki.com/images/c/c3/Search_for_New_Lands.png"},
    {"title": "Seeking the Interior", "img": "https://spiritislandwiki.com/images/c/c3/Seeking_the_Interior.png"},
    {"title": "Slave Rebellion", "img": "https://spiritislandwiki.com/images/c/c3/Slave_Rebellion.png"},
    {"title": "Strange Tales Attract Explorers", "img": "https://spiritislandwiki.com/images/c/c3/Strange_Tales_Attract_Explorers.png"},
    {"title": "Tight-Knit Communities", "img": "https://spiritislandwiki.com/images/c/c3/Tight-Knit_Communities.png"},
    {"title": "Urban Development", "img": "https://spiritislandwiki.com/images/c/c3/Urban_Development.png"},
    {"title": "Wave of Reconnaissance", "img": "https://spiritislandwiki.com/images/c/c3/Wave_of_Reconnaissance.png"},
    {"title": "Well-Prepared Explorers", "img": "https://spiritislandwiki.com/images/c/c3/Well-Prepared_Explorers.png"},
    {"title": "Years of Little Rain", "img": "https://spiritislandwiki.com/images/c/c3/Years_of_Little_Rain.png"},
    {"title": "Bureaucrats Adjust Funding", "img": "https://spiritislandwiki.com/images/c/c3/Bureaucrats_Adjust_Funding.png"},
    {"title": "Cities Rise", "img": "https://spiritislandwiki.com/images/c/c3/Cities_Rise.png"},
    {"title": "Civic Engagement", "img": "https://spiritislandwiki.com/images/c/c3/Civic_Engagement.png"},
    {"title": "Coastal Towns Multiply", "img": "https://spiritislandwiki.com/images/c/c3/Coastal_Towns_Multiply.png"},
    {"title": "Dahan Trade with the Invaders", "img": "https://spiritislandwiki.com/images/c/c3/Dahan_Trade_with_the_Invaders.png"},
    {"title": "Eager Explorers", "img": "https://spiritislandwiki.com/images/c/c3/Eager_Explorers.png"},
    {"title": "Fortune-Seekers", "img": "https://spiritislandwiki.com/images/c/c3/Fortune-Seekers.png"},
    {"title": "Gradual Corruption", "img": "https://spiritislandwiki.com/images/c/c3/Gradual_Corruption.png"},
    {"title": "Hard-Working Settlers", "img": "https://spiritislandwiki.com/images/c/c3/Hard-Working_Settlers.png"},
    {"title": "Harvest Bounty, Harvest Dust", "img": "https://spiritislandwiki.com/images/c/c3/Harvest_Bounty_Harvest_Dust.png"},
    {"title": "Invested Aristocracy", "img": "https://spiritislandwiki.com/images/c/c3/Invested_Aristocracy.png"},
    {"title": "Lesser Spirits Imperiled", "img": "https://spiritislandwiki.com/images/c/c3/Lesser_Spirits_Imperiled.png"},
    {"title": "Life's Balance Tilts", "img": "https://spiritislandwiki.com/images/c/c3/Life's_Balance_Tilts.png"},
    {"title": "Mapmakers Chart the Wild", "img": "https://spiritislandwiki.com/images/c/c3/Mapmakers_Chart_the_Wild.png"},
    {"title": "No Bravery Without Numbers", "img": "https://spiritislandwiki.com/images/c/c3/No_Bravery_Without_Numbers.png"},
    {"title": "Numinous Crisis", "img": "https://spiritislandwiki.com/images/c/c3/Numinous_Crisis.png"},
    {"title": "Overconfidence", "img": "https://spiritislandwiki.com/images/c/c3/Overconfidence.png"},
    {"title": "Provincial Seat", "img": "https://spiritislandwiki.com/images/c/c3/Provincial_Seat.png"},
    {"title": "Pull Together in Adversity", "img": "https://spiritislandwiki.com/images/c/c3/Pull_Together_in_Adversity.png"},
    {"title": "Relentless Optimism", "img": "https://spiritislandwiki.com/images/c/c3/Relentless_Optimism.png"},
    {"title": "Remnants of a Spirit's Heart", "img": "https://spiritislandwiki.com/images/c/c3/Remnants_of_a_Spirits_Heart.png"},
    {"title": "Resourceful Populace", "img": "https://spiritislandwiki.com/images/c/c3/Resourceful_Populace.png"},
    {"title": "Seek New Farmland", "img": "https://spiritislandwiki.com/images/c/c3/Seek_New_Farmland.png"},
    {"title": "Smaller Ports Spring Up", "img": "https://spiritislandwiki.com/images/c/c3/Smaller_Ports_Spring_Up.png"},
    {"title": "Sprawl Contained by the Wilds", "img": "https://spiritislandwiki.com/images/c/c3/Sprawl_Contained_by_the_Wilds.png"},
    {"title": "Temporary Truce", "img": "https://spiritislandwiki.com/images/c/c3/Temporary_Truce.png"},
    {"title": "The Frontier Calls", "img": "https://spiritislandwiki.com/images/c/c3/The_Frontier_Calls.png"},
    {"title": "The Struggles of Growth", "img": "https://spiritislandwiki.com/images/c/c3/The_Struggles_of_Growth.png"},
    {"title": "Thriving Trade", "img": "https://spiritislandwiki.com/images/c/c3/Thriving_Trade.png"},
    {"title": "Wounded Lands Attract Explorers", "img": "https://spiritislandwiki.com/images/c/c3/Wounded_Lands_Attract_Explorers.png"},
    {"title": "Accumulated Devastation", "img": "https://spiritislandwiki.com/images/c/c3/Accumulated_Devastation.png"},
    {"title": "An Ominous Dawn", "img": "https://spiritislandwiki.com/images/c/c3/An_Ominous_Dawn.png"},
    {"title": "Ethereal Conjunction", "img": "https://spiritislandwiki.com/images/c/c3/Ethereal_Conjunction.png"},
    {"title": "Far-off Wars Touch the Island", "img": "https://spiritislandwiki.com/images/c/c3/Far-off_Wars_Touch_the_Island.png"},
    {"title": "Focused Farming", "img": "https://spiritislandwiki.com/images/c/c3/Focused_Farming.png"},
    {"title": "Influx of Settlers", "img": "https://spiritislandwiki.com/images/c/c3/Influx_of_Settlers.png"},
    {"title": "Search for Unclaimed Land", "img": "https://spiritislandwiki.com/images/c/c3/Search_for_Unclaimed_Land.png"},
    {"title": "Terror Spikes Upwards", "img": "https://spiritislandwiki.com/images/c/c3/Terror_Spikes_Upwards.png"},
    {"title": "Visions Out of Time", "img": "https://spiritislandwiki.com/images/c/c3/Visions_Out_of_Time_%28ni%29.png"},
]

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
st.title("Spirit Island — Event Deck Simulator")

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
