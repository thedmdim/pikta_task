import requests, json

class IFNS:
    def __init__(self, ifns_code: int, oktmo: int):
        self.ifns_code = ifns_code
        self.oktmo = oktmo

    @property
    def info(self) -> dict:
        payload = {'c': 'next',
                   'step': '1',
                   'npKind': 'fl',
                   'ifns': str(self.ifns_code),
                   'oktmmf': str(self.oktmo),
                   }
        try:
            response = requests.post("https://service.nalog.ru/addrno-proc.json", data=payload)
        except ConnectionError:
            return "Connection error"

        if response.status_code != 200:
            return response.status_code
        else:
            return json.loads(response.text)

a = IFNS(7840, 40913000)
print(a.info)
