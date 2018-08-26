########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  dated- 26 June 2016                 #
#                 Update - 29 June 2016                #
########################################################

import os
import getpass
import bs4
import re
import requests
import tqdm
import time
import urllib 

os.makedirs('Wallhaven', exist_ok=True)

def login():
    print('NSFW images require login')
    username = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    req = requests.post('https://alpha.wallhaven.cc/auth/login', data={'username':username, 'password':password})
    return req.cookies

def category():
    print('''****************************************************************
                            Category Codes

    [1]---> all     - For 'Every' wallpaper.
    [2]---> general - For 'General' wallpapers only.
    [3]---> anime   - For 'Anime' Wallpapers only.
    [4]---> people  - For 'People' wallapapers only.
    [5]---> ga      - For 'General' and 'Anime' wallapapers only.
    [6]---> gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ')
    ALL = '111'
    ANIME = '010'
    GENERAL = '100'
    PEOPLE = '001'
    GENERAL_ANIME = '110'
    GENERAL_PEOPLE = '101'
    if ccode.lower() == "1":
        ctag = ALL
    elif ccode.lower() == "3":
        ctag = ANIME
    elif ccode.lower() == "2":
        ctag = GENERAL
    elif ccode.lower() == "4":
        ctag = PEOPLE
    elif ccode.lower() == "5":
        ctag = GENERAL_ANIME
    elif ccode.lower() == "6":
        ctag = GENERAL_PEOPLE

    print('''
    ****************************************************************
                            Purity Codes

    [1]---> sfw     - For 'Safe For Work'
    [2]---> sketchy - For 'Sketchy'
    [3]---> nsfw    - For 'Not Safe For Work'
    [4]---> ws      - For 'SFW' and 'Sketchy'
    [5]---> wn      - For 'SFW' and 'NSFW'
    [6]---> sn      - For 'Sketchy' and 'NSFW'
    [7]---> all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'1':'100', '2':'010', '3':'001', '4':'110', '5':'101', '6':'011', '7':'111'}
    ptag = ptags[pcode]

    if pcode in ['3', '5', '6', '7']:
        cookies = login()
    else:
        cookies = dict()

    CATURL = 'https://alpha.wallhaven.cc/search?categories=' + \
        ctag + '&purity=' + ptag + '&page='
    return (CATURL, cookies)


def latest():
    print('Downloading latest')
    latesturl = 'https://alpha.wallhaven.cc/latest?page='
    return (latesturl, dict())

def search():
    query = input('Enter search query: ')
    searchurl = 'https://alpha.wallhaven.cc/search?q=' + \
        urllib.parse.quote_plus(query) + '&page='
    return (searchurl, dict())

def main():
    Choice = input('''Choose how you want to download the image:

    [1]---> category - For downloading wallpapers from specified categories
    [2]---> latest   - For downloading latest wallpapers
    [3]---> search   - For downloading wallpapers from search

    Enter choice: ''').lower()
    while Choice not in ['1', '2', '3']:
        if Choice != None:
            print('You entered an incorrect value.')
        choice = input('Enter choice: ')

    if Choice == '1':
        BASEURL, cookies = category()
    elif Choice == '2':
        BASEURL, cookies = latest()
    elif Choice == '3':
        BASEURL, cookies = search()

    pgid = int(input('How Many pages you want to Download?: '))
    print('Number of Wallpapers to Download: ' + str(24 * pgid))
    for j in range(1, pgid + 1):
        totalImage = str(24 * pgid)
        url = BASEURL + str(j)
        urlreq = requests.get(url, cookies=cookies)
        soup = bs4.BeautifulSoup(urlreq.text, 'lxml')
        soupid = soup.findAll('a', {'class': 'preview'})
        res = re.compile(r'\d+')
        imgid = res.findall(str(soupid))
        imgext = ['jpg', 'png', 'bmp']
        for i in range(len(imgid)):
            currentImage = (((j - 1) * 24) + (i + 1))
            url = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.' % imgid[
                i]
            for ext in imgext:
                iurl = url + ext
                osPath = os.path.join('Wallhaven', os.path.basename(iurl))
                if not os.path.exists(osPath):
                    imgreq = requests.get(iurl, cookies=cookies)
                    if imgreq.status_code == 200:
                        print("Downloading : %s - %s / %s" % (os.path.basename(iurl), currentImage , totalImage))
                        with open(osPath, 'ab') as imageFile:
                            for chunk in imgreq.iter_content(1024):
                                imageFile.write(chunk)
                        break
                else:
                    print("%s already exist - %s / %s" % (os.path.basename(iurl), currentImage , totalImage))

if __name__ == '__main__':
    main()
