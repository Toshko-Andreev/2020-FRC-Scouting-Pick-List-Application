import requests
#team/frc2658/event/2020cadm/matches/keys
r = requests.get('https://www.thebluealliance.com/api/v3/match/2020cadm_qm87', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})

the_string = r.text

array = []
for i in the_string:
    array.append(i)

print(the_string)
#print(array)

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
#Next part is doing the outer and inner cell calculations for the blue alliance
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

firstblue = find(array, "blue")
secondblue = find_range(array, "blue", firstblue, "end")

firstred = find(array, "red")
secondred = find_range(array, ['r','e','d','"'], firstred, "end")

endred = 0
for i in range(secondred,len(array),1):
    if array[i]=='}':
        endred = i
        break

bluelist2 = []
redlist2 = []

for i in range(secondblue,secondred):
    bluelist2.append(array[i])

for i in range(secondred,endred):
    redlist2.append(array[i])

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

print("--------------------------------------------------------")  
print(get_value(redlist2, "teleopPoints"))
print(get_value(match_red(the_string), "teleopPoints"))
print(get_value(bluelist2, "teleopPoints"))
print(get_value(match_blue(the_string), "teleopPoints"))
