# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
import imdb_helper_functions
import pandas as pd

def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    result_list = imdb_helper_functions._get_actors_by_movie_soup(cast_page_soup, 
                                                                  num_of_actors_limit)
    return result_list

def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):
    result_list = imdb_helper_functions._get_movies_by_actor_soup(actor_page_soup, 
                                                                  num_of_movies_limit)
    return result_list

def get_movie_distance(actor_start_url, actor_end_url, dict,
        num_of_actors_limit=None, num_of_movies_limit=None):
    current_distance = 1
    print('Current level: ', 1)
    actor_start_movies, dict = imdb_helper_functions.get_movies_list(actor_start_url, dict, 
                                               current_distance, num_of_movies_limit)
    actor_end_movies, dict = imdb_helper_functions.get_movies_list(actor_end_url, dict, 
                                             current_distance, num_of_movies_limit)
    if len(list(actor_start_movies & actor_end_movies)) > 0:
        return current_distance, dict
    current_distance += 1
    print('Current level: ', current_distance)
    all_actors_start, dict = imdb_helper_functions.get_actors_list(actor_start_url, 
                                             actor_start_movies, dict, 
                                             num_of_actors_limit, 
                                             current_distance)
    print('Start actor checked')
    all_actors_end, dict = imdb_helper_functions.get_actors_list(actor_end_url, 
                                             actor_end_movies, dict, 
                                             num_of_actors_limit, 
                                             current_distance)
    print('End actor checked')
    if len(list(all_actors_start & all_actors_end)) > 0:
        return current_distance, dict
    return 'inf', dict

def get_movie_descriptions_by_actor_soup(actor_page_soup):
    actor_movies = imdb_helper_functions._get_movies_by_actor_soup(actor_page_soup)
    descriptions = []
    for movie in actor_movies:
        movie_link = movie[1] + 'plotsummary/'
        movie_soup = imdb_helper_functions.soup_from_url(movie_link, add_fullcredits=False)
        film_summaries = movie_soup.find('div', {'data-testid': 'sub-section-summaries'})
        try:
            short_sum = film_summaries.find('li', {'role': 'presentation'}).text
        except:
            continue
        descriptions.append(short_sum)
    return descriptions


#   THE CODE BELOW WAS USED FOR GENERATING .CSV FILE WITH DISTANCES;
#   DELETE COMMENTS AND RUN IT IF YOU WANT TO TEST IT

'''
current_ind = 0
try:
    df = pd.read_csv('distances.csv', header=0, names=['Actor_first', 'Link_first',
                                                       'Actor_second', 'Link_second', 'Distance'])
    for ind in df.index:
        if df['Distance'][ind] == 0:
            current_ind = ind
            break
except:
    actors = [['Dwayne Johnson', 'https://www.imdb.com/name/nm0425005/'], 
            ['Chris Hemsworth', 'https://www.imdb.com/name/nm1165110/'], 
            ['Robert Downey Jr.', 'https://www.imdb.com/name/nm0000375/'], 
            ['Akshay Kumar', 'https://www.imdb.com/name/nm0474774/'], 
            ['Jackie Chan', 'https://www.imdb.com/name/nm0000329/'], 
            ['Bradley Cooper', 'https://www.imdb.com/name/nm0177896/'], 
            ['Adam Sandler', 'https://www.imdb.com/name/nm0001191/'], 
            ['Scarlett Johansson', 'https://www.imdb.com/name/nm0424060/'], 
            ['Sofia Vergara', 'https://www.imdb.com/name/nm0005527/'], 
            ['Chris Evans', 'https://www.imdb.com/name/nm0262635/']]
    df = pd.DataFrame(actors, columns=['Actor', 'Link'])
    df = df.join(df, how='cross', lsuffix='_first', rsuffix='_second')
    df = df[df['Actor_first'] != df['Actor_second']]
    df['Distance'] = 0

#create a dict to store data for actors
dict = {}

for ind in df.index[current_ind:]:
    distance, dict = get_movie_distance(df['Link_first'][ind], df['Link_second'][ind], 
                                        dict = dict)
    df['Distance'][ind] = distance
    print('Row number = ', ind, ' , distance = ', distance)
    if ind%5 == 0:
        df.to_csv('distances.csv', header=False, index=False)

df.to_csv('distances.csv', header=False, index=False)
'''

#   THE CODE BELOW WAS USED FOR GENERATING .TXT FILES WITH MOVIE DESCRIPTIONS;
#   DELETE COMMENTS AND RUN IT IF YOU WANT TO TEST IT
'''
actors = [['Dwayne Johnson', 'https://www.imdb.com/name/nm0425005/'], 
            ['Chris Hemsworth', 'https://www.imdb.com/name/nm1165110/'], 
            ['Robert Downey Jr.', 'https://www.imdb.com/name/nm0000375/'], 
            ['Akshay Kumar', 'https://www.imdb.com/name/nm0474774/'], 
            ['Jackie Chan', 'https://www.imdb.com/name/nm0000329/'], 
            ['Bradley Cooper', 'https://www.imdb.com/name/nm0177896/'], 
            ['Adam Sandler', 'https://www.imdb.com/name/nm0001191/'], 
            ['Scarlett Johansson', 'https://www.imdb.com/name/nm0424060/'], 
            ['Sofia Vergara', 'https://www.imdb.com/name/nm0005527/'], 
            ['Chris Evans', 'https://www.imdb.com/name/nm0262635/']]

for actor in actors:
    actor_page_soup = imdb_helper_functions.soup_from_url(actor[1])
    descriptions = get_movie_descriptions_by_actor_soup(actor_page_soup)
    with open(actor[0]+'.txt', 'w', encoding='utf-8') as f:
        for film in descriptions:
            f.write(film+"\n")
        f.close()
'''