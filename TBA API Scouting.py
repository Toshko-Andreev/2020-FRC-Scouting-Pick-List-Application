import requests
from operator import index
import json

r = requests.get('https://www.thebluealliance.com/api/v3/match/2020cadm_qm87', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
#print(r.text)

s = requests.get('https://www.thebluealliance.com/api/v3/event/2020cadm/teams/simple', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
#print(s.text)
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

def find(list, word):
    found = False
    place = 0
    for bch in range(0,len(list)):
        count = 0
        for ch in range(0,len(word)):
            if list[bch+count] == word[ch]:
                found = True
            else:
                found = False
                break
            count += 1
        if found == True:
            return bch+len(word)
            break

def find_range(list, word, start, end):
    if end == "end":
        end = len(list)
    found = False
    place = 0
    for bch in range(start,end):
        count = 0
        for ch in range(0,len(word)):
            if list[bch+count] == word[ch]:
                found = True
            else:
                found = False
                break
            count += 1
        if found == True:
            return bch+len(word)
            break

def find_value(list, pos):
    endspot = 0
    for i in range(pos,len(list)):
        if list[i] == ',':
            endspot = i
            break
    scorelist = []
    s= ''
    for i in range(pos+3,endspot):
        scorelist.append(list[i])
    return int(s.join(scorelist))

#def get_value(list, word):
#    return find_value(list,find(list,word))

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

def match_red(in_string):
    array = []
    for i in in_string:
        array.append(i)
    firstred = find(array, "red")
    secondred = find_range(array, ['r','e','d','"'], firstred, "end")
    endred = 0
    redlist = []
    for i in range(secondred,len(array),1):
        if array[i]=='}':
            endred = i
            break
    for i in range(secondred,endred):
        redlist.append(array[i])
    return redlist

def match_blue(in_string):
    array = []
    for i in in_string:
        array.append(i)
    firstblue = find(array, "blue")
    secondblue = find_range(array, "blue", firstblue, "end")    
    firstred = find(array, "red")
    secondred = find_range(array, ['r','e','d','"'], firstred, "end")
    bluelist = []
    for i in range(secondblue,secondred):
        bluelist.append(array[i])
    return bluelist

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

def store_keys(in_string):
    array = []
    for i in in_string:
        array.append(i)
    how_many = 0
    for ch in array:
        if ch == '"':
            how_many += 1
    add = False
    key_list = []
    startpoint = 0
    for num in range(0,how_many):
        key = ""
        for chn in range(startpoint,len(array)):
            if add == False and array[chn] == '"':
                add = True
                startpoint = chn+1
                break
            elif add == True and array[chn] == '"':
                add = False
                key_list.append(key)
                startpoint = chn+1
                break
            elif add == False:
                nothing = 0
            else:
                key += array[chn]
    return key_list



print("--------------------------------------------------------")  
#print(store_keys(first.text))
#print(get_value(match_red(the_string), "teleopPoints"))
#print(get_value(match_blue(the_string), "teleopPoints"))

#for i in store_keys(first.text):
#    match = requests.get('https://www.thebluealliance.com/api/v3/match/' + i, params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
#    rtp = get_value(match_red(match.text), "teleopCellsOuter")
#    rip = get_value(match_red(match.text), "teleopCellsInner")
#    btp = get_value(match_blue(match.text), "teleopCellsOuter")
#    bip = get_value(match_red(match.text), "teleopCellsInner")
#    print("Match: " + i)
#    print("Red Top: " + str(rtp+rip))
#    print("Blue Top: " + str(btp+bip))
#    print("--------------------------------------------------------")

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

def get_alliance(num, match):
    dict = json.loads(match.text)
    for i in dict['alliances']['blue']['team_keys']:
        if i == 'frc' + str(num):
            return 'blue'
    for i in dict['alliances']['red']['team_keys']:
        if i == 'frc' + str(num):
            return 'red'
    return 'That team is not in this match.'

def which_robot(num, match):
    dict = json.loads(match.text)
    for i in range(0,len(dict['alliances']['blue']['team_keys'])):
        if dict['alliances']['blue']['team_keys'][i] == 'frc' + str(num):
            return i+1
    for i in range(0,len(dict['alliances']['red']['team_keys'])):
        if dict['alliances']['red']['team_keys'][i] == 'frc' + str(num):
            return i+1
    return 'That team is not in this match.'

def get_value(num, key, thing):
    info = requests.get('https://www.thebluealliance.com/api/v3/match/' + key, params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    dict = json.loads(info.text)
    return dict['score_breakdown'][get_alliance(num, info)][thing]

def team_average(num, thing):
    matches = requests.get('https://www.thebluealliance.com/api/v3/team/frc' + str(num) + '/event/2020cadm/matches/keys', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    thing_amount = 0
    thing_total = 0
    for match in store_keys(matches.text):
        thing_amount += 1
        thing_total += get_value(num, match, thing)
    return thing_total/thing_amount

def team_list(event_key):
    info = requests.get('https://www.thebluealliance.com/api/v3/event/' + event_key + '/teams/simple', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    dict = json.loads(info.text)
    teamlist = []
    for i in range(0,len(dict)):
        team = dict[i]
        teamlist.append(team['team_number'])
    return teamlist

print(team_list('2020cadm'))
#print(team_average(2658, 'totalPoints'))