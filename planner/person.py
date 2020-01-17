class Person(object):
    def __init__(self, name, male):
        self.name = name
        self.male = male
        self.equipment = []
        self.food = []

    def food_weight(self):
        return sum(f['weight'] for f in self.food)

    def equipment_weight(self):
        return sum(e['weight'] for e in self.equipment)

    def total_weight(self):
        return self.food_weight() + self.equipment_weight

    def __repr__(self):
        return f"<Person: name: {self.name}>"

def parse_multiline_str(mline_str):
    """ Разбивает мультистроковую константу на слова """
    return set(filter(lambda x: len(x) > 0, map(lambda n: n.strip(), mline_str.split('\n'))))
