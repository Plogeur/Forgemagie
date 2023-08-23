import forgemagie

def determineNextRune(Item, RuneReference) :
    PercentSC_SAVE = 0
    rune_SAVE = forgemagie.Rune()
    for rune in RuneReference : # test all runes to match the one that have the best % of succes 
        rune = forgemagie.Rune(rune)
        PercentSC, _, _, _ = forgemagie.CalculResultat(False, rune.featureName, rune) # Oindex : indice rune, ZIndex : indice feature
        if PercentSC > PercentSC_SAVE :
            rune_SAVE = rune
    return rune_SAVE

def testScore(Item) :
    """
    Return the value feature % of similarity compare to the maxvalue
    """
    total_percent = 0
    num_features = len(Item)

    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        if feature[feature_name]['maxValue'] != 0 : # no exo
            total_percent += (feature[feature_name]['value'] / feature[feature_name]['maxValue']) * 100

    mean_percentage = total_percent / num_features
    return mean_percentage