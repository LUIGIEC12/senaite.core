# -*- coding: utf-8 -*-
#
# Cobas C111 - Instrument Interface (SENAITE)
#

from bika.lims import bikaMessageFactory as _
from senaite.core.i18n import translate as t

import json
import traceback

# IMPORTS LOCALES
from .parser import CobasC111Parser
from .importer import CobasC111Importer


# 🔥 ESTE TITLE ES EL QUE SE MUESTRA EN LA UI
title = "Cobas C111"


def Import(context, request):
    """Importador de resultados Cobas C111"""

    errors = []
    logs = []
    warns = []

    try:
        infile = request.form.get('cobas_c111_file', None)
        fileformat = request.form.get('cobas_c111_format', None)
        instrument = request.form.get('instrument', None)

        # VALIDACIÓN ARCHIVO
        if not infile:
            errors.append(_("No file selected"))
            return json.dumps({
                'errors': errors,
                'log': logs,
                'warns': warns
            })

        # 🔥 PARSER
        parser = None

        if fileformat == 'astm':
            parser = CobasC111Parser()
        else:
            errors.append(
                t(_("Formato no soportado: ${fileformat}",
                    mapping={"fileformat": fileformat}))
            )

        if not parser:
            return json.dumps({
                'errors': errors,
                'log': logs,
                'warns': warns
            })

        # 🔥 IMPORTER (ESTRUCTURA CORRECTA SENAITE)
        importer = CobasC111Importer(
            parser=parser,
            context=context,
            override=[False, False],
            instrument_uid=instrument
        )

        # 🔥 PROCESO
        try:
            importer.process(infile)
        except Exception:
            errors.append(traceback.format_exc())

        # RESULTADOS
        errors = importer.errors
        logs = importer.logs
        warns = importer.warns

    except Exception:
        errors.append(traceback.format_exc())

    return json.dumps({
        'errors': errors,
        'log': logs,
        'warns': warns
    })


cobas_c111 = Import

Import = Import
