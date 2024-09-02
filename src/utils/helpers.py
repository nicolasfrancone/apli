from datetime import datetime


def is_within_working_hours(current_time, sheet_data):
    weekday = current_time.weekday()
    week_start_time = datetime.strptime(sheet_data['hora_inico_semana'], '%H:%M:%S').time()
    week_end_time = datetime.strptime(sheet_data['hora_fin_semana'], '%H:%M:%S').time()

    if sheet_data['horarios_no_dispo'] != '-':  # Verifica que no sea un guion
        unavailable_start, unavailable_end = [datetime.strptime(t, '%H:%M').time() for t in
                                              sheet_data['horarios_no_dispo'].split(' a ')]
    else:
        unavailable_start, unavailable_end = None, None  # No hay horarios no disponibles

    saturday_start, saturday_end = [datetime.strptime(t, '%H:%M').time() for t in
                                    sheet_data['horarios_sabados'].split(' a ')]

    if weekday < 5:  # De lunes a viernes
        if not (week_start_time <= current_time.time() < week_end_time):
            return False
    elif weekday == 5:  # Sábados
        if not (saturday_start <= current_time.time() < saturday_end):
            return False
    else:  # Domingos no se trabaja
        return False

    # Solo verificar horarios no disponibles si están definidos
    if unavailable_start and unavailable_end and unavailable_start <= current_time.time() < unavailable_end:
        return False

    return True
