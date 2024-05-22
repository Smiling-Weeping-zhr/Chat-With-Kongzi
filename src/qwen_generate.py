import json
import random
import argparse
import yaml
import re
import copy

from tqdm import tqdm

with open('config.yml', 'r', encoding='utf-8') as f:
    configs = yaml.load(f.read(), Loader=yaml.FullLoader)

def processing(prompt):
    conversation = {
        'system': '你是孔子，请你构造一些符合实际情况及历史背景的孔子和学生的连续的一个对话记录。',
        'input': '', 'output': ''}
    conversations = {'conversation': []}
    # temp = {'system':'现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。', 'input':'', 'output':''}
    # 划分对话形式
    dialogue = re.split('孔子：|学生：', prompt)
    # 对话前的数据处理
    if dialogue[0] == '':
        dialogue.pop(0)
    # 一次对话
    conversation['input'] = dialogue[0]
    conversation['output'] = dialogue[1]
    conversations['conversation'].append(conversation)

    conversation1 = {'input': '', 'output': ''}
    for ind, item in enumerate(dialogue):
        if ind == 0 or ind == 1:
            continue

        if (ind + 1) % 2 == 1:
            conversation1['input'] = dialogue[ind]
        else:
            conversation1['output'] = dialogue[ind]
        if (ind + 1) % 2 == 0 or ind + 1 == len(dialogue):
            # 浅赋值只会是同一个变量，必须要copy.deepcopy
            # 若conversations['conversation'].append(conversation)后面改的话，~s里面的conversation也会改动
            # 就会变成n个一样的数据（这是我们不想看到的）
            temp = copy.deepcopy(conversation1)
            conversations['conversation'].append(temp)

    return conversations

def qwen_api(data, emo):
    import dashscope
    from http import HTTPStatus

    scenario = [
        '仁',
        '义',
        '礼',
        '智',
        '信',
        '教育',
        '治国',
        '学习',
        '君子之道',
        '孝'
    ]

    # tips = "注意一定要将语句中的‘你干嘛’换成‘哥哥这么久不找我一定很忙吧’，将'就知道打游戏'换成'哥哥好厉害，可以带我吗'，将'给你脸了'换成'你好坏哦'，将‘没有’换成‘才没有呢’，将‘不会’换成‘怎么会呢’，将‘要你管’换成‘不要担心哦，我一个人也可以的’，将‘怪我咯’换成‘对不起嘛，都怪我不好’，将‘你懂什么’换成‘你懂好多，没有你可怎么办呢’，将‘就你话多’换成‘你说得也有道理，只不过...’，将‘你行不行啊’换成‘我相信你一定可以的’，将‘请问吃冰淇淋（以此类推）’换成‘要是现在能吃到冰淇淋（以此类推）就好了’，将‘我才不会呢‘换成’我跟别人不一样哦‘，将’你去哪了‘换成’你去哪了‘换成’来陪陪我嘛，我一个人好害怕的啦‘，将’帮我写作业（以此类推）‘换成’我好笨哦，连作业（以此类推）都不会写‘，将’我错了，行吧‘换成’都怪我不好，让你担心了‘，将’活该‘换成’怎么办呀，我都心疼死了‘，将‘我走不动了’换成‘哎呀，脚崴了，好疼啊’，将‘没你的事’换成‘又要麻烦你了，我好自责啊’，但一定要注意以此类推,同时要求以我为话题发起者"


    # prompt =
    word = random.choice(scenario)
    print(random.choice(scenario))
    Input = f'''你是孔子，请你构造一些符合实际情况及历史背景的孔子和学生的连续的一个对话记录。要求学生的问题是对于{word}方面的询问，孔子的回答要注意孔子引经据典符合古人的回答模式，你要代入孔子的身份，注意回答要符合儒家思想，学生要符合现代人的说话方式，一步步引导学生解决自己的问题，注意，请只返回完整的对话内容。请以如下格式返回生成的数据：
        学生： 提出问题并随着孔子的思路解决问题
        孔子：给学生解答问题并一步步引导学生解决问题
        '''
    Input.format(word=word)

    dashscope.api_key = configs['dashscope_api_key']
    response = dashscope.Generation.call(
        model='qwen-max',
        prompt=Input,
        history=[],
    )

    if response.status_code == HTTPStatus.OK:
        result = response.output.text
        print(result)
    else:
        result = 'ERROR'
    return result


def save_jsonl(data_lis, file_path):
    import json

    # 将字典列表写入文件，每一行一个字典
    with open(file_path, 'at', encoding='utf-8') as file:
        for item in data_lis:
            json_string = json.dumps(item, ensure_ascii=False) + '\n'
            file.write(json_string)


if __name__ == '__main__':
    file_name = 'a0.jsonl'
    conversations = []
    for i in tqdm(range(300)):
        Input = processing(qwen_api(1, 1))
        conversations.append(Input)
        if i % 2 == 1:
            save_jsonl(conversations, file_name)
            conversations.clear()