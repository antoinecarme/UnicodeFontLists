# You can get fontconfig python support from here : https://github.com/ldo/python_fontconfig
import fontconfig as fc
from fontconfig import FC

from gi.repository import GLib

def get_scripts(iCodes):
    lScripts = []
    for lCode in iCodes:
        try:
            lStr = chr(lCode)
            lScript = GLib.unichar_get_script(lStr)
            lScripts.append(lScript.value_nick)
        except:
            pass
    lScripts = list(set(lScripts))
    lScripts = sorted(lScripts)
    return [" ".join(lScripts)]

def normalize_by_lang_prop(name, lang, iDict):
    if(type(iDict[name]) == str):
        return [(iDict[lang], iDict[name])]
    if(len(iDict[name]) == 1):
        return [(iDict[lang][0], iDict[name][0])]
    return [x for x in zip(iDict[lang], iDict[name])]

def pattern_to_dict(f):
    lDict = {}
    for prop in fc.PROP:
        values = []
        result, status = f.get(prop, 0)
        while(status == FC.ResultMatch):
            values = values + [ result ]
            result, status = f.get(prop, len(values))
        if(prop.value == "charset"):
            values = get_scripts(values[0])
        if(len(values) > 0):
            if(len(values) > 1):
                lDict[str(prop.value)] = values
            else:
                if(prop.value != "lang"):
                    lDict[str(prop.value)] = values[0]
                else:
                    lDict[str(prop.value)] = values
                
    if('file' in lDict.keys()):
        fields = lDict['file'].split('/')
        lDict["file"] = '/'.join(fields[-2:])
    lLangs = list(lDict["lang"][0])
    lDict["langs"] = " ".join(lLangs)
    lDict.pop("lang")
    lDict["scripts"] = lDict["charset"]
    lDict.pop("charset")

    by_lang_tags = ["fullname", "style", "family"]
    for tag in by_lang_tags:
        if(lDict.get(tag)):
            lDict[tag] = normalize_by_lang_prop(tag, tag + "lang", lDict)
            lDict[tag] = str( lDict[tag] )
            lDict.pop(tag + "lang")
    return dict(sorted([x for x in lDict.items()]))

def get_all_system_fonts_info():
    pat = fc.Pattern.create()
    conf = fc.Config.get_current()
    conf.substitute(pat, FC.MatchPattern)
    # pat.default_substitute()

    found = conf.font_sort(pat, trim = False, want_coverage = False)
    found1 = list(found[0])
    print("FONTS_FOUND", len(found1), found1)
    lFontInfo = {}
    for f in found1 :
        # print(f)
        family = f.get(fc.PROP.FAMILY, 0)[0]
        fullname = f.get(fc.PROP.FULLNAME, 0)[0]
        if(fullname is None):
            print("FONT_HAS_NO_FULL_NAME", family, fullname, pattern_to_dict(f))
            fullname = family
        if(lFontInfo.get(fullname)):
            print("FONT_HAS_DUPLICATE_FULL_NAME", family, fullname, pattern_to_dict(f))
        
        lFontInfo[fullname] = pattern_to_dict(f)

    lFontInfo = dict(sorted([x for x in lFontInfo.items()]))
    for k in sorted(lFontInfo.keys()):
        print("FONT_INFO", (k, lFontInfo[k]))
    return lFontInfo

def save_as_csv(iFontInfo):
    import pandas as pd
    df = pd.DataFrame()
    lData = [v for (k, v) in iFontInfo.items()]
    df = df.from_records( lData )
    print(df.head(10))
    df.to_csv("font_data.csv")

def save_as_json(iFontInfo):
    import json
    with open('font_data.json', 'w') as outfile:
        json.dump(iFontInfo, outfile, indent=4)


lFontInfo = get_all_system_fonts_info()
save_as_csv(lFontInfo)
save_as_json(lFontInfo)
