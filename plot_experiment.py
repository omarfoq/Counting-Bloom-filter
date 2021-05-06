import matplotlib.pyplot as plt                                                       
import numpy as np
import mmh3
import random 
import matplotlib
import string    
from scipy.stats import binom
from random import choices

from Sample import *

while(True):

    print("Please enter the number of items") 
    n_items= int(input())


    print("Please enter the Zipf parameter") 
    alpha= float(input())


    print("Please enter the number of counters") 
    n_counters= int(input())


    print("Please enter the number of hash functions") 
    n_hashes= int(input())

    print("Please enter the number of requests") 
    n_requests= int(input())



    l=generate_estimation_items(n_requests,n_items,n_counters,n_hashes,alpha)
    items_est=l[0]
    items_count=l[1]
    sketch_bins=l[2]
    
    sketch_bins.sort()
    sketch_bins.reverse()
    
    items_rank=[0]*n_items
    for i in range(n_items):
        items_rank[i]=i+1
    
    bins_index=[0]*n_counters
    for i in range(n_counters):
        bins_index[i]=i+1
        
        
    plot1 =plt.figure(1)
    plt.scatter(items_rank,items_est,label='Estimation')
    plt.scatter(items_rank,items_count,label='Frequency')
    
    plt.xlabel("Item's rank ",fontsize=24)
    plt.ylabel("Count",fontsize=24)
    
    plt.legend(fontsize=24)
    
    
    plot2= plt.figure(2)
    
    plt.scatter(bins_index,sketch_bins)
    
    plt.xlabel("Bin's index ",fontsize=24)
    plt.ylabel("Bin's value",fontsize=24)
    
   


    plt.show()





