#!/usr/bin/env python3

import planner.food as F
import planner.equipment as E
import planner.utils as U

from members import *

# import products as P
# print("Еда.....................")
# food_table = F.food_planning(P.Food,
#                              NBreakfast=P.NBreakfast,
#                              NDinner=P.NDinner,
#                              NLunch=P.NLunch,
#                              NSnack=P.NSnack)

# print("------------------------")

print("Снаряжение..............")
import shared_equipment as S
stuff_table = E.equipment_planning(S.SharedEquipment); stuff_table

import numpy as np
avg_men_weight = np.mean([m.food_weight() + m.equipment_weight() for m in Members.values() if m.male])

U.print_grouped_by_members(stuff_table, 'shared_equipment.txt', print_screen=False)
