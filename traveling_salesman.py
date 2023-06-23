import numpy as np
import math
import matplotlib.collections as mc
import matplotlib.pylab as pl

random_seed = 1729

np.random.seed(random_seed)

N = 40
x = np.random.rand(N)
y = np.random.rand(N)

points = zip(x, y)
cities = list(points)

itinerary = list(range(0, N))


def gen_lines(cities, itinerary):
    lines = []
    for i in range(0, len(itinerary) - 1):
        lines.append([cities[itinerary[i]], cities[itinerary[i + 1]]])
    return (lines)


def pitagoras_distance(lines):
    distance = 0
    for i in range(0, len(lines)):
        distance += math.sqrt(abs(lines[i][1][0] - lines[i][0][0])
                              ** 2 + abs(lines[i][1][1] - lines[i][0][1]) ** 2)
    return (distance)


total_distance = pitagoras_distance(gen_lines(cities, itinerary))


def plotitinerary(cities, itin, plottitle, thename):
    N = 40
    x = np.random.rand(N)
    y = np.random.rand(N)
    lc = mc.LineCollection(gen_lines(cities, itin), linewidths=2)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    pl.scatter(x, y)
    pl.title(plottitle)
    pl.xlabel("Współrzędna X")
    pl.ylabel("Współrzędna Y")
    pl.savefig(str(thename) + ".png")
    pl.close()


plotitinerary(cities, itinerary,
              "The problem of the Salesman - a random itinerary", "itinerary1")


def find_nearest(cities, idx, nn_itinerary):
    point = cities[idx]
    min_distance = float("inf")
    min_idx = -1

    for i in range(0, len(cities)):
        distance = math.sqrt((point[0] - cities[i][0])
                             ** 2 + (point[1] - cities[i][1]) ** 2)

        if distance < min_distance and distance > 0 and i not in nn_itinerary:
            min_distance = distance
            min_idx = i
    return min_idx


def k_nn(cities, N):
    nn_itinerary = [0]

    for i in range(0, N-1):
        min_idx = find_nearest(
            cities, nn_itinerary[len(nn_itinerary)-1], nn_itinerary)
        nn_itinerary.append(min_idx)
    return nn_itinerary


k_nn_itineraru = k_nn(cities, N)
total_distance = pitagoras_distance(gen_lines(cities, k_nn_itineraru))

plotitinerary(cities, k_nn_itineraru,
              "The problem of the Salesman - KNN itinerary", "itinerary2")

# we have a huge improvement in the score compared to the random itinerary
# We optimized our path through the k nearest neighbor algorithm :)


# ------------------- Simulated annealing ------------------------

def random_improve(itinerary, itinerary2):
    small = 1
    big = 5

    tempinin = itinerary[small:big]
    del (itinerary2[small:big])
    neighborids3 = math.floor(np.random.rand() * len(itinerary))

    for i in range(0, len(tempinin)):
        itinerary2.insert(neighborids3+i, tempinin[i])

    return itinerary2


def pertub_sa(cities, itinerary, time, max_itin):
    global min_distance
    global min_itinerary
    global min_idx

    neighborids1 = math.floor(np.random.rand() * (len(itinerary)))
    neighborids2 = math.floor(np.random.rand() * (len(itinerary)))

    itinerary2 = itinerary.copy()

    random_draw2 = np.random.rand()
    small = min(neighborids1, neighborids2)
    big = max(neighborids1, neighborids2)

    if (random_draw2 >= 0.55):
        itinerary2[small:big] = itinerary2[small:big][::-1]

    elif (random_draw2 < 0.45):
        itinerary2 = random_improve(itinerary, itinerary2)
    else:
        itinerary2[neighborids1] = itinerary[neighborids2]
        itinerary2[neighborids2] = itinerary[neighborids1]

    distance1 = pitagoras_distance(gen_lines(cities, itinerary))
    distance2 = pitagoras_distance(gen_lines(cities, itinerary2))

    itinerary_to_return = itinerary.copy()

    random_draw = np.random.rand()
    temperature = 1/((time/1000) + 1)

    scale = 3.5

    print(temperature)
    if ((distance2 > distance1 and (random_draw) < (
        math.exp(scale * (distance1 - distance2)) * temperature)) or (
            distance1 > distance2)):
        itinerary_to_return = itinerary2.copy()


# If a long time interval elapses,
#  and we do not manage to find a better solution than the one saved,
#  which corresponds to the minimum distance,
# then we can conclude that all the changes made during this time,
#  was not beneficial and return to the one made earlier

    reset = True
    reset_thresh = 0.04

    if (reset and (time - min_idx) > (max_itin * reset_thresh)):
        itinerary_to_return = min_itinerary
        min_idx = time

    if (pitagoras_distance(gen_lines(cities, itinerary_to_return)) < min_distance):
        min_distance = pitagoras_distance(gen_lines(cities, itinerary2))
        min_itinerary = itinerary_to_return
        min_idx = time

    if (abs(time - max_itin) <= 1):
        itinerary_to_return = min_itinerary.copy()

    return (itinerary_to_return.copy())


def simulated_annealing(cities, itinerary):
    global min_distance
    global min_itinerary
    global min_idx

    new_itinerary_sa = itinerary.copy()

    min_distance = pitagoras_distance(gen_lines(cities, itinerary))
    min_itinerary = itinerary
    min_idx = 0

    max_itin = len(itinerary) * 5000
    for time in range(0, max_itin):
        new_itinerary_sa = pertub_sa(cities, new_itinerary_sa, time, max_itin)

    total = pitagoras_distance(gen_lines(cities, new_itinerary_sa))
    print(f"Your distance is: {total}")
    return new_itinerary_sa


siman_itinerary = simulated_annealing(cities, itinerary)


plotitinerary(cities, siman_itinerary,
              "The problem of the salesman - Simulated Annealing", "itinerary3")
