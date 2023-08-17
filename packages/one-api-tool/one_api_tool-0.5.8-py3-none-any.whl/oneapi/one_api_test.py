# -*- coding: utf-8 -*-
import json
from typing import Optional, Sequence, List
import openai
import anthropic
from pydantic import BaseModel
from abc import ABC, abstractmethod
import sys
import os
from typing import Callable, Optional, Sequence, List
import tiktoken
import asyncio
import transformers
import logging
from openai.openai_object import OpenAIObject
sys.path.append(os.path.normpath(f"{os.path.dirname(os.path.abspath(__file__))}/.."))
from oneapi.one_api import batch_chat, OneAPITool

def print_special_token(tokenizer_hf: transformers.PreTrainedTokenizer):
    print(f"""tokenizer:\n 
          vocab_size:{len(tokenizer_hf)},
          eos:{tokenizer_hf.eos_token},{tokenizer_hf.eos_token_id},
          bos:{tokenizer_hf.bos_token},{tokenizer_hf.bos_token_id},
          pad:{tokenizer_hf.pad_token},{tokenizer_hf.pad_token_id},
          unk:{tokenizer_hf.unk_token},{tokenizer_hf.unk_token_id},
          mask:{tokenizer_hf.mask_token},{tokenizer_hf.mask_token_id},
          cls:{tokenizer_hf.cls_token},{tokenizer_hf.cls_token_id},
          sep:{tokenizer_hf.sep_token},{tokenizer_hf.sep_token_id},
          all_special:{tokenizer_hf.all_special_tokens},{tokenizer_hf.all_special_ids},
          """)



if __name__ == "__main__":
    claude_config = '../ant/config/anthropic_config_personal.json'
    openai_config = '../ant/config/openapi_official_chenghao.json'
    azure_config = '../ant/config/openapi_azure_config_xiaoduo_dev.json'
    config_file = openai_config
    tool = OneAPITool.from_config_file(config_file)
    # a = tool._preprocess_claude_prompt(['今天天气不错？','抱歉，我不知道你在说什么', '高血压吃什么药'])
    # print(f'++++{a}+++')
    # exit()

    prompt = '今天天气不错？'
    prompt = 'how is the weather today?'
    # print(tool.coust_tokens([prompt]))
    res = asyncio.run(tool.asimple_chat(prompt, stream=True))
    print(res)
    # res = asyncio.run(batch_chat([claude_config, openai_config, azure_config], ['心率异常可以局部麻醉吗', '今天天气不错？', '你好？', '上午是几点', '热天吃什么', '胖子爱出汗', '窦性心率是什么'], stream=False))
    # print(res)