# coding: utf-8
"""Command-line helper to print cross-sections for processes defined under cmsdb.processes.

This script imports all process modules and exposes a small CLI:

Examples:
  python modules/cmsdb/cmsdb/processes/xsec_cli.py -p dy_mumu_m400to800 -e 13.6
  python xsec_cli.py --process dy_mumu_m10to50 --energy 13.6
  python xsec_cli.py -p dy_mumu_m10to50 -p dy_m50toinf -e 13 -e 13.6 --float
"""

from __future__ import annotations

import sys
import argparse

# import the package to populate locals with process symbols
import cmsdb.processes as processes  # noqa: F401

# After importing, process objects are available as names in the cmsdb.processes package
# We'll use the package's global namespace to look them up.


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print process cross-sections from cmsdb.processes")
    parser.add_argument("--process", "-p", action="append", help="Process name(s) to query (e.g. dy_mumu_m10to50)")
    parser.add_argument("--energy", "-e", action="append", type=float, help="CM energy in TeV (e.g. 13.6)")
    parser.add_argument("--float", action="store_true", help="Print numeric float values instead of scinum.Number repr")
    args = parser.parse_args(argv)

    proc_names = args.process or ["dy_mumu_m10to50"]
    energies = args.energy or [13.6]

    exit_code = 0
    pkg_ns = vars(processes)

    for pname in proc_names:
        proc = pkg_ns.get(pname)
        if proc is None:
            print(f"Unknown process '{pname}'")
            exit_code = 2
            continue

        for e in energies:
            try:
                x = proc.get_xsec(e)
            except Exception as exc:
                print(f"Failed to get xsec for {pname} at {e} TeV: {exc}")
                exit_code = 3
                continue

            if args.float:
                try:
                    print(float(x))
                except Exception:
                    try:
                        print(x.value)
                    except Exception:
                        print(x)
            else:
                print(f"{pname} @ {e} TeV: {x}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
