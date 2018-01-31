from django.shortcuts import render
import numpy as np


# TODO: Set criteria list from models?
CRITERIA_LIST = {'Criteria': {'Climate': ['Summer high',
                                          'Winter low',
                                          'Pollen',
                                          'Humidity'],
                              'Economic': ['Unemployment',
                                           'Crime rate',
                                           'Median income'],
                              'Social': ['Walkability',
                                         'Parkland']}}


def welcome(request):
    context = {}
    return(render(request, 'ahp/welcome.html', context))


def criteria(request):
    context = CRITERIA_LIST
    return(render(request, 'ahp/criteria.html', context))


def weights(request):
    selections = request.POST.getlist('selection')
    # request.session['selections'] = selections
    temp_list = [c for c in CRITERIA_LIST['Criteria']]
    top_comp = [(a, b) for a in temp_list
                for b in temp_list[temp_list.index(a) + 1:] if a != b]
    temp_list = [s for s in selections
                 if s in CRITERIA_LIST['Criteria']['Climate']]
    climate_comp = [(a, b) for a in temp_list
                    for b in temp_list[temp_list.index(a) + 1:] if a != b]
    temp_list = [s for s in CRITERIA_LIST['Criteria']['Economic']
                 if s in selections]
    economic_comp = [(a, b) for a in temp_list
                     for b in temp_list[temp_list.index(a) + 1:] if a != b]
    temp_list = [s for s in CRITERIA_LIST['Criteria']['Social']
                 if s in selections]
    social_comp = [(a, b) for a in temp_list
                   for b in temp_list[temp_list.index(a) + 1:] if a != b]

    comparisons = {'Top': top_comp,
                   'Climate': climate_comp,
                   'Economic': economic_comp,
                   'Social': social_comp}
    context = {'comparisons': comparisons}
    return(render(request, 'ahp/weights.html', context))


def results(request):
    results = request.POST.getlist('preference')
    # First element is CSRF token, so ignore.
    # Other elements should follow the pattern:
    # ['preferences', <criteria category>, <criteria>]
    # preferences = [k.split('.') for k in dict(request.POST).keys()][1:]
    preferences = {}
    for k in dict(request.POST):
        key_split = k.split('.')
        if len(key_split) == 1:
            continue
        category = key_split[1]
        pair = tuple(''.join(c for c in key_split[2]
                     if c not in "'() ").split(','))
        weight = int(dict(request.POST)[k][0])
        if category in preferences:
            preferences[category].append((pair, weight))
        else:
            preferences[category] = [(pair, weight)]
    weights = {}
    for cat in preferences:
        # TODO: Cleaner list comprehension for finding unique elements
        criteria = []
        for c in preferences[cat]:
            if c[0][0] not in criteria:
                criteria.append(c[0][0])
            if c[0][1] not in criteria:
                criteria.append(c[0][1])
        crit_to_indx = {val: indx for indx, val in enumerate(criteria)}
        indx_to_crit = {indx: val for indx, val in enumerate(criteria)}
        matrix = np.identity(len(criteria))
        for pair in preferences[cat]:
            row = crit_to_indx[pair[0][0]]
            col = crit_to_indx[pair[0][1]]
            matrix[row][col] = pair[1]
            if pair[1] != 0:
                matrix[col][row] = 1 / pair[1]
        matrix_norm = np.identity(len(criteria))
        for rindx, row in enumerate(matrix):
            for cindx, cell in enumerate(row):
                new_val = matrix[rindx][cindx] / matrix.sum(axis=0)[cindx]
                matrix_norm[rindx][cindx] = new_val
        matrix_weights = {c: 0 for c in criteria}
        for rindx, row in enumerate(matrix_norm):
            criteria = indx_to_crit[rindx]
            matrix_weights[criteria] = matrix_norm.mean(axis=1)[rindx]
        print(matrix)
        print(matrix_norm)
        print(matrix_weights)
        weights[cat] = matrix_weights
    # TODO: Values for options, calculate utility
    context = {'results': weights}
    return(render(request, 'ahp/results.html', context))
