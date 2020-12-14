import csv

def get_objects():
    objects = []

    with open('objects.csv') as csvfile:
        rd = csv.reader(csvfile)
        for row in rd:
            objects.append([int(i) for i in row])
    
    return objects