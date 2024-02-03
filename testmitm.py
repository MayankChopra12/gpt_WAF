from mitmproxy import http, ctx

def response(flow: http.HTTPFlow) -> None:
    # Check if the desired header is present in the response
    if True:
        ctx.log.info("Found the desired header in the response.")
        
        # Stop mitmproxy
        ctx.log.info("Redirecting...")
        
        # Modify the Location header for redirection
        flow.response.headers["Location"] = "http://example.com"
        flow.response.status_code = 302  # Set the status code for redirection

        # Clear the response content
        flow.response.content = b''



if __name__ == "__main__":
    from mitmproxy.tools.main import mitmdump
    mitmdump(['-s', __file__])
