# BOIDS

## Project Overview
This repo is an implementation of the classic artificial life program developed by Craig Reynolds, using the following lab assignment from Cornell as a guideline for the algorithm specifics  

[Assignment](https://people.ece.cornell.edu/land/courses/ece4760/labs/s2021/Boids/Boids.html)  
  
I had no real reason to do this project, I just thought it would be fun

## Details
This program was created using Python, relying heavily on Tkinter to create the GUI and graphics

## Tunable Parameters

Given the incredibly simple nature of the rules governming boid behavior, getting their movement to behave realistically can be somewhat of a challenge. Therefore, many of the parameters that dictate their behavior are often able to be altered, in order to eventually achieve favorable results.
  
In my project, I implemented this as sliders beside the graphical display, so you can observe the effects of your adjustments in real time. I also thought this would be interesting as it would demonstrate more clearly exactly which aspects of the behavior were controlled by each parameter.

Given the somewhat large number of adjustable parameters, I'll describe each of them briefly below

### Boid Height and Boid Width
These parameters simply control the appearance of the boid in the display, and have no effect on their behavior

### Min and Max Speed
These are rather self explanatory. It is worth noting, though, that these control the overall magnitude of a boid's speed, not individual speeds in the *x* and *y* directions.

### Avoid Range and Avoidance
Avoidance is one of the most important factors governing boid behavior. Simply put, it is the tendancy to steer away from nearby boids. As such, the range is the radius of a circle (in pixels), within which other boids will be avoided.Avoidance controls the strength of this steering movement.

### Follow Range, Alignment, and Centering
These parameters are similar to those above, except describe different ways that boids will tend to group together. The follow range is the radius of a circle (in pixels) within which these parameters will take effect.

Alignment controls how closely the boid steers in the same direction as boids within the follow range. Centering adjusts the boid's direction to move towards the average position of boids within the follow range.

### Edge Margin and Turn Strength
The edge margin is the number of pixels from the edge of the screen that a boid will begin turning away from the edge. The strength is a fraction of the maximum speed that is applied while within this margin. It is worth noting that this effect grows linearly as a boid moves farther into the margin.

### Delay
Delay in milliseconds between game updates. If it's too low the game will lag, and if it's too high the game will seem to lag.

## Future Plans

I hope to return to this project to add a third dimension. Rendering this in true 3d sounds hard, so I would probably just use the color of the boid to represent position along the z axis. Most of the logic from the 2d version should be reusable, but it's probably more difficult than I'm imagining.

The other issue with doing this is performance; already, exceeding 100-200 boids leads to unacceptable slowdown, and adding an extra dimension would only exacerbate the issue. I would like to optimize the performance in the future.
