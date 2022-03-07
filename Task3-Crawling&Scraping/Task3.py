from bs4 import BeautifulSoup as bs
import requests
import json

with open(r'C:\Users\User\Desktop\python\Task3-Crawling&Scraping\materials.json' , 'r') as f:
    materials_data = json.load(f)


headers = {
      'authority': 'standalone.kupferschluessel.de',
      'cache-control': 'max-age=0',
      'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
      'sec-ch-ua-mobile': '?0',
      'upgrade-insecure-requests': '1',
      'origin': 'https://standalone.kupferschluessel.de',
      'content-type': 'application/x-www-form-urlencoded',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-dest': 'frame',
      'referer': 'https://standalone.kupferschluessel.de/vergleichswerkstoffe.php',
      'accept-language': 'en-US,en;q=0.9',
      'cookie': 'PHPSESSID=9bvr99ivvr1hfpcqn2hq4gni02',
  }

#paths for requests
result_path = 'https://standalone.kupferschluessel.de/ergebnisse.php'
comparison_path= 'https://standalone.kupferschluessel.de/vergleichswerkstoffe.php'
content_path = 'https://standalone.kupferschluessel.de/content.php'


outer_dict = {}
material_dict = {}
material_value_dict = {}

for material in materials_data[:3]:
    data_result = {
        'werkstoff': material,
        'lang': 'english',
      }

    result_request = requests.post(result_path , headers=headers ,data=data_result )

    result_content = bs(result_request.content, 'lxml')

    material_value = result_content.find('option')['value']


    data_comparison = {
        'werkstoff2': str(material_value),
        'lang': 'english'
      }

    data_content = {
        'werkstoff': str(material_value),
        'lang': 'english'
     }

    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #comparison list part


    comparison_request = requests.post(comparison_path, headers=headers, data=data_comparison)
    comparison_content = bs(comparison_request.content, 'lxml')

    select_values = comparison_content.find_all('option')

    comparison_list = []
    for select in select_values:
        comparison_list.append(select['value'])

    material_value_dict.update({'Comparsion Materials': comparison_list })

    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


    content_request = requests.post(content_path , headers=headers , data= data_content)
    content_page = bs(content_request.content , 'lxml')

    data_dict = {}

    table_rows = content_page.find('div' , {'id':'normenlayer'}).table.contents

    sub_dict_name = "Material"
    temp_dict = {}


    for row in table_rows:
        #|||||||||||||||||||||
        #checking for blank lines over table rows and tds
        if row =='\n':
            continue

        tdsCrashed = row.contents
        realTds = []
        for td in tdsCrashed:
            if td != '\n':
                realTds.append(td)

        #||||||||||||||||||||||

        if len(realTds) != 1:
            temp_dict.update({realTds[0].text: realTds[1].text})
        else:
            data_dict.update({sub_dict_name : temp_dict})

            sub_dict_name = realTds[0].text
            temp_dict = {}


    #||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #ASEMBLIMI
    material_value_dict.update({'Data': data_dict})
    print(material_value_dict)
    print(material_value)
    print(material)
    material_dict.update({material_value : material_value_dict})
    #PRINTO >>===> print(material_dict)
    outer_dict.update({material : material_dict})


with open("jason.json" , "w") as js:
    json.dump(eval(str(outer_dict)), js, indent=2)

"""
outer_dict{

    material_dict => 127{

        material_value_dict => 01279{

            comparison_material{

            }
            data_dict{

            }
        }
    }
}
"""
