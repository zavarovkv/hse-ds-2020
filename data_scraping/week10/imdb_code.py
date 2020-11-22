import requests
import re
from bs4 import BeautifulSoup


endpoint_url = 'https://www.imdb.com/'


def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):

    actors = []

    css_selector = '#fullcredits_content > table.cast_list > tr > td:nth-child(2) > a'
    actors_soup = cast_page_soup.select(css_selector)

    if num_of_actors_limit is not None:
        actors_soup = actors_soup[:num_of_actors_limit]

    for actor in actors_soup:
        re_url = re.search(r"href=\"/(.*)\">", str(actor)).group(1)
        url_to_actor_page = endpoint_url + re_url

        re_actor = re.search(r">(.*)\s", str(actor)).group(1)
        name_of_actor = re_actor.strip()

        actors.append((name_of_actor, url_to_actor_page))

    return actors


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):

    movies = []

    css_selector = '#filmography > div:nth-child(2) > div'
    movies_soup = actor_page_soup.select(css_selector)

    for movie in movies_soup:
        re_announced = re.search(r"class=\"in_production\"", str(movie))
        if re_announced is not None:
            continue

        re_url = re.search(r"<b><a href=\"/(.*)\">", str(movie)).group(1)
        url_to_movie_page = endpoint_url + re_url

        re_name = re.search(r"<b><a href=\"(.*)\">(.*)</a>", str(movie)).group(2)
        name_of_movie = re_name.strip()

        movies.append((name_of_movie, url_to_movie_page))

        if num_of_movies_limit is not None:
            if len(movies) >= num_of_movies_limit:
                break

    return movies


def main():
    film_details = {
        'name': 'Borat Subsequent Moviefilm',
        'cast_page_url': endpoint_url + 'title/tt13143964/fullcredits'
    }

    cast_page = requests.get(film_details['cast_page_url'])

    if cast_page.status_code == 200:
        cast_page_soup = BeautifulSoup(cast_page.content, 'html.parser')
        actors_by_movie = get_actors_by_movie_soup(cast_page_soup, 5)
        print(f'Actors in \"{film_details["name"]}\":\n{actors_by_movie}\n')

    actor_details = {
        'name': 'Sacha Baron Cohen',
        'actor_page_url': endpoint_url + 'name/nm0056187/'
    }

    actor_page = requests.get(actor_details['actor_page_url'])

    if actor_page.status_code == 200:
        actor_page_soup = BeautifulSoup(actor_page.content, 'html.parser')
        movies_by_actor = get_movies_by_actor_soup(actor_page_soup, 5)
        print(f'Movies with \"{actor_details["name"]}\" (without announced):\n{movies_by_actor}\n')


if __name__ == '__main__':
    main()
