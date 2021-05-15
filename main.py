"""Main file for the program."""

import click

from reward_graph import RewardGraph

@click.command()
@click.argument('graph_file')
def main(graph_file):
    reward_graph = RewardGraph()
    reward_graph.import_graph_from_csv(graph_file)
    for node in reward_graph.nodes():
        print(f"Current RW Scale: {node['reward_scale_correct']}, Computed RW Scale: { reward_graph.get_reward_scale(node) }, {node['name']}")

if __name__ == "__main__":
    main()