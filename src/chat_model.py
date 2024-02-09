import os
import openai
import tiktoken
import time
# from retry import retry 

class ChatModel():
    def __init__(self, model_name):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model_name = model_name
    
    def get_chat_message(self, message):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": message},
                ],
                # max_tokens=100,
                # request_timeout=60, # sec
            )
            return response
        except openai.error.RateLimitError:
            # Rate Limitに達した場合は適切な待機時間を設定
            print(' Retry... ',end='',flush=True)
            time.sleep(60)  # 例: 60秒待機
            return self.get_chat_message(message)  # 再試行
        except openai.error.OpenAIError as e:
            # その他のOpenAI APIエラーの処理
            print(f" OpenAI API error: {e}")
            return ""
        
    def get_message_token_num(self, message):
        encoding = tiktoken.encoding_for_model(self.model_name)
        tokens = encoding.encode(message)
        tokens_count = len(tokens)
        return tokens_count
