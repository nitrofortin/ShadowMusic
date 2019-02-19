import numpy as np

SAMPLE_RATE=44100

def smoothstep(edge0, edge1, x):
  """
  Hermite Interpolation, lifted from OpenGL shaders.

  Converts a data stream into a sigmoid from edge0 to edge1 (outputting in the range [0.,1.])
  """
  t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
  return t * t * (3.0 - 2.0 * t)

def step(space):
  return np.heaviside(space, 0)

def space(duration, sample_rate=SAMPLE_RATE):
  """Generate a temporal space of `duration` seconds at `sample_rate` sampling frequency"""
  return np.mgrid[0:int(sample_rate*duration)] / sample_rate

def noise(space):
  """Output random noise in the same range as our temporal space"""
  return (np.random.random(len(space)) - 0.5) * 2.

def sin(space, freq,shift=0):
  """Convert an input space to a sinusoidal wave with `freq` frequency. `shift` moves the phase."""
  return np.sin(2*np.pi*space*freq+shift)

def sigmoid(space, freq, shift=0):
  """Convert an input space to a sigmoidal wave with `freq` frequency. `shift` moves the phase."""
  return smoothstep(0, 1., sin(space, freq, shift)) + smoothstep(-1., 0., sin(space, freq, shift))

def square(space, freq, shift=0):
  s = sin(space, freq, shift)
  return step(s)
  
def delay(space, distance, wet=0.5, dry=0.5, sample_rate=SAMPLE_RATE):
  """Delay and mix"""
  d = int(distance * sample_rate)
  return np.roll(space, d) * wet + space * dry
  