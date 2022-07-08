from datetime import date

import requests
from Objects.Team import Team
from Objects.League import League
from Objects.Player import Player
from bs4 import BeautifulSoup


def loadLeague(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    #page = link + "/plus/?saison_id=2019"
    page = link
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    league = pageSoup.find("div", {"class": "box-header"}).find('h1')
    league = league.text
    teams= pageSoup.find("div", {"class": "responsive-table"}).find("tbody").find_all("tr")

    result = []
    for a in teams:
        b= a.find("a")
        c = b["href"]
        link = "https://www.transfermarkt.pt" + c
        players = loadPlayers(link)
        for player in players:
            result.append(player)
    return result,league


def loadPlayers(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = link
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    team = pageSoup.find("div",{"class":"dataHeader dataExtended"}).find("span").text.strip()
    league=pageSoup.find("span",{"class":"hauptpunkt"}).find("a").text.strip()
    P = pageSoup.find("div", {"class": "responsive-table"}).find("tbody").find_all("span", {"class": "hide-for-small"})
    player_links =[]
    players = []
    print(team)
    for p in P:
        a = p.find("a")
        player_name = a.text
        player_links.append(["https://www.transfermarkt.pt" + a["href"],player_name])
    for player_page in player_links:
        player = loadPlayer(player_page[0],player_page[1],team,league)
        if player == None:
            continue
        players.append(player)
    return players


def loadPlayer(link,player_name,team,league):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = link
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    player_page = pageSoup.find("header", {"class": "data-header"})
    if player_page is None:
        return

    data = player_page.find("div", {"class": "data-header__details"})
    #get Age
    try:
        age = int(data.find("span",{"itemprop":"birthDate"}).text.split("(")[1].split(")")[0])
    except AttributeError:
        age = None

    # get nationality
    try:
        nationality = data.find("span",{"itemprop":"nationality"}).text.strip()
    except AttributeError:
        nationality = None

    # get height
    try:
        height = float(data.find("span", {"itemprop": "height"}).text.split(" ")[0].replace(",",".").strip())
    except AttributeError:
        height = None


    # get Position
    position = None
    try:
        check_pos_value = data.find_all("li",{"class":"data-header__label"})
        for element in check_pos_value:
            if element.text.strip().__contains__("Posição:"):
                position = element.find("span",{"class":"data-header__content"}).text.strip()
    except :
        position = None

    # get Agent
    agent = "N.E."
    try:
        check_agent = data.find_all("li",{"class":"data-header__label"})
        for element in check_agent:
            if element.text.strip().__contains__("Agente:"):
                agent = element.find("span",{"class":"data-header__content data-header__content--vertical-aligned"}).find("a").text.strip()
    except :
        agent = None

    # get Inter and goals
    inter = None
    goals = None
    try:
        check_inter = data.find_all("li", {"class": "data-header__label"})
        for element in check_inter:
            if element.text.strip().__contains__("Internacionalizações/Golos:"):
                inter = int(element.find_all("a")[0].text.strip())
                goals = int(element.find_all("a")[1].text.strip())
    except:
        inter = None
        goals = None

    # get value
    try:
        value = pageSoup.find("a", {"class": "data-header__market-value-wrapper"}).text.split("€")[0]
        value = value.split((" "))
        if value[1] == 'M':
            value = int(float(value[0].replace(",", ".")) * 1000000)
        elif value[1] == 'mil' :
            value = int(float(value[0].replace(",", ".")) * 1000)
        else:
            value = int(value[0])
    except AttributeError:
        value = 0

    # get years left contrat
    years_left = None
    try:
        header_club = player_page.find("div", {"class": "data-header__club-info"})
        check_years_left = header_club.find_all("span", {"class": "data-header__label"})
        for element in check_years_left:
            if element.text.strip().__contains__("Contrato até:"):
                years_left = int(element.find("span").text.strip().split("/")[2]) - date.today().year
    except:
        years_left = None

    # get preferred foot
    preferred_foot = None
    try:
        info = pageSoup.find("div", {"class": "info-table info-table--right-space"})
        array_of_info = info.find_all("span",{"class":"info-table__content info-table__content--bold"})
        for element in array_of_info:
            if element.text.strip().lower() == "direito" or element.text.strip().lower() == "esquerdo":
                preferred_foot = element.text.strip().lower()
    except AttributeError:
        preferred_foot = None
    player_data = [player_name, age, height,nationality,position,agent,inter,goals,years_left,preferred_foot,team,league,value]
    return player_data

