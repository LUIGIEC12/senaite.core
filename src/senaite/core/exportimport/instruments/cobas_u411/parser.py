# -*- coding: utf-8 -*-

class CobasU411Parser(object):

    def parse(self, file_content):
        results = []

        lines = file_content.splitlines()

        for line in lines:
            parts = line.split(";")

            if len(parts) < 2:
                continue

            sample_id = parts[0].strip()

            analytes = [
                "LEU", "NIT", "URO", "PRO", "PH",
                "BLO", "SG", "KET", "BIL", "GLU"
            ]

            for i, analyte in enumerate(analytes):
                if i + 1 >= len(parts):
                    continue

                value = parts[i + 1].strip()

                if not value:
                    continue

                results.append({
                    "SampleID": sample_id,
                    "Analysis": analyte,
                    "Result": value,
                })

        return results