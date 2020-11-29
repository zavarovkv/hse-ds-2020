import requests
import networkx as nx
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup


headers = {'Accept-Language': 'en',
           'X_FORWARDED_FOR': '2.21.184.0'}

colors_palette = ['black', 'red', 'green']


def get_actor_name_by_url(url):
    result = None
    actor_page = requests.get(url, headers=headers)

    if actor_page.status_code == 200:
        actor_page_soup = BeautifulSoup(actor_page.content, 'html.parser')
        actor_soup = actor_page_soup.find('h1', attrs={'class': 'header'})
        actor_soup = actor_soup.find('span', attrs={'class': 'itemprop'})

        result = str(actor_soup.text)

    return result


def draw_graph_by_adj_dict(adj_dict, actors, file_name):
    g = nx.Graph()
    edge_labels = {}

    short_actors_name = []

    for (actor, _) in actors:
        actor_name = actor[0] + '. ' + actor[actor.find(' ') + 1:-1]
        short_actors_name.append(actor_name)
        g.add_node(actor_name)

    for (x, y), value in adj_dict.items():
        if value > 0:
            g.add_edge(short_actors_name[x], short_actors_name[y], weight=value)
            edge_labels[(short_actors_name[x], short_actors_name[y])] = value

    node_size = [600 * len(n) for n in list(g.nodes())]
    edge_colors = [colors_palette[v-1] for _, v in edge_labels.items()]

    options = {'with_labels': True,
               'node_color': 'pink',
               'edge_color': edge_colors,
               'width': 3,
               'linewidths': 1,
               'alpha': 0.9,
               'font_size': 12,
               'node_size': node_size}

    pos = nx.spring_layout(g)
    plt.figure(4, figsize=(24, 24))

    nx.draw(g, pos, **options)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_color='red')

    plt.axis('off')
    plt.savefig(file_name)
    plt.close()
    print(f'{file_name} created.')

    return True
