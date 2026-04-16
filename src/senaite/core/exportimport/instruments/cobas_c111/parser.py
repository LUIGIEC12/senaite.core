# -*- coding: utf-8 -*-

class CobasC111Parser(object):

    def parse(self, file_content):
        results = []

        sample_id = None

        lines = file_content.split("\r")

        for line in lines:
            if not line.strip():
                continue

            fields = line.split("|")
            record_type = fields[0]

            # =========================
            # PATIENT RECORD
            # =========================
            if record_type == "P":
                if len(fields) > 3:
                    sample_id = fields[3].strip()

            # =========================
            # RESULT RECORD
            # =========================
            elif record_type == "R":

                try:
                    test_field = fields[2]
                    test_id = test_field.split("^")[3]

                    value = fields[3].strip()
                    unit = fields[4].strip() if len(fields) > 4 else ""

                    flag = fields[6].strip() if len(fields) > 6 else "N"

                    results.append({
                        "SampleID": sample_id,
                        "Analysis": test_id,
                        "Result": value,
                        "Unit": unit,
                        "Flag": flag,
                    })

                except Exception:
                    continue

        return results
