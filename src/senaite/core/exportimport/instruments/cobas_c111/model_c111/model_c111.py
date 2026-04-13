from bika.lims import bikaMessageFactory as _
from senaite.core.i18n import translate as t
from .parser import CobasC111Parser
from .importer import CobasC111Importer
import json
import traceback

title = "Cobas C111"


def Import(context, request):

    infile = request.form['cobas_c111_file']
    fileformat = request.form['cobas_c111_format']
    instrument = request.form.get('instrument', None)

    errors = []
    logs = []
    warns = []

    parser = None

    if not infile:
        errors.append(_("No file selected"))

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

cobas_c111 = "cobas_c111"
