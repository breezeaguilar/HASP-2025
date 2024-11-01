# SpectraSolis Guidance FSM

Based off of the SolSeeker MK2 system, the SpectraSolis package will need to make
certain improvements ton instrument guidance in order to achieve enough tracking
stability for a safe coronagraph image. We plan on achieving this by implementing
a closed loop vector control system. 

![SpectraSolis Guidance FSM](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/breezeaguilar/HASP-2025/Docs/RPi/Resources/main/Guidance.iuml)

## Tracking State
instead of previous mission's open loop control scheme where the sun's position in image is calculated, and instrument is moved to track. We can calculate the relative position of the sun in the sky based on the steering image, and use a closed loop control scheme to track to that vector. With just the addition of a gyroscope on the instrument package, we can estimate the required scope position some time in the future, given current conditions.

![SpectraSolis Tracking FSM](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/breezeaguilar/HASP-2025/Docs/RPi/Resources/main/Tracking.iuml)