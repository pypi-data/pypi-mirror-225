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

from datetime import date, datetime, timedelta


def period_current():
    return int(date.today().strftime('%Y%m'))

def period_previous(period = None):
    if period is None:
        period = period_current()
    previous_period = period - 1
    if len(str(period)) == 6 and int(str(previous_period)[4:]) == 0:
        previous_period = previous_period - 100 + 12
    return previous_period

def period_next(period = None):
    if period is None:
        period = period_current()
    next_period = period + 1
    if len(str(period)) == 6 and int(str(next_period)[4:]) == 13:
        next_period = next_period + 100 - 12
    return next_period

def period_range(period_from, period_to = None):
    if period_to is None:
        period_to = period_current()
    periods = []
    period = period_from
    while period <= period_to :
        periods.append(period)
        period = period_next(period)
    return periods

def period_first_day(period):
    return str(period)[0:4]+'-'+str(period)[4:]+'-01'

def period_last_day(period):
    first_day_next_period = period_first_day(period_next(period))
    first_day_next_period_object = datetime.strptime(first_day_next_period, '%Y-%m-%d')
    last_day_object = first_day_next_period_object - timedelta(days=1)
    return last_day_object.strftime('%Y-%m-%d')

def period_valid(period, year_from = 2000, year_to = 2100):
    try:
        int(period)
    except ValueError:
        return False
    period = str(period)
    n_period = len(period)
    if n_period == 4:
        period = int(period)
        return period >= year_from and period <= year_to
    elif n_period == 6:
        year = int(period[0:4])
        month = int(period[4:])
        return year >= year_from and year <= year_to and month >= 1 and month <= 12
    else:
        return False

def date_normalize(date, format_from = None, format_to = None):
    if format_from is None:
        aux = date.split(' ')
        if len(aux) == 2:
            if len(aux[1]) == 5:
                format_from = '%d/%m/%Y %H:%M'
                format_to = '%Y-%m-%d %H:%M'
            else:
                format_from = '%d/%m/%Y %H:%M:%S'
                format_to = '%Y-%m-%d %H:%M:%S'
        else:
            format_from = '%d/%m/%Y'
            format_to = '%Y-%m-%d'
    date_obj = datetime.strptime(date, format_from)
    return date_obj.strftime(format_to)

def date_add_days(days, from_date = None):
    if from_date is None:
        from_date = str(date.today().strftime('%Y-%m-%d'))
    y, m, d = from_date.split('-')
    specific_date = datetime(int(y), int(m), int(d))
    new_date = specific_date + timedelta(days = days)
    return str(new_date).split(' ')[0]

def date_count_days(date_from, date_to = None):
    if date_to is None:
        date_to = str(date.today().strftime('%Y-%m-%d'))
    y_from, m_from, d_from = str(date_from).split(' ')[0].split('-')
    y_to, m_to, d_to = str(date_to).split(' ')[0].split('-')
    delta = date(int(y_to), int(m_to), int(d_to)) - date(int(y_from), int(m_from), int(d_from))
    return delta.days if delta.days >= 0 else delta.days * -1

def month_from_string(month):
    month_lower = month.lower()
    months = {
        'enero': '01',
        'febrero': '02',
        'marzo': '03',
        'abril': '04',
        'mayo': '05',
        'junio': '06',
        'julio': '07',
        'agosto': '08',
        'septiembre': '09',
        'octubre': '10',
        'noviembre': '11',
        'diciembre': '12',
    }
    return months[month_lower] if month_lower in months else month

def month_from_index(index):
    index = int(index) % 12
    months = [
        'enero',
        'febrero',
        'marzo',
        'abril',
        'mayo',
        'junio',
        'julio',
        'agosto',
        'septiembre',
        'octubre',
        'noviembre',
        'diciembre',
    ]
    return months[index]

def month_from_number(month):
    return month_from_index(int(month)-1)
