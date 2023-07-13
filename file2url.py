import os, requests, subprocess
from pathlib import Path
try:
    from telegram.ext import Updater, MessageHandler, Filters
except ImportError:
    subprocess.run(['pip', 'install', 'python-telegram-bot==13.7.0'])
    from telegram.ext import Updater, MessageHandler, Filters
try:
    import huggingface_hub
    from huggingface_hub import HfApi
except ImportError:
    subprocess.run(['pip', 'install', 'huggingface_hub'])
    import huggingface_hub
    from huggingface_hub import HfApi
bot_token = "6666666666:ProlapSE-GaY_CumSWaLlower-FIStinG" # токен для telegram бота
hfrepo = "имя/репо" # репозиторий на huggingface
hftoken = "hf_**********************************" # токен Role:Write на huggingface
hftoken_local_path = os.path.expanduser("~")+"/.cache/huggingface/token" # путь до сохранения токена HF, для винды это обычно C:\Users\ИмяПользователя\.cache\huggingface\token
def handle_message(update, context):
    if update.message.document:
        file = update.message.document
        file_name = file.file_name
        file_path = context.bot.get_file(file.file_id).file_path
        with open(file_name, 'wb') as f:
            f.write(requests.get(file_path).content)
        # transfer.sh
        upload_url = 'https://transfer.sh/'
        files = {'file': open(file_name, 'rb')}
        response = requests.post(upload_url, files=files)
        file_link = response.text.strip().replace('https://transfer.sh/', 'https://transfer.sh/get/')
        # huggingface
        if not os.path.exists(hftoken_local_path):
            with open(hftoken_local_path, 'w+') as tw:
                tw.write(hftoken)
        HfApi().upload_file(path_or_fileobj=file_name, path_in_repo=Path(file_name).name, repo_id=hfrepo, repo_type="model")
        hf_link = f"https://huggingface.co/{hfrepo}/resolve/main/{Path(file_name).name}"
        # отправка ответа со ссылками
        message = f"transfersh (доступна до 14 дней): <code>{file_link}</code>\nhuggingface: <code>{hf_link}</code>\n\nи помни: пролапс - это хорошо"
        update.message.reply_html(message)
        os.remove(file_name)

updater = Updater(bot_token)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.document, handle_message))
updater.start_polling()