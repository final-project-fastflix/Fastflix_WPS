from django.http import JsonResponse
from django.views import View

from accounts.models import ProfileImage
from movies.models import *


class LikeOrDislike(View):
    def post(self, request, *args, **kwargs):
        sub_user = kwargs['sub_user_id']
        movie = Movie.objects.get(pk=kwargs['movie_id'])
        if sub_user in movie.likes.all():
            movie.likes.remove(sub_user)
            return JsonResponse({'data': 'remove'})
        else:
            movie.likes.add(sub_user)
            return JsonResponse({'data': 'add'})


import time
import re

from bs4 import BeautifulSoup
from selenium import webdriver

def save_profile(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
                    AppleWebKit 537.36 (KHTML, like Gecko) Chrome")

    driver = webdriver.Chrome('/home/park/Downloads/chromedriver', options=options)

    driver.implicitly_wait(3)

    # 브라우저 오픈
    driver.get('http://www.netflix.com/browse')

    driver.find_element_by_name('userLoginId').send_keys('roqkfwkehlwk@naver.com')
    time.sleep(3)
    driver.find_element_by_name('password').send_keys('admin67890!@')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@class="btn login-button btn-submit btn-small"]').click()
    time.sleep(3)

    time.sleep(15)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    selected_html = soup.select('div.lolopi-row-icon')

    p = re.compile('http.*"')

    section_name = ['대표 아이콘']

    for div in selected_html:
        name = div.attrs['aria-label']
        section_name.append(name)
        logo_url = big_image = p.findall(div.attrs['style'])[0][:-1]
        print(logo_url)
        ProfileImage.objects.create(name=name, image_path=logo_url, category='logo')

    print(section_name)

    selected_html = soup.select('div.row-with-x-columns')
    num = 0
    for div in selected_html:
        every_button = div.find_all('button')
        for image in every_button:
            category = section_name[num]
            print(category)
            image_name = ''
            try:
                image_name = image.attrs['aria-label']
                print(image_name)
            except:
                pass

            image_url = big_image = p.findall(image.attrs['style'])[0][:-1]
            print(image_url)
            ProfileImage.objects.create(name=image_name, category=category, image_path=image_url)
        num += 1
