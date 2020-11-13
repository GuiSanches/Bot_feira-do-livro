import requests
import json
import gdown
import unicodedata
import string
import re

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]  

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def download_files(dados):
    saved = []
    for publisher in dados:
        publisher_filename = publisher[1] + '.pdf'
        file_url = publisher[2]

        file_id = re.search('[-\w]{33,}', file_url).group()
        
        print(file_id, '\n', file_url)
        download_file_from_google_drive(file_id, 'catalogo/' + clean_filename(publisher_filename))
        # gdown.download(file_url, clean_filename(publisher_filename), quiet=False)
        saved.append(publisher)
        # break


if __name__ == "__main__":
    # 'https://drive.google.com/uc?export=download&id=1DS7Vj5a4vUPD2T-Qi34OaCnpEr2EKsOr'
    file_id = '1DS7Vj5a4vUPD2T-Qi34OaCnpEr2EKsOr'
    destination = 'file2.pdf'

    dados = {}
    with open('save.json', 'r') as json_file:
        dados = json.load(json_file)

    download_files(dados)
    print(clean_filename('oi.pdf'))
# download_file_from_google_drive(file_id, destination)
