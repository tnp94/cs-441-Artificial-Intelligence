# Thomas Pollard
# Programming 2
# CS441 Artificial Intelligence
# Winter 2021


"""
EXAMPLE SOLUTIONS FOUND:
[6, 4, 1, 5, 8, 2, 7, 3]
[5, 3, 1, 7, 2, 8, 6, 4]
[2, 7, 1, 4, 2, 8, 6, 3]
[4. 2. 8. 5. 7. 1. 3. 6.]
[6. 4. 1. 5. 6. 2. 7. 3.]
[4. 2. 7. 5. 1. 8. 6. 3.]
[6. 3. 7. 2. 8. 5. 1. 4.]
[6. 2. 7. 1. 4. 8. 5. 3.]
[6. 4. 7. 1. 8. 2. 5. 3.]
[2. 8. 6. 1. 3. 5. 7. 4.]
[5. 2. 4. 6. 8. 3. 1. 7.]
[2. 7. 5. 8. 1. 4. 6. 3.]
[2. 5. 7. 4. 1. 8. 6. 3.]
"""

import random
import math
import numpy as np

POPULATION_SIZE = 100
NUM_ITERATIONS = 500
MUTATE_CHANCE = .01
SOLUTIONS = {}

def randomChromosome():
  genes = np.zeros(8)
  for i in range(8):
    genes[i] = random.randint(1,8)
  return genes

def makeBabies(parent1, parent2, epoch):
  babies = []
  crossPoint = random.randint(1,7)
  #print("Crossing at", crossPoint)
  baby1Genes = np.zeros(8)
  baby2Genes = np.zeros(8)
  for i in range(8):
    if i < crossPoint:
      baby1Genes[i] = parent1.genes[i]
      baby2Genes[i] = parent2.genes[i]
    else:
      baby1Genes[i] = parent2.genes[i]
      baby2Genes[i] = parent1.genes[i]
  baby1 = eightQueensIndividual(baby1Genes, epoch)
  baby1.mutate()
  babies.append(baby1)
  baby2 = eightQueensIndividual(baby2Genes, epoch)
  baby2.mutate()
  babies.append(baby2)
  return babies

def selectiveBreeding(population, epoch):
  populationFitness = sum(individual.fitness for individual in population)
  weights = []
  for individual in population:
    weights.append(individual.fitness/populationFitness)
  #print(populationFitness)
  
  newPopulation = []
  for i in range(int(len(population)/2)):
    parent1 = np.random.choice(population, p=weights)
    #print("Parent1:", parent1)
    parent2 = np.random.choice(population, p=weights)
    while parent1 == parent2:
      parent2 = np.random.choice(population, p=weights)
    #print("Parent2", parent2)

    offspring = makeBabies(parent1,parent2, epoch)

    #print("Offspring 1:", offspring[0])
    #print("Offspring 2:", offspring[1])

    newPopulation.append(offspring[0])
    newPopulation.append(offspring[1])
  #return sorted(newPopulation, key=lambda x: x.fitness, reverse=True)
  return newPopulation


class eightQueensIndividual:
  def __init__(self, genes, epoch):
    self.genes = genes
    self.epoch = epoch
    self.calculateFitness()

  def __str__(self):
    return str(self.genes) + " Fitness: " + str(self.fitness)

  def calculateFitness(self):
    attackingPairs = 0
    for i in range(8):
      for paired in range(i+1,8):
        if self.genes[i] == self.genes[paired]:
          # Queens are on the same row
          #print(i, "is attacking", paired)
          attackingPairs += 1
        elif abs(self.genes[i] - self.genes[paired]) == abs(i-paired):
          # Queens are on the same diagonal
          #print(i, "is attacking", paired)
          attackingPairs += 1
    self.fitness = 28 - attackingPairs
    if self.fitness == 28 and str(self) not in SOLUTIONS.keys():
      #print(self, "Generation:", self.epoch)
      SOLUTIONS[str(self)] = self.epoch

  def mutate(self):
    proc = random.random()
    if proc <= MUTATE_CHANCE:
      #print("Mutated")
      index = random.randint(0,7)
      while True:
        newGene = random.randint(1,8)
        if not self.genes[index] == newGene:
          self.genes[index] = newGene
          break

population = []
for i in range(POPULATION_SIZE):
  population.append(eightQueensIndividual(randomChromosome(),0))

for epoch in range(1,NUM_ITERATIONS+1):
  population = sorted(population, key=lambda x: x.fitness, reverse=True)
  populationFitness = sum(individual.fitness for individual in population)
  print("Epoch", epoch, "Average fitness:", populationFitness/POPULATION_SIZE)
  #for i in range(len(population)):
    #print(population[i])

  population = selectiveBreeding(population, epoch)

  #for i in range(len(population)):
    #print(population[i])

##population = sorted(population, key=lambda x: x.fitness, reverse=True)
##print("Top ten individuals in last generation:")
##for i in range(10):
##    print(population[i])

print("List of solutions found:")
for individual in SOLUTIONS:
  print(individual, "Generation", SOLUTIONS[individual])
