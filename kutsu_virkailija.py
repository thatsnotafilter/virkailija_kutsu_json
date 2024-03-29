import requests, json

def get_primus_json_file(file, encode): #yksirivinen json-sanoma
    jsons = []
    with open(file, 'r', encoding = encode) as f:
        for line in f:
            jsons.append(line)
    return jsons

target_url = 'https://virkailija.untuvaopintopolku.fi'
custom_headers = {'content-type': 'application/json'}

login_params = {
    'username': '',
    'password': '',
    }

r = requests.post(target_url + '/cas/v1/tickets', login_params)

if r.status_code == 201: #201 Created (Ticket Granting Ticket)
    service_params = {'service': target_url + '/kayttooikeus-service/j_spring_cas_security_check'}
    ticket_location = r.headers['Location']
    r = requests.post(ticket_location, service_params)

    if r.status_code == 200: #200 OK (service ticket)
        custom_headers['CasSecurityTicket'] = r.text
        jsons_file = get_primus_json_file('C:\\polku_tiedostoon\\tiedosto.json', 'utf-8-sig') #Microsoft UTF-8 variant

        for entry in jsons_file:
            print(entry['sahkoposti'])
            r = requests.post(target_url + '/kayttooikeus-service/kutsu', entry.encode('utf-8'), headers = custom_headers)
            if r.status_code == 201:
                print('kutsu lähetetty')
            else:
                print('kutsun lähetyksestä saatiin viesti: {0}'.format(r.json()))

            r = requests.post(ticket_location, service_params)
            custom_headers['CasSecurityTicket'] = r.text
