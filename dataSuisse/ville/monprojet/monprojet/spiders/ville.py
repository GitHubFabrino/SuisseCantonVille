import scrapy
from scrapy.selector import Selector

class VilleSpider(scrapy.Spider):
    name = 'ville'

    def start_requests(self):
        # Chemin absolu vers le fichier HTML
        file_path = r'C:\Users\MADA-Digital\dev\Scrapy\dataSuisse\ville\monprojet\monprojet\html.html'
        
        # Lire le contenu du fichier HTML
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Créer un sélecteur à partir du contenu HTML
        selector = Selector(text=html_content)
        
        # Extraire les données
        for link in selector.css('div.dropdown-content a.dropdown-item'):
            yield {
                'nom_ville': link.css('::text').get().strip() if link.css('::text').get() else '',
                # 'code': link.attrib.get('g0', ''),
                # 'data_search': link.attrib.get('data-search', ''),
                # 'lien': link.attrib.get('href', '')
            }
