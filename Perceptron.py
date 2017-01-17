from math import sqrt,exp
from numpy import empty,ones, zeros, array, shape, copy
from random import random,randrange, seed
from visual import sphere,curve,display, rate, color
from pylab import plot, xlabel, ylabel, title,show


##calculate J[i,j] for the array, a, and output a N**2 x N**2 array
##a is an array of any number of patterns
def J(a):
    
    M = len(a.shape)
    #for dealing with arrays of patterns
    if M >2:
        print "more"
        N = len(a[0])
        ret = zeros((N**2, N**2))
        #create a copy and change the shape for looping through
        for k in range(a.shape[0]):
            b = copy(a[k])
            b.shape = (N**2,)
            #loop through twice to make an N**2 x N**2 array
            #a.shape[0] gives how many patterns are stored
            for i in range(N**2):
                for j in range(N**2):
                    ret[i,j] += (1./a.shape[0])*b[i]*b[j]
   #deal with just one pattern                 
    else:
        N = len(a)
        b = copy(a)
        b.shape = (N**2,)
        ret = zeros((N**2, N**2))
        for i in range(N**2):
            for j in range(N**2):
                ret[i,j] += (1/float(M-1))*b[i]*b[j]

    return ret
#assume inputs are same size as patterns
#takes input array of arrays, a, and output pattern b, and calculates the J for them
def Jtron(a,b):
    
    M = len(a.shape)
    #for dealing with arrays of patterns
    if M >2:
        print "more"
        N = len(a[0])
        ret = zeros((N**2, N**2))
        #create a copy and change the shape for looping through
        for k in range(a.shape[0]):
            b = copy(a[k])
            b.shape = (N**2,)
            #loop through twice to make an N**2 x N**2 array
            #a.shape[0] gives how many patterns are stored
            for i in range(N**2):
                for j in range(N**2):
                    ret[i,j] += (1./a.shape[0])*b[i]*b[j]
   #deal with just one pattern                 
    else:
        N = len(a)
        b = copy(a)
        b.shape = (N**2,)
        ret = zeros((N**2, N**2))
        for i in range(N**2):
            for j in range(N**2):
                ret[i,j] += (1/float(M-1))*b[i]*b[j]

    return ret
#Calculate energy, given an input a
def Etron(a, p):
    b = copy(a)
    N = len(a)
    b.shape = (N**2,) #help with indexing so we dont have to loop over 2d arrays
    Jp = Jtron(p)
    E = 0
    for i in range(N**2):
        for j in range(N**2):
            E += Jp[i,j]*b[i]*b[j]

    return -E

#calculate energy of a given pattern, a, using the stored patterns, p
def E(a, p):
    b = copy(a)
    N = len(a)
    b.shape = (N**2,) #help with indexing so we dont have to loop over 2d arrays
    Jp = J(p)
    E = 0
    for i in range(N**2):
        for j in range(N**2):
            E += Jp[i,j]*b[i]*b[j]

    return -E
    



# Initialize first shape to be stored(A)
N = 10
p1 = -ones((N, N))# Initialize as ones, pattern 1
p1[4:6,0 ] = 1
p1[3:8,1 ] = 1
p1[3:5,2 ] = 1
p1[6:8,2 ] = 1
p1[2:4,3 ] = 1
p1[7:9,3 ] = 1
p1[1:9,4 ] = 1
p1[:,5] = 1
p1[0:3,6 ] = 1
p1[7:10,6 ] = 1
p1[0:2,7:10 ] = 1
p1[8:10,7:10 ] = 1

#initializing second shape(C)
p2= -ones((N,N))
p2[1:10,0:2] = 1
p2[0:4,2 ] = 1
p2[0:3,3:7] = 1
p2[0:4,7] = 1
p2[1:10,8:10] = 1
#initializing third shape (B)

#copy to flip a percentage of the spins
p1_flip = copy(p1)
p2_flip = copy(p2)
#memory, where all patterns are stored
P = array([p1, p2])

    
i= 0
while i<20:
    r1 = randrange(10)
    r2 = randrange(10)
    p2_flip[r1,r2] = -p2_flip[r1,r2]
    i +=1

#sets up visual animation
for i in range(N):
    for j in range(N):
        if p2_flip[i,j] == 1:
            sphere(pos=[i-N/2,j-N/2], color=color.red)
        else:
            sphere(pos=[i-N/2,j-N/2], color=color.green)

            

choice = 1

#########################################################################
#Using just change in energy to accept flips
############################################################################
if choice == 1:
    dE = -1
    output = copy(p2_flip)
    E_out = Etron(p2_flip, P)   

    k = 0
    c = 0
    while  k< 10:
        c = 0
        #for each neuron, flip, see if its allowed, flip back if not
        for i in range(N):
            for j in range(N):
                output[i,j] = -output[i,j]
                E_new = E(output,P)
                dE = E_new - E_out
                
                #accept the flip, set new energy
                if dE <0:
                    E1 = E_new
                #reject the flip, switch back 
                if dE >=0:
                    c+=1
                    p2_flip[i,j] = -p2_flip[i,j]
               
                #update the animation
                if output[i,j] == 1:
                    sphere(pos=[i-N/2,j-N/2], color=color.red)
                   
                else:
                    sphere(pos=[i-N/2,j-N/2], color=color.green) 
        k+=1
        #break if no more changes
        if c==100:
            break

            
       
    










