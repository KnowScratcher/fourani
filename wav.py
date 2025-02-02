from scipy.io import wavfile
from matplotlib import pyplot as plt

w = wavfile.read("x9.wav")
plt.plot(w[1])
plt.show()