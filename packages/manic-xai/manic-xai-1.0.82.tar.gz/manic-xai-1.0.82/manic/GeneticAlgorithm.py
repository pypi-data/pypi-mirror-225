import os
import time

class GeneticAlgorithm:
    def __init__(self, num_generations, early_stopping, predict_fn, evaluation, selection, crossover, mutate, verbose, target_class, max_time, utils, replacement, population, base_counterfactuals, data_instance, disagreement, wachter):
        self.num_generations = num_generations
        self.early_stopping = early_stopping
        self.predict_fn = predict_fn
        self.evaluation = evaluation
        self.selection = selection
        self.crossover = crossover
        self.wachter = wachter
        self.mutate = mutate
        self.verbose = verbose
        self.target_class = target_class
        self.best_counterfactual = None
        self.best_fitness = float('inf')
        self.generation_found = float('inf')
        self.time_found = float('inf')
        self.max_time = max_time
        self.utils = utils
        self.replacement = replacement
        self.population = population
        self.base_counterfactuals = base_counterfactuals
        self.data_instance = data_instance
        self.disagreement = disagreement
        self.consecutive_generations_without_improvement = 0

    def generations_or_time_reached(self, generations, time_elapsed):
        if('patience_generations' in list(self.early_stopping.keys())):
          if(self.early_stopping['patience_generations'] <= generations):
            print(f"Early stopping at generation {generations}. No improvement for {self.early_stopping['patience_generations']} consecutive generations.")
            return True
        
        if('patience_time' in list(self.early_stopping.keys())):
          if(self.early_stopping['patience_time'] < time_elapsed / 60):
            print(f"Early stopping at time {(time_elapsed / 60):.2f} minutes. No improvement for {(self.early_stopping['patience_time']):.2f} minutes.")
            return True
        return False
          
    def should_stop(self, generations, time_elapsed):
        if('found' in list(self.early_stopping.keys()) and self.early_stopping['found'] == True):
            if(self.best_counterfactual != None):
                stop = self.generations_or_time_reached(generations, time_elapsed)
                return stop
        elif('found' in list(self.early_stopping.keys()) and self.early_stopping['found'] == False):
            stop = self.generations_or_time_reached(generations, time_elapsed)
            return stop
        else:
            return False

    def get_cpu_time(self):
      return time.process_time()

    def get_cpu_cycles(self, cpu_time_seconds):
      cpu_clock_speed_hz = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
      cpu_cycles = cpu_time_seconds * cpu_clock_speed_hz
      
      return cpu_cycles

    def generate_counterfactuals(self):
        start_time = time.time()
        cpu_start_time = self.get_cpu_time()

        for generation in range(self.num_generations):
            # Shows the current generation
            if self.verbose == 1:
                print(f"Generation {generation + 1}")
            
            # Runs selection, crossover and mutation to get the new population
            self.population, generation_best_counterfactual, generation_best_fitness = self.replacement.update_population(self.population)

            # Check if a more optimal solution has been found
            if generation_best_fitness < self.best_fitness:
                #Format the counterfactual so it is realistic
                formatted_counterfactual = self.utils.format_counterfactual(generation_best_counterfactual) 
                
                # Check if the candidate counterfactual produces the target class
                prediction = self.predict_fn(formatted_counterfactual)
                
                if prediction == self.target_class:
                    self.best_fitness = generation_best_fitness

                    # Check that the solution is an improvement
                    if(formatted_counterfactual != self.best_counterfactual):
                        self.best_counterfactual = formatted_counterfactual
                        self.generation_found = generation
                        self.time_found = time.time() - start_time

                    self.consecutive_generations_without_improvement = 0
            else:
                self.consecutive_generations_without_improvement += 1

            # Show the progress of the generation
            self.show_progress(generation, self.verbose)

            # Check if the termination criteria has been met
            if self.early_stopping is not None:
                time_elapsed = time.time() - start_time
                if(self.should_stop(self.consecutive_generations_without_improvement, time_elapsed)):
                    if self.verbose > 0:
                      break

            # Check if the specified maximum time is exceeded
            if self.max_time is not None and (time.time() - start_time) > (self.max_time * 60):
                if self.verbose > 0:
                    print(f"Stopping search after {self.max_time} minutes.")
                break

        # Calculate elapsed CPU time in seconds and convert to CPU cycles
        cpu_end_time = self.get_cpu_time()
        elapsed_cpu_time_seconds = cpu_end_time - cpu_start_time
        cpu_cycles = self.get_cpu_cycles(elapsed_cpu_time_seconds)

        # Calculate total time taken
        end_time = time.time()
        time_taken = end_time - start_time

        # Initialise scores
        proximity_score = float('inf')
        sparsity_score = float('inf')
        disagreement_score = float('inf')
        number_of_changes = float('inf')

        # Get scores
        if(self.best_counterfactual != None):
            proximity_score = self.disagreement.calculate_proximity(self.data_instance, self.best_counterfactual, True)
            sparsity_score, number_of_changes = self.disagreement.calculate_sparsity(self.best_counterfactual)
            
            if(not self.wachter):
                base_cf_scores = []
                
                # Get average disagreement
                for base_cf in self.base_counterfactuals:
                    base_cf_scores.append(self.evaluation.calculate_base_cf_scores([self.best_counterfactual], base_cf))

                disagreement_score = sum(score for score in base_cf_scores) / len(base_cf_scores)

        # Show results
        if self.verbose > 0:
            self.utils.print_results(self.best_counterfactual, self.best_fitness, generation + 1, self.generation_found, time_taken, self.time_found, cpu_cycles, proximity_score, sparsity_score, number_of_changes, disagreement_score)

        # Store results in a dictionary
        results = {
          'best_counterfactual': self.best_counterfactual,
          'best_counterfactual_fitness': self.best_fitness,
          'generation_found': self.generation_found,
          'time_found': self.time_found,
          'cpu_cycles_found': cpu_cycles,
          'proximity_score': proximity_score,
          'sparsity_score': sparsity_score,
          'number_of_changes': number_of_changes,
          'disagreement_score': disagreement_score
        }

        return results

    # Function to show the progress on each generation
    def show_progress(self, generation, verbose):
        if verbose == 2:
            print(f"Generation {generation+1}: Best Counterfactual = {self.best_counterfactual}, Fitness = {self.best_fitness}")

        if verbose == 3:
            print(f"Generation {generation+1}:")
            for idx, child in enumerate(self.population):
                print(f"Child {idx+1}: {child}")

        return self.best_counterfactual