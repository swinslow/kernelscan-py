# Copyright The Linux Foundation
# SPDX-License-Identifier: Apache-2.0

import logging

import kernelscan.scan
import kernelscan.results
import kernelscan.report

# Modify this to point to the relative path where the kernel
# sources are located.
KERNELDIR = "kernels/linux-4.17.14"

# Modify this to point to the JSON file where scan results will
# be saved and/or loaded.
SCANJSON = "output.json"

if __name__ == "__main__":
    # The following lines set up logging to a file for debug purposes.
    # Modify or comment out if not needed.
    logging.basicConfig(
        filename="runscan-log.txt",
        filemode="w",
        level=logging.DEBUG,
    )
    logging.info("----- Starting new run -----")

    # Step 1: The following lines run the actual scan for SPDX ids in the
    # kernel source code, and save it to a JSON file.
    paths = kernelscan.scan.getAllPaths(KERNELDIR)
    results = kernelscan.scan.getIdentifierForPaths(paths)
    kernelscan.results.saveResultsToJSON(SCANJSON, results)

    # Step 2: The following lines load that JSON file back into memory,
    # and analyze / print to standard output the results in various tables.
    results = kernelscan.results.loadResultsFromJSON(SCANJSON)
    kernelscan.report.printResults(results, KERNELDIR)
