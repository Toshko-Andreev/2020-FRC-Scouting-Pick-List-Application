import requests
from operator import index
#team/frc2658/event/2020cadm/matches/keys
r = requests.get('https://www.thebluealliance.com/api/v3/match/2020cadm_qm87', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
first = requests.get('https://www.thebluealliance.com/api/v3/team/frc2658/event/2020cadm/matches/keys', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
the_string = r.text
#print(the_string)
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

def get_value(list, word):
    return find_value(list,find(list,word))

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

for i in store_keys(first.text):
    match = requests.get('https://www.thebluealliance.com/api/v3/match/' + i, params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    rtp = get_value(match_red(match.text), "teleopCellsOuter")
    rip = get_value(match_red(match.text), "teleopCellsInner")
    btp = get_value(match_blue(match.text), "teleopCellsOuter")
    bip = get_value(match_red(match.text), "teleopCellsInner")
    print("Match: " + i)
    print("Red Top: " + str(rtp+rip))
    print("Blue Top: " + str(btp+bip))
    print("--------------------------------------------------------")
