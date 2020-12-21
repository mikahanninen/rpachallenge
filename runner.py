from progress.bar import Bar
from task import main
import time

sleeptime = 300
while True:
    main("rpabrowser_js")
    bar = Bar("sleeping", max=sleeptime)
    for i in range(sleeptime):
        bar.next()
        time.sleep(1)
    bar.finish()
