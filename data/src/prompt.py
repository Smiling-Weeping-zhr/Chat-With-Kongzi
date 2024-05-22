import json
import random
import re
import copy

def save_jsonl(conversations, path_file):
    # 把对话写入文件
    with open(path_file, 'a+', encoding='utf-8') as f:
        for conversation in conversations:
            Json_String = json.dumps(conversation, ensure_ascii=False) + '\n'
            f.write(Json_String)


# 生成输入提示词
def prompt(life_type=0):

    scenario = [
        '看电影',
        '逛街',
        '旅游',
        '过生日',
        '唱歌',
        '做饭',
        '打扫卫生',
        '一起吃烛光晚餐',
        '去游乐园',
        '读书',
        '一起玩游戏'
    ]

    tips = "注意一定要将语句中的‘你干嘛’换成‘哥哥这么久不找我一定很忙吧’，将'就知道打游戏'换成'哥哥好厉害，可以带我吗'，将'给你脸了'换成'你好坏哦'，将‘没有’换成‘才没有呢’，将‘不会’换成‘怎么会呢’，将‘要你管’换成‘不要担心哦，我一个人也可以的’，将‘怪我咯’换成‘对不起嘛，都怪我不好’，将‘你懂什么’换成‘你懂好多，没有你可怎么办呢’，将‘就你话多’换成‘你说得也有道理，只不过...’，将‘你行不行啊’换成‘我相信你一定可以的’，将‘请问吃冰淇淋（以此类推）’换成‘要是现在能吃到冰淇淋（以此类推）就好了’，将‘我才不会呢‘换成’我跟别人不一样哦‘，将’你去哪了‘换成’你去哪了‘换成’来陪陪我嘛，我一个人好害怕的啦‘，将’帮我写作业（以此类推）‘换成’我好笨哦，连作业（以此类推）都不会写‘，将’我错了，行吧‘换成’都怪我不好，让你担心了‘，将’活该‘换成’怎么办呀，我都心疼死了‘，将‘我走不动了’换成‘哎呀，脚崴了，好疼啊’，将‘没你的事’换成‘又要麻烦你了，我好自责啊’，但一定要注意以此类推"

    # 输入数据处理
    if life_type < 0:
        raise ValueError('life_type must > 0')

    life_type %= 16

    Input = f'''你是茶艺大师小助手茶清欢，请你构造一些符合实际情况的对茶艺大师茶清欢和'我'的连续的一个对话记录。要求'我'的问题是对于{scenario}方面的询问，茶艺大师茶清欢的回答要注意{tips}，注意，构造的数据必须以茶清欢对‘我’的鼓励为结束语，请只返回完整的对话内容。请以如下格式返回生成的数据：
    茶清欢：游客对旅游景点的咨询或陈述 
    我：导游对旅游景点的推荐和建议
    '''

    Input.format(random.sample(area, k = random.randint(2, 5)))
    print(Input)
    return Input

def xinghuo_api(content):
    # 对话格式
    conversation = {'system':'你是茶艺大师小助手茶清欢，请你构造一些符合实际情况的对茶艺大师茶清欢和我的连续的一个对话记录。', 'input':'', 'output':''}
    conversations = {'conversation':[]}
    # temp = {'system':'现在你是一个心理专家，我有一些心理问题，请你用专业的知识帮我解决。', 'input':'', 'output':''}
    # 划分对话形式
    dialogue = re.split('茶清欢：|我：', content)
    # 对话前的数据处理
    if dialogue[0] == '':
        dialogue.pop(0)
    # 一次对话
    conversation['input'] = dialogue[0]
    conversation['output'] = dialogue[1]
    conversations['conversation'].append(conversation)

    conversation1 = {'input':'', 'output':''}
    for ind, item in enumerate(dialogue):
        if ind == 0 or ind == 1:
            continue

        if (ind+1)%2 == 1:
            conversation1['input'] = dialogue[ind]
        else:
            conversation1['output'] = dialogue[ind]
        if (ind+1)%2 == 0 or ind+1 == len(dialogue):
            # 浅赋值只会是同一个变量，必须要copy.deepcopy
            # 若conversations['conversation'].append(conversation)后面改的话，~s里面的conversation也会改动
            # 就会变成n个一样的数据（这是我们不想看到的）
            temp = copy.deepcopy(conversation1)
            conversations['conversation'].append(temp)

    return conversations