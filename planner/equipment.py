from collections import Counter
import pandas as pd
import numpy as np

from .person import Person
from .utils import print_overweight

from members import *

def equipment_planning(SharedEquipment):
    names_counter = Counter()
    undistributed = []
    total_weight = 0.0

    for m in Members.values():
        m.equipment.clear()

    tbl = []

    for row in SharedEquipment:
        ename = row[0]
        weight = float(row[2])
        total_weight += weight

        assert len(row) == 3 or len(row) == 4
        names_counter[ename] += 1
        assert names_counter[ename] <= 1

        if len(row) == 3:
            undistributed.append(row)

        else:
            member = row[3]
            assert member.name in MembersList
            member.equipment.append({'kind': 'equipment', 'weight': weight, 'name': ename, 'owner': row[1]})
            tbl.append({'equipment': ename, 'weight': weight, 'Кто несет': member.name})

    print("Общий вес: %.0f" % total_weight)

    males = list(filter(lambda m: m.male, Members.values()))
    females = list(filter(lambda m: not m.male, Members.values()))
    
    cur_weight = np.sum([m.equipment_weight() for m in Members.values()])
    total_man_weight = np.sum([m.equipment_weight() for m in males])
    avg_man_weight = total_man_weight / len(males)
    avg_woman_weight = np.mean([m.equipment_weight() for m in females])

    normal_man_weight = (total_man_weight - WomanSharedEquipWeightNorm*len(females)) / len(males)
    assert normal_man_weight >= WomanSharedEquipWeightNorm
    
    print("Средний вес на мужчину: %.0f" % avg_man_weight)
    print("Норма на мужчину: %.0f" % normal_man_weight)
    print("Средний вес на женщину: %.0f\n" % avg_woman_weight)
    print("Норма на женщину: %.0f\n" % WomanSharedEquipWeightNorm)
    print()
    print_overweight(Members, Person.equipment_weight, normal_man_weight, WomanSharedEquipWeightNorm, caption='Перевес по снаряжени')

    print("\nОстаток: %.0f\n" % (total_weight - cur_weight))
    table = pd.DataFrame(data=tbl)
    return table
