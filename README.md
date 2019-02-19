# Shadow Music
A time-dimension-based synthesizer built using NumPy, for Python3.

## Shadow Philosophy
Shadow is designed to generate audio by broadcasting functions across a temporal space. This means audio generation happens entirely in memory, and instead of using musical concepts like "beats" we tend to think in terms of intersecting and overlapping waveforms. It is, in its own way, designed to emulate the behavior of OpenGL fragment shaders, but for audio.

Yes, that's a difficult and weird way to think about generating audio, but what it demonstrates is that a surpisingly small amount of code can generate a wide variety of complex sounds. This is less a tool for musical composition and more a tool for acoustic exploration.

# Getting Started
## Space and Time
The entry point for `shadow` is `space`. The `space` function generates a linear series in the time dimension, from `0.` to `n` where `n` is the `duration * sample rate`. So, a 3 second space, at 44100Hz sample rate, will be an array 132,300 elements long, and each element will store its offset in seconds. A `space` is the input for most operations.

**Example**:
```python
>>> import shadow as sp
>>> sp.space(3)
array([0.00000000e+00, 2.26757370e-05, 4.53514739e-05, ...,
       2.99993197e+00, 2.99995465e+00, 2.99997732e+00])
```

## Sound
Once you have a `space`, you can use that space to generate audio. For example, to convert a space into a 440hz sine wave, you can simply use the `sin` function.

```python
>>> import shadow as sp
>>> space = sp.space(3) # a 3 second linear space in the time dimension
>>> sp.sin(space, 440) # returns a 3 second sinusoidal wave generated from that space
array([ 0.        ,  0.06264832,  0.12505052, ..., -0.18696144,
       -0.12505052, -0.06264832])
>>> import sounddevice as sd
>>> sd.play(sp.sin(space, 440)) #play the wave using the sounddevice library
```

## Complex Outcomes
With a few basic waveforms and noise generation functions, we can create surprisingly complex sounds. For example, something similar to a beat could be created by multiplying waves together:

```python
sd.play(sp.noise(space)*sp.sigmoid(space, 2)*0.5) #the 0.5 at the end controls the overall amplitude of the wave
```

By adding and subtracting waves together, we can create very complex sounds:

```python
sd.play(sp.noise(space)*(sp.sigmoid(space, 2) - sp.sin(space,0.4) - sp.sin(space,0.25,1)) + sp.sin(space, 440)*(sp.sin(space,3)-sp.sin(space,4.25)) + sp.sin(space,310)*(sp.sin(space,3,1.254))) #complex beat
```

Also, because of numpy's broadcasting, you can pass waveforms in the frequency parameter. This creates an odd wobble sound:

```python
sd.play(sp.sin(space, sp.sin(space, 2) * 220))
```

# Simplicity Itself
Take a look at the code in `shadow/__init.py__`. It's *extremely* simple code. It's so simple, in fact, that it's barely worth even writing unit tests (though as this project matures, I'll certainly add some actual testing). By using NumPy's broadcastable functions, `mgrid` and the like, it's *extremely* easy to create audio, and to process that audio in interesting ways.