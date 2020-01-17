import numpy as np
import pandas as pd
import datetime
from collections import Counter

from .person import Person
from .utils import print_overweight

from members import *


def food_planning(food, NBreakfast, NDinner, NLunch, NSnack):
    names_counter = Counter()
    total_weight = 0

    for m in Members.values():
        m.food.clear()

    tbl = []

    for row in food:
        pname = row[0]
        one_portion_weight = float(row[1])
        portion_weight = one_portion_weight * NMembers
        times = float(row[2])
        weight = portion_weight * times
        total_weight += weight

        assert len(row) == 3 or len(row) == 4
        names_counter[pname] += 1
        assert names_counter[pname] <= 1, 'Repeating product %s' % pname

        if len(row) == 3 or row[3] is None:
            tbl.append({'product': pname,
                    'portion': portion_weight,
                    'times': times,
                    'weight': weight})

        else:
            if isinstance(row[3], Person):
                member = row[3]
                assert member.name in MembersList
                member.food.append({'kind' : 'food', 'packing_weight': portion_weight,
                                    'weight' : weight, 'name' : pname})

                tbl.append(
                    {'product': pname,
                    'portion': portion_weight,
                    'times': times,
                    'weight': weight, 'Кто несет': member.name})
            else:
                members, ks = row[3]
                assert np.sum(ks) - times < 1e-9, f"more pieces than feeding times for {row}"
                assert len(members) == len(ks)
                assert len(members) > 1

                for member, k in zip(members, ks):
                    assert member.name in MembersList
                    member.food.append({'kind' : 'food', 'packing_weight': portion_weight,
                                        'weight' : portion_weight * k, 'name' : pname})

                    tbl.append({'product': pname,
                                'portion': portion_weight,
                                'times': k,
                                'weight': portion_weight * k, 'Кто несет': member.name})

                if np.sum(ks) < times - 1e-9:
                    # Есть нераспределенное снаряжение
                    tbl.append({'product': pname,
                                'portion': portion_weight,
                                'times': times - np.sum(ks),
                                'weight': portion_weight * (times - np.sum(ks))})

    cur_weight = np.sum([m.food_weight() for m in Members.values()])

    avg_man_weight = np.mean([m.food_weight() for m in Members.values() if m.male])
    avg_woman_weight = np.mean([m.food_weight() for m in Members.values() if not m.male])

    print("Общий вес: %f" % total_weight)
    print("Распределенный вес: %f" % cur_weight)

    print("Средний вес на мужчину: %.1f" % avg_man_weight)
    print("Средний вес на женщину: %.1f" % avg_woman_weight)
    print("Вес на человека в день: %.1f" % (total_weight / NMembers / ((NBreakfast + NDinner + NSnack + NLunch) / 4)))
    print()
    print_overweight(Members, P.Person.food_weight, avg_man_weight, WomanFoodWeightNorm, caption='Перевес по еде')

    print("\nОстаток: %.1f" % (total_weight - cur_weight))

    table = pd.DataFrame(data=tbl)
    return table


def group_by_members(table, fname=None):
    for a, b in table.groupby(['Кто несет']):
            print("Участник: {}, несет: {}".format(a, b['weight'].sum()))
            print(str(b))
            print("\n\n")

    if fname is not None:
        with open(fname, 'w') as f:
            f.write("Дата создания: {}\n\n".format(datetime.datetime.now()))
            for a, b in table.groupby(['Кто несет']):
                f.write("Участник: {}, несет: {}\n".format(a, b['weight'].sum()))
                f.write(str(b))
                f.write("\n\n")

            f.write("\nСводная таблица\n")
            f.write(str(table))
