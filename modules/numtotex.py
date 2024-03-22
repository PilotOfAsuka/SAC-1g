
def text_rost(days_in):
    if days_in == 1:
        return "День"
    elif days_in < 7:
        return f"{days_in} дней"
    else:
        mouth = days_in // 30
        weak = (days_in % 30) // 7
        days = (days_in % 30) % 7
        if mouth > 0:
            if weak > 0:
                return f"{mouth} месяц, {weak} неделя и {days} дня"
            else:
                return f"{mouth} месяц и {days} дня"
        else:
            return f"{weak} неделя и {days} дня"


