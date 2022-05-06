
private_client_key = 0
public_client_key = 0
public_server_key = 0
secret_key = 0
pad_char = ''

def set_conn(sprivate_client_key,spublic_client_key,spublic_server_key,ssecret_key,spad_char):
    global private_client_key,public_client_key,public_server_key,secret_key,pad_char
    private_client_key = sprivate_client_key
    public_client_key = spublic_client_key
    public_server_key = spublic_server_key
    secret_key = ssecret_key
    pad_char = spad_char