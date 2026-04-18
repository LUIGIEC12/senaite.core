# -*- coding: utf-8 -*-

class CobasU411Parser(object):

    def __init__(self, raw_data):
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode('utf-8', errors='ignore')
        self.raw_data = raw_data

    def parse(self):
        results = []

        cleaned = self.raw_data.replace('\x02', '') \
                              .replace('\x03', '') \
                              .replace('\x17', '') \
                              .replace('\x04', '')

        records = cleaned.split('\r')

        current_sample = None

        for record in records:

            if not record:
                continue

            fields = record.split('|')
            record_type = fields[0]

            if record_type == 'O':
                current_sample = fields[2] if len(fields) > 2 else current_sample

            elif record_type == 'P' and not current_sample:
                current_sample = fields[3] if len(fields) > 3 else current_sample

            elif record_type == 'R':
                try:
                    test_field = fields[2] if len(fields) > 2 else ''
                    value = fields[3] if len(fields) > 3 else ''
                    units = fields[4] if len(fields) > 4 else ''
                    flag = fields[6] if len(fields) > 6 else ''
                    status = fields[8] if len(fields) > 8 else ''

                    test_code = test_field.split('^')[-1]

                    results.append({
                        "SampleID": current_sample,
                        "Analysis": test_code,
                        "Result": value,
                        "Units": units,
                        "Flag": flag,
                        "Status": status,
                    })

                except Exception as e:
                    print("Parser error:", str(e))
                    continue

        return results
