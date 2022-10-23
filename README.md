# Experiments

Repository with small experiments

## Random Distribution (distribution.py)

Shows the different random distributions for a circle depending on the method
used. Choosing r as random uniform, applying the square root of r, generating
random points inside a box and rejecting those outside the circle or repeating
instead of rejection until the point is inside the circle.

![distribution screenshot](docs/dist_screenshot.png)

### Usage

This script uses Python 3 with numpy, Pillow and pyglet. To install
dependencies:

`$ pip install numpy Pillow pyglet`

To run the script:

`$ python distribution.py`
