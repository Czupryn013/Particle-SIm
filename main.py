from simulation import Simulation



colors = ["blue", "red", "green"]
attract_rule = {"blue" : "red", "green" : "red"}
repulse_rule = {"blue" : "green"}
sim = Simulation(100,colors,attract_rule,repulse_rule,10)


if __name__ == '__main__':
    sim.start()

