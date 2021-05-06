import matplotlib.pyplot as plt                                                       
import numpy as np
import mmh3
import random 
import matplotlib
import string    
from scipy.stats import binom
from random import choices







#This class represents a Counting Bloom Filter that uses the conservative update operation 
class C_CBF(object):
 
 
    def __init__(self, n_hashes,n_counters):
       
        # Number of counters
        self.n_counters=n_counters
 
        # number of hash functions 
        self.n_hashes=n_hashes
 
        # array of counters 
        self.bins=[0]*n_counters
         
                
    def add(self, item):
        number_increments=0
        minimum= self.estimate(item)
        for f in range(self.n_hashes):
            c = mmh3.hash(str(item), f) % self.n_counters
            val = self.bins[c]
            if val==minimum:
                self.bins[c]=val+1
                number_increments=number_increments+1
        return number_increments
         

    def estimate(self, item):
        c=mmh3.hash(str(item), 0) % self.n_counters
        minimum= self.bins[c] 
        for f in range(1,self.n_hashes):
            c = mmh3.hash(str(item), f) % self.n_counters
            minimum = min(minimum, self.bins[c]) 
        return minimum
    
    def show_Bloom(self):
        print(self.bins)
        

        
# Constant for a Zipf distribution p_i = constant_zipf(N,alpha)/i^{alpha} . 
def constant_zipf(n_items,alpha):  
    s=0
    for i in range(n_items):
        s=s+(1/(i+1)**alpha)
    return 1/s

        
        
#The following function generates a sample drawn from a zipf distribution
def sample_zipf(n_items,alpha,n_requests):      
    weights=[]
    constant= constant_zipf(n_items,alpha)
    population=[]
    for i in range(1,n_items+1):
        p_i= constant/(i**alpha)
        population.append(i) # items 
        weights.append(p_i)   # Probability items 
    
    
    return choices(population,weights,k=n_requests)       




#Simulate a process of requests from a zipf distribution then returns the estimations of all the items 

def generate_estimation_items(n_requests,n_items,n_counters,n_hashes,alpha):
    sketch= C_CBF(n_hashes,n_counters)
    sample= sample_zipf(n_items,alpha,n_requests)
    
    items_count=[0]*n_items
    
    url_item=[""]*n_items
    for i in range(n_items):
        url_i = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))  
        url_item[i]=url_i
   
    for i in range(n_requests):
        item=sample[i]
        sketch.add(url_item[item-1])
        items_count[item-1]=items_count[item-1]+1
    
    items_estimations=[0]*n_items
    for i in range(n_items):
        items_estimations[i]=sketch.estimate(url_item[i])
        
    return [items_estimations,items_count,sketch.bins]
    
    


        