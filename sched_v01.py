import pulp
import sys

# days of the week
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

# specials (standard, durations)
specials = {
    'PE': 30,
    'Art': 60,
    'Lab': 30,
}

# available slots (day, start, duration)
slots = [
    ('Mon', '0800', 30),
    ('Mon', '0900', 60),
]

# problem definition
model = pulp.LpProblem('Schedule', sense=pulp.LpMaximize)

# lp variables
assign = {
    (special, slot): pulp.LpVariable('%r in slot %r % (talk, slot), cat=pulp.LpBinary)
    for special in specials
    for slot in slots
}
# print(assign)

# constraints
# slot constraints
for slot in slots:
    
    # each slot assigned at most once
    model.addConstraint(sum(assign[(special, slot)] for special in specials) <= 1)
    
# special constraints
for special in specials:

    # all specials must be assigned
    model.addConstraint(sum(assign[(special, slot)] for slot in slots) == 1)
    
    # special durations must fit the slots
    model.addConstraint(sum(slot[2] * assign[(special, slot)] for slot in slots) == specials[special])
