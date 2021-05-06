import matplotlib.pyplot as plt                                                       
import numpy as np
import mmh3
import random 
import matplotlib
import string    
from scipy.stats import binom
from scipy.stats import zipf
        
        
        
        
        
        
# The average number of increments per insertion is independent of the number of counters for M>>k and depends only on the number of hash functions used. It is computed by considering the case where all k bins have the same chances of being selected. 
def average_number_increments_per_insertion(n_hashes,n_requests,n_counters):
    bins=[0]*n_counters
    number_increments=0
    for j in range(n_requests): 
        hashes= random.sample(range(n_counters),n_hashes)  
        minimum=bins[hashes[0]]
        for i in range(1,n_hashes):
            minimum=min(minimum,bins[hashes[i]])
        for i in range(0,n_hashes):
            if bins[hashes[i]]==minimum:
                bins[hashes[i]]= bins[hashes[i]] +1
                if j>=n_counters:
                    number_increments=number_increments+1
    
    return number_increments/(n_requests-n_counters)


# Constant for a Zipf distribution p_i = constant_zipf(N,alpha)/i^{alpha} . 
def constant_zipf(n_items,alpha):  
    s=0
    for i in range(n_items):
        s=s+(np.power(1/(i+1),  alpha))
    return 1/s


#The following function returns an upper bound on the Error Floor given that the items are drawn from a Zipf
def upper_bound_error_floor_rate(n_items,alpha,n_counters,n_hashes,g_k):
    rate_items_ef=1    #Upper bound items contributing to the error floor
    m_ef= n_counters            # Lower bound number of counters in the error floor 
    u_bound_ef= g_k * rate_items_ef/m_ef  #Upper bound Error Floor.
    
    rank=1
    constant= constant_zipf(n_items,alpha)
    probability_item= constant *np.power(1/rank, alpha)
    
    
    while (probability_item> u_bound_ef) & (m_ef> n_hashes*rank) :
        rate_items_ef=rate_items_ef-probability_item
        m_ef=m_ef-n_hashes
        rank=rank+1
        probability_item= constant * np.power(1/rank, alpha) 
        u_bound_ef= min (u_bound_ef, g_k * rate_items_ef/ m_ef)
    return u_bound_ef



#For a given number of hash functions, this function returns the necessary memory in order to be above the noisy region. It simply looks for the value of M that verifies that the rate of item C is higher than the upper bound on the Error Floor. 
def config_n_counters(n_items,alpha,n_hashes,n_cache_slots,g_k):
    constant=constant_zipf(n_items,alpha)
    min_n_counters=n_cache_slots
    max_n_counters=n_items
    threshold=constant* np.power(1/(n_cache_slots+1), alpha) 
    
    while max_n_counters > min_n_counters+1:
        current_n_counters= (max_n_counters+min_n_counters)//2
        ef=upper_bound_error_floor_rate(n_items,alpha,current_n_counters,n_hashes,g_k)
        if ef > threshold: 
            min_n_counters=current_n_counters
        elif ef < threshold: 
            max_n_counters=current_n_counters
        else:
            break 
    return current_n_counters



# The following function is nothing but the false positive rate in a regular bloom filter where C items are inserted multiplies by the number of items other than the C most popular ones. 
def average_n_ghosts(n_items, n_counters,n_hashes,n_cache_slots): 
    return (n_items-n_cache_slots) * np.power(1- np.exp(-n_hashes*n_cache_slots/n_counters) , n_hashes)


def average_n_ghosts_ub(n_items, n_counters,n_hashes,n_cache_slots): 
    return (n_items-n_cache_slots) * np.power(n_cache_slots*n_hashes/n_counters , n_hashes)

#The following function is the final one, returns the number of counters and the number of hash functions in order to distinguish C - thres_av_n_ghosts on average. 

def config_sketch(n_items,alpha,n_cache_slots,thres_av_n_ghosts,g,n_hashes_max):
    n_hashes=2
    n_counters= config_n_counters(n_items,alpha,n_hashes,n_cache_slots,g[n_hashes-1])
    curr_av_n_ghosts= average_n_ghosts(n_items, n_counters,n_hashes,n_cache_slots)
    while  (curr_av_n_ghosts>thres_av_n_ghosts)  & (n_hashes< n_hashes_max) :
        n_hashes=n_hashes+1
        n_counters= config_n_counters(n_items,alpha,n_hashes,n_cache_slots,g[n_hashes-1])
        curr_av_n_ghosts= average_n_ghosts(n_items, n_counters,n_hashes,n_cache_slots)
        
    if n_hashes==n_hashes_max:
        n_counters_thres= n_hashes_max * n_cache_slots / np.log(1-np.power(thres_av_n_ghosts/ n_items , 1/n_hashes_max))
        n_counters= max (n_counters, n_counters_thres)
        
    return [n_counters,n_hashes]




#Returns how many popular items did we fail to dinstinguish during an experiment. 

def metric_performance(items_estimations,n_cache_slots):
    rank_est=[]
    n_items=len(items_estimations)
    for i in range(n_items):
        rank_est.append((i,items_estimations[i]))
    rank_est= sorted(rank_est, key= lambda item: item[1])
    rank_est.reverse()
    items_detected=set()
    most_popular_items=set()
    for i in range(n_cache_slots):
        items_detected.add(rank_est[i][0])
        most_popular_items.add(i)

    return n_cache_slots- len(items_detected.intersection(most_popular_items)) 




def config_cache(n_items,alpha,hit_rate):
    if alpha==1: 
        return int(np.power(n_items,hit_rate))
    if alpha<1:
        constant=constant_zipf(n_items,alpha)
        s=0
        for i in range(1,n_items+1):
            s=s+ constant * np.power(1/i, alpha)
            if s> hit_rate:
                return i     
    if alpha>1:
        return zipf.ppf(hit_rate, alpha)
            
    
    