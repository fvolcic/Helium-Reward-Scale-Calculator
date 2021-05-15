"""Download graph data for given latitude and longitude."""

import click

from utils import get_nodes_box
from utils import compute_miner_earnings
from utils import *

@click.command()
@click.argument('file')
@click.argument('nelat')
@click.argument('nelon')
@click.argument('swlat')
@click.argument('swlon')
def main_func(file, nelat, nelon, swlat, swlon):
    """For negative coords, prepend a 'n' on the number. Ex(n83 = -83)"""
    swlat = swlat.replace('n', '-')
    swlon = swlon.replace('n', '-')
    nelat = nelat.replace('n', '-')
    nelon = nelon.replace('n', '-')
    
    nodes = (get_nodes_box(swlat, swlon, nelat, nelon))

    node_info = []

    current_height = get_height()

    with open(f'{file}_nodes.csv','w') as f:
        f.write('address,name,lat,lng,reward_scale_correct\n')
        for node in nodes:
            name = node['name']
            last_poc_challene = get_last_poc_challenge(node['address'])
            s = current_height - last_poc_challene
            stat = node['status']['online']
            print(f'Contacting node: { name } | poc {s} | status {stat}')
            
            if current_height - last_poc_challene > 3600:
                continue

            #if node['status']['online'] != 'online':
            #    continue

            f.write(str(node['address'])+',')
            f.write(str(node['name'])+',')
            f.write(str(node['lat'])+',')
            f.write(str(node['lng'])+',')
            f.write(str(node['reward_scale'])+'\n')


if __name__ == "__main__":
    main_func()
