# -*- coding: utf-8 -*-

from bika.lims import bikaMessageFactory as _
from senaite.core.i18n import translate as t
from senaite.core.exportimport.instruments import IInstrumentImportInterface

from .parser import CobasC111Parser
from .importer import CobasC111Importer

from zope.interface import implementer

import json
import traceback


title = "Cobas C111"


@implementer(IInstrumentImportInterface)
class cobas_c111(object):
    """Cobas C111 Import Interface"""

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return self

    def Import(self, context, request):

        infile = request.form.get('cobas_c111_file', None)
        fileformat = request.form.get('cobas_c111_format', None)
        instrument = request.form.get('instrument', None)

        errors = []
        logs = []
        warns = []

        parser = None

        if not infile:
            errors.append(_("No file selected"))
            return json.dumps({
                'errors': errors,
                'log': logs,
                'warns': warns
            })

        # 👉 Define formatos soportados
        if fileformat == 'astm':
            parser = CobasC111Parser(infile)
        else:
            errors.append(_("Formato no soportado"))

        if parser:
            importer = CobasC111Importer(
                parser=parser,
                context=context,
                override=[False, False],
                instrument_uid=instrument
            )

            try:
                importer.process()
            except Exception:
                errors.append(traceback.format_exc())

            errors = importer.errors
            logs = importer.logs
            warns = importer.warns

        return json.dumps({
            'errors': errors,
            'log': logs,
            'warns': warns
        })
