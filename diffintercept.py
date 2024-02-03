from mitmproxy import http, ctx
import chat as gpt
import requests

from flask import flask,render_template
import os


app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

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
        send_to_gpt(client_header_string)
    d.clear()
        


def send_to_gpt(client_string):
    print("--------------------------------------------------ANALYZING RESULT FROM CHAT GPT APIS----------------------------------------------------")
    print("_________________________________ALMOST DONE ____________________________________________________________________________________________")
    prompt = "hi chat gpt i am giving you python intercept request which contains header, if the header or content is suscipious only give answer: this is suspcicous ortherwise give its ok to go ahead" + client_string
    response = gpt.generate_response(prompt)

    if response:
        print("ChatGPT Response:")
        print(response)
    if "to go ahead" in response:
         perform_redirect()
    else:
        print("YOU HAVE BEEN BLOCKED _---------------------------------------------------------------")
  
       

def perform_redirect():
    # Specify the target URL for redirection
    target_url = 'https://example.com'  # Replace with the desired website URL
    return redirect_to_website(target_url)


# Run mitmproxy with the custom script
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT',8080)))
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__, '--quiet'])




