import os

CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 600))
TOKEN = os.getenv('TOKEN')

CHECK_COMMAND = "s"
CHECK_ALIASES = ['sprawdz', 'check']
LIST_COMMAND = "l"
LIST_ALIASES = ['lista', 'list']

urls = {
    "Cannabis Flos THC 18% CBD ≤ 1% (S-Lab)": "https://www.gdziepolek.pl/produkty/117668/cannabis-flos-thc-18-cbd-1-s-lab-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 22% CBD ≤1% (S-Lab)": "https://www.gdziepolek.pl/produkty/121591/cannabis-flos-thc-22-cbd-1-s-lab-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    # ... pozostale URL'e aby sprawdzic np dla katowic trzeba zmienic ostatni parametr na w-katowicach itd
}
