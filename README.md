# End-to-end-Medical-Chatbot-using-Llama2

# How to run?

## Prerequirements

- libopenmpi-dev

```bash
sudo apt-get install libopenmpi-dev
```

- python-venv

```bash
sudo apt install python3-venv -y
```

### STEPS:

Clone the repository

```bash
Project repo: https://github.com/sonypp/Healthcare-chatbot.git
```

### STEP 01- Create a venv environment after opening the repository

```bash
venv -m venv .venv
```

```bash
source ./.venv/bin.activate
```

### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your Pinecone credentials as follows:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
PINECONE_API_ENV = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


### Download the quantize model from the link provided in model folder & keep the model in the model directory:

```ini
## Download the Llama 2 Model:

llama-2-7b-chat.ggmlv3.q4_0.bin


## From the following link:
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
```

```bash
# If you want to run with small data:
python store_index.py

# If you want to run with larger data (spend more time):
mpirun -n <number_of_max_cpu_cores> python crawl_data.py
python store_index.py
```

```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up localhost:8080
```


### Techstack Used:

- Python
- LangChain
- Flask
- Meta Llama2
- Pinecone
- MPI4PY
- BeautifulSoup
- Requests
- GooglleTrans


# Healthcare-chatbot
