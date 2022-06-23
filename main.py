from flask import *
from colorama import *
import re, os
import cloudscraper
init()

app = Flask(__name__)

def link_topla():
    ic = ["png","woff","/tag/","comment","members","#respond","t.me","/editor/","apple.com","/yazar/","pazar.evrimagaci.org","/icerikler","amazon.com","language_id","yazarlarimiz/","biz-kimiz","yazi-dizileri","yazi-dizisi","destek","linkedin.com","reddit.com","etiket","/profil/","markreadhash","jpg","jpeg","css","iletisim","js","woff2","author","xml","feed","google.com","hakkimizda","page","www.youtube.com","gmpg.org","twitter.com","ico","facebook.com","instagram.com","category","kategori"]
    links = open("sites.db","r").read().splitlines()
    sites = open("links.db","r").read().splitlines()
    news = []
    for link in links:
        try:
            scraper = cloudscraper.create_scraper()
            req = scraper.get(link, headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"
            })
        except ConnectionError:
            continue
        lnks = re.findall('href="(.*?)"', req.text)
        lnks = list(set(lnks))
        for lnk in lnks:
            er = 0
            for i in ic:
                if (i in lnk):
                    er = 1
                    break
            if (er == 0):
                
                if ("http://" not in lnk and "https://" not in lnk):
                        lnk = link + lnk  
                if (len(lnk.split('/')) > 4):
                    news.append(lnk)
    xxx = []
    for n in news:
        xy = 0
        for  site in sites:
            if (site == n):
                xy = 1
                break
        if (xy != 1):
            open("links.db","a+").write(n+"\n")
            xxx.append(n)
    return xxx

@app.route("/delete") 
def delete():
    site = request.args.get('id')
    siteler = open("sites.db","r").read().splitlines()
    pw = open("sites.db","w")
    for i in siteler:
        if (site == i):
            continue
        pw.write(i+"\n")
    return redirect(url_for('add'))

@app.route("/add", methods =['POST','GET']) 
def add():
    if request.method == 'POST':
        site = request.form.get('site')
        open("sites.db","a").write(site+"\n")
    siteler = open("sites.db","r").read().splitlines()
    return render_template('add.html', siteler=siteler)

@app.route("/scrape") 
def scrape():
    news = link_topla() 
    toplam = len(news)
    return render_template('scrape.html', news=news, toplam=toplam)

@app.route("/") 
def anasayfa():
    return render_template('index.html')

def banner():
    if (os.name=="nt"):
        os.system("cls")
    else:
        os.system("clear")
    
    banner = f"""{Fore.CYAN}
                                  v1.0{Fore.GREEN}
 __    __    ___  ____        _____   __  ____    ____  ____    ___  ____  
|  T__T  T  /  _]|    \      / ___/  /  ]|    \  /    T|    \  /  _]|    \ 
|  |  |  | /  [_ |  o  )    (   \_  /  / |  D  )Y  o  ||  o  )/  [_ |  D  )
|  |  |  |Y    _]|     T     \__  T/  /  |    / |     ||   _/Y    _]|    / 
l  `  '  !|   [_ |  O  |     /  \ /   \_ |    \ |  _  ||  |  |   [_ |    \ 
 \      / |     T|     |     \    \     ||  .  Y|  |  ||  |  |     T|  .  Y
  \_/\_/  l_____jl_____j      \___j\____jl__j\_jl__j__jl__j  l_____jl__j\_j
                                                                           {Fore.MAGENTA}

              Umut Şahin tarafından yazıldı ve geliştiriliyor{Fore.YELLOW}
                                                            
    """
    print(banner)


if (__name__=="__main__"):
    try:
        banner()
        app.run(debug = True, port = "4444")
    except KeyboardInterrupt:
        exit()



