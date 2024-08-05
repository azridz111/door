import requests
import telebot


BOT_TOKEN = '7255568673:AAGyTRIQD4tlmljjCYp-AgTUWlsEX9kqC1w'
bot = telebot.TeleBot(BOT_TOKEN)

user_data_dict = {}

def check_balance(access_token):
    url = "https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/balance"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': "okhttp/4.9.3",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'language': "AR",
        'request-id': "995fd8a7-853c-481d-b9c6-0a24295df76a",
        'flavour-type': "gms"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        accounts = response_json.get('accounts', [])

        for account in accounts:
            if account.get('label') == 'رصيد التكفل المهدى':
                return account.get('value', None)

    return None

def send_internet(access_token):
    url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'language': 'AR',
        'request-id': 'ef69f4c6-2ead-4b93-95df-106ef37feefd',
        'flavour-type': 'gms',
        'Content-Type': 'application/json'
    }
    payload = {"mgmValue": "ABC"}

    for _ in range(6):
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Request succeeded")
        else:
            print("Request failed with status code:", response.status_code)

    print('تم إرسال الإنترنت بنجاح!')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أهلاً! أدخل رقم الهاتف (يجب أن يكون رقم يوز):")
    bot.register_next_step_handler(message, process_phone_number)

def process_phone_number(message):
    num = message.text
    user_data_dict[message.chat.id] = {'phone_number': num}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }
    data = {
        'client_id': 'ibiza-app',
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }
    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)

    if 'ROOGY' in response.text:
        bot.send_message(message.chat.id, 'تم إرسال رمز. أدخل الرمز:')
        bot.register_next_step_handler(message, process_otp, headers, data)
    else:
        bot.send_message(message.chat.id, 'فشل في إرسال رمز.')

def process_otp(message, headers, data):
    otp = message.text
    data['otp'] = otp
    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        if access_token:
            bot.send_message(message.chat.id, '✅ تم التحقق بنجاح. يتم الآن إرسال الإنترنت...')
            send_internet(access_token)
            balance = check_balance(access_token)
            if balance is not None:
                bot.send_message(message.chat.id, f"📊 حجم الأنترنت المتبقي: {balance}")
            else:
                bot.send_message(message.chat.id, "❌ فشل في استرداد الرصيد.")


            bot.send_message(message.chat.id, "🎉 تم التفعيل بنجاح!")


            show_developer_info(message)
    else:
        bot.send_message(message.chat.id, '❌ فشل في التحقق من الرمز.')

def show_developer_info(message):

    bot.send_message(message.chat.id, f"💡 تم تطوير هذا البوت من قبل: yazid\nللتواصل: https://t.me/techdz4")

@bot.message_handler(commands=['developer'])
def developer(message):
    show_developer_info(message)

if __name__ == "__main__":
    bot.polling(none_stop=True)
