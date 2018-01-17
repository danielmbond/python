# Complete the function below.
import operator

def  best_hotels():
    lines = input("How many lines?")
    hotels = {}
    array = []
    for i in range(int(lines)):
        hotel = input("Enter ID space ranking:")
        id = hotel.split(" ")[0]
        print(id)
        rank = hotel.split(" ")[1]
        if id in hotels:
            count = hotels[id][1]
            hotels[id]= [int(hotels[id][0]) + int(rank), (hotels[id][1] + 1)]
        else:
            hotels[id]= [int(rank), 1]
    for i in hotels.keys():
        array.append([i,hotels[i][0]/hotels[i][1]])
    sortedArray = sorted(array, key=operator.itemgetter(1, 0), reverse=(True))
    for i in sortedArray:
        print(i[0])
best_hotels()
