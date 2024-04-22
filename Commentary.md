# Exercise 7 - Solutions Kai Schultz
The code should have implemented the ACO algorithm correctly. If you run ant-colony.py it will start running all the different combinations of alpha, beta and rho. 
It logs the initial pheromone of the current colony. Other than that it will update you in the terminal if there is a new best path.

I am running multiple runs per configuration, because due to computational limitations I cannot run larger colonies / longer iterations. So I am subject to larger deviations. 
To counteract this I am running the same configuration multiple times.


## Task 3
I tested the different variations empirically. The different combinations were:
```
alpha   [0.75,1,1.25]
beta    [2,3,4,5,6]
rho     [0.3,0.4,0.5,0.6,0.7]
```

for each combination I ran the simulation 20 times.
Each Colony was filled with 48 ants and went through 50 iterations.

While i would have preferred longer iterations, my computer cannot handle more than this

### How do parameters alpha and beta impact the performance?
Alpha is used to calculate the weight that pheromones have when deciding on what path to take. If alpha is zero, pheromones are disregarded.
Beta does the same just for the distance. 
#### Alpha 
* Lower Alpha values mean less importance of pheromone trails. Which means less importance of existing paths and higher chances of exploring new trails.
* Higher Alpha values put more importance on pheromone trails. Which means higher probability for chosing paths already known. 

Ofcourse the challange here is to find the sweet spot, where we explore all relevant trails and do not get stuck on non-optimal paths, but once we have found an optimal path wil stay on it.
Through experimenting I have found that staying on the lower side of alpha values is a bit more reliant, since even though it might take longer to find a good path, the risk of getting stuck on a less than optimal path is much lower.

#### Beta
* Lower Beta values mean less importance of closer nodes. 
* Higher Beta values mean we go for the closest node more often.

While it at first seems reasonable to go to closer nodes because then the path is shorter, this can then lead to much longer paths once all the close edges are used up. This is why it is important to sometimes use a longer edge first, so that 
an overall shorter path can be created. Through experimenting I found a neutral value to work the best for me (so 3-4).

### How does the evaporation rae rho affect the performance?
Rho is the parameter that decides how much pheromone evaporates between tours. So a higher Rho means the pheromones evaporate a lot and the results of the last tour have less influence over current decisions. A lower Rho means, that
paths explored in the last tour will still have a lot of pheromone deposited on them and therefore a higher probability to be chosen again. 
* Lower Rho values mean higher base importance of pheromone
* Higher Rho values mean less base importance of pheromone

Since in the path selection the pheromone level of the path is taken to the power of alpha, a higher pheromone level will have similar effects as a higher alpha.

#### How would you modify your implementation in orer to apply ACO to DTSP?
If cities were to be added and removed at run-time, I would have to restructure the code to allow nodes to be added and removed. Additionally whenever a new node gets added there will be n - 1 new edges and whenever a node removed there will be n -1 edges removed.
The adding of cities would have to happen after or before the ants are on tour. 
##### In case of Removal:   
    If a node gets removed we can simply remove all associated edges. The ants should then find a new optimal path.
##### In case of Addition:
    If we add a new node, we should instantialize all the new edges with a base pheromone level. if only an insignificant amount of nodes is added in comparison to the graph size, we can simply set it to the initial base pheromone level and leave it be.
    If we add a significant amount of new nodes, it might be helpful to reinitialize the entire graph. 


