from scipy.spatial import distance
allFeaturesList = [] #column by column

#store the data by columns
def addAllFeatures(data):
    col = len(data[0])
    x = 0
    tempList = []

    while (x < col):
        for i in range(len(data)):
            if (x < col):
                tempList.append(data[i][x])
        x += 1
        allFeaturesList.append(tempList)
        tempList = []

#read information from file       
def readData(fileName):
    #open file
    file = open(fileName, "r")
    temp = file.readlines()
    temp1 = []
    for line in temp:
        temp1.append(line.split())
    return temp1

#check if feature wanted to add is already in the set    
def intersect(dataSet, k):
    for i in dataSet:
        if (i == k):
            return True
    return False

#get feature values
def getX(column_feature, index):
    list1 = []
    
    for i in column_feature:
        list1.append(float(i[index]))
    return list1 

#compute accuracy of a set of features
def leave_one_out_cross_validation(data, current_features, k):
    #k is the column which is the feature
    colFeature = [] #stores actual features
    tempDst = 0 #distance of each comparison
    indexI = 0 #store the first nearest neighbor index
    indexJ = 0 #store the second nearest neighbor index
    features_classification = [] #put 1s and 0s in a list to check accuracy
    sum1 = 0 #total number of 1s
    
    if current_features:
        for i in current_features:
            colFeature.append(allFeaturesList[i])
    
    if k > 0:
        colFeature.append(allFeaturesList[k])
    
    for i in range(len(data)):
        tempArr = []
        tempArr = getX(colFeature, i)
        shortestDst = 10000
        for j in range(len(data)):
            if not (i == j):
                tempArr2 = []
                tempArr2 = getX(colFeature, j)
                tempDst = distance.euclidean(tempArr, tempArr2)
                if (tempDst < shortestDst):
                    shortestDst = tempDst
                    indexI = i
                    indexJ = j
        
        if(data[indexI][0] == data[indexJ][0]):
            features_classification.append(1)
        else:
            features_classification.append(0)
    
    for i in features_classification:
        if(i == 1):
            sum1 += 1

    return sum1 / float(len(data)) * 100

def forwardSelection(dataSet):
    best_accuracy = 0 #best accuracy overall
    current_set_of_features = []
    best_feature_index = 0
    curr_best_feature = [] #set of feature with the best accuracy overall
    
    for i in range(1, len(data[0])):
        print("On the " + str(i) + "th level of the search tree")
        feature_to_add_at_this_level = i
        best_so_far_accuracy = 0 #best accuracy at the level
        
        for j in range(1, len(data[0])):
            if not intersect(current_set_of_features, j):
                accuracy = leave_one_out_cross_validation(dataSet, current_set_of_features, j)
                if not current_set_of_features:
                    print("using feature(s) {" + str(j) + "} accuracy is " + str(accuracy) + "%")
                else:
                    print("Using feature(s) {" + str(j) + ", " + "".join(str(current_set_of_features)) + "} accuracy is " + str(accuracy) + "%")
                
                if (accuracy > best_so_far_accuracy):
                    best_so_far_accuracy = accuracy
                    feature_to_add_at_this_level = j
                    best_feature_index = j
        if (best_so_far_accuracy > best_accuracy):
            best_accuracy = best_so_far_accuracy
            curr_best_feature.append(best_feature_index)
        else:
            print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
            
        if (feature_to_add_at_this_level > 0):
            current_set_of_features.append(feature_to_add_at_this_level)
            print ("Feature set {" + "".join(str(current_set_of_features)) + "} was best, accuracy is " + str(best_so_far_accuracy) + "% \n")
    
    print("Best Feature set {" + "".join(str(curr_best_feature)) + "}, accuracy is " + str(best_accuracy) + "% \n")    
        
print("Welcome to Adrian Li's Feature Selection Algorithm")
filename = raw_input("Type in the name of the file to test: ")
print("\n")
data = readData(filename)

addAllFeatures(data)

#stores feature numbers [1,2,3,4,5,6,7,8,9,10]
allFeatures = []
for i in range(1, len(data[0])):
    allFeatures.append(i)

print("Type the number of the algorithm you want to run.")
print("\t 1) Forward Selection")
print("\t 2) Backward Elimination")
print("\t 3) Adrian's Special Algorithm")
option = input()

print ("This data has " + str(len(data[0]) - 1) + " features (not including the class attribute), with " + str(len(data)) + " instances.")
print ("\n")
print ("Running nearest neighbor with all " + str(len(data[0]) - 1) + " features, using \"leave_one_out\" evaluation, I get an accuracy of " + str(leave_one_out_cross_validation(data, allFeatures, -1)) + "% \n")


if (option == 1):
    forwardSelection(data)
elif (option == 2):
    print("backward elimination")
elif (option == 3):
    print("Adrian's Special Algorithm")
else:
    print("Wrong option")
    
