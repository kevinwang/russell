#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2, sys

matches = []
schedule_page = None

def page_from_web(event_code):
    try:
        return urllib2.urlopen('http://www2.usfirst.org/2013comp/events/%s/schedulequal.html' % event_code).read()
    except urllib2.HTTPError, e:
        print 'Error loading event: %s' % str(e)

def page_from_file(filename):
    try:
        return open(filename).read()
    except IOError, e:
        print str(e)

def load_event(page):
    if page is None:
        return '...NAAAHT'

    global schedule_page
    schedule_page = page

    global matches
    matches = []

    soup = BeautifulSoup(page)

    rows = soup.find_all('tr', {'style': 'background-color:#FFFFFF;'})

    for row in rows:
        cols = [col.text for col in row.contents if col != '\n']
        matches.append({
            'time': cols[0],
            'number': int(cols[1]),
            'red_alliance': [int(cols[2]), int(cols[3]), int(cols[4])],
            'blue_alliance': [int(cols[5]), int(cols[6]), int(cols[7])]
        })

    return soup.title.text

def get_match(match_number):
    return filter(lambda match: match['number'] == match_number, matches)[0]

def matches_with_team(team_number):
    return filter(lambda match: team_number in match['red_alliance'] or team_number in match['blue_alliance'], matches)

def print_match(match):
    print 'Match %d - %s' % (match['number'], match['time'])
    print 'Red alliance:\t%d\t%d\t%d' % (match['red_alliance'][0], match['red_alliance'][1], match['red_alliance'][2])
    print 'Blue alliance:\t%d\t%d\t%d' % (match['blue_alliance'][0], match['blue_alliance'][1], match['blue_alliance'][2])


if __name__ == '__main__':
    print 'Russell the Scout by Kevin Wang'
    print 'Type \'help\' for help, ^D to exit'
    print

    try:
        print 'Loaded event %s' % load_event(page_from_web(sys.argv[1]))
    except IndexError:
        print 'No event specified; load an event using \'event <event code>\' before continuing'

    while True:
        try:
            cmd = raw_input('--> ').split()
        except EOFError:
            break
        except KeyboardInterrupt:
            print
            continue

        if len(cmd) == 0:
            continue

        cmd[0] = cmd[0].lower()

        if cmd[0] == 'event':
            print 'Loaded event %s' % load_event(page_from_web(cmd[1]))
        elif cmd[0] == 'load':
            print 'Loaded event %s' % load_event(page_from_file(cmd[1]))
        elif cmd[0] == 'match':
            if len(cmd) < 2:
                print 'Error: No match number specified'
                continue
            try:
                print_match(get_match(int(cmd[1])))
            except IndexError:
                print 'Error: Match not found'
        elif cmd[0] == 'team':
            try:
                team_matches = matches_with_team(int(cmd[1]))
                if len(team_matches) == 0:
                    print 'No matches found for Team %d' % int(cmd[1])
                    continue
                print 'Matches with Team %d' % int(cmd[1])
                for match in team_matches:
                    print
                    print_match(match)
            except IndexError:
                print 'Error: No team number specified'
        elif cmd[0] == 'save':
            if schedule_page is None:
                print 'Error: No event loaded'
                continue
            try:
                file = open(cmd[1], 'w')
                file.write(schedule_page)
                print 'Saved event to %s' % cmd[1]
            except IndexError:
                print 'Error: No filename specified'
            except IOError, e:
                print str(e)
        elif cmd[0] == 'help':
            print 'Commands:'
            print '    event <event_code> - Load event from web'
            print '    help - Display this message'
            print '    load <filename> - Load event from file'
            print '    match <match_num> - Show match details'
            print '    save <filename> - Save event to file'
            print '    team <team_num> - Show all matches with specified team'
        else:
            print 'Command does not exist; type \'help\' for help'
