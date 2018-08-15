# Copyright The Linux Foundation
# SPDX-License-Identifier: Apache-2.0

import json

from kernelscan.scandata import ScanData

class ScanDataJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ScanData):
            d = {
                'license': o.license,
                'lineno': o.lineno,
                'scanned': o.scanned,
            }
            if not o.scanned:
                d['skipReason'] = o.skipReason

            return d
        else:
            return {'__{}__'.format(o.__class__.__name__): o.__dict__}

def saveResultsToJSON(outFile, results):
    """Export scan results to the specified JSON file."""
    # FIXME probably needs to be within a try block
    with open(outFile, "w") as f:
        json.dump(results, f, indent=4, cls=ScanDataJSONEncoder)

def loadResultsFromJSON(inFile):
    """Import prior scan results from the specified JSON file."""
    results = {}
    with open(inFile, "r") as f:
        rj = json.load(f)
        for filename, d in rj.items():
            sd = ScanData()
            sd.filename = filename
            sd.scanned = d.get('scanned')
            sd.license = d.get('license')
            sd.lineno = d.get('lineno')
            sd.skipReason = d.get('skipReason', "")
            results[filename] = sd
    return results
