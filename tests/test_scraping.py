import random

from hypothesis import given
from hypothesis.strategies import dictionaries
from hypothesis.strategies import floats
from hypothesis.strategies import from_regex
from hypothesis.strategies import text

import setbot

@given(from_regex(r'.*\d hours \d\d minutes and \d\d\.\d\d\d seconds.*', fullmatch=False))
def test_match_h_m_s(time):
    match = setbot.match_score(time)
    assert match, "no match"
    assert match.group('h'), "hours not matched"
    assert match.group('m'), "minutes not matched"
    assert match.group('s'), "seconds not matched"
    time = '0 hours 00 minutes and 23.916 seconds'
    match = setbot.match_score(time)
    assert match, "no match"
    assert match.group('h'), "hours not matched"
    assert match.group('m'), "minutes not matched"
    assert match.group('s'), "seconds not matched"
    assert match.group('h') == '0', "hours match incorrect"
    assert match.group('m') == '00', "minutes match incorrect"
    assert match.group('s') == '23.916', "seconds match incorrect"

@given(from_regex(r'.*\d\d minutes and \d\d\.\d\d\d seconds.*', fullmatch=False))
def test_match_m_s(time):
    match = setbot.match_score(time)
    assert match, "no match"
    assert not match.group('h'), "hours matched"
    assert match.group('m'), "minutes not matched"
    assert match.group('s'), "seconds not matched"
    time = '00 minutes and 23.916 seconds'
    match = setbot.match_score(time)
    assert match, "no match"
    assert not match.group('h'), "hours matched"
    assert match.group('m'), "minutes not matched"
    assert match.group('s'), "seconds not matched"
    assert match.group('m') == '00', "minutes match incorrect"
    assert match.group('s') == '23.916', "seconds match incorrect"

@given(from_regex(r'.*\d\d\.\d\d\d seconds.*', fullmatch=False))
def test_match_s(time):
    match = setbot.match_score(time)
    assert match, "no match"
    assert not match.group('h'), "hours matched"
    assert not match.group('m'), "minutes matched"
    assert match.group('s'), "seconds not matched"
    time = '23.916 seconds'
    match = setbot.match_score(time)
    assert match, "no match"
    assert not match.group('h'), "hours matched"
    assert not match.group('m'), "minutes matched"
    assert match.group('s'), "seconds not matched"
    assert match.group('s') == '23.916', "seconds match incorrect"

@given(from_regex(r'.*\d hours \d\d minutes and \d\d\.\d\d\d seconds.*', fullmatch=False))
def test_parse_h_m_s(time):
    score = setbot.parse_score(setbot.match_score(time))
    assert score is not None
    assert score >= 0.0
    assert score <= 38439.999
    time = '1 hours 01 minutes and 01.000 seconds'
    match = setbot.match_score(time)
    assert setbot.parse_score(match) == 3661.0

@given(from_regex(r'.*\d\d minutes and \d\d\.\d\d\d seconds.*', fullmatch=False))
def test_parse_m_s(time):
    score = setbot.parse_score(setbot.match_score(time))
    assert score is not None
    assert score >= 0.0
    assert score <= 6039.999
    time = '01 minutes and 01.000 seconds'
    match = setbot.match_score(time)
    assert setbot.parse_score(match) == 61.0

@given(from_regex(r'.*\d\d\.\d\d\d seconds.*', fullmatch=False))
def test_parse_s(time):
    score = setbot.parse_score(setbot.match_score(time))
    assert score is not None
    assert score >= 0.0
    assert score <= 99.999
    time = '17.000 seconds'
    match = setbot.match_score(time)
    assert setbot.parse_score(match) == 17.0

@given(from_regex(setbot.set_score_regex, fullmatch=False))
def test_regex_matching(set_score):
    assert setbot.match_score(set_score)

@given(from_regex(setbot.set_score_regex, fullmatch=False))
def test_regex_parsing(set_score):
    score = setbot.parse_score(setbot.match_score(set_score))
    assert score is not None
    assert score >= 0.0

def test_empty_leaderboard():
    leaderboard = setbot.create_leaderboard({})
    assert leaderboard == 'LEADERBOARD :trophy:\n'

def test_leaderboard_one():
    leaderboard = setbot.create_leaderboard({'Warbler': 14.872})
    assert leaderboard == ('LEADERBOARD :trophy:\n'
                  ':first_place_medal:: <@Warbler> (14.872s)\n')

def test_leaderboard_two_nosort():
    leaderboard = setbot.create_leaderboard({'Warbler': 14.872,
                                             'Trogon': 17.912})
    assert leaderboard == ('LEADERBOARD :trophy:\n'
                  ':first_place_medal:: <@Warbler> (14.872s)\n'
                  ':second_place_medal:: <@Trogon> (17.912s)\n')

def test_leaderboard_two_sort():
    leaderboard = setbot.create_leaderboard({'Trogon': 17.912,
                                             'Warbler': 14.872})
    assert leaderboard == ('LEADERBOARD :trophy:\n'
                  ':first_place_medal:: <@Warbler> (14.872s)\n'
                  ':second_place_medal:: <@Trogon> (17.912s)\n')

def test_leaderboard_three_nosort():
    leaderboard = setbot.create_leaderboard({'Warbler': 14.872,
                                             'Trogon': 17.912,
                                             'Crane': 23.179})
    assert leaderboard == ('LEADERBOARD :trophy:\n'
                  ':first_place_medal:: <@Warbler> (14.872s)\n'
                  ':second_place_medal:: <@Trogon> (17.912s)\n'
                  ':third_place_medal:: <@Crane> (23.179s)\n')

def test_leaderboard_three_sort():
    leaderboard = setbot.create_leaderboard({'Crane': 23.179,
                                             'Trogon': 17.912,
                                             'Warbler': 14.872})
    assert leaderboard == ('LEADERBOARD :trophy:\n'
                  ':first_place_medal:: <@Warbler> (14.872s)\n'
                  ':second_place_medal:: <@Trogon> (17.912s)\n'
                  ':third_place_medal:: <@Crane> (23.179s)\n')

def test_leaderboard_many_nosort():
    leaderboard = setbot.create_leaderboard({'Warbler': 14.872,
                                             'Trogon': 17.912,
                                             'Crane': 23.179,
                                             'Lapwing': 56.152,
                                             'Thrush': 142.198})
    assert leaderboard == ('LEADERBOARD :trophy:\n'
                  ':first_place_medal:: <@Warbler> (14.872s)\n'
                  ':second_place_medal:: <@Trogon> (17.912s)\n'
                  ':third_place_medal:: <@Crane> (23.179s)\n')

def test_leaderboard_many_sort():
    leaderboard = setbot.create_leaderboard({'Lapwing': 56.152,
                                             'Thrush': 142.198,
                                             'Crane': 23.179,
                                             'Trogon': 17.912,
                                             'Warbler': 14.872})
    assert leaderboard == ('LEADERBOARD :trophy:\n'
                  ':first_place_medal:: <@Warbler> (14.872s)\n'
                  ':second_place_medal:: <@Trogon> (17.912s)\n'
                  ':third_place_medal:: <@Crane> (23.179s)\n')

@given(dictionaries(text(), floats(min_value=0.0, allow_nan=False, allow_infinity=False)))
def test_leaderboard_sort(times):
    times2 = {}
    keys2 = list(times.keys())
    random.shuffle(keys2)
    for k in keys2:
        times2[k] = times[k]
    #assert setbot.create_leaderboard(times) == setbot.create_leaderboard(times2)
