# -*- coding: utf-8 -*-

from bika.lims import bikaMessageFactory as _
from ..parser import SysmexXN1000Parser
from ..importer import SysmexXN1000Importer
import json
import traceback

title = "Sysmex XN1000"


def Import(context, request):

    infile = request.form.get('file', None)
    instrument = request.form.get('instrument', None)

    errors = []
    logs = []
    warns = []

    if not infile:
        errors.append(_("No file selected"))
        return json.dumps({'errors': errors, 'log': logs, 'warns': warns})

    parser = SysmexXN1000Parser()

    importer = SysmexXN1000Importer(
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


# 🔥 CLAVE
sysmex_xn1000 = "sysmex_xn1000"