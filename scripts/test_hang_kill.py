#!/usr/bin/env python3
"""Test spawn.py's hang-kill logic against a simulated hanging child."""
import sys, os, json, signal, subprocess, threading, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stream_parser import parse_stream_event
import importlib.util
spec = importlib.util.spec_from_file_location("spawn", os.path.join(os.path.dirname(os.path.abspath(__file__)), "spawn.py"))
spawn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spawn)

# Fake child: prints a valid result event, spawns an orphaned grandchild,
# then sleeps 60s (refuses to exit) — mimics the real Builder hang.
FAKE_CHILD = r'''
import sys, json, time, subprocess
ev = {"type": "result", "subtype": "success", "is_error": False,
      "result": "HANDOFF\nSTATUS: OK\nOUTPUT: x\nSUMMARY: y",
      "duration_ms": 1000, "num_turns": 2, "total_cost_usd": 0.01, "usage": {}}
print(json.dumps(ev), flush=True)
subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)"])
time.sleep(60)
'''

t0 = time.time()
proc = subprocess.Popen(
    [sys.executable, "-c", FAKE_CHILD],
    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
    start_new_session=True,
)

result_event = None

def pump():
    global result_event
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        etype, summary, event = parse_stream_event(line)
        if etype == "result" and event:
            result_event = event
            return

th = threading.Thread(target=pump, daemon=True)
th.start()
th.join(timeout=600)
print("pump alive after join:", th.is_alive(), "(want False)")
print("got result_event:", result_event is not None, "(want True)")

try:
    proc.wait(timeout=15)
    print("ERROR: exited cleanly, rc =", proc.returncode)
except subprocess.TimeoutExpired:
    print("grace timeout -> killing process group")
    spawn.kill_process_group(proc)
    print("killed; rc =", proc.returncode)

# Verify grandchild (orphan) was also killed: nothing should reference sleep(300)
elapsed = time.time() - t0
print(f"elapsed: {elapsed:.1f}s (want ~15s, NOT 60s)")
assert result_event is not None, "FAIL: no result captured"
assert elapsed < 25, "FAIL: took too long"
print("PASS")
