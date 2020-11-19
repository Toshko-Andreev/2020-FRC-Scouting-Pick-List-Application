import requests
#team/frc2658/event/2020cadm/matches/keys
r = requests.get('https://www.thebluealliance.com/api/v3/match/2020cadm_qm87', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})

the_string = r.text
array = [];

for i in the_string:
    array.append(i)

print(the_string)
#print(array)

where = 0;
for i in range(0,len(array),1):
    if array[i]=='b' and array[i+1]=='l' and array[i+2]=='u' and array[i+3]=='e':
        where = i+4
        break
where2 = 0;
for i in range(where,len(array),1):
    if array[i]=='b' and array[i+1]=='l' and array[i+2]=='u' and array[i+3]=='e':
        where2 = i
        break
where3 = 0;
for i in range(0,len(array),1):
    if array[i]=='r' and array[i+1]=='e' and array[i+2]=='d' and array[i+3]=='"':
        where3 = i+4
        break
where4 = 0;
for i in range(where3,len(array),1):
    if array[i]=='r' and array[i+1]=='e' and array[i+2]=='d' and array[i+3]=='"':
        where4 = i
        break
where5 = 0;
for i in range(where4,len(array),1):
    if array[i]=='}':
        where5 = i
        break

bluelist = []
redlist = []

for i in range(where2,where4):
    bluelist.append(array[i])

for i in range(where4,where5):
    redlist.append(array[i])

#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
#Next part is doing the outer and inner cell calculations for the blue alliance
#----------------------------------------------------------------------------------------------------------------

outercells = 0
for i in range(0,len(bluelist)):
    if bluelist[i] == 't' and bluelist[i+1] == 'e' and bluelist[i+2] == 'l' and bluelist[i+3] == 'e' and bluelist[i+4] == 'o' and bluelist[i+5] == 'p' and bluelist[i+6] == 'C' and bluelist[i+7] == 'e' and bluelist[i+8] == 'l' and bluelist[i+9] == 'l' and bluelist[i+10] == 's' and bluelist[i+11] == 'O' and bluelist[i+12] == 'u' and bluelist[i+13] == 't' and bluelist[i+14] == 'e' and bluelist[i+15] == 'r':
        outercells = i+16
end1 = 0;
for i in range(outercells,len(bluelist)):
    if bluelist[i] == ',':
        end1 = i
        break
outerlst = []
s= ''
for i in range(outercells+3,end1):
    outerlst.append(bluelist[i])
outerscore = int(s.join(outerlst))

innercells = 0;
for i in range(0,len(bluelist)):
    if bluelist[i] == 't' and bluelist[i+1] == 'e' and bluelist[i+2] == 'l' and bluelist[i+3] == 'e' and bluelist[i+4] == 'o' and bluelist[i+5] == 'p' and bluelist[i+6] == 'C' and bluelist[i+7] == 'e' and bluelist[i+8] == 'l' and bluelist[i+9] == 'l' and bluelist[i+10] == 's' and bluelist[i+11] == 'I' and bluelist[i+12] == 'n' and bluelist[i+13] == 'n' and bluelist[i+14] == 'e' and bluelist[i+15] == 'r':
        innercells = i+16
end2 = 0;
for i in range(innercells,len(bluelist)):
    if bluelist[i] == ',':
        end2 = i
        break
innerlst = []
s= ''
for i in range(innercells+3,end2):
    innerlst.append(bluelist[i])
innerscore = int(s.join(innerlst))

#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

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

print("--------------------------------------------------------")  
print(get_value(redlist, "teleopPoints"))
print(get_value(bluelist, "teleopPoints"))