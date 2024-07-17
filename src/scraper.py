import requests
from bs4 import BeautifulSoup

def fetch_availability(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    apteki = soup.find_all('li', class_='MuiListItem-root')

    data = []
    for apteka in apteki:
        apteka_nazwa_elem = apteka.find('a', class_='MuiTypography-h2')
        apteka_adres_elem = apteka.find_all('p')[1] if len(apteka.find_all('p')) > 1 else None  
        apteka_status_elem = apteka.find('span', class_='MuiTypography-root')
        
        # Znajdowanie odmiany leku
        odmiana_elems = apteka.find_all('p', class_='MuiTypography-body2')
        apteka_odmiana_elem = odmiana_elems[1] if len(odmiana_elems) > 1 and 'krótkie daty ważności' not in odmiana_elems[1].text else None  
        
        # Znajdowanie krótkiej daty ważności i przecen
        apteka_rodzaj_elem = apteka.find('p', text=lambda t: t and 'krótkie daty ważności' in t)
        apteka_przeceny_elem = []
        if apteka_rodzaj_elem:
            sibling = apteka_rodzaj_elem.find_next_sibling('p')
            while sibling and 'krótkie daty ważności' not in sibling.text:
                if '➔' in sibling.text:
                    apteka_przeceny_elem.append(sibling.text.strip())
                sibling = sibling.find_next_sibling('p')

        apteka_nazwa = apteka_nazwa_elem.text.strip() if apteka_nazwa_elem else 'Brak nazwy'
        apteka_adres = apteka_adres_elem.text.strip() if apteka_adres_elem else 'Brak adresu'
        apteka_status = apteka_status_elem.text.strip() if apteka_status_elem else 'Brak statusu'
        apteka_odmiana = apteka_odmiana_elem.text.strip() if apteka_odmiana_elem else 'Brak odmiany'
        apteka_rodzaj = apteka_rodzaj_elem.text.strip() if apteka_rodzaj_elem else 'Brak rodzaju'
        apteka_przeceny = ' '.join(apteka_przeceny_elem) if apteka_przeceny_elem else 'Brak przeceny'

        data.append([apteka_nazwa, apteka_adres, apteka_status, apteka_odmiana, apteka_rodzaj, apteka_przeceny])

    return data
