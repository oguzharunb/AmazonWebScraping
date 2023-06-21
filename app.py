import requests
import string
from dict2xml import dict2xml

url = 'https://www.amazon.com.tr/%C4%B0nsanl%C4%B1%C4%9F%C4%B1m%C4%B1-Yitirirken-Kapak-de%C4%9Fi%C5%9Febilir-Osamu/dp/6258401473/ref=pd_bxgy_img_sccl_1/262-1162542-1516046?content-id=amzn1.sym.0a9a6dd3-e8c5-460e-bc2b-2edd85853c33&pd_rd_i=6258401473&psc=1'
response = requests.get(url)
content = response.content # content of the page
content = str(content)

dic = {
    'title': ['<span id="productTitle" class="a-size-extra-large">', '</span>'],
    'auth': ['<span class="author notFaded" data-width="">','</a>'],
    'price': ['<span id="price" class="a-size-medium a-color-price header-price a-text-normal">','</span>'],
    'infos': ['<div id="detailBullets_feature_div">','</div>'],
    'desc': ['<p class="a-spacing-base">','</p>'],
    'images': ['<div id="imageBlockOuter" class="a-row">',"""</div>

    </div>"""]
}


newdic = {}
for x in dic:
    start_index = content.find(dic[x][0])
    end_index = content.find(dic[x][1], start_index)
    data = content[start_index:end_index][len(dic[x][0]):]
    newdic[x] = data

imagestartindex = newdic['images'].find('src="')
imageendindex = newdic['images'].find('"', imagestartindex+5)
newdic['images'] = newdic['images'][imagestartindex + 5:imageendindex]

infos = []
for x in newdic['infos'].split('</span> <span>')[1:]:
    infos.append(x.split('</span> </span></li>')[0])

newdic['Publisher'] = infos[0]
newdic['Language'] = infos[1]
newdic['Pages'] = infos[2]
newdic['isbn10'] = infos[3]
newdic['isbn13'] = infos[4]
newdic['sizes'] = infos[5]
newdic['auth'] = newdic['auth'].split('>')[1].split('<')[0]
newdic.pop('infos')

print(dict2xml(newdic))