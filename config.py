import os.path

TOKEN = os.getenv('APIKEY')

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
voice_message_dir = current_dir + 'voicemessage/'