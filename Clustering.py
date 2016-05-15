import random as rand
import matplotlib.pyplot as plt
import sys
#These two constants are used to specify coordinate
#sizes for the genFile() function.
MAX_COORD_SIZE = 1000
MIN_COORD_SIZE = 0

def main():
#Uncomment the two lines below to quickly generate a list of coordinates
#    genFile("file.txt",1000)
#    return
    data = loadFile(sys.argv[2])
    clusters = []
    colors = []

    #Stores the number of clusters as specified from the command line
    NUM_OF_CLUSTERS = int(sys.argv[1])

    #Randomly pick coordinates for the number of clusters
    for i in range(NUM_OF_CLUSTERS):
        randCoord = data[rand.randint(0,len(data)-1)]

        #Prevent adding two clusters at the same coordinate
        while [randCoord] in clusters:
            randCoord = data[rand.randint(0,len(data)-1)]            

        clusters.append([randCoord])

        #I don't know what the max clusters are, so I randomly generate the
        #colors for each cluster to make sure each has a unique color
        if i % 2 == 0:
            colors.append([rand.random(),0.5,rand.random()])
        elif i % 3 == 0:
            colors.append([rand.random(),rand.random(),0.5])
        else:
            colors.append([0.5,rand.random(),rand.random()])

    #First classification. Finds all nearest to the original coordinate.
    means = classifyData(data,clusters)
    iteration = 1
    print("Classification cycle 1 complete")
    run = True

    #Keep adjusting the mean coordinate value and clusters until the mean
    #repeats, indicating it is finished clustering.
    while run:
        newMeans = classifyData(data,clusters)
        iteration += 1
        print("Classification cycle",iteration,"complete")
        if means == newMeans:
            run = False
        else:
            means = newMeans

    #Build the graph
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    for i in range(0,len(clusters)):

        #Adds coordinates and their cluster's color
        x,y = zip(*clusters[i])
        title = "C"+str(i+1)
        ax.scatter(x,y,color=colors[i],label=title)

        #Adds a star to represent the final mean coordinate in the cluster
        mean = getMean(clusters[i])
        meanClass = ax.scatter(mean[0],mean[1],
                               marker="*",s=150,
                               color=colors[i],label=title+" Mean Value")

    #The legend for some reason would keep breaking when I used show();
    #therefore I opted to just save it as an image.
    handles, labels = ax.get_legend_handles_labels()
    leg = ax.legend(handles,labels, loc=2, bbox_to_anchor=(1,1))
    fig.savefig('Clusters', bbox_extra_artists=(leg,), bbox_inches='tight')
    print("Finished! Image written to Clusters.png")

#classifyData - Classifies a set of data coordinates with a set of clusters
#Returns the mean coordinates of each cluster once every new coordinate has
#been added
def classifyData(data,clusters):
    for coord in data:
        classifyCoord(coord,clusters)
    means = []
    for cluster in clusters:
        means.append(getMean(cluster))
    return means

#classifyCoord - Adds one coord to a certain cluster based on which has
#the closest mean value
def classifyCoord(coord,clusters):
    bestDistance = getDistance(getMean(clusters[0]),coord)
    bestCluster = 0
    #Find the nearest cluster
    for i in range(0,len(clusters)):
        clusterDistance = getDistance(getMean(clusters[i]),coord)
        if clusterDistance < bestDistance:

            bestDistance = clusterDistance
            bestCluster = i
    #Remove the coordinate from any previous cluster it may have already been
    #a part of.
    for cluster in clusters:
        if coord in cluster:
            cluster.remove(coord)
    
    clusters[bestCluster].append(coord)

#getMean - Finds the mean coordinate value of a cluster
#Returns the coordinate as a tuple in the form of (x,y)
def getMean(cluster):
    totalx = 0
    totaly = 0
    for coord in cluster:
        totalx += coord[0]
        totaly += coord[1]
    totalx /= len(cluster)
    totaly /= len(cluster)
    return (totalx,totaly)    

#getDistance - Returns the total distance between two coordinates.
def getDistance(coord1,coord2):
    xDist = abs(coord1[0]-coord2[0])
    yDist = abs(coord1[1]-coord2[1])
    return xDist+yDist

#genFile - Generates a file containing coordinates for testing.
def genFile(filename,num_of_coords):
    myFile = open(filename,"a")
    for i in range(num_of_coords*2):
        myFile.write(str(rand.randint(MIN_COORD_SIZE,MAX_COORD_SIZE)))
        if i % 2 == 0:
            myFile.write(" ")
        else:
            myFile.write("\n")
    myFile.close()

#Loads a file containing coordinates into a list of tuples [(x0,y0),...,(xn,yn)]
def loadFile(filename):
    data = []
    myFile = open(filename,"r")
    lines = myFile.readlines()
    for line in lines:
        coords = line.strip().split(" ")
        x = int(coords[0])
        y = int(coords[1])
        data.append((x,y))
    myFile.close()
    return data

main()
