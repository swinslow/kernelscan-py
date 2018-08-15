# Copyright The Linux Foundation
# SPDX-License-Identifier: Apache-2.0

from collections import defaultdict
from tabulate import tabulate

# def tallyResults(results):
#     tallyLicenses = defaultdict(int)
#     tallyLinenos = defaultdict(int)
#     for _, sd in results.items():
#         tallyLicenses[sd.license] += 1
#         if sd.lineno != -1:
#             tallyLinenos[sd.lineno] += 1

#     pprint.pprint(tallyLicenses)
#     pprint.pprint(tallyLinenos)

def buildOverallTable(results):
    tallyFound = 0
    tallyNotFound = 0
    tallySkipped = 0
    total = 0
    for _, sd in results.items():
        total += 1
        lic = sd.license
        if lic == None:
            tallyNotFound += 1
        elif lic == "SKIPPED":
            tallySkipped += 1
        else:
            tallyFound += 1
    return tallyFound, tallyNotFound, tallySkipped, total

def buildLicensesTable(results):
    tally = defaultdict(int)
    total = 0
    for _, sd in results.items():
        lic = sd.license
        if lic != None and lic != "SKIPPED":
            total += 1
            tally[lic] += 1
    return tally, total

def buildLinenoTable(results):
    tally = defaultdict(int)
    total = 0
    for _, sd in results.items():
        if sd.lineno != -1:
            total += 1
            tally[sd.lineno] += 1
    return tally, total

def buildSkipTable(results):
    tally = defaultdict(int)
    total = 0
    for _, sd in results.items():
        if sd.license == "SKIPPED":
            total += 1
            tally[sd.skipReason] += 1
    return tally, total

def addTotalRows(tableRows, total):
    tableRows.append(["========================", "======"])
    tableRows.append(["TOTAL", total])

def printResults(results):
    fmt = "presto"

    # print overall results
    tallyFound, tallyNotFound, tallySkipped, total = buildOverallTable(results)
    overallHeaders = ["Result", "#"]
    overallRows = [
        ["License found", tallyFound],
        ["License not found", tallyNotFound],
        ["Skipped", tallySkipped],
    ]
    addTotalRows(overallRows, total)
    print(tabulate(overallRows, headers=overallHeaders, tablefmt=fmt))

    # print reasons for skipping
    skipTableHeaders = ["Reason for skipping", "#"]
    rows, total = buildSkipTable(results)
    skipTableRows = sorted(rows.items(), key=lambda x:(-x[1],x[0]))
    print("")
    addTotalRows(skipTableRows, total)
    print(tabulate(skipTableRows, headers=skipTableHeaders, tablefmt=fmt))

    # print license results
    licTableHeaders = ["License", "#"]
    rows, total = buildLicensesTable(results)
    licTableRows = sorted(rows.items(), key=lambda x:(-x[1],x[0]))
    print("")
    addTotalRows(licTableRows, total)
    print(tabulate(licTableRows, headers=licTableHeaders, tablefmt=fmt))

    # print line number for ID
    linenoTableHeaders = ["Line number", "#"]
    rows, total = buildLinenoTable(results)
    linenoTableRows = sorted(rows.items())
    print("")
    addTotalRows(linenoTableRows, total)
    print(tabulate(linenoTableRows, headers=linenoTableHeaders, tablefmt=fmt))

