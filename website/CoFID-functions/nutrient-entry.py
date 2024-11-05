def NutrientEntry(key):
    """
    (Old implementation) Checks key is for a nutrient with RDA information
    """
    # missing_entries = ["water", "choline", "chromium", "fluoride", "molybdenum"]
    if key in ["name", "_sa_instance_state", "age", "category", "sex", "id"] or "_percent" in key:
        return False
    # elif key in missing_entries:
    #     print(f"{key} is a missing entry")
    #     return False
    else:
        return True
def NutrientEntryIsNone(ingredient_nutrition_per100g, key):
    """
    Some data in CoFID uses 'NULL' as an entry to say zero
    """
    if ingredient_nutrition_per100g[key] == None or ingredient_nutrition_per100g[key] == "NULL":
        return True
    else:
        return False
def NutrientEntryIsUnknown(ingredient_nutrition_per100g, key):  # Not zero but not known
    """
    Some data in CoFID uses 'N' as an entry to say 'not sure'
    """
    if ingredient_nutrition_per100g[key] == "N":
        return True
    else:
        return False
def NutrientEntryIsTrace(ingredient_nutrition_per100g, key):
    """
    Some data in CoFID uses 'Tr' as an entry to say it exists in small amount but exact value not known
    """
    if ingredient_nutrition_per100g[key] == "Tr":
        return True
    else:
        return False