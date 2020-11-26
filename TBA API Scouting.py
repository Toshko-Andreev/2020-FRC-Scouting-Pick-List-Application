import requests
from operator import index
import json

r = requests.get('https://www.thebluealliance.com/api/v3/match/2020cadm_qm87', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
#print(r.text)

s = requests.get('https://www.thebluealliance.com/api/v3/event/2020cadm/teams/simple', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
#print(s.text)

t = requests.get('https://www.thebluealliance.com/api/v3/event/2020cadm/rankings', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
#print (t.text)

#----------------------------------------------------------------------------------------------------------------
#Start of all the basic functions for pulling match and team data
#----------------------------------------------------------------------------------------------------------------

#Outputs a list of all the qualification match keys for a team at an event
def qm_match_key_list(team_num, event_key):
    info = requests.get('https://www.thebluealliance.com/api/v3/team/frc' + str(team_num) + '/event/' + event_key + '/matches/keys', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    list = json.loads(info.text)
    qm_matches = []
    for i in list:
        if i[len(event_key)+1] == 'q' and i[len(event_key)+2] == 'm':
            qm_matches.append(i)
    return qm_matches

#Outputs a list of all the match keys for a team at an event    
def all_match_key_list(team_num, event_key):
    info = requests.get('https://www.thebluealliance.com/api/v3/team/frc' + str(team_num) + '/event/' + event_key + '/matches/keys', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    list = json.loads(info.text)
    matches = []
    for i in list:
        matches.append(i)
    return matches

#Finds out which alliance a team belongs to for a given match
def get_alliance(num, match):
    dict = json.loads(match.text)
    for i in dict['alliances']['blue']['team_keys']:
        if i == 'frc' + str(num):
            return 'blue'
    for i in dict['alliances']['red']['team_keys']:
        if i == 'frc' + str(num):
            return 'red'
    return 'That team is not in this match.'

#Finds out which number robot a specific team is for a given match
def which_robot(num, match):
    dict = json.loads(match.text)
    for i in range(0,len(dict['alliances']['blue']['team_keys'])):
        if dict['alliances']['blue']['team_keys'][i] == 'frc' + str(num):
            return i+1
    for i in range(0,len(dict['alliances']['red']['team_keys'])):
        if dict['alliances']['red']['team_keys'][i] == 'frc' + str(num):
            return i+1
    return 'That team is not in this match.'

#Gets the value of a desired value in the score breakdown of a match
def get_value(num, match_key, thing):
    info = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_key, params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    dict = json.loads(info.text)
    return dict['score_breakdown'][get_alliance(num, info)][thing]

#----------------------------------------------------------------------------------------------------------------
#End of all the basic functions for pulling match and team data
#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------
#Start of all functions for overall team or event
#----------------------------------------------------------------------------------------------------------------

#Finds the team average overall all qualification matches for a specific value
def team_average(num, event_key, thing):
    thing_amount = 0
    thing_total = 0
    matches = qm_match_key_list(num, event_key)
    for match in matches:
        thing_amount += 1
        thing_total += get_value(num, match, thing)
    return thing_total/thing_amount

#Outputs a list of all the teams at an event
def team_list(event_key):
    info = requests.get('https://www.thebluealliance.com/api/v3/event/' + event_key + '/teams/simple', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    dict = json.loads(info.text)
    teamlist = []
    for i in range(0,len(dict)):
        team = dict[i]
        teamlist.append(team['team_number'])
    return teamlist

#Gets a climb number based on how many times a team has climbed or not
def climb_num(num, event_key):
    total_points = 0
    total_amount = 0
    matches = qm_match_key_list(num, event_key)
    for match_key in matches:
        match = requests.get('https://www.thebluealliance.com/api/v3/match/' + match_key, params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
        robot = which_robot(num, match)
        climb = get_value(num, match_key, 'endgameRobot' + str(robot))
        if climb == 'Hang':
            total_points += 1
        total_amount += 1
    return total_points/total_amount

#Creates a list with the climb number, auto ball number, and teleop ball number for each team        
def data_list(event_key):
    datalist = {}
    tn = 1
    teamlist = team_list(event_key)
    for team in teamlist:
        print("Data List: " + str(tn) + "/" + str(len(teamlist)) + " Done")
        datalist[team] = {'climb':climb_num(team, event_key), 'auto_balls':team_average(team, event_key, 'autoCellsInner') + team_average(team, event_key, 'autoCellsOuter'), 'teleop_balls':team_average(team, event_key, 'teleopCellsInner') + team_average(team, event_key, 'teleopCellsOuter')}
        tn += 1
    return datalist

#Calculates the rank number for a given team at a given event
def rank_num(num, event_key):
    climb = climb_num(num, event_key)
    auto_balls = team_average(num, event_key, 'autoCellsInner') + team_average(num, event_key, 'autoCellsOuter')
    teleop_balls = team_average(num, event_key, 'teleopCellsInner') + team_average(num, event_key, 'teleopCellsOuter')
    return (0.4*teleop_balls)+(0.4*climb)+(+0.2*auto_balls)

#Calculates the average number of balls scored in the inner and outer port during auto for a team at an event
def auto_num(num, event_key):
    return team_average(num, event_key, 'autoCellsInner') + team_average(num, event_key, 'autoCellsOuter')

#Calculates the average number of balls scored in the inner and outer port during teleop for a team at an event
def teleop_num(num, event_key):
    return team_average(num, event_key, 'teleopCellsInner') + team_average(num, event_key, 'teleopCellsOuter')

#Gets the official rank list of the event
def official_ranklist(event_key):
    info = requests.get('https://www.thebluealliance.com/api/v3/event/' + event_key + '/rankings', params = {'X-TBA-Auth-Key': 'ZxhuACw5seFvz5VqNxNGKG9yC9sbDZshpjM4PisgEgVc533hlJQSp20zDrYZe1FX'})
    rankings = json.loads(info.text)
    ranklist1 = []
    for i in rankings['rankings']:
        ranklist1.append(i['team_key'])
    ranklist2 = []
    for str in ranklist1:
        new_str = str[3:]
        ranklist2.append(int(new_str))
    return ranklist2

#Finds the difference between the official and unofficial (personal) rank lists
def diff_in_rank(event_key, team, unofficial_rank):
    official = official_ranklist(event_key)
    unofficial = []
    for i in unofficial_rank:
        unofficial.append(i[0])
    official_index = official.index(team)
    unofficial_index = unofficial.index(team)
    return official_index - unofficial_index

#Gets the personalized rank list for an event
def get_ranklist(event_key):
    ranklist = {}
    tn = 1
    teamlist = team_list(event_key)
    for team in teamlist:
        print("Rank list: " + str(tn) + "/" + str(len(teamlist)) + " Done")
        ranklist[team] = rank_num(team, event_key)
        tn += 1
    return sorted(ranklist.items(), key=lambda x: x[1], reverse=True)

#Prints the rank list created
def print_ranklist(event_key):
    ranks = get_ranklist(event_key)
    print("------------------------------------------")
    count = 1
    for i in ranks:
        print(str(count) + ". " + str(i[0]) + " (Rank Num: " +  str(round(i[1],2)) + ")" + "(Climb Num: " + str(round(float(str(climb_num(i[0], event_key))),2)) + ")" + "(Teleop Num: " + str(round(float(str(teleop_num(i[0], event_key))),2)) + ")" + "(Auto Num: " + str(round(float(str(auto_num(i[0], event_key)), 2))) + ")" + " (Difference: " + str(diff_in_rank(event_key, i[0], ranks)) + ")")
        count += 1

#Gets the rank of a team from the data list
def data_rank(team, datalist):
    climb = datalist[team]['climb']
    auto = datalist[team]['auto_balls']
    teleop = datalist[team]['teleop_balls']
    return (0.4*teleop)+(0.4*climb)+(+0.2*auto) 
    
#Gets the ranklist of an event from the data list
def data_ranklist(event_key, datalist):
    ranklist = {}
    tn = 1
    teamlist = team_list(event_key)
    for team in teamlist:
        ranklist[team] = data_rank(team, datalist)
        tn += 1
    return sorted(ranklist.items(), key=lambda x: x[1], reverse=True)

#Prints the data list created rank list 
def print_data_ranks(ranks, datalist, event_key):
    print("------------------------------------------")
    count = 1
    for i in ranks:
        print(str(count) + ". " + str(i[0]) + " (Rank Num: " +  str(round(i[1],2)) + ")" + "(Climb Num: " + str(round(float(str(datalist[i[0]]['climb'])),2)) + ")" + "(Teleop Num: " + str(round(float(str(datalist[i[0]]['teleop_balls'])),2)) + ")" + "(Auto Num: " + str(round(float(str(datalist[i[0]]['auto_balls'])), 2)) + ")" + " (Difference: " + str(diff_in_rank(event_key, i[0], ranks)) + ")")
        count += 1
#----------------------------------------------------------------------------------------------------------------
#End of all functions for overall team or event
#----------------------------------------------------------------------------------------------------------------

datalist = data_list('2020cadm')
print(datalist)
print("--------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------")
print(data_ranklist('2020cadm', datalist))
print("--------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------")
print_data_ranks(data_ranklist('2020cadm', datalist), datalist, '2020cadm')