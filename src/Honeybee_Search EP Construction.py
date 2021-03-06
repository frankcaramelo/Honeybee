# Filter EnergyPlus Construction
# By Mostapha Sadeghipour Roudsari
# Sadeghipour@gmail.com
# Honeybee started by Mostapha Sadeghipour Roudsari is licensed
# under a Creative Commons Attribution-ShareAlike 3.0 Unported License.

"""
Search EnergyPlus construction based on Energy modeling standards, climate zone, surface type and building program

-
Provided by Honeybee 0.0.56
    
    Args:
        _EPConstrList: List of EPConstructions from Honeybee construction library
        _standard: Energy modeling standard [0:"ASHRAE 90.1-2004", 1:"ASHRAE 90.1-2007", 2:"ASHRAE 90.1-2010", 3:"ASHRAE 189.1", 4:"CBECS 1980-2004", 5:"CBECS Before-1980"]
        climateZone_: Optional input for climate zone
        surfaceType_: Optional input for surface type > 0:'WALL', 1:'ROOF', 2:'FLOOR', 3:'CEILING', 4:'WINDOW'
        altBldgProgram_: Optional input for building type > 0:'RESIDENTIAL', 1:'OFFICE', 2:'HOSPITAL'
        keyword_: List of optional keywords in the name of the construction (ie. METAL, MASS, WOODFRAME).
    Returns:
        EPSelectedConstr:  List of selected EP constructions that matches the the inputs

"""


ghenv.Component.Name = "Honeybee_Search EP Construction"
ghenv.Component.NickName = 'searchEPConstruction'
ghenv.Component.Message = 'VER 0.0.56\nFEB_01_2015'
ghenv.Component.Category = "Honeybee"
ghenv.Component.SubCategory = "06 | Energy | Material | Construction"
#compatibleHBVersion = VER 0.0.56\nFEB_01_2015
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import scriptcontext as sc
import Grasshopper.Kernel as gh


def main(constrList, standard, climateZone, surfaceType, keywords):
    
    # Make sure Honeybee is flying
    if not sc.sticky.has_key('honeybee_release'):
        print "You should first let Honeybee to fly..."
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, "You should first let Honeybee to fly...")
        return -1

    try:
        if not sc.sticky['honeybee_release'].isCompatible(ghenv.Component): return -1
    except:
        warning = "You need a newer version of Honeybee to use this compoent." + \
        " Use updateHoneybee component to update userObjects.\n" + \
        "If you have already updated userObjects drag Honeybee_Honeybee component " + \
        "into canvas and try again."
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, warning)
        return -1
    
    # get the constuction
    try:
        hb_EPMaterialAUX = sc.sticky["honeybee_EPMaterialAUX"]()
    except:
        msg = "Failed to load EP constructions!"
        ghenv.Component.AddRuntimeMessage(w, msg)
        return -1
    
    surfaceTypesDict = {'0':'WALL', '1':'ROOF', '2':'FLOOR', '3':'CEILING', '4':'WINDOW',
                        'WALL':'WALL', 'ROOF':'ROOF', 'FLOOR':'FLOOR', 'CEILING':'CEILING', 'CEILING':'WINDOW',
                        '':'', None:''}
    
    selConstruction = hb_EPMaterialAUX.filterMaterials(constrList, standard, \
                        climateZone, surfaceTypesDict[surfaceType.upper()], \
                        "", keywords, ghenv.Component)
    
    # constrList, standard, climateZone, surfaceType, bldgProgram, constructionType, ghenv.Component
    
    return selConstruction
    
    
if len(_EPConstrList)!=0 and _standard:
    result = main(_EPConstrList, _standard, climateZone_, surfaceType_, keywords_)
    if result!= -1:
        EPSelectedConstr = result