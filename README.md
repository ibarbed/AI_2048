AI_2048
=======

My take on an AI using minimax with alpha-beta pruning to beat the 2048 game

=======

Player AI

The player AI uses LDS-DFS minimax with alpha-beta pruning and a maximum depth of 4 (i.e. sees 3 player moves ahead). The utility function is calculated as follows:

- The base utility is calculated by aggregating the individual tile utility. The points assigned to each value correspond to the scoring system original to the 2048 game (i.e. 16 for the 8 tile, 9,216 for the 1024 tile and 20,480 for the 2048 tile) the advantage of this utility function is that since it is a growing function it encourages the AI to merge tiles.

- To sphisticate the strategy of the AI, we penalize the utility function if the tiles are not in decreasing (or increasing) order in a row or column as we want to keep the board "tidy". If a tile is not in the appropriate order within its row or column we substract the difference in utility between the two adjacen tiles to the base utility mentioned in the first point. This, for example, heavily penalizes the player AI if he moves in a certain direction that allows the computer AI to put a "2" adjacent to a 2048 tile

- To incentivize merging and allow the player AI to order the tiles in a way that is organized and facilitates merging, we add a "bonus" to the base function if two tiles with close values are adjacent (e.g. 256 and 512, or two 512 tiles) since that will facilitate future merges

- I have investigated with different depths and utility functions and this combination has the best aggregate performance.


Computer AI

The computer AI uses the same Utility function as the player AI but plays to minimize the outcome. In a sense, the main objective of the computer AI is to deploy the new tile as close to the to the maximum tile as possible

