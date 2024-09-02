from datetime import datetime, timedelta
from collections import defaultdict
from pytz import timezone as pytz_timezone
from src.utils.helpers import is_within_working_hours

class Scheduler:
    def __init__(self):
        self.sheet_data = {}
        self.calendar_data = {}
        self.available_slots = []
        self.sheet_time_zone = None
        self.sheet_interval = None
        self.start_date_schedule = None
        self.end_date_schedule = None
        self.modalidad = None

    def update_sheet_data(self, data):
        self.sheet_data = data
        self.sheet_time_zone = data.get('timezone')
        self.sheet_interval = data.get('intervalo')
        self.start_date_schedule = data.get("interview_start_schedule")
        self.end_date_schedule = data.get("interview_end_schedule")
        self.modalidad = data.get('modalidad')

    def update_calendar_data(self, data):
        self.calendar_data = data

    def process_availability(self):
        if not self.sheet_data or not self.calendar_data:
            print("No se han recibido ambos conjuntos de datos.")
            return

        tz = pytz_timezone(self.sheet_time_zone)
        start_time, end_time = self.get_schedule_time_range(tz)
        availability_view_interval = int(self.sheet_interval)
        max_candidates_per_interval = int(self.sheet_data['candidatos_por_intervalo'])

        availability_view = self.calendar_data["value"][0]["availabilityView"]
        self.available_slots.clear()
        interval_counts = self.count_intervals(tz, availability_view_interval, max_candidates_per_interval)

        print(availability_view_interval)
        total_intervals = int((end_time - start_time).total_seconds() / (availability_view_interval * 60))
        print(f"Total de intervalos calculados: {total_intervals}")

        self.populate_available_slots(start_time, total_intervals, availability_view, interval_counts, max_candidates_per_interval)

        for slot in self.available_slots:
            print(f"Disponible: {slot}")

    def get_schedule_time_range(self, tz):
        start_date_str = self.sheet_data['formatted_start_date']
        end_date_str = self.sheet_data['formatted_end_date']
        start_time = tz.localize(datetime.strptime(f"{start_date_str} 00:00:00", '%Y-%m-%d %H:%M:%S'))
        end_time = tz.localize(datetime.strptime(f"{end_date_str} 23:00:00", '%Y-%m-%d %H:%M:%S'))
        return start_time, end_time

    def count_intervals(self, tz, availability_view_interval, max_candidates_per_interval):
        interval_counts = defaultdict(int)
        for schedule_info in self.calendar_data["value"]:
            for item in schedule_info["scheduleItems"]:
                start_time_item = datetime.fromisoformat(item["start"]["dateTime"]).replace(
                    tzinfo=pytz_timezone('UTC')).astimezone(tz)
                end_time_item = datetime.fromisoformat(item["end"]["dateTime"]).replace(
                    tzinfo=pytz_timezone('UTC')).astimezone(tz)

                # Aquí calculamos el intervalo de inicio al que corresponde el evento
                start_block_time = start_time_item.replace(minute=0, second=0, microsecond=0) + \
                                   timedelta(minutes=(
                                                                 start_time_item.minute // availability_view_interval) * availability_view_interval)

                current_time_item = start_block_time

                while current_time_item < end_time_item:
                    interval_key = current_time_item.strftime('%Y-%m-%dT%H:%M:%S')
                    if "Apli" in item.get("subject", ""):
                        interval_counts[interval_key] += 1
                        print(
                            f"Contando reunión 'Apli' en {interval_key}. Total en este intervalo: {interval_counts[interval_key]}")
                    else:
                        # Si el evento no tiene 'Teams' en la ubicación, anulamos el intervalo completo
                        interval_counts[interval_key] = max_candidates_per_interval + 1
                        print(f"Intervalo {interval_key} marcado como no disponible por evento sin 'Apli'")

                    current_time_item += timedelta(minutes=availability_view_interval)
        return interval_counts

    def populate_available_slots(self, start_time, total_intervals, availability_view, interval_counts,
                                 max_candidates_per_interval):
        current_time = start_time
        now = datetime.now(pytz_timezone(self.sheet_time_zone))
        tomorrow = now + timedelta(days=1)
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        print(tomorrow_start)
        print(current_time)

        for i in range(total_intervals):
            interval_key = current_time.strftime('%Y-%m-%dT%H:%M:%S')
            print(f"Evaluando intervalo: {interval_key}, Índice: {i}")

            if current_time < tomorrow_start:  # Verifica si el intervalo es anterior al comienzo del día siguiente
                print(f"Omitiendo {interval_key} porque es una fecha pasada o la actual.")
                current_time += timedelta(minutes=self.sheet_interval)
                continue  # Salta a la siguiente iteración si el intervalo es anterior al comienzo de mañana

            if i >= len(availability_view):
                print(
                    f"Advertencia: Índice {i} fuera del rango para availability_view. Longitud de availability_view: {len(availability_view)}")
                break

            if is_within_working_hours(current_time, self.sheet_data):
                print(f"{interval_key} está dentro del horario laboral")

                # Verificamos si el intervalo no ha sido marcado como no disponible por evento sin 'Apli'
                if interval_counts[interval_key] <= max_candidates_per_interval:
                    if availability_view[i] == '0':
                        print(f"{interval_key} está totalmente disponible")
                        self.available_slots.append(interval_key)
                    elif availability_view[i] == '2':
                        print(f"{interval_key} tiene estado 2. Reuniones contadas: {interval_counts[interval_key]}")
                        if interval_counts[interval_key] < max_candidates_per_interval:
                            print(
                                f"{interval_key} tiene {interval_counts[interval_key]} reuniones. Máximo permitido: {max_candidates_per_interval}")
                            self.available_slots.append(interval_key)

            current_time += timedelta(minutes=self.sheet_interval)


scheduler = Scheduler()
