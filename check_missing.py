import os
hf = set(os.listdir('.'))
missing = ['creative-engine.html','decision-visualization.html','gallery.html',
           'memory-health.html','memory-visualization.html','queue-behavior.html',
           'recursive-thought.html']
for m in missing:
    status = "OK" if m in hf else "MISSING"
    print(m + ": " + status)
