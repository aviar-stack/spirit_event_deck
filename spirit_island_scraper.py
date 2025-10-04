import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Optional

class SpiritIslandScraper:
    def __init__(self):
        self.base_url = "https://spiritislandwiki.com"
        self.event_cards_url = "https://spiritislandwiki.com/index.php?title=List_of_Event_Cards"
        
    def fetch_event_cards(self) -> List[Dict[str, str]]:
        """Fetch all event card names and their details from the wiki"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.event_cards_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main table containing event cards
            tables = soup.find_all('table', {'class': 'wikitable'})
            
            event_cards = []
            
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header row
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        # Extract card name from the link
                        card_link = cells[1].find('a')
                        if card_link:
                            card_name = card_link.get_text().strip()
                            card_url = self.base_url + card_link.get('href')
                            
                            # Try to get box art info from first cell
                            box_cell = cells[0]
                            box_img = box_cell.find('img')
                            box_name = "Unknown"
                            if box_img:
                                box_name = box_img.get('alt', 'Unknown')
                            
                            event_cards.append({
                                'name': card_name,
                                'url': card_url,
                                'box': box_name,
                                'status': 'Active'  # Default status
                            })
            
            # Also try to get retired and replaced cards
            self._add_retired_cards(soup, event_cards)
            self._add_replaced_cards(soup, event_cards)
            
            return event_cards
            
        except Exception as e:
            print(f"Error fetching event cards: {e}")
            return []
    
    def _add_retired_cards(self, soup: BeautifulSoup, event_cards: List[Dict]):
        """Add retired event cards to the list"""
        # Look for retired cards section
        retired_section = soup.find('h2', string='Retired Event Cards')
        if retired_section:
            retired_table = retired_section.find_next('table')
            if retired_table:
                rows = retired_table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        card_link = cells[1].find('a')
                        if card_link:
                            card_name = card_link.get_text().strip()
                            card_url = self.base_url + card_link.get('href')
                            
                            box_cell = cells[0]
                            box_img = box_cell.find('img')
                            box_name = "Unknown"
                            if box_img:
                                box_name = box_img.get('alt', 'Unknown')
                            
                            event_cards.append({
                                'name': card_name,
                                'url': card_url,
                                'box': box_name,
                                'status': 'Retired'
                            })
    
    def _add_replaced_cards(self, soup: BeautifulSoup, event_cards: List[Dict]):
        """Add replaced event cards to the list"""
        # Look for replaced cards section
        replaced_section = soup.find('h2', string='Replaced Event Cards')
        if replaced_section:
            replaced_table = replaced_section.find_next('table')
            if replaced_table:
                rows = replaced_table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 3:
                        # Original card
                        card_link = cells[1].find('a')
                        if card_link:
                            card_name = card_link.get_text().strip()
                            card_url = self.base_url + card_link.get('href')
                            
                            box_cell = cells[0]
                            box_img = box_cell.find('img')
                            box_name = "Unknown"
                            if box_img:
                                box_name = box_img.get('alt', 'Unknown')
                            
                            # Get replacement info
                            replacement_link = cells[2].find('a')
                            replacement_name = replacement_link.get_text().strip() if replacement_link else "Unknown"
                            
                            event_cards.append({
                                'name': card_name,
                                'url': card_url,
                                'box': box_name,
                                'status': 'Replaced',
                                'replacement': replacement_name
                            })
    
    def get_card_image_url(self, card_url: str) -> Optional[str]:
        """Get the image URL for a specific event card"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(card_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the main card image
            # Usually in an infobox or as the first large image
            infobox = soup.find('table', {'class': 'infobox'})
            if infobox:
                img = infobox.find('img')
                if img:
                    img_url = img.get('src')
                    if img_url:
                        return self.base_url + img_url
            
            # Fallback: look for any large image
            images = soup.find_all('img')
            for img in images:
                src = img.get('src', '')
                if 'Event' in src or 'event' in src:
                    return self.base_url + src
            
            return None
            
        except Exception as e:
            print(f"Error fetching card image for {card_url}: {e}")
            return None

def main():
    """Test the scraper"""
    scraper = SpiritIslandScraper()
    cards = scraper.fetch_event_cards()
    
    print(f"Found {len(cards)} event cards:")
    for i, card in enumerate(cards[:10]):  # Show first 10
        print(f"{i+1}. {card['name']} ({card['box']}) - {card['status']}")
    
    if len(cards) > 10:
        print(f"... and {len(cards) - 10} more cards")
    
    # Save to JSON file
    with open('event_cards.json', 'w', encoding='utf-8') as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(cards)} cards to event_cards.json")

if __name__ == "__main__":
    main()

