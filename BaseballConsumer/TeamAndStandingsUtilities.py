def get_division_for_teamId(teamId):
    if teamId in [144, 146, 121, 143, 120]: return 'nle'
    if teamId in [112, 113, 158, 134, 138]: return 'nlc'
    if teamId in [109, 115, 119, 135, 137]: return 'nlw'
    if teamId in [110, 111, 147, 139, 141]: return 'ale'
    if teamId in [145, 114, 116, 118, 142]: return 'alc'
    if teamId in [117, 108, 133, 136, 140]: return 'alw'
    return 'no division for teamId: {}'.format(teamId)
