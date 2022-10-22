from simulation import Simulation

colors = ["blue","red", "purple"]
attract_rule = [("purple","red"), ("red", "purple"), ("blue", "purple")] #red,blue = red goes to blue
repulse_rule = [("blue", "red")] #red,blue = red goes away from blue
sim = Simulation(50,colors,attract_rule,repulse_rule,100)


if __name__ == '__main__':
    sim.start()









