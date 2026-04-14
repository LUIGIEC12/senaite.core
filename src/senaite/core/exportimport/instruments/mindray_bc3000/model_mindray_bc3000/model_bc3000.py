# -*- coding: utf-8 -*-

from bika.lims import bikaMessageFactory as _
from senaite.core.i18n import translate as t
from ..parser import MindrayBC3000Parser
from ..importer import MindrayBC3000Importer
import json
import traceback

title = "Mindray BC3000"


def Import(context, request):

    infile = request.form.get('file', None)
    instrument = request.form.get('instrument', None)

    errors = []
    logs = []
    warns = []

    if not infile:
        errors.append(_("No file selected"))
        return json.dumps({'errors': errors, 'log': logs, 'warns': warns})

    parser = MindrayBC3000Parser()

    importer = MindrayBC3000Importer(
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


# 🔥 CRÍTICO (esto hace que aparezca en la lista)
mindray_bc3000 = "mindray_bc3000"