import numpy as np
import re
import os
import pandas as pd
import html
import json
geos = './geos/'
geos_content = os.listdir(geos)
firstfile = geos+'aa.html'
country_files = [g for g in geos_content if len(g.split('.')[0])==2]
#remember to remove 'other' from all features
cols = ['name','code','loc','spec_loc','landlocked','island','tropical','desert','marine','temperate','bordering','northern','western','coord']
#with open(firstfile, 'r', encoding='utf-8') as infile:
#    linelist = infile.readlines()
#    for i in range(len(linelist)):#is island, more specific locaton
#        if '<div id="field-location">' in linelist[i]:
#            spec_loc = linelist[i+2].split(',')[0].strip(' ')
#            island = 'island' in linelist[i+2]
#        if '<title>' in linelist[i]:#Main location,Place Name
#            name = linelist[i].split(' :: ')[1].split(' — ')[0]
#            loc = linelist[i].split(' :: ')[0][len('  <title>'):]
#        if '<div id="field-religions">' in linelist[i]:#features related to religion
#            religions = re.sub("[\(\[].*?[\)\]]", "", linelist[i+2])
#            religions = ','.join([i for i in religions.split(',') if 'other' not in i and 'unspecified' not in i])
#            religions_list = religions.split('%')[:-1]
#            rel_levels = [int(re.findall("\d+", i)[0]) for i in religions_list]
#            is_many_rel = [i>10 for i in rel_levels]
#            religions = re.sub("[\(\[].*?[\)\]]", "", religions)
#            religions = ''.join( c for c in religions if  c not in '0123456789.,' )
#            religions = [i.strip(' ') for i in religions.split('%')[:-1]]
#            religions = [i for i in religions]
#            official_religions = [i for i in linelist[i+2].split('%') if 'official' in i]
#            official_religions = [''.join( c for c in i if  c not in '0123456789.,' ) for i in official_religions]
#            official_religions = [re.sub("[\(\[].*?[\)\]]", "", i).strip(' ') for i in official_religions]
#        if '<div id="field-coastline">' in linelist[i]:#landlocked?
#            landlocked = not np.any([int(i) for i in linelist[i+3] if i.isdigit()])
#        if '<div id="field-climate">' in linelist[i]:
#            tropical = 'tropical' in linelist[i+2]
#            marine = 'marine' in linelist[i+2]
#            temperate = 'temperate' in linelist[i+2]
#            desert = 'desert' in linelist[i+2]
#        if '<div id="field-languages">' in linelist[i]:#language related features
#            languages = ','.join([i for i in linelist[i+2].split(',') if 'other' not in i and 'unspecified' not in i])
#            languages = re.sub("[\(\[].*?[\)\]]", "", languages)
#            if '%,' in languages:
#                languages_list = languages.split('%')[:-1]
#                languages = [i.strip(' ') for i in languages_list[:-1]]
#                lang_levels = [int(re.findall("\d+", i)[0]) for i in languages_list]
#                is_many_speakers = [i>10 for i in lang_levels]
#            else:
#                languages = languages.split(',')
#                language_list = [i.strip('\n').strip(' ') for i in languages]
#            languages = ''.join( c for c in languages if  c not in '0123456789.,' )
#            official_languages = [i for i in linelist[i+2].split('%') if 'official' in i]
#            official_lang_unkown_or_absent = len(official_languages)>0
#            official_languages = [''.join( c for c in i if  c not in '0123456789.,' ) for i in official_languages]
#            official_languages = [re.sub("[\(\[].*?[\)\]]", "", i).strip(' ') for i in official_languages]
#        if '<div id="field-government-type">' in linelist[i]:#features related to governance
#            gov = linelist[i+2]
#            kingdom = 'kingdom' in gov.lower() or 'kingdom' in name.lower()
#            democracy = 'democracy' in gov.lower()
#            princedom = 'prince' in gov.lower()
#            monarchy = kingdom or princedom or ('monarch' in gov.lower())
#        if '<span class="subfield-name">border countries' in linelist[i]:#countries sharing border
#            bordering = linelist[i+1].strip('\n')
#            bordering = ''.join( c for c in bordering if  c not in '0123456789.')
#            bordering = [i.strip('km').strip(' ') for i in bordering.split(',')]
#        if '<div id="field-geographic-coordinates">' in linelist[i]:#hemispheres
#            coord = linelist[i+2].strip('\n').split(',')
#            coord = [c.strip(' ') for c in coord]
#            coord = [c.replace(' ','.') for c in coord]
#            coord = [c[:-2]+c[-1] for c in coord]
#            northern_hem = coord[0][-1]=='N'
#            western_hem = coord[1][-1]=='W'
def get_countries():
    countries = {}
    for country in country_files:
        countryfilename = geos + country
        with open(countryfilename, 'r', encoding='utf-8') as infile:
            linelist = infile.readlines()
            temp = {}
            for c in cols: temp[c] = None
            for i in range(len(linelist)):#is island, more specific locaton
                if '<div id="field-location">' in linelist[i]:
                    temp['spec_loc'] = linelist[i+2].split(',')[0].strip(' ').strip('\n')
                    temp['spec_loc'] = temp['spec_loc'].split(';')[0].split(':')[0]
                    temp['spec_loc'] = re.sub("[\(\[].*?[\)\]]", "", temp['spec_loc']).strip(' ')
                    temp['spec_loc'] = temp['spec_loc'].replace('<p>','').replace('<strong>','')
                    temp['island'] = 'island' in linelist[i+2]
                if '<title>' in linelist[i]:#Main location,Place Name
                    linelist[i] = linelist[i].replace('&amp;#39;',"'")
                    temp['name'] = linelist[i].split(' :: ')[1].split(' — ')[0]
                    if ',' in temp['name']:
                        temp['name'] = temp['name'].split(',')
                        temp['name'] = re.sub("[\(\[].*?[\)\]]", "",temp['name'][1] + ' ' + temp['name'][0])
                        temp['name'] = temp['name'].strip(' ')
                    temp['loc'] = linelist[i].split(' :: ')[0][len('  <title>'):]
                if '<div id="field-religions">' in linelist[i]:#features related to religion
                    religions = re.sub("[\(\[].*?[\)\]]", "", linelist[i+2])
                    religions = ','.join([i for i in religions.split(',') if 'other' not in i and 'unspecified' not in i])
                    religions_list = religions.split('%')[:-1]
                    rel_levels = [int(re.findall("\d+", i)[0]) for i in religions_list]
                    is_many_rel = [i>10 for i in rel_levels]
                    religions = re.sub("[\(\[].*?[\)\]]", "", religions)
                    religions = ''.join( c for c in religions if  c not in '0123456789.,' )
                    religions = [i.strip(' ') for i in religions.split('%')[:-1]]
                    religions = [i for i in religions]
                    temp['religion'] = religions
                    official_religions = [i for i in linelist[i+2].split('%') if 'official' in i]
                    official_religions = [''.join( c for c in i if  c not in '0123456789.,' ) for i in official_religions]
                    official_religions = [re.sub("[\(\[].*?[\)\]]", "", i).strip(' ') for i in official_religions]
                if '<div id="field-coastline">' in linelist[i]:#landlocked?
                    temp['landlocked'] = not np.any([int(i) for i in linelist[i+3] if i.isdigit()])
                if '<div id="field-climate">' in linelist[i]:
                    temp['tropical'] = 'tropical' in linelist[i+2]
                    temp['marine'] = 'marine' in linelist[i+2]
                    temp['temperate'] = 'temperate' in linelist[i+2]
                    temp['desert'] = 'desert' in linelist[i+2]
                if '<div id="field-languages">' in linelist[i]:#language related features
                    languages = ','.join([i for i in linelist[i+2].split(',') if 'other' not in i and 'unspecified' not in i])
                    languages = re.sub("[\(\[].*?[\)\]]", "", languages)
                    temp['english'] = 'English' in languages
                    temp['chinese'] = 'Mandarin' in languages or 'Chinese' in languages or 'Cantonese' in languages
                    temp['french'] = 'French' in languages
                    temp['spanish'] = 'Spanish' in languages
                    temp['portuguese'] = 'Portuguese' in languages
                    temp['arabic'] = 'Arabic' in languages
                    temp['german'] = 'German' in languages
                    temp['dutch'] = 'Dutch' in languages
                    temp['swahili'] = 'Swahili' in languages or 'Kiswahili' in languages
                    temp['russian'] = 'Russian' in languages
                    if '%,' in languages:
                        languages_list = languages.split('%')[:-1]
                        languages = [i.strip(' ') for i in languages_list[:-1]]
                        lang_levels = [int(re.findall("\d+", i)[0]) for i in languages_list]
                        is_many_speakers = [i>10 for i in lang_levels]
                    else:
                        languages = languages.split(',')
                        languages_list = [i.strip('\n').strip(' ') for i in languages]
                    if len(languages_list)<=3:
                        short_lang = ' '.join(languages_list)
                    else:
                        short_lang = ' '.join(languages_list[:3])
                    languages = ''.join( c for c in languages if  c not in '0123456789.,' )
                    official_languages = [i for i in linelist[i+2].split('%') if 'official' in i]
                    official_lang_unkown_or_absent = len(official_languages)>0
                    official_languages = [''.join( c for c in i if  c not in '0123456789.,' ) for i in official_languages]
                    official_languages = [re.sub("[\(\[].*?[\)\]]", "", i).strip(' ') for i in official_languages]
                    temp['languages'] = languages_list
                if '<div id="field-government-type">' in linelist[i]:#features related to governance
                    gov = linelist[i+2]
                    kingdom = 'kingdom' in gov.lower() or 'kingdom' in temp['name'].lower()
                    democracy = 'democracy' in gov.lower()
                    princedom = 'prince' in gov.lower()
                    monarchy = kingdom or princedom or ('monarch' in gov.lower())
                if '<span class="subfield-name">border countries' in linelist[i]:#countries sharing border
                    linelist[i+1] = linelist[i+1].replace('&amp;#39;',"'")
                    bordering = linelist[i+1].strip('\n')
                    bordering = re.sub("[\(\[].*?[\)\]]", "", bordering).replace(' km','')
                    bordering = ''.join( c for c in bordering if  c not in '0123456789.')
                    temp['bordering'] = [i.strip('km').strip(' ') for i in bordering.split(',')]
                if '<div id="field-geographic-coordinates">' in linelist[i]:#hemispheres
                    coord = linelist[i+2].strip('\n').split(',')
                    coord = [c.strip(' ').split(';')[0] for c in coord[:2]]
                    coord = [c.replace(' ','.') for c in coord]
                    temp['coord'] = [c[:-2]+c[-1] for c in coord]
                    temp['coord'][0] = '.'.join(temp['coord'][0].split('.')[-2:])
                    temp['northern'] = coord[0][-1]=='N'
                    temp['western'] = coord[1][-1]=='W'
                if '<div id="field-internet-country-code">' in linelist[i]:
                    code = linelist[i+2].strip('\n').strip(' ')
                    m = code.index('.')
                    temp['code'] = code[m+1:m+3]
                    temp['code'] = temp['code'].upper()
                    countries[temp['name']] = temp
    return countries 



countries = get_countries()

#ERATA
countries['France']['island'] = False

borderlineyes = [0.8,0.2]
borderlineno = [0.2,0.8]
northyes = [0.95,0.05]
northno = [0.05,0.95]
westyes = [0.6,0.4]
westno = [0.4,0.6]
locyes = [0.95,0.05]
locno = [0.05,0.95]
slocyes = [0.7,0.3]
slocno = [0.3,0.7]
islandyes = [0.8,0.2]
islandno = [0.2,0.8]
lockyes = [0.7,0.3]
lockno = [0.3,0.7]

questions = []

bordering = set()
for key in countries.keys():
    if 'bordering' in countries[key].keys():
        if countries[key]['bordering'] != None:
            bordering = bordering.union(set(countries[key]['bordering']))

bordering = list(bordering)

locs = set()
for key in countries.keys():
    if 'loc' in countries[key].keys():
        locs = locs.union([countries[key]['loc']])

locs = list(locs)

slocs = set()
for key in countries.keys():
    if 'spec_loc' in countries[key].keys():
       slocs = slocs.union([countries[key]['spec_loc']])

slocs = list(slocs)

bordering_answers = {}

for key in countries.keys(): 
    country = countries[key]
    border_answers = np.zeros((len(bordering),3))
    for i in range(len(bordering)):
        if 'bordering' in country.keys():
            if country['bordering'] != None:
                if bordering[i] in countries[key]['bordering']:
                    border_answers[i,0] = 1.
                    questions.append(['Does your country border ' + bordering[i] +'?',key,countries[key]['code'],borderlineyes])
                else:
                    border_answers[i,2] = 1.
                    questions.append(['Does your country border '+ bordering[i]+'?',key,countries[key]['code'],borderlineno])
            else:
                border_answers[i,2] = 1.
        else:
            border_answers[i,2] = 1. 
    bordering_answers[key] = border_answers

hemisphere_answers = {}

for key in countries.keys(): 
    country = countries[key]
    hemi_answers = np.zeros((2,3))
    if 'northern' in country.keys():
        if country['northern']:
            hemi_answers[0,0] += 1.               
            questions.append(['Is your country in the northern hemisphere?',key,countries[key]['code'],northyes])
        else:
            hemi_answers[0,2] += 1.
            questions.append(['Is your country in the northern hemisphere?',key,countries[key]['code'],northno])
    else:
        hemi_answers[0,1] += 1. 
    if 'western' in country.keys():
        if country['western']:
            hemi_answers[1,0] += 1.  
            questions.append(['Is your country in the western hemisphere?',key,countries[key]['code'],westyes])             
        else:
            hemi_answers[1,2] += 1.
            questions.append(['Is your country in the western hemisphere?',key,countries[key]['code'],westno])  
    else:
        hemi_answers[1,1] += 1. 
    hemisphere_answers[key] = hemi_answers
    
slocs_answers = {}

for key in countries.keys(): 
    country = countries[key]
    sloc_answers = np.zeros((len(slocs),3))
    for i in range(len(slocs)):
        if 'spec_loc' in country.keys():
            if country['spec_loc'] != None:
                if slocs[i] in countries[key]['spec_loc']:
                    sloc_answers[i,0] = 1.
                    questions.append(['Is your country in '+slocs[i]+'?',key,countries[key]['code'],slocyes])  
                else:
                    sloc_answers[i,2] = 1.   
                    questions.append(['Is your country in '+slocs[i]+'?',key,countries[key]['code'],slocno])
            else:
                sloc_answers[i,2] = 1.
        else:
            sloc_answers[i,1] = 1. 
    slocs_answers[key] = sloc_answers

locs_answers = {}

for key in countries.keys(): 
    country = countries[key]
    loc_answers = np.zeros((len(locs),3))
    for i in range(len(locs)):
        if 'loc' in country.keys():
            if country['loc'] != None:
                if locs[i] in countries[key]['loc']:
                    loc_answers[i,0] = 1.
                    questions.append(['Is your country in '+locs[i]+'?',key,countries[key]['code'],locyes])
                else:
                    loc_answers[i,2] = 1. 
                    questions.append(['Is your country in '+locs[i]+'?',key,countries[key]['code'],locno])
            else:
                loc_answers[i,2] = 1.
        else:
            loc_answers[i,1] = 1. 
    locs_answers[key] = sloc_answers
    
geo_answers = {}

for key in countries.keys(): 
    country = countries[key]
    g_answers = np.zeros((2,3))
    if 'landlocked' in country.keys():
        if country['landlocked']:
            g_answers[0,0] += 1.  
            questions.append(['Is your country landlocked?',key,countries[key]['code'],lockyes])             
        else:
            g_answers[0,2] += 1.
            questions.append(['Is your country landlocked?',key,countries[key]['code'],lockno])    
    else:
        g_answers[0,1] += 1. 
    if 'island' in country.keys():
        if country['island']:
            g_answers[1,0] += 1.   
            questions.append(['Is your country an island nation?',key,countries[key]['code'],islandyes])             
        else:
            g_answers[1,2] += 1.
            questions.append(['Is your country an island nation?',key,countries[key]['code'],islandno])  
    else:
        g_answers[1,1] = 1. 
    geo_answers[key] = g_answers

lang_answers = {}

langyes = [0.85,0.15]
langno = [0.2,0.8]
for key in countries.keys(): 
    country = countries[key]
    l_answers = np.zeros((9,3))
    if 'english' in country.keys():
        if country['english']:
            l_answers[0,0] += 1.  
            questions.append(['Is English an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[0,2] += 1.
            questions.append(['Is English an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[0,1] += 1. 
        
    if 'chinese' in country.keys():
        if country['chinese']:
            l_answers[1,0] += 1.  
            questions.append(['Is Chinese an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[1,2] += 1.
            questions.append(['Is Chinese an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[1,1] += 1. 

    if 'french' in country.keys():
        if country['french']:
            l_answers[2,0] += 1.  
            questions.append(['Is French an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[2,2] += 1.
            questions.append(['Is French an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[2,1] += 1. 


    if 'spanish' in country.keys():
        if country['spanish']:
            l_answers[3,0] += 1.  
            questions.append(['Is Spanish an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[3,2] += 1.
            questions.append(['Is Spanish an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[3,1] += 1. 

    if 'portuguese' in country.keys():
        if country['portuguese']:
            l_answers[4,0] += 1.  
            questions.append(['Is Portuguese an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[4,2] += 1.
            questions.append(['Is Portuguese an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[4,1] += 1. 

    if 'arabic' in country.keys():
        if country['arabic']:
            l_answers[5,0] += 1.  
            questions.append(['Is Arabic an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[5,2] += 1.
            questions.append(['Is Arabic an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[5,1] += 1. 

    if 'german' in country.keys():
        if country['german']:
            l_answers[6,0] += 1.  
            questions.append(['Is German an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[6,2] += 1.
            questions.append(['Is German an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[6,1] += 1. 
        
    lang_answers[key] = l_answers


    if 'dutch' in country.keys():
        if country['dutch']:
            l_answers[7,0] += 1.  
            questions.append(['Is Dutch an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[7,2] += 1.
            questions.append(['Is Dutch an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[7,1] += 1. 

    if 'swahili' in country.keys():
        if country['swahili']:
            l_answers[8,0] += 1.  
            questions.append(['Is Kiswahili or Swahili an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[8,2] += 1.
            questions.append(['Is Kiswahili or Swahili an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[8,1] += 1.
        
    if 'russian' in country.keys():
        if country['russian']:
            l_answers[8,0] += 1.  
            questions.append(['Is Russian an official or important language in your country?',key,countries[key]['code'],langyes])             
        else:
            l_answers[8,2] += 1.
            questions.append(['Is Russian an official or important language in your country?',key,countries[key]['code'],langno])
    else:
        l_answers[8,1] += 1.
        
    lang_answers[key] = l_answers

#Still have to add UN security info to knowledge base
un_sec = ['China','Russia','United States','United Kingdom','France']
sec_q = 'Is your country one of the five permanent members of the UN security council?'
secyes = [0.7,0.3]
secno = [0.3,0.7]
for key in countries.keys():
    country = countries[key]
    if country['name'] in un_sec:
        questions.append([sec_q,key,country['code'],secyes])
    else:
        questions.append([sec_q,key,country['code'],secno])

with open('questions.json', 'w') as f:
    json.dump(questions, f)