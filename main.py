import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types, F
from playwright.async_api import async_playwright

TOKEN = "8210784635:AAEZQ_Hnb_FWHPCloq_OCgFUCBWuMgCzEc4"
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_crypto_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    data = requests.get(url).json()
    return {
        "name": data['name'],
        "symbol": data['symbol'].upper(),
        "price": data['market_data']['current_price']['uzs'],
        "change": round(data['market_data']['price_change_percentage_24h'], 2),
        "icon": data['image']['small']
    }

async def generate_screenshot(info):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # HTML faylni yuklash (Fayl manzili to'g'ri bo'lishi kerak)
        path = os.path.abspath("index.html")
        await page.goto(f"file://{path}")
        
        # JS funksiyasini chaqirib ma'lumotlarni yuborish
        await page.evaluate(f"setData('{info['name']}', '{info['symbol']}', {info['price']}, {info['change']}, '{info['icon']}')")
        
        await page.locator("#crypto-card").screenshot(path="result.png")
        await browser.close()

@dp.message(F.text.lower().in_(["btc", "ton", "eth"]))
async def crypto_handler(message: types.Message):
    coin_map = {"btc": "bitcoin", "ton": "the-open-network", "eth": "ethereum"}
    coin_id = coin_map[message.text.lower()]
    
    await message.answer("📊 Ma'lumotlar yuklanmoqda...")
    info = await get_crypto_data(coin_id)
    await generate_screenshot(info)
    
    photo = types.FSInputFile("result.png")
    await bot.send_photo(message.chat.id, photo)

async def main():
    print("Bot yoqildi...")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())