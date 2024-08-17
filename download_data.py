import gdown

def download_data(file_id):
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    output = 'data.csv'
    gdown.download(download_url, output, quiet=False)

download_data('1ZdsrtNY3H7Oh_ojb3vootMMyV84Kw002')


