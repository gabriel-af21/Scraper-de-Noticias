import requests
from bs4 import BeautifulSoup
import json, csv

#Url dos sites que o Scraper vai capturar as manchetes
urls=[
    'https://www.cnnbrasil.com.br',
    "https://www.folha.uol.com.br"
]

#Função para pegar as noticias
def PegarNoticias(url):
    try:
        response=requests.get(url)
        
        if response.status_code == 200:
            soup=BeautifulSoup(response.content, 'html.parser')
            news_list=[]
            if 'cnnbrasil.com' in url:
                articles = soup.find_all('div', class_='has--thumb')  # Para CNN Brasil                
                headlines = [article.find('h3') for article in articles]    
                print(f"Encontrados {len(headlines)} artigos em {url}")            
                           
            elif 'folha.uol.com.br' in url:  
                articles = soup.find_all('div', class_='c-headline__content')  # Folha                
                headlines = [article.find('h2') for article in articles]
                print(f"Encontrados {len(headlines)} artigos em {url}")
                

             # Iterar pelos artigos e extrair manchetes e links
            for article in articles:
                headline = article.find('h3')  # Pegue o título (pode mudar para h2 dependendo do site)
                if headline == None:
                     headline = article.find('h2')
                link = article.find('a', href=True)  # Pegar o link
                
                
                

        
                if headline and link:
                    news_info = {
                        'headline': headline.get_text().strip(),
                        'link': link['href'] if link['href'].startswith('http') else url + link['href']  # Corrigir link relativo
                    }
                    
                    news_list.append(news_info)
                    


            return news_list
        else:
            print(f"Erro ao acessar o site {url}: {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro ao processar o site {url}: {e}")
        return []
    

all_news =[]

for url in urls:
    print(f"Extraindo noticias de: {url}")
    news_info = PegarNoticias(url)

    all_news.extend(news_info)
    

for i, news in enumerate(all_news,1):
    print(f"{i}. Título: {news['headline']}")
    print(f"   Link: {news['link']}\n")

#Salvar em JSON
with open('all_news.json', 'w', encoding='utf-8') as f:
    json.dump(all_news, f, ensure_ascii=False, indent=4)

#Salvar em CSV
with open('all_news.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['headline', 'link'])
    writer.writeheader()
    for news in all_news:
        writer.writerow(news)
    


            
