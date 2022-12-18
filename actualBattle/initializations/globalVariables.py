from BattlePrep import bag


def init():
    global protagonist
    protagonist = ""
    global everySkill
    everySkill = []
    global everyWeapon
    everyWeapon = []
    global everyArmor
    everyArmor = []
    global equippedSkills
    equippedSkills = []
    global monsterList1
    monsterList1 = []

    global allUnlocksFromJson
    allUnlocksFromJson = {}
    global allSaveData
    allSaveData = {}
    global varietyPathUnlocks
    varietyPathUnlocks = []

    global currentArmor
    global currentWeapon
    currentWeapon = ""
    currentArmor = ""
    global itemBag
    itemBag = bag.Inventory(20)
    global ourStage
    global ourNode
    ourStage = 1
    ourNode = 1
