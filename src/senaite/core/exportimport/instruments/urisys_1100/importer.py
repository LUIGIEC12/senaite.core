# -*- coding: utf-8 -*-

from senaite.core.exportimport.instruments.importer import AnalysisResultsImporter


class Urisys1100Importer(AnalysisResultsImporter):

    def __init__(self, parser, context, instrument_uid):
        super(Urisys1100Importer, self).__init__(
            parser=parser,
            context=context,
            override=[False, False],
            instrument_uid=instrument_uid
        )