import parseCsv
import forgemagie
import botForgemagie

file_path_reference = 'RunesReference.csv' 
referencesRunes = parseCsv.parse_csv_reference_rune(file_path_reference)

file_path_item = 'Voiledencre.csv'  # Replace to argv
itemFeature, lvlItem = parseCsv.parse_csv_item(file_path_item)

item = forgemagie.Item(itemFeature, lvlItem, 0)

print(f"################## BEFORE FORGEMAGIE ##################")
print(f"Current item feature : ")
forgemagie.print_item_features(item)
print(f"")

score = 95 # % of match between current item feature and perfect item feature 
CurrentScore = botForgemagie.testScore(forgemagie.get_feature(item))
numberRuneTested = 0
while CurrentScore >= score : #While the actual item feature didn't reash at least 95% of the perfect item feature continue 
    rune = botForgemagie.determineNextRune(item, referencesRunes)
    itemFeature = forgemagie.get_feature(item)
    lvlItem = forgemagie.get_lvlItem(item)
    well = forgemagie.get_well(item)
    item = forgemagie.forgemagie(itemFeature, lvlItem, well)
    CurrentScore = botForgemagie.testScore(forgemagie.get_feature(item))
    numberRuneTested += 1

print(f"################## AFTER FORGEMAGIE ##################")
print(f"Current item feature : ")
parseCsv.print_item_features(item)
print(f"Number of runes used to the bot : {numberRuneTested}")