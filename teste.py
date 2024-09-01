def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"
        
def time_to_minute(time_str):
    hour, minute = map(int, time_str.split(":"))
    return hour * 60 + minute

tempo = "-6:00"     
hora_minutos = time_to_minute(tempo)
minutos_horas = minutes_to_time(hora_minutos)

print(f"{tempo} convertido para minutos: {hora_minutos},\nminutos convertidos novamente para horas: {minutos_horas}")