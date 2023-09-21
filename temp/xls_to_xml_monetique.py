import toolbox.xls as xls
import toolbox.utils as utils
import os

# PARAMETERS
path = "C:/Users/abstraore/Downloads/monetique.xlsx"

establishement = "BDMSA"

pages = ["Fichier OK", "Fichier erreur_MTQ01", "Fichier erreur_MTQ02", "Fichier erreur MTQ03",
         "Fichier erreur_MTQ04", "Fichier erreur_MTQ05", "Fichier erreur_MTQ06", "Fichier erreur_MTQ07"]

period = [{"debut_period": "01-01-2020", "fin_period": "31-03-2020"}, {"debut_period": "01-04-2020", "fin_period": "30-06-2020"},
          {"debut_period": "01-07-2020", "fin_period": "30-09-2020"}, {"debut_period": "01-10-2020", "fin_period": "31-12-2020"}]

column = [{"nombre": "G", "alt_nombre": "K", "valeur": "M"}, {"nombre": "I", "alt_nombre": "O", "valeur": "Q"},
          {"nombre": "K", "alt_nombre": "S", "valeur": "U"}, {"nombre": "M", "alt_nombre": "W", "valeur": "Y"}]

detail_col = "B"

version = len(pages)

workbook = xls.load_workbook(path)


for page in pages:
    # START
    print("starting\n")
    if not os.path.exists("c:/Programming/scripts_queries/scripts/python/results/"+page):
        os.makedirs(
            "c:/Programming/scripts_queries/scripts/python/results/"+page)

    for i in range(0, len(period)):
        nombre = column[i]["nombre"]
        alt_nombre = column[i]["alt_nombre"]
        valeur = column[i]["valeur"]

        sections = {
            "01": {"row_start": 40, "row_end": 54, "section_row_codes": "1-8", "nombre": nombre},
            "02": {"row_start": 59, "row_end": 73, "section_row_codes": "1-6|AU|00", "nombre": nombre},
            "03": {"row_start": 78, "row_end": 92, "section_row_codes": "1-7|AU", "nombre": nombre},
            "04": {"row_start": 96, "row_end": 112, "section_row_codes": "1-9", "nombre": nombre},
            "05": {"row_start": 121, "row_end": 131, "section_row_codes": "1-4|AU|00", "nombre": alt_nombre, "valeur": valeur},
            "06": {"row_start": 137, "row_end": 145, "section_row_codes": "1-3|AU|00", "nombre": alt_nombre, "valeur": valeur},
            "07": {"row_start": 153, "row_end": 163, "section_row_codes": "1-4|AU|00", "nombre": alt_nombre, "valeur": valeur},
            "08": {"row_start": 168, "row_end": 176, "section_row_codes": "1-3|AU|00", "nombre": alt_nombre, "valeur": valeur},
            "09": {"row_start": 184, "row_end": 194, "section_row_codes": "1-4|AU|00", "nombre": alt_nombre, "valeur": valeur},
            "10": {"row_start": 199, "row_end": 207, "section_row_codes": "1-3|AU|00", "nombre": alt_nombre, "valeur": valeur},
            "11": {"row_start": 212, "row_end": 216, "section_row_codes": "1-2|00", "nombre": alt_nombre, "valeur": valeur}
        }

        # TEMPLATES
        monetique_template = """<?xml version="1.0" encoding="utf-8"?>\n<monetique>  \n<declaration>  \n<debutperiode>%(debut_period)s</debutperiode> \n<finperiode>%(fin_period)s</finperiode>  \n</declaration> \n<details>  %(data)s  </details>\n</monetique>"""
        data_template = """\n<data code="%(code)s">%(nombre)s %(valeur)s %(details)s</data>\n"""
        nombre_template = """\n   <nombre>%(nombre)s</nombre>\n"""
        valeur_template = """\n   <valeur>%(valeur)s</valeur>\n"""
        details_template = """\n   <details>%(details)s</details>\n"""

        # INITIALISATIONS
        code_prefix = "MTQ"
        debut_period = period[i]["debut_period"]
        fin_period = period[i]["fin_period"]

        filename = 'c:/Programming/scripts_queries/scripts/python/results/%(page)s/EME_%(establishement)s_%(fin_period)s_T_MONETIQUE_%(version)s_XML.XML' % {"page": page, "establishement": establishement,
                                                                                                                                                             "fin_period": fin_period, "version": version}
        data_tag = ""

        print("running .....")
        print("building data .....")
        for section_code, section in sections.items():

            # loop trough the sections rows
            expanded_section_code = utils.expand_section_code(
                section["section_row_codes"])

            for row in [str(row_int) for row_int in range(section["row_start"], section["row_end"]+1, 2)]:
                code = nombre = valeur = details = ""

                code = code_prefix + section_code + "_" + expanded_section_code.pop()

                if "nombre" in section:
                    if code not in ["MTQ04_08", "MTQ04_09"]:
                        nombre = nombre_template % {"nombre": xls.load_cell(
                            workbook, page, row, section["nombre"])}
                    else:
                        valeur = valeur_template % {"valeur": xls.load_cell(
                            workbook, page, row, section["nombre"])}

                if "valeur" in section:
                    valeur = valeur_template % {"valeur": xls.load_cell(
                        workbook, page, row, section["valeur"])}

                details = details_template % {"details": xls.load_cell_string(
                    workbook, page, row, detail_col)}

                data_tag += data_template % {"code": code,
                                             "nombre": nombre, "valeur": valeur, "details": details}

        print("generating xml ....%(page)s/%(debut)s - %(fin)s.\n" %
              {"page": page, "debut": debut_period, "fin": fin_period})

        xml = monetique_template % {
            "debut_period": debut_period, "fin_period": fin_period, "data": data_tag}

        with open(filename, 'w') as f:
            print(xml, file=f)

    # update version
    version -= 1
print("done.")
