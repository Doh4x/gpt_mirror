import g4f

ai_models = {
            # GPT-3.5 4K Context
            "gpt_35_turbo" : g4f.models.gpt_35_turbo,
            "gpt_35_turbo_0613" : g4f.models.gpt_35_turbo_0613,

            # GPT-3.5 16K Context
            "gpt_35_turbo_16k" : g4f.models.gpt_35_turbo_16k,
            "gpt_35_turbo_16k_0613" : g4f.models.gpt_35_turbo_16k_0613,

            # Llama
            "llama3_70b" : g4f.models.llama3_70b_instruct,
            "llama2_70b" : g4f.models.llama2_70b,
            
            # Mixtral
            "mixtral-8x22b" : g4f.models.mixtral_8x22b,
            
            # GigaChat
            "gigachat" : g4f.models.gigachat,
            "gigachat_plus": g4f.models.gigachat_plus,
            "gigachat_pro" : g4f.models.gigachat_pro,

            # GPT-4 8K Context
            # g4f.models.gpt_4,
            # g4f.models.gpt_4_0613,

            # GPT-4 32K Context
            # g4f.models.gpt_4_32k,
            # g4f.models.gpt_4_32k_0613,
}
        
gpt35_error_messages = [
    "\u6d41\u91cf\u5f02\u5e38,\u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883",
    "\u5f53\u524d\u5730\u533a\u5f53\u65e5\u989d\u5ea6\u5df2\u6d88\u8017\u5b8c, \u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883"
]