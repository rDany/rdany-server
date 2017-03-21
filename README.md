# rdany-server
Server backend for rDany

## Running rDany locally
Joing rDany Telegram group: https://t.me/joinchat/AAAAAD_mgtrLzFNPDtdbIg

    mkdir rdany
    cd rdany
    git clone https://github.com/llSourcell/tensorflow_chatbot.git
    virtualenv -p python2 venv
    . venv/bin/activate
    pip install numpy scipy six tensorflow==0.12

Edit the file seq2seq.ini changing:

    mode = test
    enc_vocab_size = 40000
    dec_vocab_size = 40000
    num_layers = 4
    layer_size = 256
    batch_size = 16

Ask for the last model on the Telegram Group
Unzip the model file on the folder working_dir

Finally run:

    python execute.py

Will take a moment to load and when a symbol `>` appear you can write. When writting each message you will need to preppend `_enc_rdany`  for instance `_enc_rdany hello`
