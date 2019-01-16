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

def getTopLevelDir(filePath, topDirPrefix):
    # strip out prefix dirs to get to top level
    p = filePath.partition(topDirPrefix)
    pathParts = p[2].split("/")
    if pathParts[0] == "":
        pathParts.pop(0)
    if len(pathParts) == 1:
        return "/"
    else:
        return pathParts[0]

def buildTopLevelDirsTable(results, topDirPrefix):
    tallyWithLicense = defaultdict(int)
    tallySkipped = defaultdict(int)
    tallyTotal = defaultdict(int)
    for _, sd in results.items():
        topLevelDir = getTopLevelDir(sd.filename, topDirPrefix)
        if topLevelDir != "/":
            topLevelDir = "/" + topLevelDir
        tallyTotal[topLevelDir] += 1
        if sd.license == None:
            continue
        elif sd.license == "SKIPPED":
            tallySkipped[topLevelDir] += 1
        else:
            tallyWithLicense[topLevelDir] += 1
    return tallyWithLicense, tallySkipped, tallyTotal

def addTotalRows(tableRows, total):
    tableRows.append(["========================", "======"])
    tableRows.append(["TOTAL", total])

def printResults(results, topDir):
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

    # print overall findings by directory
    tallyWithLicense, tallySkipped, tallyTotal = buildTopLevelDirsTable(results, topDir)
    dirs = sorted(tallyTotal.keys())
    print("\nLicenses by top-level directory:\n")
    for d in dirs:
        # don't print LICENSES directory
        if d == "/LICENSES":
            continue
        suffix = ""
        if tallySkipped[d] > 0:
            suffix = f"({tallySkipped[d]} skipped)"
        print(f"{d:15} => {tallyWithLicense[d]:6} found / {tallyTotal[d]:6} total {suffix}")

