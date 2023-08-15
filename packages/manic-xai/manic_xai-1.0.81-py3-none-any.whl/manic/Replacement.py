import random

class Replacement:
    def __init__(self, crossover, mutation, evaluation, selection):
        self.crossover = crossover
        self.mutate = mutation
        self.evaluation = evaluation
        self.selection = selection

    def update_population(self, population):
        fitness_scores = self.evaluation.evaluate_population(population)

        #Maybe remove normalisation, not sure if it works with our method
        normalise=False

        if(normalise):
            min_score = min(fitness_scores)
            max_score = max(fitness_scores)

            if min_score == max_score:
                # Handle the case when all scores are the same
                fitness_scores = [1.0] * len(fitness_scores)
            else:
                fitness_scores = [(score - min_score) / (max_score - min_score) for score in fitness_scores]
        
        parents = self.selection.tournament_selection(population, fitness_scores)
        offspring = self.crossover(parents)
        offspring = self.mutate(offspring)
        
        # Combine elites and offspring
        elites = self.selection.select_elites(population, fitness_scores)
       
        # Randomly replace candidates in offspring with elites
        num_replacements = min(len(offspring), len(elites))
        replacement_indices = random.sample(range(len(offspring)), num_replacements)
        
        for i, idx in enumerate(replacement_indices):
            offspring[idx] = elites[i]

        population = offspring

        # Find best solution and fitness
        best_idx = fitness_scores.index(min(fitness_scores))
        generation_best_counterfactual = population[best_idx]
        generation_best_fitness = fitness_scores[best_idx]
        
        return population, generation_best_counterfactual, generation_best_fitness
    
