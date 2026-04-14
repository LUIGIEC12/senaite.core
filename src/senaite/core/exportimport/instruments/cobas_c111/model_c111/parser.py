# -*- coding: utf-8 -*-

class CobasC111Parser(object):

    def __init__(self, infile):
        self.infile = infile

    def parse(self):
        results = {}
        content = self.infile.read()

        if isinstance(content, bytes):
            content = content.decode("utf-8")

        lines = content.splitlines()

        for line in lines:
            parts = line.split(";")

            if len(parts) < 3:
                continue

            sample_id = parts[0].strip()
            analysis = parts[1].strip()
            value = parts[2].strip()

            if sample_id not in results:
                results[sample_id] = {
                    "SampleID": sample_id,
                    "Analyses": []
                }

            results[sample_id]["Analyses"].append({
                "Keyword": analysis,
                "Result": value
            })

        return list(results.values())
