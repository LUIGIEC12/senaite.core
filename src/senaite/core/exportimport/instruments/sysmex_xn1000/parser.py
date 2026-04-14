# -*- coding: utf-8 -*-

class SysmexXN1000Parser(object):

    def parse(self, file_content):
        results = []

        lines = file_content.splitlines()

        for line in lines:
            parts = line.split(";")

            if len(parts) < 3:
                continue

            results.append({
                "SampleID": parts[0].strip(),
                "Analysis": parts[1].strip(),
                "Result": parts[2].strip(),
            })

        return results