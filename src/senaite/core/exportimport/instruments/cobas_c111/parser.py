class CobasC111Parser(object):

    def parse(self, file_content):
        results = []

        lines = file_content.splitlines()

        for line in lines:
            parts = line.split(";")  # ajusta según tu archivo

            if len(parts) < 3:
                continue

            sample_id = parts[0]
            analysis = parts[1]
            value = parts[2]

            results.append({
                "SampleID": sample_id,
                "Analysis": analysis,
                "Result": value,
            })

        return results
