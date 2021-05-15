# HNT Prediction Algorithms

## About
<ul> The goal of this project is to eventually provide a program that will allow one to estimate the earnings of a helium nodes given its lat and lng. This would help improve the Helium network as a whole, along with improving HNT earned by those in the network. </ul>

## TODO	
<ol>
 <li> Create a HNT revenue estimation algorithm. </li>	
  <li> Generate a heatmap of a given region that shows where the most profitable areas are. </li>
</ol>

## How To Use

<ul> To run this program on a given area, you must first download the dataset for a given area. To generate the base data set, go into the "downloader" folder, then run 'python3 scaling.py (output_file) (NE LAT) (NE LNG) (SW LAT) (SW LNG)'. This will download a dataset for all the nodes that currently lie within the box contained within the given coordinates. Copy this dataset into 'graph_data', then create a file with the same suffix, but change the prefix to (output_file)_edges_file.csv. In this file, just type rssi, save, then close. Next, if you would like to determine the reward scale of a node you want to place, add its lat and lng into the (output_file)_nodes_file.csv file. Finally, just run 'python3 main.py (output_file)' and all the reward scales will be printed to the terminal. </ul>
# helium_predictor
