from ..utills import MODEL_LIST, get_config, menu, set_config_value, into

def config():
    while True:
        global_config = get_config()

        options = menu("Select an edit point", [f"AI PROVIDER ({global_config['AI_PROVIDER']})", f"API KEY ({''.join(['*' for _ in range(len(global_config['API_KEY']))])})", f"API URL [Proxy path to OpenAI api. Only openai provider]  ({global_config['API_URL']})", f"AI MODEL ({global_config['MODEL']})", f"TOKENS MAX INPUT ({global_config['TOKENS_MAX_INPUT']})", f"TOKENS MAX OUTPUT ({global_config['MAX_TOKENS_OUTPUT']})", f"USE EMOJI ({global_config['EMOJI']})", f"ONE LINE COMMIT ({global_config['ONE_LINE_COMMIT']})", f"DESCRIPTION COMMIT ({global_config['DESCRIPTION']})", f"Language ({global_config['LANGUAGE']})", "EXIT"])

        if options.startswith('AI PROVIDER'):
            provider = menu("Select provider", options=list(MODEL_LIST.keys()))
            set_config_value("AI_PROVIDER", provider)
            set_config_value("MODEL", MODEL_LIST[provider][0])
        elif options.startswith("API KEY"):
            set_config_value("API_KEY", into("Please write api key"))
        elif options.startswith("API URL"):
            set_config_value("API_URL", into("Please write api url"))
        elif options.startswith('AI MODEL'):
            set_config_value("MODEL", menu(title="Select model", options=MODEL_LIST[global_config['AI_PROVIDER']]))
        elif options.startswith('TOKENS MAX INPUT'):
            set_config_value("TOKENS_MAX_INPUT", into("Please write max tokens input"))
        elif options.startswith('TOKENS MAX OUTPUT'):
            set_config_value("MAX_TOKENS_OUTPUT", into("Please write max tokens output"))
        elif options.startswith('USE EMOJI'):
            set_config_value("EMOJI", not global_config['EMOJI'])
        elif options.startswith('ONE LINE COMMIT'):
            set_config_value("ONE_LINE_COMMIT", not global_config['ONE_LINE_COMMIT'])
        elif options.startswith('DESCRIPTION COMMIT'):
            set_config_value("DESCRIPTION", not global_config['DESCRIPTION'])
        elif options == 'EXIT':
            break
