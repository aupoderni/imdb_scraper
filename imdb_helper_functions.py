import urllib.request
from bs4 import BeautifulSoup

def helper_function_example():
    return 'Hello, I am a supposed to be a helper function'

def soup_from_url(url, add_fullcredits=True):
    if add_fullcredits:
        req = urllib.request.Request(
            url=url+'fullcredits', 
            headers={'User-Agent': 'Mozila/5', 'Accept-Language': 'en'}
            )
    else:
        req = urllib.request.Request(
            url=url, 
            headers={'User-Agent': 'Mozila/5', 'Accept-Language': 'en'}
            )
    data = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(data, 'html.parser')
    return soup

def get_correct_url(url):
    correct_url = ''
    for letter in url:
        if letter == '?':
            break
        correct_url += letter
    return correct_url

def _get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    cast_list = cast_page_soup.find('table', {'class': 'cast_list'})
    all_actors = cast_list.find_all('tr', {'class': ['odd', 'even']})
    result_list = []
    i = 0
    for actor in all_actors:
        if '(uncredited)' in actor.text or (num_of_actors_limit
                                        and i >= num_of_actors_limit):
            break
        actor_link = actor.find_all('a')[1]
        actor_name = actor_link.text.strip()
        link = urllib.parse.urljoin('https://www.imdb.com/', actor_link['href'])
        link = get_correct_url(link)
        result_list.append((actor_name, link))
        i += 1
    return result_list

def _get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):
    film_list = actor_page_soup.find('div', {'id': 'filmo-head-actor'})
    if not film_list:
        film_list = actor_page_soup.find('div', {'id': 'filmo-head-actress'})
    film_list = film_list.find_next('div')
    film_list = film_list.find_all('div', {'class': ['filmo-row odd', 'filmo-row even']})
    result_list = []
    i = 0
    for  film in film_list:
        if num_of_movies_limit and i >= num_of_movies_limit:
            break
        text = film.text[film.text.find('('):film.text.find(')') + 1]
        if text:
            continue
        film_link = film.find_all('a')
        film_name = film_link[0].text
        link = link = urllib.parse.urljoin('https://www.imdb.com/', film_link[0]['href'])
        link = get_correct_url(link)
        result_list.append((film_name, link))
        i += 1
    return result_list

def get_movies_list(url, dict, level, num_of_movies_limit):
    if dict.get(url):
        actor_movies = dict[url]['level_'+str(level)+'_movies']
    else:
        actor_soup = soup_from_url(url)
        actor_movies = set(_get_movies_by_actor_soup(actor_soup, num_of_movies_limit))
        dict[url] = {'level_'+str(level)+'_movies': actor_movies}
    return actor_movies, dict

def get_actors_list(url, actor_movies, dict, num_of_actors_limit, level):
    all_actors = set()
    if dict.get(url).get('level_'+str(level)+'_actors'):
        all_actors = dict[url]['level_'+str(level)+'_actors']
    else:
        for movie in actor_movies:
            movie_soup = soup_from_url(movie[1])
            actors = set(_get_actors_by_movie_soup(movie_soup, num_of_actors_limit))
            all_actors = all_actors | actors
        dict[url].update({'level_'+str(level)+'_actors': all_actors})
    return all_actors, dict