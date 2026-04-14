# -*- coding: utf-8 -*-

from bika.lims import bikaMessageFactory as _
from senaite.core.i18n import translate as t
from ..parser import Urisys1100Parser
from ..importer import Urisys1100Importer
import json
import traceback

title = "Urisys 1100"


def Import(context, request):

    infile = request.form.get('file', None)
    instrument = request.form.get('instrument', None)

    errors = []
    logs = []
    warns = []

    if not infile:
        errors.append(_("No file selected"))
        return json.dumps({'errors': errors, 'log': logs, 'warns': warns})

    parser = Urisys1100Parser()

    importer = Urisys1100Importer(
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
        'log': logs,
        'warns': warns
    })


# 🔥 CLAVE PARA QUE APAREZCA
urisys_1100 = "urisys_1100"