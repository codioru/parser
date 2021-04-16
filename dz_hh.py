import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
 
# https://izhevsk.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=true
#url = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python'
 
main_link = 'https://hh.ru'
 
# job = input('Введите желаему должность: ')
#job = 'Data scientist'
job = 'Аналитик продуктовый'
 
r_params = {'L_save_area': 'true',
          'clusters': 'true',
          'enable_snippets': 'true',
          'text': job,
          'showClusters': 'true'}
 
r_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}
 
response = requests.get(main_link + '/search/vacancy', params=r_params, headers=r_headers)
# pprint(type(response.text))
soup = bs(response.text, 'html.parser')
 
# print(type(vacansy_list))
 
all_vacansies = []
cnt = 1
while True:
    vacansy_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
    for vacansy in vacansy_list:
        vacansy_data = {}
        link = vacansy.find('a')
        vacansy_url = link['href']
        vacansy_name = link.getText()
        vacansy_salary = vacansy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
 
        vacansy_min = None
        vacansy_max = None
        vacansy_cur = None
        if vacansy_salary is not None:
            vacansy_salary = vacansy_salary.getText().replace('\u202f','')
            vacansy_cur = vacansy_salary.split()[-1]
            if vacansy_salary.find('–') > -1:
                vacansy_min = int(vacansy_salary.split()[0])
                vacansy_max = int(vacansy_salary.split()[2])
            elif vacansy_salary.find('от'):
                vacansy_min = int(vacansy_salary.split()[1])
            elif vacansy_salary.find('до'):
                vacansy_max = int(vacansy_salary.split()[1])
 
        vacansy_data['url'] = vacansy_url
        vacansy_data['name'] = vacansy_name
        vacansy_data['salary_min'] = vacansy_min
        vacansy_data['salary_max'] = vacansy_max
        vacansy_data['salary_cur'] = vacansy_cur
        all_vacansies.append(vacansy_data)

    next_button = soup.find('a', {'data-qa': 'pager-next'})
    if next_button is None:
        break
    else:
        next_link = main_link + next_button['href']
        response = requests.get(next_link, headers=r_headers)
        soup = bs(response.text, 'html.parser')
        print("Страница ", cnt, " - обработана")
        #print(f'Обработано {cnt} страниц')
        cnt += 1
pprint(all_vacansies)
print(len(all_vacansies))

