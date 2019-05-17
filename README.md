# Aquatic-Attack
2-player duelling game created using Python 2.7 and Pygame where two players control a Pufferfish and a Seahorse and must battle it out. 

One player will need to use the speed and sturdiness of the Pufferfish, while the other must take advantage of the Seahorse's superior range and maneuverability. 

Movement
The Pufferfish is controlled by the arrow keys and the Seahorse is controlled by the keys w,a,s and d.
The Pufferfish is faster than the Seahorse but the Seahorse has more manuverability and will need to use this to his advantage in order to win

Attacking
The Pufferfish deals damage to the Seahorse when they come in contact, due to its spikes, however the player can choose to press 0 to send out its spikes and damage the Seahorse
The Pufferfish however will be deflated and spikeless for a few seconds unable to damage the Seahorse
The Seahorse deals damage by sending out bubbles in the direction he is facing (one at a time) with the space bar
The Seahorse cannot fire a bubble as long as another bubble is already existing, the bubble ability is considered on cooldown.
This means that missing a shot will result in a longer wait until another one can be fired

Powerup
There are several fish that will appear from the right side of the screen. If either player gets eats/touches one of these fish they will receive a damage boost of x2 for a limited duration
The duration of the damage boost will appear either on the top left (Seahorse) or the top right (Pufferfish)

Map
If a player goes off one side of the screen they will come out of the other one, this does not work vertically, if the player touches the top wall or the floor they will stop
The Pufferfish can use the pillar as protection from the Seahorses bubbles because they cannot pass through it

Game end
A round is finshed when one players health reaches 0, at which time the players can start a new round by pressing p or exit the program with Escape
The number of rounds won (score) of each player is displayed at the top left and top right of the screen
