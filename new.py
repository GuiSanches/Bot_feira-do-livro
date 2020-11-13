import tabula
#the pd is the standard shorthand for pandas
import pandas as pd
import os



#declare the path of your file
# file_path = "./catalogo/Alameda.pdf"#Convert your file
# df = tabula.read_pdf(file_path, pages='all')

errors = []
for pdf in os.listdir('catalogo'):
    try:
        file_path = './catalogo/' + pdf
        df = tabula.read_pdf(file_path, pages='all')
    except:
        errors.append(pdf)

print(len(errors), errors)
        

# for publisher in dados:
#         publisher_filename = publisher[1] + '.pdf'
#         file_url = publisher[2]

#         file_id = re.search('[-\w]{33,}', file_url).group()
        
#         print(file_id, '\n', file_url)
#         download_file_from_google_drive(file_id, 'catalogo/' + clean_filename(publisher_filename))
#         # gdown.download(file_url, clean_filename(publisher_filename), quiet=False)
#         saved.append(publisher)
#         # break
# print(df)