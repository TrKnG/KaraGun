# Web_Scraping

Projenin Özeti:
Projenin hedefi belirli e-ticaret sitelerindeki
laptop ürünlerini web-scraping yöntemiyle kazıyıp, 
veri tabanına kaydedip daha sonra bunları bir web 
sayfası aracılığıyla yansıtmaktır

Projenin Gereklilikleri:
Projeyi çalıştırabilmek için python ve mongodb servisi yüklü olması gerekmektedir.
Import edilen kütüphaneleri yüklemeyi unutmayınız.
Veri tabanını ve koleksiyonu projeyi çalıştırmadan oluşturmak gerekir. Veri tabanını Web_Scraping, koleksiyonu Laptop adıyla oluşturmanız gerekiyor.

#Veritabanına bağlanmak için

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Web_Scraping"]

mycol =mydb["Laptop"]

