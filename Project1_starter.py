import sys
import ast

def createWorkingSchedule (person1_busy_Schedule, person1_work_hours, person2_busy_Schedule, person2_work_hours, duration_of_meeting):

    updatePerson1 = updateSchedule(person1_busy_Schedule, person1_work_hours)
    updatePerson2 = updateSchedule(person2_busy_Schedule, person2_work_hours)
    mergedSchedule = mergeSchedules(updatePerson1, updatePerson2)
    sortedSchedules = sortedSchedules(mergedSchedule)
    print (matchedAvailabilities(sortedSchedules,duration_of_meeting))

def updateSchedule(Schedule, p1_work_hours):
    updatedSchedule = Schedule[:]  
    newWorkHours = p1_work_hours[:]

    updatedSchedule = convert_to_data(updatedSchedule)
    newWorkHours = convert_to_data(newWorkHours)
    
    updatedSchedule.insert(0, ['0:00', newWorkHours[0]])  
    updatedSchedule.append([newWorkHours[1], '23:59'])  
    return updatedSchedule

def convert_to_data(schedule_string):
    schedule = schedule_string[:]
    schedule = schedule.replace('‘','\'')
    schedule = schedule.replace('’','\'')  
    schedule = ast.literal_eval(schedule)
    return schedule

def mergeSchedules(person1_busy_Schedule, person2_busy_Schedule):
    merged =[[0,0]]
    i,j =0,0

    person1_busy_ScheduleMinutes = convertListToMinutes(person1_busy_Schedule)
    person2_busy_ScheduleMinutes = convertListToMinutes(person2_busy_Schedule)

    while i < len(person1_busy_ScheduleMinutes) and j< len(person2_busy_ScheduleMinutes):
        meeting1, meeting2 =person1_busy_ScheduleMinutes[i], person2_busy_ScheduleMinutes[j]
        if meeting1[0]<= meeting2[0]:
            if meeting1[1] > merged[-1][1]:
                merged.append(meeting1)
            i+=1
        else:
            if meeting2[1] > merged[-1][1]:
                merged.append(meeting2)
            j+=1
    while i< len(person1_busy_ScheduleMinutes):
        meeting1 = person1_busy_ScheduleMinutes[i]
        if meeting1[1] > merged[-1][1]:
            merged.append(meeting1)
        i+=1
    while j< len(person2_busy_ScheduleMinutes):
        meeting2 = person2_busy_ScheduleMinutes[j]
        if meeting2[1] > merged[-1][1]:
            merged.append(meeting2)
        j+=1
    return merged

def sortedSchedules (Schedule):
    '''finds all of the possible availabilities in the schedules'''
    possibleAvailabilities = []
    index = 0
    while index < (len(Schedule) - 1):
        if Schedule[index][1] < Schedule[index + 1][0]:
            possibleAvailabilities.append([Schedule[index][1], Schedule[index + 1][0]])
            index+=1
        else:
            index+=1
    return possibleAvailabilities

    
def matchedAvailabilities(Schedule, duration_of_meeting):
    availabilities=[]
    for possible_availability in Schedule:
        if possible_availability[1] - possible_availability[0] >= int(duration_of_meeting):
            availabilities.append(possible_availability)

    availabilities_reconverted =  []
    for plan in availabilities:
        hoursPlan = []
        for bound in plan:
            hoursPlan.append(minToHour(bound))
        availabilities_reconverted.append(hoursPlan)

    return availabilities_reconverted

def convertToMinutes(time):
    hours, minutes = list(map(int, time.split(":")))
    return hours * 60 + minutes

def convertListToMinutes(schedule_list):
    '''converts a 2d list of a time schedule into minutes'''
    scheduleMinutes = [] 
    for plan in schedule_list:
        minutesPlan = []
        for bound in plan:
            minutesPlan.append(convertToMinutes(bound))
        scheduleMinutes.append(minutesPlan)
    return scheduleMinutes

def minToHour(minutes):
    hours = minutes // 60
    mins = minutes% 60
    toString = str(hours)
    toStringMins = "0" + str(mins) if mins< 10 else str(mins)
    return toString +":" + toStringMins

def main():
    person1_busy_Schedule = input("Person 1 schedule: ")
    person2_busy_Schedule = input("Person 2 schedule: ")
    person1_work_hours = input("Person 1 availability: ")
    person2_work_hours = input("Person 2 availability: ")
    duration_of_meeting = input("Meeting duration: ")
    whenToMeet = createWorkingSchedule(person1_busy_Schedule, person1_work_hours, person2_busy_Schedule, person2_work_hours,duration_of_meeting )

if __name__ == '__main__':
    main()