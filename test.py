import difflib


def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


a = 'I need already finished appartment findsed'
b = 'finished'
fl = False
for i in a.split():
    if similarity(i, b) >= 0.8:
        fl = True