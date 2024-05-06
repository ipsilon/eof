import matplotlib.pyplot as plt

CALL_COST = 100


def legacy_call_gas(g):
    return g - g // 64 - CALL_COST


def eof_call_gas(r, g):
    return g - max(g // 64, r) - CALL_COST


def compute_max_depth(call_gas_fn, gas_limit):
    g = gas_limit
    depth = 0
    while g > 0:
        g = call_gas_fn(g)
        depth += 1
    return depth


retaineds = (0, 2300 // 2, 2300, 2 * 2300, 5000, 5000 * 3 // 2, 10000, 15000, 20000, 20000 * 3 // 2)
gas_limits = list(reversed((0.1, 0.5, 1, 2, 5, 30, 60, 120)))
depths = []

for gas_limit in gas_limits:
    gl = int(gas_limit * 1_000_000)
    depths.append([])
    dd = depths[len(depths) - 1]
    for r in retaineds:
        dd.append(compute_max_depth(lambda g: eof_call_gas(r, g), gl))

plt.figure(figsize=(12, 8))

for i, dd in enumerate(depths):
    line = plt.plot(retaineds, dd)
    plt.setp(line, label=f"{gas_limits[i]}M")

plt.xlabel("caller min retained gas")
plt.ylabel("max call depth")
plt.xticks(range(0, 30001, 2500))
plt.legend()
plt.grid(True)
plt.show()
