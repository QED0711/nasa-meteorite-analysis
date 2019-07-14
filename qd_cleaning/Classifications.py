
class Classifications:

    subclasses = {
    "Chondrite": (
        "CB", 
        "CH",
        "CK",
        "CM",
        "CR",
        "CV",
        "CO",
        "CI",

        "H",
        "L",
        "LL",

        "R",

        "EH",
        "EL",
        
        # observed
        "E",
        "Chondrite",
        # wiki
        "OC", # ordinary chondrite
        "K",
        "C" # ungrouped Carbonaceous
    ),
    
    "Achondrite" : (
        "Iodranite",
        "Acapulcoite",
        "Winonaite",
        
        "Martian",
        "Shergottite",
        "Nakhlite",
        "Chassignite",
        "ALH 84001 opx",
        
        "Aubrite",
        "Ureilite",
        "HED",
        "Eucrite",
        "Diogenite",
        "Howardite",
        
        "Angrite",
        
        "Brachinite",
        
        "Lunar",
        "breccia",
        "basaltic",
        "polymict",
        
        # observed
        
        "Achondrite",
        "achon",
    ),
    
    "Stony-Iron": (        
        "Pallasite",
        "Mesosiderite",
        
        "Stone", # observation
    ),
    
    "Iron": (
        "Iron",
        
        "IAB",
        "IIAB",
        "IIIAB",
        "IVAB",
    )
}
    
    @classmethod
    def gen_classifiers(cls):
        subclass_match = {}
        for _class, subclass_list in cls.subclasses.items():
            for sc in subclass_list:
                subclass_match[sc] = _class
        return subclass_match

    @classmethod
    def classify_subclasses(cls, df):
        major_classifications = []
        subclass_category = []

        classifiers = cls.gen_classifiers()

        for i, rc in enumerate(df.recclass):
                major_classifications.append("uncategorized")
                subclass_category.append(None)
                for subclass in classifiers:
                    if subclass in rc:
                        major_classifications[i] = classifiers[subclass]
                        subclass_category[i] = subclass

        df['major_classification'] = major_classifications
        df['subclass_category'] = subclass_category
        return df