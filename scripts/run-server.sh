#!/usr/bin/env bash
echo "source bashrc"
source ~/.bashrc
echo "cd nlp-project"
cd /nfs/hpc/share/lallya/nlp-project || exit 123
echo "activate env"
conda activate visdial-diversity

echo "opening tunnel"
ngrok http 8652 --log=stdout &

echo "running server"
FLASK_APP=web_demo/serve.py flask run -p 8652 &

echo "wait"
wait
