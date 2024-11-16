import telebot
import requests
import json
import os



token = "7829782312:AAGN3FUf05wUJJtHd5NV3BaJ3bo0S-Gxslc"
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "اهلا بك عزيزي ارسل النص بلغه الانكليزيه لتحويله لصوره")
@bot.message_handler(func=lambda message: True)
def generate_image(message):
	user_input = message.text
	headers = {
    'authority': 'www.blackbox.ai',
    'accept': '*/*',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
     'cookie': 'sessionId=ae730a29-981e-4dcb-9cd8-b72415e86d68; __Host-authjs.csrf-token=317b4272e5639c2a132bc8bdc7e20706302a75cb53c90c18b3ee2561e5de43ec%7Cdd079965257f03619ec75462ef6afa9041acb16d651d151931d05b61aaa49640; __Secure-authjs.callback-url=https%3A%2F%2Fwww.blackbox.ai; intercom-id-jlmqxicb=a3660d6f-a754-48fb-be30-2ffe26e35e6b; intercom-session-jlmqxicb=; intercom-device-id-jlmqxicb=04ca5dee-12de-44b2-9066-c109b7d891eb',
    'origin': 'https://www.blackbox.ai',
    'referer': 'https://www.blackbox.ai/agent/ImageGenerationLV45LJp',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}


	json_data = {
    'messages': [
        {
            'id': 'BInlT_BidR17C9Q9LuxPP',
            'content': user_input,
            'role': 'user',
        },
    ],
    'id': 'BInlT_BidR17C9Q9LuxPP',
    'previewToken': None,
    'userId': None,
    'codeModelMode': True,
    'agentMode': {
        'mode': True,
        'id': 'ImageGenerationLV45LJp',
        'name': 'Image Generation',
    },
    'trendingAgentMode': {},
    'isMicMode': False,
    'maxTokens': 1024,
    'playgroundTopP': None,
    'playgroundTemperature': None,
    'isChromeExt': False,
    'githubToken': None,
    'clickedAnswer2': False,
    'clickedAnswer3': False,
    'clickedForceWebSearch': False,
    'visitFromDelta': False,
    'mobileClient': False,
    'userSelectedModel': None,
    'validated': '00f37b34-a166-4efb-bce5-1312d87f2f94',
}


	rr = requests.post('https://www.blackbox.ai/api/chat', headers=headers, json=json_data).text
	print(rr)
	parts = rr.split('(')
	if len(parts) > 1:
		link = parts[1].split(')')[0]
		bot.send_photo(message.chat.id,link)
	else:
		print("لا يوجد رابط في النص")
		
bot.polling()
@app.route('/')
