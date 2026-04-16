# -*- coding: utf-8 -*-

import re


class Urisys1100Parser(object):

    def parse(self, raw):
        """
        Auto-detecta formato del equipo Urisys 1100
        """

        if isinstance(raw, bytes):
            raw = raw.decode(errors="ignore")

        raw = raw.strip()

        # 🔥 DETECCIÓN AUTOMÁTICA
        if raw.startswith("H|") or "|R|" in raw:
            return self._parse_astm(raw)

        return self._parse_text(raw)

    # =========================
    # ASTM MODE
    # =========================
    def _parse_astm(self, raw):
        results = []
        current_sample = None

        records = raw.split("\r")

        for rec in records:
            fields = rec.split("|")

            if not fields:
                continue

            rec_type = fields[0]

            # SAMPLE
            if rec_type == "O":
                current_sample = fields[2] or fields[3]

            # RESULT
            elif rec_type == "R":
                test_id = fields[2].replace("^", "")
                value = fields[3]
                unit = fields[4] if len(fields) > 4 else ""

                results.append({
                    "SampleID": current_sample,
                    "Analysis": test_id,
                    "Result": value,
                    "Unit": unit,
                })

        return results

    # =========================
    # TEXT MODE (URYSIS REAL)
    # =========================
    def _parse_text(self, raw):
        results = []
        current_sample = "UNKNOWN"

        lines = raw.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # SAMPLE ID
            if "ID" in line.upper():
                current_sample = re.sub(r'[^A-Za-z0-9\-]', '', line)
                continue

            # 🔥 PARÁMETROS DE ORINA
            match = re.match(r"([A-Za-z]+)\s*[:=]\s*(.+)", line)

            if match:
                param = match.group(1).upper()
                value = match.group(2)

                results.append({
                    "SampleID": current_sample,
                    "Analysis": param,
                    "Result": value,
                })

            # 🔥 FORMATO TABULAR
            parts = re.split(r'[;\t|]', line)

            if len(parts) >= 2:
                results.append({
                    "SampleID": current_sample,
                    "Analysis": parts[0].strip().upper(),
                    "Result": parts[1].strip(),
                })

        return results
