# -*- coding: utf-8 -*-

from senaite.core.exportimport.instruments.importer import AnalysisResultsImporter
from .parser import MindrayBC3000Parser


class MindrayBC3000Importer(AnalysisResultsImporter):

    def __init__(self, parser, context, instrument_uid):
        super(MindrayBC3000Importer, self).__init__(
            parser=parser,
            context=context,
            override=[False, False],
            instrument_uid=instrument_uid
        )