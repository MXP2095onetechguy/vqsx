import vqsx
import argparse, sys

parser = argparse.ArgumentParser()

parser.add_argument("input",
                    help="Location of the test binary to run.",
                    type=str)

# parse and fetch
args = parser.parse_args(sys.argv[1:])
finput = args.input

class obsrv(vqsx.VQsXObserver):
    def __init__(self, vm : vqsx.VQsXObserver):
        self.vm : vqsx.VQsXaObserver = vm
    
    def onstep(self, post : bool):
        print("ONSTEP", post, self.vm.status)

    def fetchinst(self, inst : vqsx.Instructions):
        nam = vqsx.inst_to_name(inst)
        if nam is not None: nam = f"[{nam.name}]"
        print("FETCHINST", nam)

    def halt(self, faulty : bool):
        print("HALT", "faulty" if faulty else "hlt")


ve = vqsx.VQsXExecutor(vqsx.NullOpBehavior.NOOP)
ve.register(obsrv(ve))
with open(finput, "rb") as f:
    ve.load(f.read())
ve.run()