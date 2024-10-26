

def selection(population, score):
    population.remove(score.index(min(score)))
    score.remove(score.index(min(score)))
    population.remove(score.index(min(score)))
    score.remove(score.index(min(score)))
