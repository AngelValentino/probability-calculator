import copy
import random

class Hat:
    def __init__(self, **kwargs):
        # Check if at least one marble is provided
        total_marbles = sum(kwargs.values())
        if total_marbles < 1:
            raise ValueError('You must provide at least one marble.')

        # Converts the marbles dictionary into a list of colors
        self.contents = self.set_colors(kwargs)

    def set_colors(self, marbles):
        formatted_colors = []

        # Converts the marbles dictionary into a list of colors
        for color, quantity in marbles.items():
            # Depending on how many marbles there are for each color, add their name to the list accordingly
            for _ in range(quantity):
                formatted_colors.append(color)
        
        return formatted_colors # Return the list of formatted colors
    
    def draw(self, tries):
        drawn_colors = []

        if tries <= 0:
            raise ValueError('Number of tries must be a positive integer.')
        
        # Check if there are enough marbles to be drawn
        if tries > len(self.contents):
            drawn_colors = copy.copy(self.contents) # Make a copy of the hat's contents list
            self.contents.clear() # Clear the contents of the hat
            return drawn_colors

        # Draw marbles and append them to the drawn_colors list
        for _ in range(tries):
            random_index = random.choice(range(len(self.contents))) # Randomly select an index to draw from the contents
            drawn_colors.append(self.contents.pop(random_index)) # Remove a marble at the random index and add it to drawn_colors

        return drawn_colors # Return which colors have been drawn


def experiment(hat, expected_marbles, num_marbles_drawn, num_experiments):
    successful_draws = 0

    # Repeat the experiment for the specified number of times
    for _ in range(num_experiments):
        current_hat = copy.deepcopy(hat) # Create a deep copy of the hat for this experiment
        expected_drawn_marbles = copy.copy(expected_marbles) # Create a copy of the expected marbles to track their count
        drawn_marbles = current_hat.draw(num_marbles_drawn) # Draw a specified number of marbles from the hat

        # Iterate over each color that has been drawn from the hat
        for color in drawn_marbles:
            # Check if the drawn color is among the expected colors
            if color in expected_drawn_marbles:
                # Check if we still need to draw more of this specific color
                if expected_drawn_marbles[color] > 0:
                    # Decrement the count of the expected color by 1,
                    # indicating that one instance of this color has been successfully drawn
                    expected_drawn_marbles[color] -= 1

        # Check if all expected marbles have been drawn
        if all(value == 0 for value in expected_drawn_marbles.values()): # Ensure all values are zero
            successful_draws += 1 # Increment the success counter if all expected marbles were drawn
        
    # Return the probability of drawing the expected marbles
    return successful_draws / num_experiments

hat = Hat(black=6, red=4, green=3)
probability = experiment(
    hat=hat,
    expected_marbles={'red': 2, 'green': 1},
    num_marbles_drawn=5,
    num_experiments=2000
)
print(probability)