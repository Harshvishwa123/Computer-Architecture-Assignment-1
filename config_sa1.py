import m5
from m5.objects import *
from argparse import ArgumentParser
from m5.objects import MemCtrl, DDR3_1600_8x8
# ----- Cache Classes -----
class L1ICache(Cache):
    def __init__(self, size="16kB", assoc=2, lat=2):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = lat
        self.data_latency = lat
        self.response_latency = lat
        self.mshrs = 4
        self.tgts_per_mshr = 20
        self.is_read_only = True

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L1DCache(Cache):
    def __init__(self, size="16kB", assoc=2, lat=2):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = lat
        self.data_latency = lat
        self.response_latency = lat
        self.mshrs = 8
        self.tgts_per_mshr = 20

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L2Cache(Cache):
    def __init__(self, size="512kB", assoc=4, lat=10):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = lat
        self.data_latency = lat
        self.response_latency = lat
        self.mshrs = 16
        self.tgts_per_mshr = 20
        self.clusivity = "mostly_incl"

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L3Cache(Cache):
    def __init__(self, size="1MB", assoc=8, lat=20):
        super().__init__()
        self.size = size
        self.assoc = assoc
        self.tag_latency = lat
        self.data_latency = lat
        self.response_latency = lat
        self.mshrs = 32
        self.tgts_per_mshr = 20
        self.clusivity = "mostly_incl"

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# ----- Argument Parser -----
parser = ArgumentParser()
parser.add_argument("--cpu", choices=["timing","o3"], default="timing")
parser.add_argument("--l2-size", default="512kB")
parser.add_argument("--l2-assoc", type=int, default=4)
parser.add_argument("--l2-lat", type=int, default=10)
parser.add_argument("--l3-size", default="1MB")
parser.add_argument("--l3-assoc", type=int, default=8)
parser.add_argument("--l3-lat", type=int, default=20)
parser.add_argument("--cmd", required=True)
parser.add_argument("--args", nargs="*", default=[])
parser.add_argument("--cwd", default=".")
args = parser.parse_args()

# ----- System -----
system = System()
system.clk_domain = SrcClockDomain(clock="1GHz", voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

if args.cpu == "timing":
    system.cpu = RiscvTimingSimpleCPU()
else:
    system.cpu = RiscvO3CPU()
system.cpu.createInterruptController()
# L1 caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# L2 and L3
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache = L2Cache(size=args.l2_size, assoc=args.l2_assoc, lat=args.l2_lat)
system.l2cache.connectCPUSideBus(system.l2bus)

system.l3bus = L2XBar()
system.l2cache.connectMemSideBus(system.l3bus)
system.l3cache = L3Cache(size=args.l3_size, assoc=args.l3_assoc, lat=args.l3_lat)
system.l3cache.connectCPUSideBus(system.l3bus)

# Memory
system.membus = SystemXBar()
system.l3cache.connectMemSideBus(system.membus)
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8(range=system.mem_ranges[0])
# Connect memory controller to the membus
if hasattr(system.membus, "mem_side_ports"):
    system.mem_ctrl.port = system.membus.mem_side_ports
elif hasattr(system.membus, "master"):
    system.mem_ctrl.port = system.membus.master
else:
    system.mem_ctrl.port = system.membus.slave

# System port remains the same
system.system_port = system.membus.cpu_side_ports
# Workload using SEWorkload API
system.workload = SEWorkload.init_compatible(args.cmd)
process = Process()
process.executable = args.cmd
process.cmd = [args.cmd] + list(args.args)
process.cwd = args.cwd
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate and run
root = Root(full_system=False, system=system)
m5.instantiate()
print("Starting simulation...")
exit_event = m5.simulate()
print("Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause()))
m5.stats.dump()
