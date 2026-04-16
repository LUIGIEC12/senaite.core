# -*- coding: utf-8 -*-

class CobasC111Parser(object):

    def parse(self, raw_data):
        results = []

        # 🔥 1. Limpiar capa ASTM (control chars)
        cleaned = raw_data.replace('\x02', '').replace('\x03', '') \
                          .replace('\x17', '').replace('\x04', '')

        # 🔥 2. Separar registros ASTM (CR)
        records = cleaned.split('\r')

        current_sample = None

        for record in records:

            if not record:
                continue

            fields = record.split('|')
            record_type = fields[0]

            # 🧾 PATIENT
            if record_type == 'P':
                if len(fields) > 3:
                    current_sample = fields[3].strip()

            # 🧪 ORDER
            elif record_type == 'O':
                if len(fields) > 2:
                    current_sample = fields[2].strip()

            # 🔬 RESULT (🔥 CLAVE)
            elif record_type == 'R':
                try:
                    test_field = fields[2]  # ^^^111
                    value = fields[3]
                    units = fields[4]
                    flag = fields[6]
                    status = fields[8]

                    # 🔥 Extraer código de test (ej: 111)
                    test_code = test_field.split('^')[-1]

                    results.append({
                        "SampleID": current_sample,
                        "Analysis": test_code,
                        "Result": value,
                        "Units": units,
                        "Flag": flag,
                        "Status": status,
                    })

                except Exception:
                    continue

        return results
