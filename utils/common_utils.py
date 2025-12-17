def get_status_message(code): 
    return {200:"Success",
            400:"Bad req",
            401:"Unauthorized",
            404:"Not found"}.get(code,"Unknown")
    
def mask_token(headers: dict, visible=15):
    masked = {}
    for k, v in headers.items():
        if k.lower() == "authorization" and isinstance(v, str):
            token = v.split(" ", 1)[-1]
            if len(token) > visible * 2:
                masked[k] = f"Bearer {token[:visible]}...{token[-visible:]}"
            else:
                masked[k] = v
        else:
            masked[k] = v

    return masked