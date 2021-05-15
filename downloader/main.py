"""Download graph data for given latitude and longitude."""

import click

from utils import get_nodes_box
from utils import compute_miner_earnings

@click.command()
@click.argument('nelat')
@click.argument('nelon')
@click.argument('swlat')
@click.argument('swlon')
def main_func(nelat, nelon, swlat, swlon):
    """For negative coords, prepend a 'n' on the number. Ex(n83 = -83)"""
    swlat = swlat.replace('n', '-')
    swlon = swlon.replace('n', '-')
    nelat = nelat.replace('n', '-')
    nelon = nelon.replace('n', '-')
    
    nodes = (get_nodes_box(swlat, swlon, nelat, nelon))

    earnings = []

    for i, node in enumerate(nodes):
        node_addr = node['address']
        lat = node['lat']
        lng = node['lng']
        reward_scale = node['reward_scale']

        
        node_earnings = compute_miner_earnings(node_addr)['total']

        print('Indexing node: {i} - {e}'.format(i=i, e=node_earnings))

        earnings.append( (node_earnings, lat, lng, reward_scale, node_addr) )

    earnings = sorted(earnings, key = lambda t: float(t[0]), reverse=True)

    with open('tmp.txt', 'w') as f:
        for node in earnings:
            f.write(
                "{e},{lat},{lng},{rs},{addr}\n".format(
                    e = node[0],
                    lat = node[1],
                    lng = node[2],
                    rs = node[3], 
                    addr = node[4]
                )
            )


if __name__ == "__main__":
    main_func()
