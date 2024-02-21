import pymongo
import requests
from bs4 import BeautifulSoup
import re
import datetime
import webbrowser

#Veritabanına bağlanmak için
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Web_Scraping"]
mycol =mydb["Laptop"]

#Laptopları ve özellikleri 2 boyutlu items listesine listele
laptoplar = []
n=1 # giriş yapılan laptop sayısı için
#Tarayıcıyı aç
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

#Amazon için
#Arama motoruna laptop yaz
search_query = 'laptop'.replace(' ', '+')
base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)


for i in range(1, 10):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    #bs4 ile webscraping yapmanın ilk aşaması
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #sayfada bütün ürünlerin olduğu kısımları bul
    sonuclar = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for sonuc in sonuclar:
        try:
            urun_numara = n
            urun_ad = sonuc.h2.text
            urun_kaynak = 'https://www.amazon.com' + sonuc.a['href']
            urun_foto = sonuc.find('img', {'class', 's-image'})
            urun_foto = str(urun_foto)
            urun_yildiz_satiri = sonuc.find('i',{'class':'a-icon'}).text
            urun_yildiz = urun_yildiz_satiri.split(" ")[0]
            urun_puan = sonuc.find_all('span', {'aria-label': True})[1].text
            fiyat_1 = sonuc.find('span', {'class': 'a-price-whole'}).text
            fiyat_2 = sonuc.find('span', {'class': 'a-price-fraction'}).text
            urun_fiyat = (fiyat_1 + fiyat_2) + " $"
            urun_fiyat_r = urun_fiyat.split(" ")[0]
            urun_fiyat_r = urun_fiyat_r.replace(",","")
            urun_fiyat_rakam = float(urun_fiyat_r) * 18.61 #dolar kuruyla çarptım
            urun_site="Amazon"
            n = n+1
            laptoplar.append([urun_numara,urun_ad,urun_yildiz,urun_puan, urun_fiyat, urun_kaynak,urun_site,urun_foto])
        except AttributeError:
            continue
#Trednyoldan resim çekemediğim için son resmi koyuyorum
urun_foto = "sonuc.find('img', {'class', 's-image'})"
urun_foto = str(urun_foto) +" TEMSİLİDİR "

#Trendyol için
search_query = 'laptop'.replace(' ', '+')
base_url = 'https://www.trendyol.com/sr?q={0}'.format(search_query)

for i in range(1, 10 ):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    sonuclar = soup.find_all('div', {'class': 'prdct-cntnr-wrppr', 'class': 'p-card-chldrn-cntnr card-border'})

    for sonuc in sonuclar:
        try:
            urun_numara = n
            urun_yildiz = 0.0
            urun_yildiz_satiri = sonuc.find_all('div',{'class':'star-w'})
            for urun_yildiz_satir in urun_yildiz_satiri:
                urun_yildizlar = urun_yildiz_satir.find('div',{'class':'full'}).get('style')
                #string içindeki rakamları bulup birleştirip bunları floata çevir
                urun_yildiz = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", urun_yildizlar)[0])+urun_yildiz
            urun_yildiz = urun_yildiz / 100
            urun_fiyat = sonuc.find('div', {'class': 'prc-box-dscntd'}).text
            urun_fiyat_r = urun_fiyat.split(" ")[0]
            urun_fiyat_r = urun_fiyat_r.replace(",", "")
            urun_ad= sonuc.find('span',{'class':'prdct-desc-cntnr-name'}).text
            urun_puan = sonuc.find('div', {'class': 'ratings-container'}).text
            urun_kaynak="https://www.trendyol.com"
            urun_kaynak=urun_kaynak+sonuc.a['href']
            urun_site="Trendyol"
            n= n+1
            laptoplar.append([urun_numara,urun_ad,urun_yildiz,urun_puan, urun_fiyat, urun_kaynak,urun_site,urun_foto])
        except AttributeError:
            continue
#n11 için
search_query = 'laptop'.replace(' ', '+')
base_url = 'https://www.n11.com/arama?q={0}'.format(search_query)

for i in range(1, 10 ):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    sonuclar = soup.find_all('li', {'class': 'column'})

    for sonuc in sonuclar:
        try:
            urun_numara = n
            urun_yildiz_satiri = sonuc.find('span',['class','rating'])
            urun_yildiz_seviyesi = str(urun_yildiz_satiri.get('class')[1])
            if urun_yildiz_seviyesi == "":
                urun_yildiz_seviyesi= "r0"
            urun_yildiz = float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)",urun_yildiz_seviyesi)[0])
            urun_yildiz = urun_yildiz/20
            urun_ad = sonuc.h3.text
            urun_fiyat = sonuc.ins.text
            urun_fiyat_r = urun_fiyat.split(" ")[0]
            urun_fiyat_r = urun_fiyat_r.replace(",", "")
            urun_puan = sonuc.find('span',{'class':'ratingText'}).text
            urun_kaynak = sonuc.a['href']
            urun_foto_kaynak = sonuc.find('img',{'class':'lazy cardImage'})
            urun_foto_link = str(urun_foto_kaynak).split("src=")[1]
            urun_foto ="<img src=" + urun_foto_link + "/>"
            urun_site = "N11"
            n = n+1
            laptoplar.append([urun_numara,urun_ad,urun_yildiz,urun_puan, urun_fiyat, urun_kaynak,urun_site,urun_foto])
        except AttributeError:
            continue

#hepsiburada için
search_query = 'laptop'.replace(' ', '+')
base_url = 'https://www.hepsiburada.com/ara?q={0}'.format(search_query)

for i in range(1, 10 ):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    sonuclar = soup.find_all('li', {'class':'productListContent-zAP0Y5msy8OHn5z7T_K_'})
    for sonuc in sonuclar:
        try:
            urun_numara = n
            urun_yildiz = 0.0
            urun_yildiz_satiri = sonuc.find_all('li',{'role':'radio'})
            for w in urun_yildiz_satiri:
                t = str(w).split(">")
                z = str(t[1]).split(" ")
                r = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", z[4])
                urun_yildiz = float(r[0]) + urun_yildiz
            urun_yildiz = urun_yildiz/100
            urun_ad = sonuc.h3.text
            urun_fiyat = sonuc.find('div',{'data-test-id':'price-current-price'}).text
            urun_fiyat_r = urun_fiyat.split(" ")[0]
            urun_fiyat_r = urun_fiyat_r.replace(",", "")
            urun_puan = sonuc.find('div',{'data-test-id':'review'}).text
            urun_kaynak = "https://www.hepsiburada.com/"
            urun_kaynak = urun_kaynak + sonuc.a['href']
            urun_foto = sonuc.find('img')
            urun_foto = str(urun_foto)
            urun_site="Hepsiburada"
            n = n+1
            laptoplar.append([urun_numara,urun_ad,urun_yildiz,urun_puan, urun_fiyat, urun_kaynak,urun_site,urun_foto])
        except AttributeError:
            continue

#itemleri veritabanına yazmak için
for laptop in laptoplar:
    mydict = {"_id":laptop[0],'timestamp': datetime.datetime.now() ,"Ürün numara": laptop[0],"Ürün ad":laptop[1],"Ürün yıldız":laptop[2],"Ürünü puanlayan kişi sayısı":laptop[3],"Ürünün fiyatı":laptop[4],"Ürünün linki":laptop[5],"Ürünün satıldığı site":laptop[6],"Ürünün fotoğrafı":laptop[7]}
    try:
        x = mycol.insert_one(mydict)
    except pymongo.errors.DuplicateKeyError:
        pass

#html'e yazmak
tablo_ekle = []
tablo = "<thead>\n<tr>\n<td>Ürün Numara</td>\n<td>Ürün ad</td>\n<td>Ürün yıldız</td>\n<td>Ürünü puanlayan kişi sayısı</td>\n<td>Ürün fiyatı</td>\n<td>Ürünün linki</td>\n<td>Ürünün satıldığı site</td>\n<td>Ürünün fotoğrafı</td>\n</tr>\n</thead>\n"
tablo_ekle.append(tablo)
for y in mycol.find():
    numara_t = "<tr>\n<td>%d</td>\n"%y['Ürün numara']
    tablo_ekle.append(numara_t)
    ad_t = "<td>%s</td>\n"%y['Ürün ad']
    tablo_ekle.append(ad_t)
    yildiz_t = "<td>%s</td>\n"%y['Ürün yıldız']
    tablo_ekle.append(yildiz_t)
    puan_t = "<td>%s</td>\n" %y ['Ürünü puanlayan kişi sayısı']
    tablo_ekle.append(puan_t)
    fiyat_t = "<td>%s</td>\n" %y['Ürünün fiyatı']
    tablo_ekle.append(fiyat_t)
    link_t = "<td><a href=%s>LİNK</a></td>\n" %y['Ürünün linki']
    tablo_ekle.append(link_t)
    site_t = "<td>%s</td>\n" %y['Ürünün satıldığı site']
    tablo_ekle.append(site_t)
    foto_t = "<td>%s</td>\n</tr>" %y['Ürünün fotoğrafı']
    tablo_ekle.append(foto_t)
tablo_metin = ""
for z in tablo_ekle:
    tablo_metin = tablo_metin + z
contents = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8"/>
     <meta content="width-device-width, initial scale=1, shrink-to-fit=no name=viewport"/>
<title>Kara Gün</title>
<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
<script src="../jquery.simplePagination.js"></script>
<link href="../simplePagination.css" rel="stylesheet" type="text/css" />
    <style type="text/css">
table {{
    width: 100%;
    border-collapse: collapse;
    border: 1px solid #ddd;
}}

th, td {{
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}}

th {{
    background-color: #333;
    color: #fff;
}}

tbody tr:nth-child(even) {{
    background-color: #f2f2f2;
}}

tbody tr:hover {{
    background-color: #ddd;
}}

input[type=text] {{
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
}}
</style>
<script>
function searchTable() {{
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {{
        td = tr[i].getElementsByTagName("td")[0]; // Sadece ilk sütunu ara
        if (td) {{
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                tr[i].style.display = "";
            }} else {{
                tr[i].style.display = "none";
            }}
        }}
    }}
}}
</script>
</head>
<body>
<div id="container">
    <div id="search-container">
        <input type="text" id="myInput" onkeyup="searchTable()" name="arama" placeholder="Ara...">
    </div>
    <table border="1" id="myTable">
        <thead>
            <tr>
                <th>Ürün Numarası</th>
                <th>Ürün Adı</th>
                <th>Ürün Yıldız</th>
                <th>Ürünü Puanlayan Kişi Sayısı</th>
                <th>Ürün Fiyatı</th>
                <th>Ürünün Linki</th>
                <th>Ürünün Satıldığı Site</th>
                <th>Ürünün Fotoğrafı</th>
            </tr>
        </thead>
        <tbody>
            {tablo_metin}
        </tbody>
    </table>
</div>
</body>
</html>
'''


net_ad = 'home.html'

def dosya_ac(contents,net_ad):
    net = open(net_ad,"w", encoding="utf-8")
    net.write(contents)
    net.close()
dosya_ac(contents,net_ad)

webbrowser.open_new_tab("file:///C:/Users/etok6/PycharmProjects/pythonProject14/home.html")
