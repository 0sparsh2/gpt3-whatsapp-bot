import logging
import openai

# To deplay on Azure
import azure.functions as func

#sample request
# {"model":"text-davinci-003", "prompt":"Test Prompt",  "temperature":0.6, "max_tokebs":200}

secret_key = "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"


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # give OpenAI secret key to authenticate
    openai.api_key = secret_key

    # get variables from the HTTP request body
    req_body = req.get_json()

    # call the OpenAI API
    output = openai.Completion.create(
        model= req_body['model'], #"text-davinci-003",
        prompt= req_body['prompt'],
        temperature= req_body['temperature'], #0.6,
        max_tokens = req_body['max_tokens'] #200
        )

    # format the response
    output_text = output['choices'][0]['text']
    # provide the response

    return func.HttpResponse(output_text,status_code = 200)
