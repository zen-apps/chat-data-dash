# Chat with you data with Python Dash & OpenAI 

## About

This is a very simple python Dash application allowing you to upload a XLSX/CSV file, and easily chat with the data in natural language. 

This is all made possbile as the code is connected to [OpenAI](https://openai.com/) ChatGPT LLM using [Langchain](https://python.langchain.com/docs/get_started/introduction.html).  

It's a 2 step process:

1. Data Upload: First, users upload their data. The app samples this data, sending it to ChatGPT LLM to obtain data definitions. Using these definitions, a simple database is set up within the app.

2. Questioning the Data: Users can then pose questions related to their data. This question (or prompt) is communicated to the ChatGPT LLM. In response, ChatGPT returns the appropriate SQL code, which is then executed on the database created in the first step. It's important to note that ChatGPT doesn't directly query the data - its primary function is to generate the most suitable SQL query based on the user's prompt.

![Prompt Diagram](data_chat_diagram.png?raw=true)

### To Build and Run from Linux 
- in Linux command line, ensure [Docker](https://docs.docker.com/engine/install/ubuntu/) is installed
- in the env file ```/dash_app/config/dev.env```, enter you OpenAI key (no spaces or quotes)
- run ```Make up``` (or you could just run the docker command from the Makefile ```up``` manually on the linux command line, you'll just need to hardcode the variables along the top of Makefile)
- go to the port specified on the ```APP_PORT``` variable on top of ```Makefile```

### Deployment to GCP Cloud Run

If you want to run outside of your Linux machine, here are instructions to deploy as web app in GCP (Google Cloud Platform -- and you will need any account)

- in Linux command line, install [gcloud](https://cloud.google.com/sdk/docs/install#linux)
- ```gcloud builds submit --tag gcr.io/<project-id>/<cloud run service name>```
- ```gcloud run deploy --image gcr.io/<project-id>/<cloud run service name>  --platform managed```
- the link to your new GCP hosted app will be provided in the terminal