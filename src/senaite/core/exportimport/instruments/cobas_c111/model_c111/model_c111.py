# -*- coding: utf-8 -*-

from bika.lims import bikaMessageFactory as _
from senaite.core.i18n import translate as t
from .parser import CobasC111Parser
from .importer import CobasC111Importer
import json
import traceback


class CobasC111(object):
    """Modelo del instrumento Cobas C111 para SENAITE"""

    title = "Cobas C111"
    description = "Interfaz de importación para Cobas C111"
    file_formats = ("astm",)

    def __init__(self):
        self.parser = CobasC111Parser
        self.importer = CobasC111Importer

    def Import(self, context, request):
        """Punto de entrada para la importación desde la UI"""

        errors = []
        logs = []
        warns = []

        try:
            # 🔹 Obtener datos del formulario
            infile = request.form.get('cobas_c111_file')
            fileformat = request.form.get('cobas_c111_format')
            instrument_uid = request.form.get('instrument')

            # 🔴 Validaciones básicas
            if not infile:
                errors.append(_("No file selected"))
                return self._response(errors, logs, warns)

            if not fileformat:
                errors.append(_("No file format selected"))
                return self._response(errors, logs, warns)

            if fileformat not in self.file_formats:
                errors.append(_("Formato no soportado: %s") % fileformat)
                return self._response(errors, logs, warns)

            if not instrument_uid:
                warns.append(_("Instrumento no especificado"))

            logs.append(_("Iniciando importación Cobas C111"))

            # 🔹 Crear parser
            parser = self.parser(infile)

            # 🔹 Crear importer
            importer = self.importer(
                parser=parser,
                context=context,
                override=[False, False],
                instrument_uid=instrument_uid
            )

            # 🔹 Ejecutar proceso
            importer.process()

            # 🔹 Recoger resultados
            errors.extend(importer.errors)
            logs.extend(importer.logs)
            warns.extend(importer.warns)

            logs.append(_("Importación finalizada"))

        except Exception:
            errors.append(traceback.format_exc())

        return self._response(errors, logs, warns)

    # 🔧 Helper para respuesta estándar SENAITE
    def _response(self, errors, logs, warns):
        return json.dumps({
            'errors': errors,
            'log': logs,
            'warns': warns
        })


# 🔥 REGISTRO OBLIGATORIO DEL INSTRUMENTO
cobas_c111 = CobasC111
