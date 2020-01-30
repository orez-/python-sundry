import signal
import sys
import time


def _sigterm_handler(signum, frame):
    # Before anything else: unregister this handler.
    # We only ever want to raise a SystemExit once, not during the
    # cleanup phase.
    # This probably isn't 100% foolproof for more than one SIGTERM in
    # quick succession.
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    sys.exit(0)
signal.signal(signal.SIGTERM, _sigterm_handler)


print("Time to sleep!")
try:
    time.sleep(15)
except SystemExit:
    print("Whoa gosh! Time to wake up!")
    time.sleep(15)
    print("Alright, I'm up. Goog morming")
else:
    print("What a great nap!")
