# 对话孔子（Chat-With-Kongzi）
## 1.项目简介
我们项目使用InternLM-chat-7b模型使用自定义数据集进行微调，从而达到与先贤孔子对话的目的。在对话过程中你可以充分体会到孔子的智慧，并且孔子会将有有关《论语》《春秋》等古典文献给你讲解，并且给你进行答疑解惑，让你念头通达，体会到君子之境。

## 2.数据集来源
链接现有大模型如千问、星火、智谱等的API利用prompt工程进行多轮对话数据集收集，并且对于格式不符合Json形式或者质量较差部分就行剔除，然后保留大概4000条左右数据进行多轮训练（大模型几乎所有的知识都来自于预训练，并且只需要有限的指令微调数据就可以使大模型产生高质量的输出）引用论文《LIMA: Less Is More for Alignment》 


## 3.微调使用技术
我们的对话孔子大模型是一个利用PyTorch、XTuner、Deepspeed、Transformers和Streamlit技术的对话AI系统。它通过深度学习模型来理解和回应用户的问题需求，，并通过Streamlit部署为用户友好的Web应用，实现随时随地的辅导对话解答服务。
详细内容请见[文档](https://github.com/Smiling-Weeping-zhr/Chat-With-Kongzi)
