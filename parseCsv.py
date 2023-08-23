import csv
import forgemagie

"""
parse csv file 
"""

def parse_csv_item(file_path):
    item = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # Skip the header row
        for row in reader:
            feature = {}
            if row[0] == 0 :
                break
            featureName = row[4]
            feature[featureName] = {
                'value': int(row[0]),
                'maxValue': int(row[1]),
                'weight': float(row[2]),
                'cumulatedWeight': float(row[3]),
                'natif' : True
                }
            item.append(feature)
            lvlItem = int(row[5])
    return item, lvlItem

def parse_csv_reference_rune(file_path):
    runes = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            runename = row[0]
            weight = float(row[1])
            value = float(row[2])
            featurename = row[3]
            runes[runename] = weight, value, featurename
    return runes

def search_item_feature(item, featureName) :
    itemFeature = forgemagie.Item.get_feature(item)
    for feature in itemFeature :
        feature_name = list(feature.keys())[0]
        if feature_name == featureName :
            value = feature[feature_name]['value']
            maxvalue = feature[feature_name]['maxValue']
            weight = feature[feature_name]['weight']
            cumulatedWeight = feature[feature_name]['cumulatedWeight']
            natif = feature[feature_name]['natif']
            return value, maxvalue, weight, cumulatedWeight, natif
    return None

# file_path_reference = 'RunesReference.csv' 
# referencesRunes = parse_csv_reference_rune(file_path_reference)

# file_path_item = 'Voiledencre.csv'  # Replace to argv
# itemFeature, lvlItem = parse_csv_item(file_path_item)

# item = forgemagie.Item(itemFeature, lvlItem, 0)
# print_item_features(item)