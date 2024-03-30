def text_rost(days_in):
    try:
        if days_in == 1:
            return "1 день"
        elif days_in < 7:
            return f"{days_in} дня" if days_in in (2, 3, 4) else f"{days_in} дней"
        else:
            months = days_in // 30
            weeks = (days_in % 30) // 7
            days = (days_in % 30) % 7
            result = ""
            if months > 0:
                result += f"{months} месяц, " if months == 1 else f"{months} месяца, "
            if weeks > 0:
                result += f"{weeks} неделя, " if weeks == 1 else f"{weeks} недели, "
            if days > 0:
                result += f"{days} день" if days == 1 else f"{days} дня"
            return result
    except TypeError:
        return None
