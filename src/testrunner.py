import vqsx
import argparse, sys

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--silent",
                    dest="silent",
                    action="store_true",
                    help="Silent output?")

parser.add_argument("input",
                    help="Location of the test binary to run.",
                    type=str)

# parse and fetch
args = parser.parse_args(sys.argv[1:])
finput = args.input
silent = args.silent


ve = vqsx.VQsXExecutor(vqsx.NullOpBehavior.NOOP)
observer = vqsx.obsrv(ve, silent)
ve.register(observer)
with open(finput, "rb") as f:
    ve.load(f.read())
ve.run()
