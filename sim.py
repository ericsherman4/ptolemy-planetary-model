from vpython import *
from gui_control import *

class inputs:
    # https://en.wikipedia.org/wiki/Deferent_and_epicycle
    # units is earth radius
    moon_orbit_radius =  48
    mercury_orbit_radius = 115
    venus_orbit_radius = 622.5
    sun_orbit_radius = 1210
    mars_orbit_radius = 5040
    jupiter_orbit_radius = 11504
    saturn_orbit_radius = 17026 
    
    # for visualization
    earth_sim_radius = 5
    orbit_marker_radius = 1
    
    # rotation
    delta_ang_moon_epicycle = 0.007
    delta_ang_moon_orbit = 0.002

    # scene
    width = 1800
    height = 1000

class time:
    t = 0
    end = 1000
    delta = 0.03
    rate = 60
    
class solarsys:
    
    planets = list()
    orbits = list()
    epicycles = list()
    sticks = list()
    delta_orbit_ang = list()
    delta_epicycle_ang = list()
    
    def __init__(self):
        # create earth
        self.earth = sphere(pos = vector(0,0,0), color =  color.green, radius = inputs.earth_sim_radius)
    
    def add_planet(self, color_in : color, planet_radius, orbit_radius, epicycle_radius, delta_orbit_ang_in, delta_epicycle_ang_in):
        
        solarsys.planets.append(sphere(pos=vector(0,orbit_radius+epicycle_radius,0),
                                color = color_in, radius = planet_radius, make_trail = True))
        
        solarsys.orbits.append(sphere(pos=vector(0,orbit_radius,0),
                                     color = color.gray(0.6), radius = inputs.orbit_marker_radius, make_trail = True))
        
        solarsys.epicycles.append(ring(pos=solarsys.orbits[-1].pos,axis=vector(0,0,1),
                                     radius=epicycle_radius, thickness = epicycle_radius/100))
        
        solarsys.delta_orbit_ang.append(delta_orbit_ang_in)
        solarsys.delta_epicycle_ang.append(delta_epicycle_ang_in)
        
        solarsys.sticks.append(arrow(pos = vector(0,orbit_radius,0), axis =vector(0,epicycle_radius,0), round=True, shaftwidth = epicycle_radius/50 , headwidth = epicycle_radius/50, color=color.gray(0.6))) 
        
        
        
    def update(self):
        for i in range(0, len(solarsys.planets)):
            # moves epicycle to where the orbit marker is
            solarsys.epicycles[i].pos = solarsys.orbits[i].pos
            
            # rotates the planet around the epicycle
            solarsys.planets[i].rotate(angle = solarsys.delta_epicycle_ang[i], axis = vector(0,0,1), origin = solarsys.epicycles[i].pos)
            solarsys.planets[i].rotate(angle= solarsys.delta_orbit_ang[i], axis = vector(0,0,1), origin = self.earth.pos)
            solarsys.sticks[i].rotate(angle = solarsys.delta_epicycle_ang[i], axis = vector(0,0,1), origin = solarsys.epicycles[i].pos)
            solarsys.sticks[i].rotate(angle= solarsys.delta_orbit_ang[i], axis = vector(0,0,1), origin = self.earth.pos)
            
            
            # rotates the epicycle around the earth
            solarsys.orbits[i].rotate(angle= solarsys.delta_orbit_ang[i], axis = vector(0,0,1), origin = self.earth.pos)

            # check kill / pause events
            monitor_terminate()
            monitor_pause()
        
        
    

scene = canvas(width=inputs.width,height=inputs.height)    
sys = solarsys()


# params: color_in : color, planet_radius, orbit_radius, epicycle_radius, delta_orbit_ang_in, delta_epicycle_ang_in

# moon
sys.add_planet(color.gray(0.5), 4, inputs.moon_orbit_radius, 20, 0.03, 0.03*7)

# mercury
sys.add_planet(color.blue, 7, inputs.mercury_orbit_radius, 26, 0.01, 0.05)

# venus
sys.add_planet(vector(1, 192/255, 2/255), 50, inputs.venus_orbit_radius,  150, 0.01, 0.02)

#sun
sys.add_planet(color.orange, 200, inputs.sun_orbit_radius, 200, 0.003, 0)

#mars
sys.add_planet(color.red, 250, inputs.mars_orbit_radius, 3300, 0.005, 0.01)

#jupiter
sys.add_planet(color.yellow, 300, inputs.jupiter_orbit_radius, 1700, 0.002, 0.04) #if last param over 2nd to last = whhole number, then it starts and ends at same spot

#saturn
sys.add_planet(color.white, 300, inputs.saturn_orbit_radius, 1200, 0.001, 0.04)



while( time.t < time.end):
    rate(time.rate)
    time.t += time.delta
    
    sys.update()
    # print(scene.camera.pos)
    # scene.camera.pos = vector(scene.camera.pos.x, scene.camera.pos.y, scene.camera.pos.z+1)
