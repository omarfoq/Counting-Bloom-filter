from util import *
from sample import *


# Associate for each number of hash functions the corresponding average number of increments per insertions. 
g = [0, 1, 1.24, 1.53, 1.82, 2.09, 2.35,
     2.6, 2.85, 3.09, 3.33, 3.56, 3.79,
     4.01, 4.23, 4.45, 4.66, 4.88, 5.09,
     5.30, 5.50, 5.71, 5.92, 6.12, 6.32,
     6.52, 6.72, 6.91, 7.12, 7.31, 7.50]  


while(True):
    print("Please enter the number of items")
    n_items = int(input())

    print("Please enter the Zipf parameter")
    alpha = float(input() )

    print("Please enter the hit rate desired")
    hit_rate = float(input())

    n_cache_slots = config_cache(n_items,alpha, hit_rate)
    print("This corresponds to a number of cache slots of: ", n_cache_slots )

    print("Please enter the average fraction of non distonguished items tolerated(0<h<1)")
    thres_av_n_ghosts = float(input()) * n_cache_slots

    print("Please enter the maximum number of hash functions to use")
    n_hashes_max = int(input())

    l=config_sketch(
        n_items,
        alpha,
        n_cache_slots,
        thres_av_n_ghosts,
        g,
        n_hashes_max
    )

    n_counters=l[0]
    n_hashes=l[1]

    print("The configuration proposed by our strategy is: " ) 

    print(f"The number of counters: {n_counters}") 
    print(f"The number of hash functions: {n_hashes}") 

    print("Please enter number of trials to compute the average of non distinguished items")
    trials= int(input())

    print("Please enter the number of requests in each trial")
    n_requests=int(input())

    n_ghosts=0
    for i in range(trials):
        items_estimations = generate_estimation_items(n_requests, n_items, n_counters, n_hashes, alpha)[0]
        n_ghosts = n_ghosts + metric_performance(items_estimations, n_cache_slots)

    av = n_ghosts / trials 
    av = av / n_cache_slots

    print(f"The average fraction of non distinguished items in the experiment is: {av}")
    