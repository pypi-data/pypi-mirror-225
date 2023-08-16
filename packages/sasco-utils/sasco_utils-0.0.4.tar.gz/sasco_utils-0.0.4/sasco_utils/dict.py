# -*- coding: utf-8 -*-

"""
Python Utils by SASCO
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

import json
import csv


def dict_save_to_json(json_filename, dict_data, sort_keys = False, indent = 4):
    json_data = json.dumps(dict_data, sort_keys = sort_keys, indent = indent)
    with open(json_filename, 'w') as f:
        f.write(json_data)

def dict_save_to_csv(csv_filename, dict_data, delimiter = ';'):
    if len(dict_data) > 0:
        keys = dict_data[0].keys()
        with open(csv_filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames = keys, delimiter = delimiter)
            dict_writer.writeheader()
            dict_writer.writerows(dict_data)
    else:
        with open(csv_filename, 'w') as f:
            f.write('')

def dict_load_from_csv(csv_filename, delimiter = ';'):
    dict_data = []
    with open(csv_filename, newline='') as input_file:
        reader = csv.DictReader(input_file, delimiter = delimiter)
        for row in reader:
            dict_data.append(row)
    return dict_data
