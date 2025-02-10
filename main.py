from utils import funcs
minterms = funcs.parse_minterms()
print(minterms)
step_1 = funcs.step_1(minterms)
print(step_1)
step_2 = funcs.step_2(step_1)
print(step_2)