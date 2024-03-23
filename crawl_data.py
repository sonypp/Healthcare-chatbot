import requests
from bs4 import BeautifulSoup
from mpi4py import MPI
from googletrans import Translator
from fpdf import FPDF


# Get the number of processes
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

link_extensions = []

if rank == 0:

    # Connect to the website
    resp = requests.get("https://www.vinmec.com/vi/benh/")
    soup = BeautifulSoup(resp.text, 'html.parser')


    # Get the link extentions and divide them into processes
    uls = soup.find_all('ul', class_='collapsible-target')
    lis = [li for ul in uls for li in ul.find_all('li')]
    link_extensions = [li.find('a')['href'] for li in lis if li.find('a') is not None]
    print("Number of links: ", len(link_extensions))
    link_extensions = [link_extensions[i::size] for i in range(size)]
link_extensions = comm.scatter(link_extensions, root=0)


# Initialize the translator
translator = Translator()


# Get and process the content of per link
for link in link_extensions:
    try:
        # Get the filename to save the pdf
        filename = link.split('/')[-2]
        
        print("Core: ", rank, " - Processing: ", filename)
        
        # Create the pdf file
        pdf = FPDF()
        pdf.add_font('DejaVu', '', "./fonts/DejaVuSansCondensed.ttf", uni=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.add_page()
        
        # Connect to the website
        link = "https://www.vinmec.com" + link
        resp = requests.get(link)
        while resp.status_code != 200:
            resp = requests.get(link)
        soup = BeautifulSoup(resp.text, 'html.parser')
        content = soup.find('div', class_='content')

        # Write the content to the pdf file
        for element in content.find_all('p'):
            text = element.get_text()
            if 'Xem thêm' in text:
                break
            pdf.write(8, translator.translate(text, src='vi', dest='en').text)
            pdf.ln()
            
        # Save the pdf file
        pdf.output('./data/' + filename + '.pdf','F')
    except Exception as e:
        continue