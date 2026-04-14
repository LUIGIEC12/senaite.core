# -*- coding: utf-8 -*-

from bika.lims import bikaMessageFactory as _
from senaite.core.i18n import translate as t
from ..parser import CobasU411Parser
from ..importer import CobasU411Importer
import json
import traceback

title = "Cobas U 411"


def Import(context, request):

    infile = request.form.get('file', None)
    instrument = request.form.get('instrument', None)

    errors = []
    logs = []
    warns = []

    if not infile:
        errors.append(_("No file selected"))
        return json.dumps({'errors': errors, 'log': logs, 'warns': warns})

    parser = CobasU411Parser()

    importer = CobasU411Importer(
        parser=parser,
        context=context,
        instrument_uid=instrument
    )

    try:
        importer.process(infile)
    except Exception:
        errors.append(traceback.format_exc())

    return json.dumps({
        'errors': importer.errors,
        'log': importer.logs,
        'warns': importer.warns
    })


# 🔥 CLAVE PARA QUE APAREZCA
cobas_u411 = "cobas_u411"