import planner.person as P

_women_str = \
"""
Карпова
Борохович
"""

_men_str = \
"""
Лебедев
Пименов
Василец
Покровский
Сальников
Качанов
Устинов
Клебан
"""

WomanFoodWeightNorm = 2000
WomanSharedEquipWeightNorm = 1200

Women = P.parse_multiline_str(_women_str)
Men = P.parse_multiline_str(_men_str)

assert len(Women.intersection(Men)) == 0

MembersList = Women.union(Men)

Members = {}
for m in MembersList:
    s = "%s = P.Person('%s', '%s' in Men); Members['%s'] = %s" % (m,m,m,m,m)
    exec(s)

NWomen = len(Women)
NMembers = len(Members)

print(sorted(MembersList))

print("Количество участников:", NMembers)
print("Среди них женщин:", NWomen)
