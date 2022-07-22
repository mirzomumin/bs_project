from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import requests
import bs4


def start(update, context):
	username = update.message.from_user.first_name
	update.message.reply_html(f'Hello, {username}. I\'m ASAXIY BOT🤖\n\
		\nType me in what you want to find out')


def send_info(update, context):
	text = update.message.text
	url = f'https://asaxiy.uz/product?key={text}'
	response = requests.get(url)

	soup = bs4.BeautifulSoup(response.text, 'html.parser')
	rows = soup.select('div.col-6.col-xl-3.col-md-4')

	for row in rows[0:10]:
		# print(type(row))
		if type(row) == bs4.element.Tag:
			image = row.select('div.product__item-img img')[0]['data-src']
			if image[-5:] == '.webp':
				image = image[:-5]
			info = row.select('div.product__item-info > a > h5')[0].text
			price = row.select('div.product__item-info > div.product__item-info--prices > div > span')[0].text
			try:
				update.message.reply_photo(image, f'{info}\n \nPrice: {price}')
			except:
				pass

def main():
	updater = Updater('5504055914:AAFnMBGhvmsm7VUWLhfdv5gurvyv-BL6hKc', use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('start', start))
	dp.add_handler(MessageHandler(Filters.text, send_info))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()