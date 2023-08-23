import math 
import sys 
import random

class Rune : 
    def __init__(self, runeName='', runeValue=1, featureName='', weight=0):
        self.runeName = runeName
        self.runeValue = runeValue
        self.featureName = featureName
        self.weight = weight

    #Getter
    @classmethod
    def get_featureName(cls, rune) :
        return rune.featureName
    @classmethod
    def get_runeName(cls, rune) :
        return rune.runeName
    @classmethod   
    def get_runeValue(cls, rune) :
        return rune.runeValue
    @classmethod    
    def get_runeWeight(cls, rune) :
        return rune.weight

class Item :
    def __init__(self, features, lvlItem, well) :
        self.features = features
        self.lvlItem = lvlItem
        self.well = well

    # features :
    # feature[featureName] = {
    #                 'value': int,
    #                 'maxValue': int,
    #                 'weight': float,
    #                 'cumulatedWeight': float
    #                 'natif': bool(True)

    # Getter
    @classmethod
    def get_feature(cls, item) :
        return item.features
    @classmethod
    def get_lvlItem(cls, item) :
        return item.lvlItem
    @classmethod
    def get_well(cls, item) :
        return item.well
    @classmethod
    def getWellFromFeatureName(cls, item, NewFeatureName) :
        itemfeature = Item.get_feature(item)
        for feature in itemfeature :
            feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
            if NewFeatureName == feature[feature_name] :
                return feature[feature_name]['cumulatedWeight']
            
    # Setter
    @classmethod
    def set_well(cls, item, Well) :
        item.well = Well
    @classmethod
    def set_feature(cls, item, feature) :
        item.feature = feature
    
def print_item_features(item):
    lvlItem = Item.get_lvlItem(item)
    print(f"lvl item : {lvlItem}")
    itemFeature = Item.get_feature(item)
    for feature in itemFeature :
        feature_name = list(feature.keys())[0] 
        value = feature[feature_name]['value']
        maxvalue = feature[feature_name]['maxValue']
        print(f"{feature_name} : {value}/{maxvalue}")

def forgemagie(item, rune, well) :
    """
    Modify the item and identify if the feature will be added to the item 
    $Item[$x][1] = PWR_ACTUEL : Somme cumulatedweight of the item 
    $Item[$x][4] = Round($Rune[$Index][1] / $Rune[$Runeindex][2], 2) = cumulatedweight for 1
	$Item[$x][5] = jet_max * PWR pour 1 : cumulatedweight max
    """
    _, _, _, Random = CalculResultat(item, rune)

    if Random == 1 :
        if Rune.get_featureName(rune) not in [list(feature.keys())[0] for feature in item] : # exo 
            CreateExotique(item, rune)
        else :
            Gain()
    elif Random == 2 :
        Gain()
        Perte()
    elif Random == 3 :
        Perte()
    else :
        print("error in random output")
        sys.exit(1)

    Fusion = Fusion + 1
    PWRitem = getPWRitem(item)

def CreateExotique(Item, rune) :
    """
    Add new feature by creating an exo on the item
    """
    feature = {}
    feature[Rune.get_featureName(rune)] = {
                'value': int(Rune.get_runeValue(rune)),
                'maxValue': int(math.floor(100/int(Rune.get_runeWeight(rune)))),
                'weight': float(Rune.get_runeWeight(rune)),
                'cumulatedWeight': float(Rune.get_runeWeight(rune)),
                'natif': False
                }
    Item.append(feature)

def RecalculPWRfeature(Item, listModifyFeature) :
    """
    Modify the cumulatedWeight for the item when a feature is modify
    """
    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        for modifyFeature in listModifyFeature :
            if modifyFeature == feature_name :
                feature[feature_name]['cumulatedWeight'] = feature[feature_name]['weight'] * feature[feature_name]['value']

def getPWRitem(Item) :
    """
    Return the cumulated weight for all feature in the item
    """
    PWRitem = 0
    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        PWRitem += feature[feature_name]['cumulatedWeight']
    return PWRitem

def DeleteExotique(Item) : # Supprime la ligne du Jet Exotique  
    for feature in range(0, len(Item, 2) - 1) :
        Item[len(Item) - 1][feature] = 0

def CheckExotique(Item, rune) -> bool :
    """
    True si Exotique Déjà présent ou si la rune créerait un exo
    """
    overExo = True
    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        feature_rune = Rune.get_featureName(rune)
        if feature[feature_name]['natif'] == False : # exo already present
            return True
        if feature_rune == feature[feature_name] : # feature native 
            return False
    return overExo # New feature (exo)

def CheckOvermax(Item, rune) -> bool :
    """
    True si Overmax Déjà présent ou si la rune créer un overmax
    """
    Overmax = False
    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        feature_rune = Rune.get_featureName(rune)
        if feature_rune == feature[feature_name] :
            if feature[feature_name]['value'] + Rune.get_runeValue(rune) > feature[feature_name]['maxvalue'] : # overmax
                return True
    return Overmax

def GetPWRGoveretExo(Item) :
    """
    Return the PWRG Exotique + PWRG Overmax
    """
    PWRGover = 0
    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        if feature[feature_name]['value'] > feature[feature_name]['maxvalue'] :
            PWRGover += feature[feature_name]['cumulatedWeight']
        if feature[feature_name]['natif'] == False :
            PWRGover += feature[feature_name]['cumulatedWeight']
            return PWRGover

    for x in range(1, len(Item) - 1) : #Calcul Du PWRG des Jets en Overmax
        if int(Item[x][0]) > int(Item[x][3]) :
            PWRGover = PWRGover + ((int(Item[x][0]) - int(Item[x][3])) * int(Item[x][4]))
	
    return PWRGover + (int(Item[len(Item) - 1][0]) * int(Item[len(Item) - 1][4])) # On ajoute le PWR de l'exo car il n'est pas considéré comme over

def Gain(Item, rune) :
    """
    Update the actual jet
    """
    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        feature_rune = Rune.get_featureName(rune)
        if feature_rune == feature[feature_name] :
            feature[feature_name]['value'] = feature[feature_name]['value'] + Rune.get_runeValue(rune)
            feature[feature_name]['cumulatedWeight'] = feature[feature_name]['cumulatedWeight'] + Rune.get_runeValue(rune)*feature[feature_name]['weight']
    return

def Perte(item, rune) :
    """
    Modify the item by removing one or more features in it
    """
    PwrPerte = Rune.get_runeWeight(rune) # calcul the weight to loose
    Well = Item.get_well(item)

    if Well >= PwrPerte and Well > 0 : # Si le puit est supérieur à la perte et s'il y a du Well
        Well = Well - PwrPerte # Le Well diminue
        Item.set_well(item, Well)
        return
    else :
        #PwrPerteOrigin = PwrPerte
        PwrPerte = PwrPerte - Well # La perte diminue si le Well ne vaut pas 0    
        Item.set_well(item, 0) # Well = 0

    if PwrPerte > GetPWRGactuel(True) :
        PwrPerte = 0

    while PwrPerte > 0 :
        JetDown = ChercherLeJetQuiBaisse() # Recherche du jet qui baisse
        PwrActual = Item.getWellFromFeatureName(item)
        Y = math.floor(PwrPerte / PwrActual) # Le jet peut baisser de
        if Y - int(Item[JetDown][0]) > 0 : # Si la perte est supérieur au jet actuel
            Y = int(Item[JetDown][0]) # Le perte devient le jet actuel
		
        if Y < 1 : # Debug Ex: 1/20 = 0 = 1
            Y = 1
        
        Perte = random(0, Y, 1)
        if Perte != 0 : # s'il la perte n'est pas nulle
            Item[JetDown][0] = int(Item[JetDown][0]) - Perte # mise à jour du jetactuel
            PwrPerte = PwrPerte - math.ceil(Perte * int(Item[JetDown][4]))

            if PwrPerte < 0 : # si perte trop importante , création du Well
                Well = Well - PwrPerte
                Item.set_well(item, Well)

    if Item[len(Item) - 1][0] == 0 :
        DeleteExotique()

def CalculResultat(Item, rune, lvlItem, GetPWRGactuel, GetPWRGmax) :
    OverMax = CheckOvermax(Item, rune)
    Exotique = CheckExotique(Item, rune)

    if Exotique : 
        EtatPWR = 2
    else :
        EtatPWR = (int(Item[IndexJet][0]) + Rune[IndexJet][2] - int(Item[IndexJet][2])) / (int(Item[IndexJet][3]) - int(Item[IndexJet][2])) # Calcul PWR du jet

    EtatPWRG = (GetPWRGactuel(True) / (GetPWRGmax() - Item[IndexJet][5])) # Calcul PWRG moins le PWR du jet en cours de modification
    InfluencePWRG = 30
    if Item[IndexJet][3] == 1 : # Le Calcul du PWR ne compte pas pour les objets dont le jet max est 1 (PA,PO,PM,etc...)
        InfluencePWR = 0
    else :
        InfluencePWR = 20

    i = EtatPWR * 100
    FI1 = (-0.5) * ((abs(i - 50) - (i - 50)) / (i - 50))
    FS1 = (0.5) * ((abs(i - 50) - (i - 50)) / (i - 50)) + 1
    G1 = (-(0 / 50) * (i - 50)) + 66
    H1 = (-(50 / 50) * (i - 50)) + 66
    tmp = (FI1 * G1) + (FS1 * H1)

    j = EtatPWRG * 100
    FI2 = (-0.5) * ((abs(j - 80) - (j - 80)) / (j - 80))
    FS2 = (0.5) * ((abs(j - 80) - (j - 80)) / (j - 80)) + 1
    G2 = (-(23 / 80) * (j - 80)) + 43
    H2 = (-(108 / 80) * (j - 80)) + 43
    TMP2 = (FI2 * G2) + (FS2 * H2)

    Moy = ((3 * TMP2) + (2 * tmp)) / 5
    Moy2 = math.sqrt(((3 * tmp / 5) * (3 * tmp / 5)) + ((2 * TMP2 / 5) * (2 * TMP2 / 5)))

    if EtatPWR * 100 < 1  :
        EtatPWR = 0

    if EtatPWRG * 100 < 1 :
        EtatPWRG = 0

    if Exotique or OverMax : 
        CoefOvermax = (1 - ((GetPWRGoveretExo() + int(Rune[IndexRune][1])) / 100)) / 2
        PercentSN = math.floor(50 - (16 * (EtatPWR + EtatPWRG) / 2))
  
    elif EtatPWR * 100 > 80 and GetPWRGactuel(True) > 50 :
        CoefOvermax = 1 * ((EtatPWR + EtatPWRG) / 2)
        PercentSN = math.floor(50 - (8 * (EtatPWR + EtatPWRG) / 2))

    elif EtatPWRG * 100 > 50 :
        CoefOvermax = 1 * EtatPWRG
        PercentSN = 50

    elif EtatPWR * 100 > 80 :
        CoefOvermax = 1 * EtatPWR
        PercentSN = 50

    else :
        CoefOvermax = 1
        PercentSN = 50

    CoefRune = 1 - (Rune[IndexRune][1] / 200)
    CoefLvl = 1 - ((lvlItem / 200) / 6)

    PercentSC =  math.ceil(80 - ((InfluencePWR * EtatPWR) + (InfluencePWRG * EtatPWRG)))
    PercentSC =  math.floor(PercentSC * CoefLvl * CoefRune * CoefOvermax)

    if not Exotique and not OverMax and PercentSC < 15 :
        PercentSN = PercentSN - (15 - PercentSC)
        PercentSC = 15

    PercentEC = 100 - (PercentSC + PercentSN)
    if not Exotique and not OverMax and PercentEC > 35 :
        PercentSN = PercentSN - (PercentEC - 35)
        PercentEC = 35

    if Exotique and Rune[IndexRune][1] > 50 :
        PercentEC = 99
        PercentSC = 1
        PercentSN = 0

    if GetPWRGoveretExo() + Rune[IndexRune][1] > 100 :
        PercentEC = 100
        PercentSC = 0
        PercentSN = 0

    if int(Item[IndexJet][0]) + int(Rune[IndexRune][2]) > int(Item[IndexJet][3]) :
        if int(Item[IndexJet][0]) + int(Rune[IndexRune][2]) > (100 - int(Item[IndexJet][3]) * int(Item[IndexJet][4])) / (int(Item[IndexJet][4] * 2)) + int(Item[IndexJet][3]) :
            PercentEC = 100
            PercentSC = 0
            PercentSN = 0
    if PercentSN < 0  :
        PercentEC = 0
        PercentSC = 0
        PercentSN = 0

    if SelectionResutat :
        Random = SelectionResultat()

    return PercentSC, PercentSN, PercentEC, Random

def SelectionResultat(PercentSC, PercentSN) :
    """
    Return the current type of success for the rune 
    """
    tmp = Random(1, 100, 1)
    Random = 0
    if tmp <= PercentSC :
        Random = 1
    elif tmp <= (PercentSN + PercentSC) :
        if tmp > PercentSC :
            Random = 2
        else :
            Random = 1
    else : 
        Random = 3
    return Random

def GetPWRGactuel(Item, rune) -> str :
    """
    Return the actual feature weight of the item 
    """
    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        feature_rune = Rune.get_featureName(rune)
        if feature_name == feature_rune :
            return feature_name[feature]['cumulatedWeight']

def ChercherLeJetQuiBaisse(Item, rune, Random, PwrPerteOrigin) -> str :
    """
    Return the feature name on the down feature 
    """
    # actuelJet = 
    # if actuelJet != 0 and Random == 3: # full loose 
    #     return Nom_du_jet_item
    
    # if actuelJet != 0 and Nom_du_jet_rune != Nom_du_jet_item :
    #     return Nom_du_jet_item

    for feature in Item :
        feature_name = list(feature.keys())[0]  # Get the featureName from the dictionary key
        if feature[feature_name]['value'] > feature[feature_name]['maxvalue']:
            return feature[feature_name]
    
    listFeature = [list(feature.keys())[0] for feature in Item]
    #print(listFeature)
    while True :
        RdmJet = Random(1, len(Item), 1) # un jet choisit aléatoirement.
        if Item[listFeature[RdmJet]['value']] == 0 or Item[listFeature[RdmJet]] == Rune.get_featureName(rune) : 
        # if jet value == 0 or rune value == rdmjet : continue
            continue
        if Item[listFeature[RdmJet]['cumulatedWeight']] >= PwrPerteOrigin :
            Epargne = Random(1, 100, 1)
        if Epargne <= (PwrPerteOrigin / Item[listFeature[RdmJet]['cumulatedWeight']]) * 100 :
            return RdmJet
        return RdmJet