from datetime import datetime, timedelta


def parse_time(input_time: str):
    units = {
        "s": ("секунда", "секунды", "секунд"),
        "m": ("минута", "минуты", "минут"),
        "h": ("час", "часа", "часов"),
        "d": ("день", "дня", "дней")
    }

    def choose_plural(n, titles):
        if n % 10 == 1 and n % 100 != 11:
            return titles[0]
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            return titles[1]
        else:
            return titles[2]

    number = int(input_time[:-1])
    unit = input_time[-1]

    if unit in units:
        if unit == "s":
            time_delta = timedelta(seconds=number)
        elif unit == "m":
            time_delta = timedelta(minutes=number)
        elif unit == "h":
            time_delta = timedelta(hours=number)
        elif unit == "d":
             time_delta = timedelta(days=number)

        end_time = datetime.now() + time_delta

        time_str = ""
        if time_delta.days > 0:
            time_str += f"{time_delta.days} {choose_plural(time_delta.days, units['d'])} "

        total_seconds = time_delta.seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if hours > 0:
            time_str += f"{hours} {choose_plural(hours, units['h'])} "

        if minutes > 0:
            time_str += f"{minutes} {choose_plural(minutes, units['m'])}"

        return end_time, time_str.strip()
    else:
        raise ValueError("Неподдерживаемый тип времени. Поддерживаются типы: 's', 'm', 'h', 'd'.")
