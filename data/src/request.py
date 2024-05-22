import requests

headers2 = {'Content-Type': 'application/json'}
# data = {
#   "model": "internlm2-chat-7b",
#   "messages": "我很焦虑怎么办？",
#   "temperature": 0.7,
#   "top_p": 1,
#   "n": 1,
#   "max_tokens": 512,
#   "stop": False,
#   "stream": False,
#   "presence_penalty": 0,
#   "frequency_penalty": 0,
#   "user": "string",
#   "repetition_penalty": 1,
#   "renew_session": False,
#   "ignore_eos": False
# }

data = {
  "model": "internlm2-chat-7b",
  "messages": [
    {
      "content": "我很焦虑怎么办？",
      "role": "user"
    }
  ],
  "temperature": 0.7,
  "top_p": 1,
  "n": 1,
  "max_tokens": 512,
  "stop": None,
  "stream": False,
  "presence_penalty": 0,
  "frequency_penalty": 0,
  "user": "string",
  "repetition_penalty": 1,
  "session_id": -1,
  "ignore_eos": False,
  "skip_special_tokens": True,
  "top_k": 40
}

x = requests.post('http://127.0.0.1:23333/v1/chat/completions', headers=headers2, json=data,
                  verify=False)

r = x.json()
print(x.text)
print(r["choices"][0]["message"]["content"])
