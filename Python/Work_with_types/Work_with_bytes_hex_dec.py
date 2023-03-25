
def pow_m(a,power,mod = 2^32):                          # (a**b)%m
    result = 1
    bit = a % mod

    while (power > 0):
        if (power&1 == 1):
            result *= bit
            result %= mod
        bit *= bit
        bit %= mod
        power >>= 1
    # print(result)
    return result

def chunkstring(string, length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))

def hex_string_to_bytes_in_10cc(string):                # переводим строку их 16сс в список 10-чных значений для последующих операций
    if len(string) % 2:
        string = '0' + string
    string = chunkstring(string, 2)
    string = [int(d,16) for d in string]
    return string

def prepare_data_to_send(data):                         # readable string to utf-8 hex
    data = data.encode("utf-8")
    data = data.hex()
    return data

def hex_to_str(hex_str):                                # из 16 сс в читаемый формат   
    data = ''
    for i in range (0,len(hex_str),2):
       data+=chr(int(hex_str[i:i+2],16))
    return data

data = "Hi! I will prepeare you to future, so relax."

if __name__ == "main":

    data_in_hex = prepare_data_to_send(data)

    print("Data in hex:\n" + data_in_hex)

    restore_data = hex_to_str(data_in_hex)

    print("Data in readable view:\n" + restore_data)

    bytee = hex_string_to_bytes_in_10cc(data_in_hex)
    print("Bytes as dec string:\n"+str(bytee))