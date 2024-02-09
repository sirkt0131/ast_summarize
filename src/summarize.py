from src.load import Loader
from src.utils import clean_text, split_text
from src.create_prompt import CreatePrompt
from src.cost import Cost

def summarize(url, max_word, chat_model, model_info):
    # return "Result", "Title", col, row, url, Cost(1, 2, 3, 4)
    text = Loader.load_url(url)
    text = clean_text(text)
    text_list = split_text(text, max_word)

    input_message_token_num = chat_model.get_message_token_num(text)
    input_cost = input_message_token_num * model_info["input_price"] / 1000

    message = ""
    if len(text_list) == 1:
        message = text_list[0]
    elif len(text_list) > 1:
        for text in text_list:
            result_tmp = chat_model.get_chat_message(
                CreatePrompt.create_part_summary_prompt(text))
            message += result_tmp.choices[0].message.content
    result = chat_model.get_chat_message(
        # CreatePrompt.create_summary_prompt(message, 'Japanese'))
        CreatePrompt.create_prompt(message, 'Japanese'))
    result = result.choices[0].message.content

    output_message_token_num = chat_model.get_message_token_num(result)
    output_cost = output_message_token_num * model_info["output_price"]/1000

    return result, Cost(input_message_token_num, input_cost, output_message_token_num, output_cost)


