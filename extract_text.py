from bs4 import BeautifulSoup

with open('/home/ubuntu/orderofplan_extracted/word/document.xml', 'r') as f:
    data = f.read()

Bs_data = BeautifulSoup(data, 'xml')

text_content = Bs_data.find_all('w:t')

with open('/home/ubuntu/orderofplan.txt', 'w') as f:
    for tag in text_content:
        f.write(tag.get_text())


