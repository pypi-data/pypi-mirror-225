class Termination:
    def __init__(self):
        self.meow = "meow"

    def should_stop(self, generations, time_elapsed):
      if('found' in list(self.early_stopping.keys()) and self.early_stopping['found'] == True):
        if('patience_generations' in list(self.early_stopping.keys())):
          if(self.early_stopping['patience_generations'] <= generations):
            print(f"Early stopping at generation {generations}. No improvement for {self.early_stopping['patience_generations']} consecutive generations.")
            return True
        if('patience_time' in list(self.early_stopping.keys())):
          if(self.early_stopping['patience_time'] < time_elapsed / 60):
            print(f"Early stopping at time {(time_elapsed / 60):.2f} minutes. No improvement for {(self.early_stopping['patience_time']):.2f} minutes.")
            return True
        else:
          return False
      else:
        return False
      
    def asd (self):
      # Check if the termination criteria has been met
        if self.early_stopping is not None:
            time_elapsed = time.time() - start_time
            if(self.should_stop(generation, time_elapsed)):
                if self.verbose > 0:
                    break

        # Check if the specified maximum time is exceeded
        if self.max_time is not None and (time.time() - start_time) > (self.max_time * 60):
            if self.verbose > 0:
                print(f"Stopping search after {self.max_time} minutes.")
            break

    #Stop if max time exceeded
    #Stop if max generations reached
    #Stop if no progress in given time
    #Stop if no progress in given generations
    #Stop if number of CFs found
    #Stop if fitness value reached
    #Stop if sparsity score reached
    #Remember to add a condition to modify behaviour depending on whether a CF is found