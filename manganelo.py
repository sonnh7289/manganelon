import urllib, json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import sqlite3
import re


#############################################
#                                           #
#   Thay đổi const theo đúng yêu cầu        #
#                                           #
#############################################

_LINK_SAVE_DB = "D:\Project App Manga ThinkDriff\Crawl Data\Database\MangaServer.db" # Đường dẫn đến database
_BASE_LINK = "https://ww5.manganelo.tv" # Không thay đổi dòng này
_API_KEY = "fd81b5da86e162ade162a05220c0eb89"#TK: kaidodo10 Không thay đổi dòng này
_IMGBB_UPLOAD_LINK = "https://api.imgbb.com/1/upload" # Không thay đổi dòng này
_WORK_DIR = 'D:\\Project App Manga ThinkDriff\\Crawl Data\\Data Manga Image' # Đường dẫn đến folder chứa ảnh
PAGE = 1 # Số trang muốn crawl

def processing_SoLuongView(SoLuongView):
    if SoLuongView.isnumeric() :
        return SoLuongView
    elif SoLuongView.find('K') != -1:
        SoLuongView = SoLuongView.replace("K", "")
        return int(float(SoLuongView) * 1000)
    elif SoLuongView.find('M') != -1:
        SoLuongView = SoLuongView.replace("M", "")
        return int(float(SoLuongView) * 1000000)
    elif SoLuongView.find('B') != -1:
        SoLuongView = SoLuongView.replace("B", "")
        return int(float(SoLuongView) * 1000000000)
    return 0

def insertChapterIntoTable(id_chapter, id_manga, list_image_chapter_server_goc, list_image_chapter_da_upload, thoi_gian_release):
    try:
        currentDictionary = os.getcwd()
        fileDatabase = os.path.dirname(os.path.abspath(__file__)) + "/son.db"
        sqliteConnection = sqlite3.connect(fileDatabase)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO ListChapterTruyenTranh
                          (id_chapter, id_manga, list_image_chapter_server_goc, list_image_chapter_da_upload, thoi_gian_release) 
                          VALUES (?, ?, ?, ?, ?);"""
        
        data_tuple = (id_chapter, id_manga, list_image_chapter_server_goc, list_image_chapter_da_upload, thoi_gian_release)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Chapter inserted successfully into SqliteDb_developers table: " + id_chapter)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
def uploadImagetoImgbb(LinkImagePoster_linkgoc):
    LinkPostImage = _IMGBB_UPLOAD_LINK + "?key=" + _API_KEY + "&image=" + LinkImagePoster_linkgoc
    linktmp = ""
    try:
        response = Request(LinkPostImage, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urlopen(response).read().decode(urlopen(response).info().get_param('charset') or 'utf-8'))
    except:
        linktmp = ""
    else:
        linktmp = data["data"]["image"]["url"]
    return linktmp

def insertMangaIntoTable(ID_Manga,
       SoLuongView,
       Rate,
       DescriptManga,
       LinkImagePoster_linkgoc,
       Link_Detail_Manga,
       ListChapter,
       Tac_Gia,
       ListCategories,
       Status,
       Title_Manga,
       id_Server,
       LinkImagePoster_link_Upload):
    try:
        currentDictionary = os.getcwd()
        fileDatabase = os.path.dirname(os.path.abspath(__file__)) + "/son.db"
        sqliteConnection = sqlite3.connect(currentDictionary)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO ListManga
                          (ID_Manga,SoLuongView, Rate, DescriptManga, LinkImagePoster_linkgoc, Link_Detail_Manga, ListChapter, Tac_Gia, ListCategories, Status, Title_Manga, id_Server, LinkImagePoster_link_Upload) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        
        data_tuple = (ID_Manga,
       SoLuongView,
       Rate,
       DescriptManga,
       LinkImagePoster_linkgoc,
       Link_Detail_Manga,
       ListChapter,
       Tac_Gia,
       ListCategories,
       Status,
       Title_Manga,
       id_Server,
       LinkImagePoster_link_Upload)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Manga inserted successfully into SqliteDb_developers table: " + ID_Manga)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


for pageIndex in range(PAGE):
    linkListManga = _BASE_LINK + "/genre?page=" + str(pageIndex + 1)
    requestListManga = requests.get(linkListManga)
    soupListManga = BeautifulSoup(requestListManga.text, 'html.parser')
    for mangaIndex in soupListManga.findAll('div', class_='content-genres-item'):

        ID_Manga = _BASE_LINK + mangaIndex.find('div', {"class": "genres-item-info"}).find('h3').find('a').get("href")
        SoLuongView = processing_SoLuongView(mangaIndex.find('div', {"class": "genres-item-info"}).find('p', {"class" : "genres-item-view-time text-nowrap"}).find('span', {"class" : "genres-item-view"}).text.strip())
        Rate = mangaIndex.find('a').find('em').text
        DescriptManga = mangaIndex.find('div', {"class": "genres-item-info"}).find('div', {"class" : "genres-item-description"}).text.strip()
        LinkImagePoster_linkgoc = _BASE_LINK + mangaIndex.find('a', {"class" : "genres-item-img"}).find('img', {"class" : "img-loading"}).get('src')
        Link_Detail_Manga = _BASE_LINK + mangaIndex.find('div', {"class": "genres-item-info"}).find('h3').find('a').get("href")
        Tac_Gia = mangaIndex.find('div', {"class": "genres-item-info"}).find('p', {"class" : "genres-item-view-time text-nowrap"}).find('span', {"class" : "genres-item-author"}).text
        Title_Manga =  mangaIndex.find('div', {"class": "genres-item-info"}).find('h3').find('a').text
        id_Server = _BASE_LINK

        
        LinkImagePoster_link_Upload = uploadImagetoImgbb(LinkImagePoster_linkgoc)
        currentDictionary = os.getcwd()
        mode = 0o777
        workdiction = os.path.join(currentDictionary, "CrawlData")
        if os.path.exists(workdiction) == False:
            os.mkdir(workdiction, mode)
        os.chdir(workdiction)
        pathFolderManga = os.path.join(workdiction, re.sub("[\\/:*?\"<>|]","",Title_Manga))
        if os.path.exists(pathFolderManga) == False:
            os.mkdir(pathFolderManga)
        print(Link_Detail_Manga)
        requestMangaIndex = requests.get(Link_Detail_Manga)
        soupMangaIndex = BeautifulSoup(requestMangaIndex.text, 'html.parser')

        ListChapter = []
        ListLinkChapter = []
        ListCategories = []
        thoi_gian_release = []
        for chapterIndex in soupMangaIndex.findAll('li', class_='a-h'):
            ListChapter.append(chapterIndex.find('a').text)
            ListLinkChapter.append(_BASE_LINK + chapterIndex.find('a').get('href'))
            thoi_gian_release.append(chapterIndex.select('span')[1].text)
        for indexI in range(len(ListChapter)):
            pathFolderChapter = os.path.join(pathFolderManga, re.sub("[\\/:*?\"<>|]","",ListChapter[indexI]))
            if os.path.exists(pathFolderChapter) == False:
                os.mkdir(pathFolderChapter)
            os.chdir(pathFolderChapter)
            
            requestChapterIndex = requests.get(ListLinkChapter[indexI])
            soupChapterIndex = BeautifulSoup(requestChapterIndex.text, 'html.parser')
            print(ListLinkChapter[indexI])
            cnt = 1
            list_image_chapter_server_goc = []
            list_image_chapter_da_upload = []
            for Image in soupChapterIndex.findAll('img', class_='img-loading'):
                linkImage = Image.get('data-src')
                list_image_chapter_server_goc.append(linkImage)
                list_image_chapter_da_upload.append(uploadImagetoImgbb(linkImage))
                response = requests.get(linkImage)
                with open( str(cnt) + ".jpg", "wb") as f:
                    f.write(response.content)
                print(str(cnt))
                cnt += 1
            list_image_chapter_server_goc = ','.join(list_image_chapter_server_goc)
            list_image_chapter_da_upload = ','.join(list_image_chapter_da_upload)
            insertChapterIntoTable(ListLinkChapter[indexI], ID_Manga, list_image_chapter_server_goc, list_image_chapter_da_upload, thoi_gian_release[indexI])

        ListChapter = ','.join(ListChapter)
        for categoryIndex in soupMangaIndex.find('div', {"class" : "story-info-right"}).find('table', {"class" : "variations-tableInfo"}).find('tbody').select('tr')[3].find('td', {"class" : "table-value"}).findAll('a', class_='a-h'):
            ListCategories.append(categoryIndex.text)
        ListCategories = ','.join(ListCategories)
        Status = soupMangaIndex.find('div', {"class" : "story-info-right"}).find('table', {"class" : "variations-tableInfo"}).find('tbody').select('tr')[2].find('td', {"class" : "table-value"}).text.strip()
        insertMangaIntoTable(ID_Manga,SoLuongView, Rate, DescriptManga, LinkImagePoster_linkgoc, Link_Detail_Manga, ListChapter, Tac_Gia, ListCategories, Status, Title_Manga, id_Server, LinkImagePoster_link_Upload)
        
        break
    break