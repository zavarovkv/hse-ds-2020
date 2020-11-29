import requests
import re
from bs4 import BeautifulSoup
import itertools
import pickle

from data_scraping.week10_11.imdb_helper_functions import get_actor_name_by_url, \
    draw_graph_by_adj_dict, headers


endpoint_url = 'https://www.imdb.com/'
distance_limit = 3
cache = {}


def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    actors = []

    css_selector = '#fullcredits_content > table.cast_list > tr > td:nth-child(2) > a'
    actors_soup = cast_page_soup.select(css_selector)

    # Check limit of actors
    if num_of_actors_limit is not None:
        actors_soup = actors_soup[:num_of_actors_limit]

    for actor in actors_soup:
        # Get URL to actor page
        re_url = re.search(r"href=\"/(.*)\">", str(actor)).group(1)
        if not re_url:
            continue
        url_to_actor_page = endpoint_url + re_url

        # Get actor's name
        re_actor = re.search(r">(.*)\s", str(actor)).group(1)
        if not re_actor:
            continue
        name_of_actor = re_actor.strip()

        actors.append((name_of_actor, url_to_actor_page))

    return actors


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):
    movies = []

    # if male
    movies_soup = actor_page_soup.find('div', attrs={'data-category': 'actor'})
    # else female
    if movies_soup is None:
        movies_soup = actor_page_soup.find('div', attrs={'data-category': 'actress'})
    # else actor hasn't movies
    if movies_soup is None:
        return movies

    movies_soup = movies_soup.find_next('div')
    movies_soup = movies_soup.find_all('div', recursive=False)

    for movie in movies_soup:
        # Skip all announced movies
        re_announced = re.search(r"class=\"in_production\"", str(movie))
        if re_announced:
            continue

        # Get URL to movie page
        re_url = re.search(r"<b><a href=\"/(.*)\">", str(movie)).group(1)
        if not re_url:
            continue
        url_to_movie_page = endpoint_url + re_url

        # Get name of movie
        re_name = re.search(r"<b><a href=\"(.*)\">(.*)</a>", str(movie)).group(2)
        if not re_name:
            continue
        name_of_movie = re_name.strip()

        # Check 'TV Series' or 'TV Mini-Series' or smth else
        is_series = False
        re_series = re.search(r"<b><a href=\"(.*)\">(.*)</a></b>\n(.*)\n<br/>", str(movie))
        if re_series:
            if len(re_series.groups()) >= 3:
                is_series = True

        if not is_series:
            movies.append((name_of_movie, url_to_movie_page))
        else:
            continue

        # Check limit of movies
        if num_of_movies_limit is not None:
            if len(movies) >= num_of_movies_limit:
                break

    return movies


# actor_start_url, actor_end_url - urls to imdb pages of actors, that we want to measure movie distance between
# The function return an integer, a movie distance between the given actors
# The function may also get optional arguments: num_of_actors and num_of_movies
def get_movie_distance(actor_start_url, actor_end_url, num_of_actors_limit=None, num_of_movies_limit=None):
    current_distance = 1
    actor_start = (get_actor_name_by_url(actor_start_url), actor_start_url)
    actor_end = (get_actor_name_by_url(actor_end_url), actor_end_url)

    actors = [actor_start]

    while current_distance < distance_limit + 1:
        movies = []

        for (actor, url) in actors:
            if url in cache:
                actor_page_soup = cache[url]
            else:
                actor_page = requests.get(url, headers=headers)
                actor_page_soup = BeautifulSoup(actor_page.content, 'html.parser')
                cache[url] = actor_page_soup

            movies_by_actor = get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit)
            movies.extend(movies_by_actor)

        actors = []

        for (title, url) in movies:
            if url in cache:
                movie_page_soup = cache[url]
            else:
                movie_page = requests.get(url + 'fullcredits/', headers=headers)
                movie_page_soup = BeautifulSoup(movie_page.content, 'html.parser')
                cache[url] = movie_page_soup

            actors_by_movie = get_actors_by_movie_soup(movie_page_soup, num_of_actors_limit)
            actors.extend(actors_by_movie)

        if actor_end in actors:
            return current_distance

        current_distance += 1

    return 0


def main():
    actors = [('Dwayne Johnson',        'nm0425005'),
              ('Chris Hemsworth',       'nm1165110'),
              ('Robert Downey Jr.',     'nm0000375'),
              ('Akshay Kumar',          'nm0474774'),
              ('Jackie Chan',           'nm0000329'),
              ('Bradley Cooper',        'nm0177896'),
              ('Adam Sandler',          'nm0001191'),
              ('Scarlett Johansson',    'nm0424060'),
              ('Sofia Vergara',         'nm0005527'),
              ('Chris Evans',           'nm0262635')]

    adj_dict = {}
    actors_combinations_idx = list(itertools.combinations(range(0, len(actors)), 2))

    try:
        with open('data.pickle', 'rb') as f:
            adj_dict = pickle.load(f)

    except FileNotFoundError:
        print('Data wasn\'t founded in storage. Process will start over.')

    else:
        if len(adj_dict) == len(actors_combinations_idx):
            print(f'{len(adj_dict)} from {len(actors_combinations_idx)} records were founded in storage. '
                  f'Process completed.')

            draw_graph_by_adj_dict(adj_dict, actors, file_name='all_edges_graph.png')

            # Get uniq values from weight without 0
            weight_list = list(set([v for v in adj_dict.values()]) - {0})

            for weight in weight_list:
                adj_dict_tmp = {k: v for k, v in adj_dict.items() if v == weight}
                draw_graph_by_adj_dict(adj_dict_tmp, actors, file_name=str(weight) + '_edges_graph.png')

            return

        else:
            print(f'{len(adj_dict)} from {len(actors_combinations_idx)} records were founded in storage. '
                  f'Process will continue...')

    idx = len(adj_dict)

    for (actor_start_idx, actor_end_idx) in actors_combinations_idx:

        if (actor_start_idx, actor_end_idx) in adj_dict:
            continue

        idx += 1

        actor_start_url = endpoint_url + 'name/' + actors[actor_start_idx][1] + '/'
        actor_end_url = endpoint_url + 'name/' + actors[actor_end_idx][1] + '/'

        actor_start = get_actor_name_by_url(actor_start_url)
        actor_end = get_actor_name_by_url(actor_end_url)

        print(f'{idx} / {len(actors_combinations_idx)}. '
              f'Calculating distance between actors {actor_start} <-> {actor_end} ...')

        distance = get_movie_distance(actor_start_url, actor_end_url, 5, 5)
        adj_dict[(actor_start_idx, actor_end_idx)] = distance

        with open('data.pickle', 'wb') as f:
            pickle.dump(adj_dict, f)

        print(f'{idx} / {len(actors_combinations_idx)}. '
              f'Distance between actors {actor_start} <-> {actor_end}: {distance}')

    print('Process completed. If you want draw edges graph/s - run program one mote time.')


if __name__ == '__main__':
    main()
