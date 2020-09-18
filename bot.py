import telebot                  
from telebot import types       
import config
from geopy.distance import geodesic


bot = telebot.TeleBot(config.token)     


"""Створюємо клавіатуру(кнопки)"""
keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)        
button_addres = types.KeyboardButton("Найближчий відділ 'Нова Пошта'", request_location=True)       

keyboard_menu.add(button_addres)       


@bot.message_handler(commands=['start'])        

def send_welcome(message):      
    bot.send_message(message.chat.id, 'Привіт користувач!\nСпочатку увімкни доступ до геоданих, а потім натисни на кнопку, та що нижче ⬇️', reply_markup=keyboard_menu)   
@bot.message_handler(content_types=["location"])       
def departments(message):
    bot.send_message(message.chat.id, "Це було ваше місце розташування ⬆️")
    lon = message.location.longitude        
    lat = message.location.latitude

    distance = []   
    for m in config.departments:     
        result = geodesic((m["lant"], m["lont"]), (lon, lat)).meters   
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, "А тут ⬇️ найближче відділення")
    bot.send_venue(message.chat.id,                            
                   config.departments[index]["lont"],
                   config.departments[index]["lant"],
                   config.departments[index]["working hours"],
                   config.departments[index]["address"])
    bot.send_message(message.chat.id, "Якщо бажаєш прокласти маршрут до запропонованого відділення, то натисни на його.")


bot.polling() 
