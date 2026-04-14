# -*- coding: utf-8 -*-

from senaite.core.exportimport.instruments.importer import AnalysisResultsImporter


class CobasC111Importer(AnalysisResultsImporter):

    def __init__(self, parser, context, override, instrument_uid):
        super(CobasC111Importer, self).__init__(
            parser=parser,
            context=context,
            override=override,
            instrument_uid=instrument_uid
        )

    def process(self):
        # Aquí puedes personalizar si quieres
        super(CobasC111Importer, self).process()
