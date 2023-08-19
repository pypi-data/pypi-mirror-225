import argparse
import logging
import shlex
import subprocess
import sys

# from .config import DRY_RUN, NO_NETWORK, NO_VM, PRINT_NETWORK, PRINT_VM
import deployer.globals as globals
from .globals import OP_CREATE, OP_DELETE


def ProcessArguments() -> str:
    parser = argparse.ArgumentParser(description="Parse topology config")
    parser.add_argument("-c", "--config", required=True)
    parser.add_argument("-l", "--log", type=str, choices=["DEBUG", "INFO",
                                                          "WARNING", "ERROR",
                                                          "CRITICAL"])
    parser.add_argument("--dry-run", action="store_true")

    parser.add_argument("-o", "--operation", type=str, required=True,
                        choices=["create", "delete", "CREATE", "DELETE"])

    parser.add_argument("--recreate-nw", action="store_true")
    parser.add_argument("--print-nw", action="store_true")
    parser.add_argument("--print-vm", action="store_true")

    skip_operation = parser.add_mutually_exclusive_group()
    skip_operation.add_argument("--no-network", action="store_true")
    skip_operation.add_argument("--no-vm", action="store_true")

    args = parser.parse_args()

    if args.log:
        log_level = getattr(logging, args.log.upper(), None)
        if not isinstance(log_level, int):
            raise ValueError("Invalid log level: {}".format(args.log))
        logging.basicConfig(level=log_level)

    if args.dry_run:
        globals.DRY_RUN = args.dry_run

    if args.operation.upper() == "CREATE":
        globals.OP = OP_CREATE
    else:
        globals.OP = OP_DELETE

    if args.no_network:
        globals.NO_NETWORK = args.no_network

    if args.no_vm:
        globals.NO_VM = args.no_vm

    if args.recreate_nw:
        globals.RECREATE_NW = args.recreate_nw
        globals.NO_VM = True

    if args.print_nw:
        globals.PRINT_NETWORK = args.print_nw

    if args.print_vm:
        globals.PRINT_VM = args.print_vm

    return args.config

def ExecuteCommand(cmd: str) -> None:
    if not globals.DRY_RUN:
        logging.info("Executing command : {}".format(cmd))
        ret = subprocess.call(shlex.split(cmd))
        if ret != 0:
            logging.error("Command {} failed wih return code : {}".format(cmd, ret))
            sys.exit(ret)
    else:
        logging.debug("Dry Run enabled. Command : {}".format(cmd))

def ExecuteCommandWithOutput(cmd: str) -> str:
    logging.info("Executing command : {}".format(cmd))
    res = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        logging.error("Command {} failed wih return code : {}".format(cmd, res.returncode))
        logging.error("Error message : {}".format(res.stderr))
        sys.exit(res.returncode)
    return res.stdout.decode('utf-8').strip()
