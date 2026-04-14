# -*- coding: utf-8 -*-
class CobasC111Importer(object):

    def __init__(self, parser, context, override, instrument_uid):
        self.parser = parser
        self.context = context
        self.override = override
        self.instrument_uid = instrument_uid

        self.errors = []
        self.logs = []
        self.warns = []

    def process(self):
        data = self.parser.parse()
        self.logs.append("Procesado OK")
