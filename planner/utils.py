import datetime

def print_overweight(members, get_weight, man_weight_norm, woman_weight_norm, caption=None):
    overweight = {}
    for name, member in sorted(members.items()):
        w = get_weight(member)
        if member.male:
            d = w - man_weight_norm
        else:
            d = w - woman_weight_norm
        overweight[name] = d

    worst_overweights = sorted(overweight.items(), key=lambda x:abs(x[1]), reverse=True)

    if caption is None:
        caption = 'Перевес'
    print('*** %s:' % caption)
    for n, d in worst_overweights:
        print("%-12s %5.0f %.0f" % (n, get_weight(members[n]), d))

    return overweight


def print_grouped_by_members(table, fname):
    for a, b in table.groupby(['Кто несет']):
            print("Участник: {}, несет: {}".format(a, b['weight'].sum()))
            print(str(b))
            print("\n\n")

    if not fname:
        return

    with open(fname, 'w') as f:
        f.write("Дата создания: {}\n\n".format(datetime.datetime.now()))
        for a, b in table.groupby(['Кто несет']):
            f.write("Участник: {}, несет: {}\n".format(a, b['weight'].sum()))
            f.write(str(b))
            f.write("\n\n")

        f.write("\nСводная таблица")
        f.write(str(table))
