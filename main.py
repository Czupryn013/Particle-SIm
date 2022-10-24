from simulation import Simulation

colors = ["blue","red", "purple"]
rules = {"blue":{"blue":0, "red":0, "purple":- 5},
         "red": {"blue":0, "red":2,"purple":10},
         "purple":{"blue":3, "red":-5, "purple":0}}
attract_rule = [("purple","red"), ("red", "purple"), ("blue", "purple")] #red,blue = red goes to blue
repulse_rule = [("blue", "red")] #red,blue = red goes away from blue
sim = Simulation(100,colors,attract_rule,repulse_rule,rules, 100)


if __name__ == '__main__':
    sim.start()









