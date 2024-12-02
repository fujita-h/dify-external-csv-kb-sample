# dify-external-csv-kb-sample

Dify's knowledge base has the ability to extract data using vector search or full-text search. They provide a feature called RAG. These features are similar to search engines. It is important to note that this feature does not retrieve specific data from a database.

Dify cannot reliably retrieve the required data from a database specified using a key or keyword. In such cases, you need to create a separate knowledge system and connect it to Dify. This repository provides an example for this purpose.

## Quick Start

### Create a sample csv file by using 
```bash
python tools/create-sample-csv.py
```

### Run server
```bash
python src/main.py
```

Now, you can access API via `http://127.0.0.1:8000`.


## Connect with Dify

> If you use the cloud version, you will need to expose the API to the Internet in some way. Since this is a sample, we will use ngrok to proceed.  
> In the case of Self-Hosted (Docker), you can use it without exposing it to the Internet as long as it is reachable within the network from Dify.

## Add External Kowledge API

Select the Dify knowledge tab and click "External Knowledge API" in the upper right. Click the "+ Add an External Knowledge API" button.

Choose any name in the Name field. Enter the your public URL for ngrok like `https://4732-23-97-62-147.ngrok-free.app` in API Endpoint. The API Key is set to `secret` by default. You will need to change it to an appropriate one if you are actually using it.

![image](https://github.com/user-attachments/assets/64ca21e7-6ee6-4851-ab7f-d5f7daf8da69)

## Connect to an External Knowledge Base

Once you have finished configuring the API, connect the knowledge. Click "Connect to an External Knowledge Base" at the bottom of the Create Knowledge card.

Enter any name in External Knowledge Name. Confirm that the API you created earlier is in External Knowledge API. Enter `address` in External Knowledge ID. This is the name of the knowledge provided in this sample. Retrieval Setting can be any value. This value is not referenced in this sample.

![image](https://github.com/user-attachments/assets/950247b0-5407-41de-8435-dbad577dffa0)

After that, you can use it like normal knowledge base.
