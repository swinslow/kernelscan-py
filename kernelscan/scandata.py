# Copyright The Linux Foundation
# SPDX-License-Identifier: Apache-2.0

class ScanData(object):
    def __init__(self):
        self.filename = ""
        self.scanned = False
        self.skipReason = ""
        self.license = None
        self.lineno = -1
