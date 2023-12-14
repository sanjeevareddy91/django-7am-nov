from pprint import pprint as pp

def make_day(num_teams, day,teams_list):
    # using circle algorithm, https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
    assert not num_teams % 2, "Number of teams must be even!"
    # generate list of teams
    lst = teams_list
    # rotate
    day %= (num_teams - 1)  # clip to 0 .. num_teams - 2
    if day:                 # if day == 0, no rotation is needed (and using -0 as list index will cause problems)
        lst = lst[:1] + lst[-day:] + lst[1:-day]
    # pair off - zip the first half against the second half reversed
    half = num_teams // 2
    return list(zip(lst[:half], lst[half:][::-1]))

def make_schedule(teams_list):
    """
    Produce a double round-robin schedule
    """
    # number of teams must be even
    num_teams = len(teams_list)
    if num_teams % 2:
        num_teams += 1  # add a dummy team for padding

    # build first round-robin
    schedule = [make_day(num_teams, day,teams_list) for day in range(num_teams - 1)]
    # generate second round-robin by swapping home,away teams
    swapped = [[(away, home) for home, away in day] for day in schedule]

    return schedule + swapped

def main(list_of_teams):
    teams_list = list_of_teams
    schedule = make_schedule(teams_list)
    # pp(schedule)
    return schedule

# if __name__ == "__main__":
#     main()