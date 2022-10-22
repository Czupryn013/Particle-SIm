from simulation import Simulation

colors = ["blue","red", "green", "yellow", "purple"]
attract_rule = [("green","red"), ("purple","yellow"), ("purple", "green"),
                ("blue","purple"), ("red", "blue")] #red,blue = red goes to blue
repulse_rule = [("blue", "red"), ("blue", "yellow")] #red,blue = red goes away from blue
sim = Simulation(50,colors,attract_rule,repulse_rule,100)


if __name__ == '__main__':
    sim.start()









