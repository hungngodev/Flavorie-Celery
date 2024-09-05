import re
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel
from app.utils import post_process, match_ingredients
from PIL import Image
import requests
from io import BytesIO
import logging
import nltk

logging.basicConfig(level=logging.DEBUG)
print("Loading model")

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
         
def process_receipt_task(img, mongo_client):
        print("Processing image")   
        processor = DonutProcessor.from_pretrained("AdamCodd/donut-receipts-extract")
        model = VisionEncoderDecoderModel.from_pretrained("AdamCodd/donut-receipts-extract")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        task_prompt = "<s_receipt>"
        decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
        pixel_values = processor(img, return_tensors="pt").pixel_values
        # print("Sharing memory")
        # model.share_memory()
        print("Generating output")
    
        print("Before generate")
        outputs = model.generate(
            pixel_values.to(device),
            decoder_input_ids=decoder_input_ids.to(device),
            max_length=model.decoder.config.max_position_embeddings,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            use_cache=True,
            bad_words_ids=[[processor.tokenizer.unk_token_id]],
            return_dict_in_generate=True,
        )
        print("Output generated")
        # except Exception as e:
        #     logging.error("An error occurred: %s", str(e))
        #     logging.error("Stack Trace: %s", traceback.format_exc())
        #     return {"error": "Error processing image"}
        print("Decoding output")
        sequence = processor.batch_decode(outputs.sequences)[0]
        sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
        sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  
        structured_data = processor.token2json(sequence)
        structured_receipts = post_process(structured_data)
        print("Matching ingredients")
        matched_items = match_ingredients(structured_receipts['items'], mongo_client)

        return matched_items

def scan_receipt(img_url, mongo_client):

    if img_url == "":
        return ({"error": "No selected file"})
    try:
        # fetch img data from url, stream=True allows writing even when the download is not done
        print("Fetching image")
        response = requests.get(img_url, stream=True)

        # if error occur, return httperror object
        response.raise_for_status()
        # response.content is in bytes
        img = Image.open(BytesIO(response.content)).convert("RGB")
        print("Image loaded")
        final_res = process_receipt_task(img, mongo_client)
        return final_res

    except Exception as e:
        print(e)
        