import os
import aiml

k = aiml.Kernel()
files = [f for f in os.listdir('.') if os.path.isfile(f)]

for file in files:
    k.learn(file)