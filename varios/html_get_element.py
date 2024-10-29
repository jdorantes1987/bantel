from urllib.request import urlopen
from lxml import etree
print('Hola')
url = "https://www.bcv.org.ve/"
response = urlopen(url)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)

tree.xpath('//*[@id="dolar"]/div/div/div[2]/strong')
print(tree())
