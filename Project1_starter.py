import ast

def makeSchedule(person1_busy_Schedule, person1_work_hours, person2_busy_Schedule, person2_work_hours, duration_of_meeting):
    updatePerson1 = fixSchedule(person1_busy_Schedule, person1_work_hours)
    updatePerson2 = fixSchedule(person2_busy_Schedule, person2_work_hours)
    mergedSchedule = combineSchedules(updatePerson1, updatePerson2)
    sortedSchedulesResult = sortSchedules(mergedSchedule)
    availabilities = matchedAvailabilities(sortedSchedulesResult, duration_of_meeting)
    return availabilities

def fixSchedule(Schedule, p1_work_hours):
    updatedSchedule = Schedule[:]
    newWorkHours = p1_work_hours[:]
    
    # Convert strings to lists of time intervals
    updatedSchedule = convertStringToList(updatedSchedule)
    newWorkHours = convertStringToList(newWorkHours)
    
    # Add the start and end of the workday
    updatedSchedule.insert(0, ['0:00', newWorkHours[0]])  
    updatedSchedule.append([newWorkHours[1], '23:59'])  
    return updatedSchedule

def convertStringToList(schedule_string):
    # If the input is already a list, return it
    if isinstance(schedule_string, list):
        return schedule_string
    
    # Replace invalid quotation marks and evaluate the string as a list
    schedule_string = schedule_string.replace('‘', "'").replace('’', "'")
    return ast.literal_eval(schedule_string)


def combineSchedules(person1_busy_Schedule, person2_busy_Schedule):
    merged = [[0,0]]
    i, j = 0, 0

    person1_busy_ScheduleMinutes = convertListToMinutes(person1_busy_Schedule)
    person2_busy_ScheduleMinutes = convertListToMinutes(person2_busy_Schedule)

    while i < len(person1_busy_ScheduleMinutes) and j < len(person2_busy_ScheduleMinutes):
        meeting1, meeting2 = person1_busy_ScheduleMinutes[i], person2_busy_ScheduleMinutes[j]
        if meeting1[0] <= meeting2[0]:
            if meeting1[1] > merged[-1][1]:
                merged.append(meeting1)
            i += 1
        else:
            if meeting2[1] > merged[-1][1]:
                merged.append(meeting2)
            j += 1
    while i < len(person1_busy_ScheduleMinutes):
        meeting1 = person1_busy_ScheduleMinutes[i]
        if meeting1[1] > merged[-1][1]:
            merged.append(meeting1)
        i += 1
    while j < len(person2_busy_ScheduleMinutes):
        meeting2 = person2_busy_ScheduleMinutes[j]
        if meeting2[1] > merged[-1][1]:
            merged.append(meeting2)
        j += 1
    return merged

def sortSchedules(Schedule):
    possibleAvailabilities = []
    index = 0
    while index < (len(Schedule) - 1):
        if Schedule[index][1] < Schedule[index + 1][0]:
            possibleAvailabilities.append([Schedule[index][1], Schedule[index + 1][0]])
        index += 1
    return possibleAvailabilities

def matchedAvailabilities(Schedule, duration_of_meeting):
    availabilities = []
    for possible_availability in Schedule:
        if possible_availability[1] - possible_availability[0] >= int(duration_of_meeting):
            availabilities.append(possible_availability)
    return availabilities

def convertToMinutes(time):
    if ':' not in str(time):
        return 0

    hours, minutes = time.split(':')
    hours = int(hours)
    minutes = int(minutes)

    return hours * 60 + minutes

def convertListToMinutes(schedule_list):
    scheduleMinutes = []
    for plan in schedule_list:
        minutesPlan = []
        for bound in plan:
            minutesPlan.append(convertToMinutes(bound))
        scheduleMinutes.append(minutesPlan)
    return scheduleMinutes

def minutesToHours(minutes):
    hours = minutes // 60
    mins = minutes % 60
    toString = str(hours)
    toStringMins = "0" + str(mins) if mins < 10 else str(mins)
    return toString + ":" + toStringMins

def main():
    try:
        with open('input.txt', 'r') as file:
            lines = [line.strip() for line in file]

        # Iterate over the list of lines and process each test case
        for line_index in range(0, len(lines), 6):
            # Extract the data for the current test case
            person1_busy_Schedule = lines[line_index].replace("person1_busy_Schedule = ", "")
            person1_work_hours = lines[line_index + 1].replace("person1_work_hours = ", "")
            person2_busy_Schedule = lines[line_index + 2].replace("person2_busy_Schedule = ", "")
            person2_work_hours = lines[line_index + 3].replace("person2_work_hours = ", "")
            duration_of_meeting = lines[line_index + 4].replace("duration_of_meeting = ", "")

            # Generate the availability schedule for the current test case
            whenToMeet = makeSchedule(person1_busy_Schedule, person1_work_hours, person2_busy_Schedule, person2_work_hours, duration_of_meeting)

            # Write the availability schedule for the current test case to the output file
            with open('output.txt', 'a') as output_file:
                output_file.write(f"Test case {line_index // 6 + 1}:\n")
                for availability in whenToMeet:
                    output_file.write(f"Available from {minutesToHours(availability[0])} to {minutesToHours(availability[1])}\n")
                output_file.write("\n")

    except Exception as e:
        print(f"Error processing input file: {e}")

if __name__ == '__main__':
    main()