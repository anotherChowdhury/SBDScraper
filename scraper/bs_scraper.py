import math
import shutil
import time
from threading import Thread

import bs4
import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options



def format_placeholders(title, cdn, taka, link, advnc_req, discount, week):
    body = f"\n-->> BLACK FRIDAY DEAL [24HRS] <<--" \
           f"\n----------------------------------" \
           f"\n{title}{ ' - ' + str(discount) + ' OFF' if discount !=[] else ''}" \
           f"\nSale Price - ${str(cdn)} (with Tax)" \
           f"\nIN BDT - TK {taka} " \
           f"\n+\nWeight Charge (To be Added After Product Arrival to BD)" \
           f"\n Rate - 160TK/100g" \
           f"\n----------------------------------" \
           f"\nProduct Link: {str(link)} " \
           f"\n----------------------------------" \
           f"\nAdvance Required - TK {advnc_req}" \
           f"\nQuantity Available - Limited" \
           f"\n Deal Starts - Today " \
           f"\n Deal Ends - 24hrs from Post (While Stock Lasts)" \
           f"\nExpected Shipment Arrival: \n{str(week)}" \
           f"\n----------------------------------" \
           f"\n How to Order (For Black Friday Only):" \
           f"\n\nHow to Order:" \
           f"\nStep 1:" \
           f"\n- Sign In/Sign Up to our Ordering Portal here: http://app.shoptobd.com/" \
           f"\n- Place the order. (Tutorial Video, if needed: http://bit.ly/shoptobdorder)" \
           f"\n- Shoptobd will verify the order & generate the Initial Invoice. Log back later to check it & contact us to confirm." \
           f"\nStep 2:  " \
           f"\nOnce order is confirmed, it will placed right away (provided the deal is still active)." \
           f"\nStep 3: " \
           f"\nYou will have 48-hrs to proceed with the advance for your order. Payment Methods are mentioned in your account dashboard.\n"
    return body


def scrap_data(url: str, i, rate: int = 75, week: str = "Mid December"):


    if url.startswith('https://www.amazon.ca'):
        res = requests.get(url.strip(), headers={
            'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/37.0.2062.120 Safari/537.36'})
        textFile = res.text


        amazon = bs4.BeautifulSoup(textFile, 'html.parser')
        title = amazon.find_all('span', attrs={'id': 'productTitle'})[0].getText().strip()
        price = amazon.find_all('span', attrs={'id':['priceblock_ourprice','priceblock_dealprice']})[0].getText().strip()
        discount = amazon.find_all('tr', attrs={'id': ['regularprice_savings',"dealprice_savings"]})
        image_link = amazon.find_all('img',
                                     attrs={'class': ['a-   dynamic-image', ' a-stretch-vertical'],
                                            'id': 'landingImage'})[0].attrs['data-old-hires'].strip()
        if image_link=='':
            image_link = amazon.find_all('img',
                                         attrs={'class': ['a-dynamic-image', ' a-stretch-vertical'],
                                                'id': 'landingImage'})[0].attrs['src'].strip()


        filename = str(i)+'.' + title + '.jpg'
        filename = filename.replace("'",'')
        filename = filename.replace("/", '')
        # image_req = requests.get(image_link)

        urllib.request.urlretrieve(image_link, filename)

        price = price.replace('CDN$', '').strip()
        cdn = math.ceil((float(price) + ((float(price) * 15) / 100)))
        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)

        taka = "{:,}".format(taka)
        cdn = "{:,}".format(cdn)

        if len(discount) != 0:
            discount = discount[0].getText().strip()
            discount = discount[-4:-1]

        output = "Title: " + title + "\nPrice: " + str(price) + (
            "\nDiscount: " + discount if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + ("*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()

    elif url.startswith('https://www.aldoshoes.com'):

        res = requests.get(url.strip(), headers={
            'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/37.0.2062.120 Safari/537.36'})
        textFile = res.text

        aldo = bs4.BeautifulSoup(textFile, 'html.parser')
        halftitle2 = aldo.find('h1', attrs={'class': ["c-heading c-buy-module__product-title","c-heading c-mx3-buy-module-header__heading"]}).text

        # help = halftitle.findall('span').text

        halftitle1 = aldo.find_all('a', attrs={'class': 'c-breadcrumb__link c-breadcrumb--product-detail__link'})

        color = aldo.find('span', attrs={'class': 'c-product-option__label-current-selection'}).text
        original_price = float(aldo.find('span', attrs={'class': 'c-product-price__formatted-price'})
                               .text.replace('$', '').strip())
        discounted__price = aldo.find('span', attrs={
            'class': 'c-product-price__formatted-price c-product-price__formatted-price--is-reduced'})



        if discounted__price is not None:
            discounted__price = discounted__price.text.replace('$','')
            cdn = float(discounted__price)
            discount = math.floor(((original_price - cdn) / original_price)*100)
            discount = str(discount) + '%'
        else:
            discount = []
            cdn = original_price

        cdn = math.ceil((float(cdn) + ((float(cdn) * 15) / 100)))

        #
        # if discount != []:
        #     cdn = math.ceil((float(cdn) + ((float(cdn) * 15) / 100)))
        # else:
        #     discount = "20%"
        #     cdn = (float(cdn) - ((float(cdn) * 20) / 100))
        #     cdn = math.ceil((float(cdn)+ (float(cdn) * 15) / 100))

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)

        taka = "{:,}".format(taka)
        cdn = "{:,}".format(cdn)

        name = ""

        for element in halftitle1:
            name = name + ' ' + element.text

        words = name.split()
        halftitle1 = " ".join(sorted(set(words), key=words.index))


        title = (' '.join(['Aldo', halftitle1, halftitle2, '(Color:', color, ')'])).title()

        title = title.replace('Outlet','')


        # [x['srcset'] for x in aldo.findAll('picture', attrs={'class':['c-picture c-picture--has-gray-placeholder', 'c-picture--is-loaded']})[-1]
        #  if srcset:
        #         image_link = srcset
        #     else:
        #         image_link = "ERROR"

        image_link = aldo.find_all('picture', attrs={
            'class': ['c-picture c-picture--has-gray-placeholder','c-picture--is-loaded']})[-1].find('img').attrs['srcset']
        # image_link = image_link[len(image_link)-1]

        # image_link = image_link.find('img')
        # image_link = image_link.attrs['srcset'

        #image_link = ''.join(image_link)

        image_link = image_link.split(', ')
        image_link = image_link[-1].split(" ")
        image_link = image_link[0].strip()

        image_link = 'http:' + image_link

        filename = str(i)+'. '+ halftitle2 + '.jpg'



        urllib.request.urlretrieve(image_link, filename)

        output = "Title: " + title + "\nPrice: " + str(cdn) + (
            "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + ("*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()


    elif url.startswith('https://www.fossil.com/ca/'):

        res = requests.get(url.strip(), headers={
            'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/37.0.2062.120 Safari/537.36'})
        textFile = res.text

        fossil = bs4.BeautifulSoup(textFile, 'html.parser')
        title = fossil.find_all('h1', attrs={'class': ["text-display-4 product-title hidden-xs"]})[0].getText().strip()
        model = fossil.find('div',attrs={'class':"product-stylenumber"}).getText().strip()
        title = 'Fossil '+title + '(' + model + ')'

        price = fossil.find('div', attrs={
            'class': ["product-price-display"]}).text.strip()
        price = price.replace("CAD", '')
        price = price.replace("\n", '')
        price = price.replace("\t", '')
        price = price.split(" ")[1]

        price = float(price)

        discount = fossil.find_all('span', attrs={'class': 'text-danger'})
        image_link = fossil.find_all('a', attrs={'class': ['magnifik']})[0].attrs['href'].strip()



        if (discount != []):

            discount = fossil.find_all('span', attrs={'class': 'text-danger'})[0].getText().strip()
            discount = discount.replace("CAD ", "")
            discounted_price = float(discount)
            # if 'Hybrid' not in title:
            #     cdn = math.ceil(((float(discounted_price)+ 0.25 )+ (((float(discounted_price)+ 0.25) * 15) / 100)))
            #     discount = math.floor(((float(price) - float(discount)) / float(price)) * 100)
            #     discount = str(discount) + '%'
            # else:
            discounted_price_extra = float(discounted_price) - ((float(discounted_price) * 30) / 100)
            discount = math.floor(((price - discounted_price_extra) / price) * 100)
            discount = str(discount) + '%'

            cdn = math.ceil(((discounted_price_extra + 0.25) + ((discounted_price_extra + 0.25) * 15) / 100))

        else:
            discount = '30%'
            discounted_price_extra = float(price) - ((float(price) * 30) / 100)
            cdn = math.ceil(
                ((float(discounted_price_extra) + 0.25) + ((float(discounted_price_extra) + 0.25) * 15) / 100))

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)

        taka = "{:,}".format(taka)
        cdn = "{:,}".format(cdn)

        filename = str(i)+ '.'+ title + '.jpg'
        urllib.request.urlretrieve(image_link, filename)

        output = "Title: " + title + "\nPrice: " + str(cdn) + (
            "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + (
                         "*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()

    elif url.startswith('https://www.zara.com/ca'):

        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(executable_path='webDrivers/geckodriver', options=options)
        browser.get(url)

        res = browser.page_source

        browser.quit()

        zara = bs4.BeautifulSoup(res, 'html.parser')

        image_link = zara.find_all('a', attrs={'_seoImg main-image'})



        title = zara.find('h1', attrs={'class': 'product-name'}).text.strip().replace('Details', '').strip()

        try:
            Thread(target=download_image, args=(image_link,title,i)).start()
        except Exception:
            print (Exception)


        color = zara.find('span', attrs={'class': '_colorName'}).text.strip()

        title = "ZARA " + title + '(Color:' + color + ')'

        price = zara.find('div', attrs={'class': "price _product-price"}).text
        price = price.replace('CAD', '')
        price = price.split()

        original_price = float(price[0])

        if len(price) == 1:
            discounted__price = None
        else:
            discounted__price = float(price[1])

        if discounted__price is not None:
            cdn = float(discounted__price)
            discount = math.floor(((original_price - cdn) / original_price) * 100)
            discount = str(discount) + '%'
        else:
            discount = []
            cdn = float(original_price)

        if cdn < 50:
            cdn = math.ceil((float(cdn) + 5) + (((float(cdn) + 5) * 15) / 100))


        else:
            cdn = math.ceil((float(cdn) + ((float(cdn) * 15) / 100)))







        # count = len(image_link)


        # for links in range(len(image_link)):
        #     link = image_link[links].find('img').attrs['src']
        #     link = 'https:' + link
        #     filename = str(i)+ '.' + str(count) + title + '.jpg'
        #
        #     response = requests.get(link,stream=True)
        #     with open(filename, 'wb') as out_file:
        #         shutil.copyfileobj(response.raw, out_file)

            # count = count - 1

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)

        taka = "{:,}".format(taka)
        cdn = "{:,}".format(cdn)




        output = "Title: " + title + "\nPrice: " + str(cdn) + (
        "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + (
                     "*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()

    elif url.startswith('https://www.michaelkors.ca/'):

        options = Options()
        options.add_argument("--headless")

        browser = webdriver.Firefox(executable_path='webDrivers/geckodriver', options=options)
        browser.get(url)

        res = browser.page_source

        browser.quit()

        mk = bs4.BeautifulSoup(res, 'html.parser')

        name = mk.find_all('li', attrs={'class': 'product-name'})
        print(name)

        image_link = mk.find_all('figure', attrs={'class':'gallery-images-item'})

        try:
            Thread(target=download_image, args=(image_link,name,i)).start()
        except Exception:
            print (Exception)

        title = mk.find_all('div', attrs={'class': 'commerce-area-wrapper large-8 pdp-main-commerce'})
        print(title)
        color = mk.find('span', attrs={'class': 'selected-color'}).text

        title = title.replace('KORS','KORS ').replace('Kors','Kors ') + '(Color:' + color + ')'

        original_price = float(mk.find('div', attrs={'class': ['listPrice','Price']}).text.split('$')[1])
        discounted__price = mk.find('div', attrs={'class': 'salePrice'})





        # count = len(image_link)
        #
        # for links in range(len(image_link)):
        #     link = image_link[links].find('img').attrs['src']
        #     link = 'https:' + link
        #     filename = str(i)+ '.' + str(count) + name + '.jpg'
        #
        #     response = requests.get(link,stream=True)
        #     with open(filename, 'wb') as out_file:
        #         shutil.copyfileobj(response.raw, out_file)
        #
        #     count = count - 1

        if discounted__price is not None:
            discounted__price = discounted__price.text.split('$')[1]
            cdn = float(discounted__price)
            discount = math.floor(((original_price - cdn) / original_price) * 100)
            discount = str(discount) + '%'
        else:
            discount = []
            cdn = original_price

        if cdn < 99:
            cdn = math.ceil((float(cdn) + 5) + (((float(cdn) + 5) * 15) / 100))

        else:
            cdn = math.ceil((float(cdn) + ((float(cdn) * 15) / 100)))

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)
        taka = "{:,}".format(cdn * rate)






        output = "Title: " + title + "\nPrice: " + str(cdn) + (
        "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + (
                     "*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()
    elif url.startswith('https://www2.hm.com/en_ca/'):

        options = Options()
        options.add_argument("--headless")

        browser = webdriver.Firefox(executable_path='webDrivers/geckodriver', options=options)
        browser.get(url)

        res = browser.page_source

        browser.quit()

        hm = bs4.BeautifulSoup(res, 'html.parser')

        title = hm.find_all('section', attrs={'class': 'name-price'})[0].find('h1').text.strip()

        image_link = [hm.find('div',attrs={'class': 'product-detail-main-image-container'}).find('img').attrs['src']]
        image_link.append(hm.find('figure',attrs={'class': 'pdp-secondary-image pdp-image'}).find('img').attrs['src'])

        try:
            Thread(target=download_image, args=(image_link,title,i)).start()
        except Exception:
            print (Exception)


        color = hm.find('h3', attrs={'class': 'product-input-label'}).text.strip()

        title = 'H&M ' + title + '(Color:' + color + ')'

        price = hm.find('div', attrs={'class': 'price parbase'}).text.strip().split('$')

        discounted_price = ''

        if len(price) == 3:
            discounted_price = float(price[1])
            original_price = float(price[2])

        else:
            original_price = price[1]





        # count = len(image_link)
        #
        #
        # for links in range(len(image_link)):
        #     link = 'https:' + image_link[links]
        #     filename = str(i)+ '.' + str(count) + title + '.jpg'
        #     urllib.request.urlretrieve(link, filename)
        #     count = count - 1



        if discounted_price:
            cdn = discounted_price
            discount = math.floor(((original_price - cdn) / original_price) * 100)
            discount = str(discount) + '%'
        else:
            discount = []
            cdn = original_price

        # if cdn < 50:

        cdn = math.ceil((cdn+8)+(((cdn+8)*15)/100))

        # else:
        #     cdn = math.ceil((float(cdn) + ((float(cdn) * 15) / 100)))

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)
        taka = "{:,}".format(cdn * rate)

        output = "Title: " + title + "\nPrice: " + str(cdn) + (
        "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + (
                     "*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()

        try:
            Thread(target=download_image, args=(image_link,title,i)).start()
        except Exception:
            print (Exception)




    elif url.startswith('https://www.adidas.ca/'):

        options = Options()
        options.add_argument("--headless")

        browser = webdriver.Firefox(executable_path='webDrivers/geckodriver', options=options)
        browser.get(url)
        time.sleep(1)
        res = browser.page_source
        browser.quit()

        adidas = bs4.BeautifulSoup(res, 'html.parser')

        product_information = adidas.find_all('div', attrs={'class': 'product_information___1Tt1L gl-vspacing-m'})[0]

        title_category = product_information.find('div', attrs={'data-auto-id': 'product-category'}).text.strip()
        title_product = product_information.find('h1', attrs={'data-auto-id': 'product-title'}).text.strip()
        price = product_information.find('div', attrs={'class': 'gl-price'}).text.strip().replace('C$', '', 2).split()


        discounted_price = None

        if len(price) == 2:
            original_price = float(price[1])
            discounted_price = float(price[0])
        else:
            original_price = float(price[0])

        title = 'Adidas ' + title_category + ' ' + title_product

        image_link = adidas.find_all('div', attrs={'class': 'container hero_container___nM-YT'})[0].find('img').attrs['src']

        if discounted_price:
            cdn = discounted_price
            discount = math.floor(((original_price - cdn) / original_price) * 100)
            discount = str(discount) + '%'
        else:
            discount = []
            cdn = original_price


        cdn = math.ceil(cdn + ((cdn*15)/100))


        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)
        taka = "{:,}".format(cdn*rate)


        filename = str(i)+ '.' + title_product+'.jpg'

        response = requests.get(image_link, stream=True)
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        output = "Title: " + title + "\nPrice: " + str(cdn) + (
        "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + (
                     "*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()
    elif url.startswith('https://www.guess.ca/'):

        options = Options()
        options.add_argument("--headless")

        browser = webdriver.Firefox(executable_path='webDrivers/geckodriver', options=options)
        browser.get(url)

        res = browser.page_source

        browser.quit()

        guess = bs4.BeautifulSoup(res, 'html.parser')

        title = guess.find_all('div', attrs={'class': 'rightdetails col-lg-3 col-sm-6'})[0].find('h1').text.strip()
        title = 'Guess ' + title

        image_link = guess.find_all('div', attrs={'class': 's7staticimage'})

        try:
            Thread(target=download_image, args=(image_link, title, i)).start()
        except Exception:
            print(Exception)



        original_price = float(guess.find('span', attrs={'class': 'original'}).text.strip().replace('CAD', ''))
        discounted_price = float(guess.find('span', attrs={'class': 'priceVal actual'}).text.strip().replace('CAD', ''))
        if discounted_price == original_price:
            discounted_price = None






        # count = len(image_link)

        # for links in range(len(image_link)):
        #
        #     link = image_link[links].find('img').attrs['src']
        #     filename = str(i)+ '.' + str(count) + title + '.jpg'
        #
        #     response = requests.get(link,stream=True)
        #     with open(filename, 'wb') as out_file:
        #         shutil.copyfileobj(response.raw, out_file)
        #
        #     count = count - 1


        if discounted_price:
            cdn = discounted_price
            discount = math.floor(((original_price - cdn) / original_price) * 100)
            discount = str(discount) + '%'
        else:
            discount = []
            cdn = original_price

        if cdn < 125:
            cdn = math.ceil((cdn+13) + (((cdn+13)*15)/100))

        else:
           cdn = math.ceil((cdn+((cdn*15)/100)))

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)
        taka = "{:,}".format(cdn*rate)





        output = "Title: " + title + "\nPrice: " + str(cdn) + (
        "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + (
                     "*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()
    elif url.startswith('https://www.forever21.com/ca/'):


        options = Options()
        options.add_argument("--headless")

        browser = webdriver.Firefox(executable_path='webDrivers/geckodriver', options=options)
        browser.get(url)

        res = browser.page_source

        browser.quit()

        f21 = bs4.BeautifulSoup(res, 'html.parser')

        name = f21.find('div', attrs={'class': 'container row pr_10 pl_10'}).find('h1').text.strip()
        image_links = [f21.find('div', attrs={'class': 'owl-stage'})]

        try:
            Thread(target=download_image, args=(image_links,name ,i)).start()
        except Exception:
            print(Exception)

        title = 'Forever21 ' + name

        original_price = float(f21.find('span', attrs={'class': ['pr_20', 'p_old_price pr_5']}).text.replace("CAD $",
                                                                                                              '').strip())

        discounted_price = f21.find('span', attrs={'class': 'p_sale t_bold t_pink pt_10'})


        if discounted_price is not None:
            discounted_price = discounted_price.text.replace("CAD $", '').strip()
            cdn = float(discounted_price)
            discount = math.floor(((original_price - cdn) / original_price) * 100)
            discount = str(discount) + '%'
        else:
            cdn = original_price


        if cdn < 50:
            cdn = math.ceil((cdn+11.95) + (((cdn+11.95)*15)/100))

        else:
           cdn = math.ceil((cdn+((cdn*15)/100)))

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)
        taka = "{:,}".format(cdn*rate)





        output = "Title: " + title + "\nPrice: " + str(cdn) + (
        "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + (
                     "*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()
    elif url.startswith('https://www.globoshoes.com/ca/en/'):

        options = Options()
        options.add_argument("--headless")

        browser = webdriver.Firefox(executable_path='webDrivers/geckodriver', options=options)
        browser.get(url)

        brand = browser.find_element_by_css_selector("h1.c-buy-module__brand").text
        product_name = browser.find_element_by_css_selector('h2.c-buy-module__product-title').text
        color = browser.find_element_by_css_selector(".c-product-option__label-current-selection").text
        price = browser.find_elements_by_css_selector('.c-product-price__formatted-price')
        original_price = float(price[0].text.replace('$','').strip())
        if len(price)>1:
            discounted__price = float(price[1].text.replace('$','').strip())
        else:
            discounted__price = ""

        chobi = browser.find_element_by_css_selector('.c-picture img').get_attribute('srcset' or 'data-srcset').split("//")[-1].split()[0]

        title = f"{brand} {product_name}({color})"

        if discounted__price:
            cdn = discounted__price
            discount = math.floor(((original_price - cdn) / original_price) * 100)
            discount = str(discount) + '%'
        else:
            cdn = original_price


        if cdn < 60:
            cdn = math.ceil((cdn+6) + (((cdn+6)*15)/100))

        else:
           cdn = math.ceil((cdn+((cdn*15)/100)))

        taka = cdn * rate
        advnc_req = "{:,}".format(math.ceil((taka / 2.5) / 100) * 100)
        taka = "{:,}".format(cdn*rate)

        image_link = 'http://' + chobi

        filename = str(i)+'. '+ product_name + '.jpg'
        urllib.request.urlretrieve(image_link, filename)

        output = "Title: " + title + "\nPrice: " + str(cdn) + (
        "\nDiscount: " + str(discount) if discount != [] else "") + "\nShipping Time: " + str(week) + "\n" + (
                     "*" * 30)
        print(output)
        outfile = open("out.txt", "a+")
        outfile.write(format_placeholders(title, cdn, taka, url, advnc_req, discount, week))
        outfile.close()

        browser.quit()







def download_image(image_link,name:str,i:int):



    count = len(image_link)


    for links in range(len(image_link)):
        link = image_link[links].find('img').attrs['src']
        if 'Guess' and 'forever21' not in name:
            link = 'https:' + link
        print(link)
        filename = str(i) + '.' + str(count) + name + '.jpg'

        response = requests.get(link, stream=True)
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        count = count - 1




