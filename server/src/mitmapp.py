from mitmproxy import http, ctx
import chat as gpt
import requests
import os
import time
chat_gpt_response ="hi how are you??"

response_file_path = "response_file.txt"
mitm_log_file_path = "mitm_log.txt"
malicious=False
i=0


def initialize_files():
 if not os.path.exists(response_file_path):
        open(response_file_path, 'w').close()
 if not os.path.exists(mitm_log_file_path):
     open(mitm_log_file_path, 'w').close()


def request(flow: http.HTTPFlow) -> None:
    # Access the request object
    request = flow.request
    client_header_string=""
    d=dict()
    refere=""
    
   

 # Get all headers from the request
    all_headers_client = request.headers
    
    # Print the headers
    for header, value in all_headers_client.items():
        d[header]=value
        client_header_string+=f"{header}: {value} \n"
   
    if 'referer' in d:
        refere = str(d['referer'])
        print("refere---------",refere)
    if "ginandjuice" in refere:
        print(client_header_string)
        #response_g = send_to_gpt(client_header_string)
        send_to_gpt(client_header_string)
        if(True):
            print("hi")
            
    d.clear()




def response(flow: http.HTTPFlow) -> None:
    # Check if the desired header is present in the response
    # if chat_gpt_response ==True
    
    
        
        
        # Modify the Location header for redirection
        global i
        i=i+1
        print("i value :--------------------------------------------- : :",i)
        if(malicious):      #or i>10  ######blocking it if more than 10 request at a time
            ctx.log.info("Found the desired header in the response.")
        
            # Stop mitmproxy
            ctx.log.info("Redirecting...")
            
            flow.response.headers["Location"] = "http://example.com"
            flow.response.status_code = 302  # Set the status code for redirection

            # Clear the response content
            flow.response.content = b''


def send_to_gpt(client_string):
    print("--------------------------------------------------ANALYZING RESULT FROM CHAT GPT APIS----------------------------------------------------")
    print("_________________________________ALMOST DONE ____________________________________________________________________________________________")
    prompt = "hi chat gpt i am giving you python intercept request which contains header, if the header or content is suscipious only give answer: this is suspcicous ortherwise give its ok to go ahead" + client_string
    chat_gpt_response = gpt.generate_response(prompt)

    if chat_gpt_response:
        print("ChatGPT Response:")
        print(chat_gpt_response)
    #if "to go ahead" in chat_gpt_response:
         #return True
    else:
        print("YOU HAVE BEEN BLOCKED _---------------------------------------------------------------")
    with open(response_file_path, "a") as response_file:
        response_file.write(chat_gpt_response)

    # Append the mitmproxy logs to the file
    with open(mitm_log_file_path, "a") as mitm_log_file:
        mitm_log_file.write(f"Request:\n{client_string}\n\nResponse:\n{chat_gpt_response}\n\n")





  







    
