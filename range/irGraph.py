import numpy, matplotlib.pyplot as p
#chart of distance vs volts
d = numpy.loadtxt('irCalibration.txt', delimiter=",", skiprows=1, usecols=(0,))
mean = numpy.loadtxt('irCalibration.txt', delimiter=",", skiprows=1, usecols=(3,))
mmax = numpy.loadtxt('irCalibration.txt', delimiter=",", skiprows=1, usecols=(2,))
mmin = numpy.loadtxt('irCalibration.txt', delimiter=",", skiprows=1, usecols=(1,))

#p.show()

lind = 1.0 / (d + 0.42)

def f(v):
  return (1.0 / (v / 15.69)) - 0.42

def f2(v):
  return (1.0 / (v / 13.15)) - 0.35

#p.plot(d, mean, f(mean), mean)
p.plot(d, mean, label='Measured Distance')
#p.plot(f(mean), mean, label='Calculated Distance')
p.plot(f2(mean), mean, label='Calculated Distance')
#p.plot(d, mmin, label='Min')
#p.plot(d, mmax, label='Max')
p.xlabel('distance (cm)')
p.ylabel('value (V)')
p.legend()


#p.plot(lind, d)#, lind, 15.69 * lind)
p.show()

# todo: proper linear regresssion
#eyeballing it, goes through the origin. max is v = 2.87, linx = 0.184
#so that's y = 15.69 * x


