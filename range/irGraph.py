import numpy, matplotlib.pyplot as p
#chart of distance vs volts
d = numpy.loadtxt('irCalibration.txt', delimiter=",", skiprows=1, usecols=(0,))
v = numpy.loadtxt('irCalibration.txt', delimiter=",", skiprows=1, usecols=(2,))

#p.show()

lind = 1.0 / (d + 0.42)

def f(v):
  return (1.0 / (v / 15.69)) - 0.42

p.plot(d, v, f(v), v)


#p.plot(linx, y, linx, 15.69 * linx)
p.show()

# todo: proper linear regresssion
#eyeballing it, goes through the origin. max is v = 2.87, linx = 0.184
#so that's y = 15.69 * x


