# Spirit Island Event Card Deck

A simple Streamlit web application for drawing and managing Spirit Island Event Cards from the official deck.

## Features

- **Complete Event Card Database**: Contains all 62 active event cards from the official Spirit Island expansions
- **Deck Simulation**: Shuffle, draw, and discard cards just like in the real game
- **Statistics**: Track deck size, discarded cards, and more

## Event Cards Included

### Active Cards (62 total)
- **Branch and Claw** (23 cards): Cultural Assimilation, Distant Exploration, Farmers Seek the Dahan for Aid, etc.
- **Jagged Earth** (30 cards): Bureaucrats Adjust Funding, Cities Rise, Civic Engagement, etc.
- **Nature Incarnate** (9 cards): Accumulated Devastation, An Ominous Dawn, Ethereal Conjunction, etc.

### Additional Cards
- **Retired Cards** (2): A Strange Madness Among the Beasts, Outpaced
- **Replaced Cards** (1): War Touches the Island's Shores (replaced by Far-off Wars Touch the Island)

## How to Run

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run spirit_island_app.py
   ```

3. **Open your browser** to the URL shown in the terminal (usually `http://localhost:8501`)

## How to Use

### Deck Controls
- **Shuffle Deck**: Randomly shuffle the remaining cards
- **Draw Card**: Draw the top card from the deck
- **Reset Deck**: Reset to original shuffled state
- **Discard Current**: Discard the currently drawn card

### Features
- **Current Card Display**: Shows the currently drawn card with details
- **Recent Cards**: Lists recently discarded cards
- **Deck Statistics**: Shows cards remaining, discarded, and total

## Data Source

Event card data is sourced from the [Spirit Island Wiki](https://spiritislandwiki.com/index.php?title=List_of_Event_Cards) and includes:
- Card names
- Expansion boxes
- Card status (Active/Retired/Replaced)
- Links to wiki pages

## Files

- `spirit_island_app.py`: Main Streamlit application
- `event_cards_data.py`: Static event card database
- `spirit_island_scraper.py`: Web scraper (not used in current version)
- `requirements.txt`: Python dependencies

## Dependencies

- streamlit
- requests
- beautifulsoup4
- lxml

## Notes

This is a fan-made tool and is not affiliated with Greater Than Games or the official Spirit Island game. All card names and game elements are trademarks of Greater Than Games.
