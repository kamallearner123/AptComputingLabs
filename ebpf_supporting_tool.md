## Installation

sudo apt-get install bpfcc-tools linux-headers-$(uname -r)
sudo apt-get install python3-bpfcc

## Sample python code
```
from bcc import BPF
import sys

# Check if process ID is provided
if len(sys.argv) != 2:
    print("Usage: {} <PID>".format(sys.argv[0]))
    exit(1)

pid = int(sys.argv[1])

# Define BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

BPF_HASH(counts, u32);

int trace_open(struct pt_regs *ctx, int dfd, const char __user *filename, int flags, umode_t mode) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;

    // Only track events for the given process ID
    if (pid == PID) {
        u64 *val, zero = 0;
        val = counts.lookup_or_init(&pid, &zero);
        (*val)++;
    }

    return 0;
}
"""

# Replace PID in the BPF program with the actual PID
bpf_text = bpf_text.replace("PID", str(pid))

# Load the BPF program
b = BPF(text=bpf_text)
b.attach_kprobe(event="do_sys_open", fn_name="trace_open")

# Print output
print("Tracing open syscalls for PID {}... Press Ctrl+C to stop.".format(pid))

# Loop and print counts
try:
    while True:
        counts = b["counts"]
        for k, v in counts.items():
            print("PID: {}, Open syscall count: {}".format(k.value, v.value))
        counts.clear()
except KeyboardInterrupt:
    print("Detaching BPF program...")

```
