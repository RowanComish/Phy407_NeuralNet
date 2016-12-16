from math import sqrt,exp
from numpy import empty,ones, zeros, array, shape, copy
from random import random,randrange, seed
from visual import sphere,curve,display, rate, color
from pylab import plot, xlabel, ylabel, title,show


##calculate J for the array and output a N**2 x N**2 array
##a is an array containing all stored patterns
def J(a):
    
    M = len(a.shape)
    #for dealing with arrays of patterns
    if M >2:
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

#Calculate energy, given a spin orientation array(a), using the patterns stored
#in p
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
p3 = -ones((N,N))
p3[1:, 8:10] = 1
p3[1:2, 1:] = 1
p3[8:10, 1:] = 1
p3[1:, 5] = 1
p3[1:, 0:2] = 1
p3[9,5] = -1
#initializing fourth shape(D)
p4 = -ones((N,N))
p4[0:2, :] = 1
p4[:9, 0:2] = 1
p4[:9, 8:10] = 1
p4[8:10, 2:8]= 1
#initializing fifht shape(E)
p5 = -ones((N,N))
p5[0:2, :] = 1
p5[:, 0:2]=1
p5[:, 4:6]=1
p5[:, 8:10] = 1
    
#copy to flip a percentage of the spins
p1_flip = copy(p1)
p2_flip = copy(p2)
p3_flip = copy(p3)
P5 = array([p2, p3, p1, p4, p5])
P4 = array([p1,p2,p3,p4])
P3 = array([p1,p2,p3])
P2 = array([p1,p3])
P1 = array([p3])

i= 0




#CHoose which way to use the neural network
choice = 1


#########################################################################
#Using just change in energy to accept flips
##########################################################################

if choice == 1:
    ###CHOOSE THE Pn(number of patterns) P1,P2,P3,P4,P5
##    P5 = array([p2, p3, p1, p4, p5])
##    P4 = array([p1,p2,p3,p4])
##    P3 = array([p1,p2,p3])
##    P2 = array([p1,p3])
##    P1 = array([p3])
    P = P3
    ###CHOOSE THE PATTERN TO FLIP p1(A upside down),p2(C),p3(B),p4(D),p5(E)
    ###MAKE SURE IT IS IN THE Pn CHOSEN ABOVE
    p_flip = copy(p1)


    
    #flip some of the neurons in one of the patterns
    #increase the number of flips can cause issues for multiple patterns
    seed(17)
    while i<50:
        r1 = randrange(10)
        r2 = randrange(10)
        p_flip[r1,r2] = -p_flip[r1,r2]
        i +=1
    #sets up visual animation
    for i in range(N):
        for j in range(N):
            if p_flip[i,j] == 1:
                sphere(pos=[i-N/2,j-N/2], color=color.red)
            else:
                sphere(pos=[i-N/2,j-N/2], color=color.green)

    dE = -1
    E1 = E(p_flip, P)
    k = 0
    c =0
    while  k < 10:
        
        for i in range(N):
            for j in range(N):
                p_flip[i,j] = -p_flip[i,j]
                E_new = E(p_flip,P)
                dE = E_new - E1
                
                #accept the flip, set new energy
                if dE <0:
                    E1 = E_new
                #reject the flip, switch back 
                if dE >=0:
                    c+=1
                    p_flip[i,j] = -p_flip[i,j]
                  
                #update the animation
                if p_flip[i,j] == 1:
                    sphere(pos=[i-N/2,j-N/2], color=color.red)
                   
                else:
                    sphere(pos=[i-N/2,j-N/2], color=color.green)     
        k += 1
        if c==100:
            break
    

#################################################################
#Using temperature
################################################################



elif choice == 2:
    ###CHOOSE THE Pn(number of patterns) P1,P2,P3,P4,P5
    P = P1
    ###CHOOSE THE PATTERN TO FLIP p1(A upside down),p2(C),p3(B),p4(D),p5(E)
    p_flip = copy(p3)

    #flip some of the neurons in one of the patterns(this case its p3)
    #increase the number of flips can cause issues for multiple patterns

    i= 0
    seed(17)
    #changing the value the loop stops at can make the flipped array tend
    #to different places
    while i<50:
        r1 = randrange(10)
        r2 = randrange(10)
        p_flip[r1,r2] = -p_flip[r1,r2]
        i +=1

    #sets up visual animation
    for i in range(N):
        for j in range(N):
            if p_flip[i,j] == 1:
                sphere(pos=[i-N/2,j-N/2], color=color.red)
            else:
                sphere(pos=[i-N/2,j-N/2], color=color.green)

    
    E1 = E(p_flip, P)
    T_min = 1.
    t = 0
    Tmax =15.
    T= Tmax
    tau = 1e2
    while T> T_min:
        
        for i in range(N):
            if T<=T_min: #need this because we only update over each pass through of
                        #of the network, so we could go below T_min
                break
            for j in range(N):
                if T<=T_min:
                    break
                
                T = Tmax*exp(-t/tau)
                old_E1 = E1            
                p_flip[i,j] = -p_flip[i,j]
                E1 = E(p_flip,P)
                dE = E1 - old_E1
                
                if dE >0:
                    #check if it is rejected, otherwise the move is accepted
                    if random() > exp(-dE/T):
                        #print "rejected"
                        p_flip[i,j] = -p_flip[i,j]
                        E1 = old_E1

                        
                  
                    #update the animation
                if p_flip[i,j] == 1:
                    sphere(pos=[i-N/2,j-N/2], color=color.red)
                else:
                    sphere(pos=[i-N/2,j-N/2], color=color.green)     
        #increase t after each pass through, so each neuron has an equal
        #chance to flip, did this because this is a systematic pass through
        t+=100                   
          




