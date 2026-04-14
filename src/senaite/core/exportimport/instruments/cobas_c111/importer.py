# -*- coding: utf-8 -*-
from senaite.core.exportimport.instruments.importer import BaseImporter
from .parser import CobasC111Parser

class CobasC111Importer(BaseImporter):

    def __init__(self, instrument):
        super(CobasC111Importer, self).__init__(instrument)
        self.parser = CobasC111Parser()

    def process(self, infile):
        data = infile.read()
        parsed = self.parser.parse(data)

        for item in parsed:
            self.process_result(item)

    def process_result(self, item):
        sample_id = item.get("SampleID")
        analysis = item.get("Analysis")
        result = item.get("Result")

        # 🔥 Buscar muestra
        sample = self.get_sample(sample_id)

        if not sample:
            self.log("Sample not found: %s" % sample_id)
            return

        # 🔥 Buscar análisis
        analysis_obj = self.get_analysis(sample, analysis)

        if not analysis_obj:
            self.log("Analysis not found: %s" % analysis)
            return

        # 🔥 Guardar resultado
        analysis_obj.setResult(result)
        analysis_obj.reindexObject()

        self.log("Imported %s -> %s" % (analysis, result))
