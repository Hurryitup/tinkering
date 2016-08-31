'''
Tour guide scheduler for Tufts University
Created: 8/31/2016
Copyright: Aditya Hurry
'''

import numpy
import pandas

''' Constants '''
location = r'/Users/adityahurry/Documents/compSci/tinkering/schedule-maker/scheduling-responses.csv'
shortLocation = 'scheduling-responses.csv'
one_upto3Specials = "1(2-3)"
one_5specials = "1(5)"
zero_5specials = "5SP"
two_noSpecials = "2"
slotNames = ['Monday Morning', 'Monday Afternoon', 'Tuesday Morning', 'Tuesday Afternoon', 'Wednesday Morning',
             'Wednesday Afternoon', 'Thursday Morning', 'Thursday Afternoon', 'Friday Morning', 'Friday Afternoon',
             'Saturday Morning', 'Saturday Afternoon']
inorder_slotnames = ['Monday Morning', 'Monday Afternoon', 'Tuesday Morning', 'Tuesday Afternoon', 'Wednesday Morning',
             'Wednesday Afternoon', 'Thursday Morning', 'Thursday Afternoon', 'Friday Morning', 'Friday Afternoon',
             'Saturday Morning', 'Saturday Afternoon']
numpy.random.shuffle(slotNames)
tours_per_week = "tours_per_week"
slots = {}
num_per_slot = 3
for slot in slotNames:
    slots[slot] = num_per_slot

''' Utility functions '''


def derive_not_chosen_list():
    chosen_people = []
    for slot in people_for_slot:
        for person in people_for_slot[slot]:
            if person.values[0] not in chosen_people:
                chosen_people.append(person.values[0])

    print "\nChosen\n"
    print len(chosen_people)
    # print chosen_people

    not_chosen = data[~data['Name'].isin(chosen_people)]

    print "\nNot chosen\n"
    print len(not_chosen.index)
    # print not_chosen.Name.values

    return not_chosen


def normalize_preferences(x):
    if x == one_upto3Specials:
        return 1
    elif x == zero_5specials:
        return 0
    elif x == one_5specials:
        return 1
    elif x == two_noSpecials:
        return 2
    else:
        return numpy.nan


''' Data Manipulation '''
data = pandas.read_csv(location)
data = data[data["Name"].notnull()]
data = data[data["Name"] != "Blah"]
data[tours_per_week] = data['Scheduling Preferences'].map(normalize_preferences)
data = data[data[tours_per_week] > 0]
people_for_slot = {}
people_tpw_tracker = {}


def select_random_person(slot_people, slot):
    person = slot_people.ix[numpy.random.choice(slot_people.index, 1)]
    person_name = person.Name.values[0]
    person_tpw = person.tours_per_week.values[0]
    people_tpw_tracker[person_name] = people_tpw_tracker[
                                          person_name] - 1 if person_name in people_tpw_tracker else person_tpw
    if people_tpw_tracker[person_name] > 0:
        try:
            people_for_slot[slot].append(person['Name'])
        except KeyError:
            people_for_slot[slot] = [person['Name']]
        finally:
            people_tpw_tracker[person_name] -= 1


def distribute_people(people, limit_per_slot=True):
    for slot in slotNames:
        slot_people = people[people[slot] == "Yes"]
        if len(slot_people.index) == 0:
            continue
        tries_remaining = 1000
        if limit_per_slot:
            while slots[slot] > 0 and tries_remaining > 0:
                select_random_person(slot_people, slot)
                tries_remaining -= 1
                slots[slot] -= 1
        else:
            select_random_person(slot_people, slot)


'''
Process:
    - first round of distributions:
        - select people who are free for a slot
        - randomly select one to add to the slot
        - continue until all positions in a slot are filled
        - repeat for remaining slots
    - following round of distributions:
        - derive number of people that haven't yet been chosen
        - if there are people that haven't been chosen:
            - from not_chosen, select people who are free for a given slot
            - randomly select a person and add them to the positions in a slot
            - re-derive the not_chosen list
        - repeat above two steps until the not_chosen list is empty
'''
def create_schedule():
    distribute_people(data)

    not_chosen = derive_not_chosen_list()
    while len(not_chosen.index) > 0:
        distribute_people(not_chosen, limit_per_slot=False)
        not_chosen = derive_not_chosen_list()

    for slot in inorder_slotnames:
        print slot
        print people_for_slot[slot]


if __name__ == '__main__':
    create_schedule()