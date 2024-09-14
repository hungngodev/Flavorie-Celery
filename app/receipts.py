import re
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel
from app.utils import post_process, match_ingredients
from PIL import Image
import requests
from io import BytesIO
import logging
import nltk
import time

logging.basicConfig(level=logging.DEBUG)
print("Loading model")

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

local_directory = "/Users/hung/Documents/coding/SoftwareDevelopment/Flavorie-Celery/app/model"
         
def process_receipt_task(img, mongo_client):
        print("Processing image")   
        processor = DonutProcessor.from_pretrained(local_directory, local_files_only=True)
        model = VisionEncoderDecoderModel.from_pretrained(local_directory, local_files_only=True)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        task_prompt = "<s_cord-v2>" # <s_receipt> for v2
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
        time.sleep(6)
        return data[0]
        
        
        
data = [
      {
        "name": "ZUCCHINI GREEN 0.778kg",
        "price": "$4.66",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "green tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-tomato.png",
            "potential_id": "66254e71de4729f9b4e62dfb"
          },
          {
            "potential_name": "green olive",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-olives---sliced.jpg",
            "potential_id": "66502aa21f0b300ad1ef9610"
          },
          {
            "potential_name": "green shrimp",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-prawns.png",
            "potential_id": "66230c207ac4b51272baa045"
          },
          {
            "potential_name": "diced tomatoes with green chillis",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomatoes-canned.png",
            "potential_id": "66254e72de4729f9b4e63410"
          },
          {
            "potential_name": "green mangos",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mango.jpg",
            "potential_id": "6628774b1672f75fb7c067ac"
          },
          {
            "potential_name": "dandelion greens",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/dandelion-greens.jpg",
            "potential_id": "66879d4ae74918f2c9a219c8"
          },
          {
            "potential_name": "green papayas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/papaya.png",
            "potential_id": "66287b121f3b4350727a14c0"
          },
          {
            "potential_name": "green chili",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chili-peppers-green.jpg",
            "potential_id": "66287bec1f3b4350727aab9d"
          },
          {
            "potential_name": "green apples",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/grannysmith-apple.png",
            "potential_id": "662876532b648b647ae21d75"
          },
          {
            "potential_name": "dried green peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/split-peas-green.jpg",
            "potential_id": "66254f91de4729f9b4e6bf87"
          },
          {
            "potential_name": "dried green lentils",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/lentils-green.jpg",
            "potential_id": "66502b441f0b300ad1ef965e"
          },
          {
            "potential_name": "yellow tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomato-yellow.png",
            "potential_id": "66254e70de4729f9b4e62bd9"
          },
          {
            "potential_name": "yellow onions",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/brown-onion.png",
            "potential_id": "66254eb7de4729f9b4e65eb8"
          },
          {
            "potential_name": "mustard greens",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chinese-mustard-green.jpg",
            "potential_id": "6626ff36a6be53e4db073278"
          },
          {
            "potential_name": "green peppercorns",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/capers.jpg",
            "potential_id": "66254f51de4729f9b4e6bbec"
          },
          {
            "potential_name": "green food colour",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/food-coloring.png",
            "potential_id": "6656d9bcc70e5874845b6a4d"
          },
          {
            "potential_name": "purple cabbage",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/red-cabbage.png",
            "potential_id": "66254f02de4729f9b4e686d8"
          },
          {
            "potential_name": "green bell pepper",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-pepper.jpg",
            "potential_id": "66254eb9de4729f9b4e66677"
          },
          {
            "potential_name": "green tea",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-tea-leaves.jpg",
            "potential_id": "666e4633c853ec80ce6b6045"
          },
          {
            "potential_name": "diced green chile peppers",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/pickled-jalapenos.png",
            "potential_id": "66287be71f3b4350727a94e9"
          }
        ]
      },
      {
        "name": "BANANA CAVENDISH 0.442kg",
        "price": "$1.32",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "bananas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/bananas.jpg",
            "potential_id": "662877011672f75fb7c04557"
          },
          {
            "potential_name": "banana leaf",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/banana-leaf.jpg",
            "potential_id": "666e44dbc853ec80ce6ace21"
          },
          {
            "potential_name": "banana shallots",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/banana-shallots.jpg",
            "potential_id": "66254e79de4729f9b4e657af"
          },
          {
            "potential_name": "banana peppers",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/wax-peppers.png",
            "potential_id": "66287bea1f3b4350727aa080"
          },
          {
            "potential_name": "banana liqueur",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/limoncello.jpg",
            "potential_id": "665a72f7a7da0532eed123a5"
          },
          {
            "potential_name": "banana squash",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/pink-banana-squash.jpg",
            "potential_id": "66254f9ade4729f9b4e6dff8"
          },
          {
            "potential_name": "banana bread",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/quick-bread.png",
            "potential_id": "66285498aa5852cf1cbd495b"
          },
          {
            "potential_name": "mashed bananas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/bananas.jpg",
            "potential_id": "662877011672f75fb7c045a1"
          },
          {
            "potential_name": "banana blossom",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/banana-blossoms.jpg",
            "potential_id": "66879d4ce74918f2c9a2730f"
          },
          {
            "potential_name": "banana chips",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/banana-chips.jpg",
            "potential_id": "662877011672f75fb7c04632"
          },
          {
            "potential_name": "pineapple with juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/pineapple-with-can.png",
            "potential_id": "662876552b648b647ae2267d"
          },
          {
            "potential_name": "pineapple juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/pineapple-juice.jpg",
            "potential_id": "6628774e1672f75fb7c06e9e"
          },
          {
            "potential_name": "Mango Fruit Puree",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mango-puree.png",
            "potential_id": "6628774c1672f75fb7c06a81"
          },
          {
            "potential_name": "pineapples",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/pineapple.jpg",
            "potential_id": "662876542b648b647ae225a9"
          },
          {
            "potential_name": "vanilla sandwich biscuits",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/vanilla-sandwich-cookies.png",
            "potential_id": "6626feeaa6be53e4db06df85"
          },
          {
            "potential_name": "mangos",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mango.jpg",
            "potential_id": "6628774b1672f75fb7c06763"
          },
          {
            "potential_name": "blueberry juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/blueberry-juice.jpg",
            "potential_id": "662877091672f75fb7c05d2e"
          },
          {
            "potential_name": "pineapple jam",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/pineapple-preserves.jpg",
            "potential_id": "6628774d1672f75fb7c06e53"
          },
          {
            "potential_name": "waxy potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/red-potatoes.jpg",
            "potential_id": "66254e75de4729f9b4e647a3"
          },
          {
            "potential_name": "sugar-free blueberry jam",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/blueberry-jam.jpg",
            "potential_id": "662877091672f75fb7c05ca2"
          }
        ]
      },
      {
        "name": "SPECIAL",
        "price": "$0.99",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "lucky charms",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/lucky-charms.png",
            "potential_id": "662854e4aa5852cf1cbd865f"
          },
          {
            "potential_name": "super fine sugar",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sugar-in-bowl.png",
            "potential_id": "6629d884a4c95127604b079f"
          },
          {
            "potential_name": "semi sweet chocolate chips",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-chips.jpg",
            "potential_id": "6656dd1984bdb46d9f6fda23"
          },
          {
            "potential_name": "real bacon recipe pieces",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/bacon-bits.jpg",
            "potential_id": "662310164651165a8f3f49c7"
          },
          {
            "potential_name": "extra firm tofu",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tofu.png",
            "potential_id": "6656d8f6c70e5874845b4162"
          },
          {
            "potential_name": "extra sharp cheddar cheese",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cheddar-cheese.png",
            "potential_id": "6626fdd3a6be53e4db061610"
          },
          {
            "potential_name": "summer savory",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/summer-savory.jpg",
            "potential_id": "6656dd7d84bdb46d9f70002d"
          },
          {
            "potential_name": "sweet italian sausage",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/raw-pork-sausage.png",
            "potential_id": "6623101b4651165a8f3f5cb5"
          },
          {
            "potential_name": "sweet chilli sauce",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/fish-sauce.jpg",
            "potential_id": "6626ff7aa6be53e4db0741f0"
          },
          {
            "potential_name": "sweet potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sweet-potato.png",
            "potential_id": "66254e76de4729f9b4e65070"
          },
          {
            "potential_name": "gluten free all purpose baking flour",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/gluten-free-flour.jpg",
            "potential_id": "6629d8c9a4c95127604b288f"
          },
          {
            "potential_name": "devil's food cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-cake.jpg",
            "potential_id": "666d2f26b8ed437e5b352cc6"
          },
          {
            "potential_name": "allergy free chocolate chips",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-chips.jpg",
            "potential_id": "6656ddb784bdb46d9f70230e"
          },
          {
            "potential_name": "spring mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mixed-greens-or-mesclun.jpg",
            "potential_id": "666d2f0bb8ed437e5b2f1519"
          },
          {
            "potential_name": "chocolate cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-cake.jpg",
            "potential_id": "666bd42904a8f740be2dad0a"
          },
          {
            "potential_name": "instant hot cocoa",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cocoa-powder.png",
            "potential_id": "665a7233c646b1b0feb705c0"
          },
          {
            "potential_name": "candy coated chocolate pieces",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/candy-coated-chocolate-pieces-or-M&M's.jpg",
            "potential_id": "6656dac584bdb46d9f6f5964"
          },
          {
            "potential_name": "mix of brownies",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/brownie-isolated.png",
            "potential_id": "6656d6d7c70e5874845ad220"
          },
          {
            "potential_name": "cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/no.jpg",
            "potential_id": "665a7237c646b1b0feb83252"
          },
          {
            "potential_name": "regular chex cereal",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/regular-chex.png",
            "potential_id": "662854e2aa5852cf1cbd7f12"
          }
        ]
      },
      {
        "name": "SPECIAL",
        "price": "$1.50",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "lucky charms",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/lucky-charms.png",
            "potential_id": "662854e4aa5852cf1cbd865f"
          },
          {
            "potential_name": "super fine sugar",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sugar-in-bowl.png",
            "potential_id": "6629d884a4c95127604b079f"
          },
          {
            "potential_name": "semi sweet chocolate chips",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-chips.jpg",
            "potential_id": "6656dd1984bdb46d9f6fda23"
          },
          {
            "potential_name": "real bacon recipe pieces",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/bacon-bits.jpg",
            "potential_id": "662310164651165a8f3f49c7"
          },
          {
            "potential_name": "extra firm tofu",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tofu.png",
            "potential_id": "6656d8f6c70e5874845b4162"
          },
          {
            "potential_name": "extra sharp cheddar cheese",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cheddar-cheese.png",
            "potential_id": "6626fdd3a6be53e4db061610"
          },
          {
            "potential_name": "summer savory",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/summer-savory.jpg",
            "potential_id": "6656dd7d84bdb46d9f70002d"
          },
          {
            "potential_name": "sweet italian sausage",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/raw-pork-sausage.png",
            "potential_id": "6623101b4651165a8f3f5cb5"
          },
          {
            "potential_name": "sweet chilli sauce",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/fish-sauce.jpg",
            "potential_id": "6626ff7aa6be53e4db0741f0"
          },
          {
            "potential_name": "sweet potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sweet-potato.png",
            "potential_id": "66254e76de4729f9b4e65070"
          },
          {
            "potential_name": "gluten free all purpose baking flour",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/gluten-free-flour.jpg",
            "potential_id": "6629d8c9a4c95127604b288f"
          },
          {
            "potential_name": "devil's food cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-cake.jpg",
            "potential_id": "666d2f26b8ed437e5b352cc6"
          },
          {
            "potential_name": "allergy free chocolate chips",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-chips.jpg",
            "potential_id": "6656ddb784bdb46d9f70230e"
          },
          {
            "potential_name": "spring mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mixed-greens-or-mesclun.jpg",
            "potential_id": "666d2f0bb8ed437e5b2f1519"
          },
          {
            "potential_name": "chocolate cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-cake.jpg",
            "potential_id": "666bd42904a8f740be2dad0a"
          },
          {
            "potential_name": "instant hot cocoa",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cocoa-powder.png",
            "potential_id": "665a7233c646b1b0feb705c0"
          },
          {
            "potential_name": "candy coated chocolate pieces",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/candy-coated-chocolate-pieces-or-M&M's.jpg",
            "potential_id": "6656dac584bdb46d9f6f5964"
          },
          {
            "potential_name": "mix of brownies",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/brownie-isolated.png",
            "potential_id": "6656d6d7c70e5874845ad220"
          },
          {
            "potential_name": "cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/no.jpg",
            "potential_id": "665a7237c646b1b0feb83252"
          },
          {
            "potential_name": "regular chex cereal",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/regular-chex.png",
            "potential_id": "662854e2aa5852cf1cbd7f12"
          }
        ]
      },
      {
        "name": "POTATOES BRUSHED 1.328kg",
        "price": "$3.97",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/potatoes-yukon-gold.png",
            "potential_id": "66254e74de4729f9b4e6475a"
          },
          {
            "potential_name": "white potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/potatoes-yukon-gold.png",
            "potential_id": "66254e75de4729f9b4e6494e"
          },
          {
            "potential_name": "russet potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/russet-or-idaho-potatoes.png",
            "potential_id": "66254e75de4729f9b4e64832"
          },
          {
            "potential_name": "potato flakes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/instant-potatoes.png",
            "potential_id": "66254e77de4729f9b4e652a9"
          },
          {
            "potential_name": "french fried potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/french-fries-isolated.jpg",
            "potential_id": "66254e77de4729f9b4e65453"
          },
          {
            "potential_name": "purple potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/potatoes-purple.jpg",
            "potential_id": "66254e75de4729f9b4e64a6c"
          },
          {
            "potential_name": "red potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/red-potatoes.jpg",
            "potential_id": "66254e76de4729f9b4e64b86"
          },
          {
            "potential_name": "white sweet potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sweet-potato.png",
            "potential_id": "66254e76de4729f9b4e65148"
          },
          {
            "potential_name": "waxy potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/red-potatoes.jpg",
            "potential_id": "66254e75de4729f9b4e647a3"
          },
          {
            "potential_name": "potato crisps",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/potato-chips.png",
            "potential_id": "6656dc5f84bdb46d9f6fa489"
          },
          {
            "potential_name": "potato bread",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/white-bread.jpg",
            "potential_id": "66285456aa5852cf1cbd309b"
          },
          {
            "potential_name": "red skinned sweet potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sweet-potato.png",
            "potential_id": "66254e76de4729f9b4e650b9"
          },
          {
            "potential_name": "sweet potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sweet-potato.png",
            "potential_id": "66254e76de4729f9b4e65070"
          },
          {
            "potential_name": "fingerling potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/fingerling-potatoes.jpg",
            "potential_id": "66254e75de4729f9b4e649dd"
          },
          {
            "potential_name": "cooked long-grain brown rice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/rice-brown-cooked.png",
            "potential_id": "6626ffbba6be53e4db074c48"
          },
          {
            "potential_name": "cooked longgrain white rice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/rice-white-long-grain-or-basmatii-cooked.jpg",
            "potential_id": "6626ffbea6be53e4db0755ca"
          },
          {
            "potential_name": "hash browned potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/hash-brown-potatoes.png",
            "potential_id": "66254e77de4729f9b4e652f3"
          },
          {
            "potential_name": "sweet potato starch noodles",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/dangmyeon.png",
            "potential_id": "6628540baa5852cf1cbca91c"
          },
          {
            "potential_name": "mashed bananas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/bananas.jpg",
            "potential_id": "662877011672f75fb7c045a1"
          },
          {
            "potential_name": "potato rolls",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/dinner-yeast-rolls.jpg",
            "potential_id": "66285456aa5852cf1cbd300e"
          }
        ]
      },
      {
        "name": "BROCCOLI 0.808kg",
        "price": "$4.84",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "broccoli sprouts",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/alfalfa-sprouts.png",
            "potential_id": "66254e30de4729f9b4e622bd"
          },
          {
            "potential_name": "romanesco broccoli",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/romanesco.png",
            "potential_id": "66254e30de4729f9b4e624cb"
          },
          {
            "potential_name": "broccoli florets",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccoli.jpg",
            "potential_id": "66254e2fde4729f9b4e62112"
          },
          {
            "potential_name": "broccoli slaw",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/slaw-mix.png",
            "potential_id": "66254e30de4729f9b4e62235"
          },
          {
            "potential_name": "broccoli raab",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccoli-rabe.jpg",
            "potential_id": "66254e2fde4729f9b4e621eb"
          },
          {
            "potential_name": "broccoli spears",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccoli.jpg",
            "potential_id": "6623139853a069c18baf41eb"
          },
          {
            "potential_name": "cauliflower",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cauliflower.jpg",
            "potential_id": "66254f96de4729f9b4e6d1ef"
          },
          {
            "potential_name": "kale",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/kale.jpg",
            "potential_id": "66254f97de4729f9b4e6d648"
          },
          {
            "potential_name": "low-sodium vegetable broth",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chicken-broth.png",
            "potential_id": "66287be31f3b4350727a891e"
          },
          {
            "potential_name": "spinach fettucine",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/spinach-pasta.jpg",
            "potential_id": "66254e31de4729f9b4e626c7"
          },
          {
            "potential_name": "cabbages",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cabbage.jpg",
            "potential_id": "66254f02de4729f9b4e684f1"
          },
          {
            "potential_name": "refrigerated spinach tortelini",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tortellini-isolated.jpg",
            "potential_id": "66254e31de4729f9b4e62712"
          },
          {
            "potential_name": "broccolini",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccolini.jpg",
            "potential_id": "66254e2fde4729f9b4e621a2"
          },
          {
            "potential_name": "cooked angelhair pasta",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/angelhair.jpg",
            "potential_id": "66285408aa5852cf1cbc9879"
          },
          {
            "potential_name": "angelhair pasta",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/angelhair.jpg",
            "potential_id": "662853c7aa5852cf1cbc89da"
          },
          {
            "potential_name": "riced cauliflower",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cauliflower.jpg",
            "potential_id": "66254f96de4729f9b4e6d2cd"
          },
          {
            "potential_name": "spaghetti squashes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/spaghetti-squash.jpg",
            "potential_id": "66254f9bde4729f9b4e6e087"
          },
          {
            "potential_name": "frozen spinach",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/spinach-frozen.jpg",
            "potential_id": "66254e31de4729f9b4e6255f"
          },
          {
            "potential_name": "savoy cabbage",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/savoy-cabbage.jpg",
            "potential_id": "66254f02de4729f9b4e68649"
          },
          {
            "potential_name": "chinese celery cabbage",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/napa-cabbage.jpg",
            "potential_id": "66254f03de4729f9b4e68b37"
          }
        ]
      },
      {
        "name": "BRUSSEL SPROUTS 0.322kg",
        "price": "$5.15",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "brussel sprouts",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/brussels-sprouts.jpg",
            "potential_id": "66254f97de4729f9b4e6d5fc"
          },
          {
            "potential_name": "broccoli sprouts",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/alfalfa-sprouts.png",
            "potential_id": "66254e30de4729f9b4e622bd"
          },
          {
            "potential_name": "mung bean sprouts",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/bean-sprouts.jpg",
            "potential_id": "66254fdbde4729f9b4e6f7ca"
          },
          {
            "potential_name": "broccoli florets",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccoli.jpg",
            "potential_id": "66254e2fde4729f9b4e62112"
          },
          {
            "potential_name": "broccoli slaw",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/slaw-mix.png",
            "potential_id": "66254e30de4729f9b4e62235"
          },
          {
            "potential_name": "romanesco broccoli",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/romanesco.png",
            "potential_id": "66254e30de4729f9b4e624cb"
          },
          {
            "potential_name": "kale",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/kale.jpg",
            "potential_id": "66254f97de4729f9b4e6d648"
          },
          {
            "potential_name": "celery root",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/celeriac.jpg",
            "potential_id": "66254f05de4729f9b4e68ff2"
          },
          {
            "potential_name": "broccoli raab",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccoli-rabe.jpg",
            "potential_id": "66254e2fde4729f9b4e621eb"
          },
          {
            "potential_name": "broccoli spears",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccoli.jpg",
            "potential_id": "6623139853a069c18baf41eb"
          },
          {
            "potential_name": "root vegetables",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/root-vegetables.png",
            "potential_id": "6656dcf384bdb46d9f6fc7c2"
          },
          {
            "potential_name": "celery seeds",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/celery-seed.jpg",
            "potential_id": "66254f05de4729f9b4e68f5e"
          },
          {
            "potential_name": "fennel seed",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/fennel-seeds.jpg",
            "potential_id": "66255020de4729f9b4e70b33"
          },
          {
            "potential_name": "moong beans",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mung-beans.png",
            "potential_id": "665a72c04eaecb1611c62b88"
          },
          {
            "potential_name": "edamame beans",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/edamame.png",
            "potential_id": "6656d8e2c70e5874845b3a74"
          },
          {
            "potential_name": "cauliflower",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cauliflower.jpg",
            "potential_id": "66254f96de4729f9b4e6d1ef"
          },
          {
            "potential_name": "broccolini",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccolini.jpg",
            "potential_id": "66254e2fde4729f9b4e621a2"
          },
          {
            "potential_name": "fennel",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/fennel.png",
            "potential_id": "66255020de4729f9b4e709d1"
          },
          {
            "potential_name": "roasted garlic",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/garlic-roasted.jpg",
            "potential_id": "66254fdcde4729f9b4e6f9f9"
          },
          {
            "potential_name": "kohlrabi",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/kohlrabi.jpg",
            "potential_id": "666d2f1eb8ed437e5b3229eb"
          }
        ]
      },
      {
        "name": "SPECIAL",
        "price": "$0.99",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "lucky charms",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/lucky-charms.png",
            "potential_id": "662854e4aa5852cf1cbd865f"
          },
          {
            "potential_name": "super fine sugar",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sugar-in-bowl.png",
            "potential_id": "6629d884a4c95127604b079f"
          },
          {
            "potential_name": "semi sweet chocolate chips",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-chips.jpg",
            "potential_id": "6656dd1984bdb46d9f6fda23"
          },
          {
            "potential_name": "real bacon recipe pieces",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/bacon-bits.jpg",
            "potential_id": "662310164651165a8f3f49c7"
          },
          {
            "potential_name": "extra firm tofu",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tofu.png",
            "potential_id": "6656d8f6c70e5874845b4162"
          },
          {
            "potential_name": "extra sharp cheddar cheese",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cheddar-cheese.png",
            "potential_id": "6626fdd3a6be53e4db061610"
          },
          {
            "potential_name": "summer savory",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/summer-savory.jpg",
            "potential_id": "6656dd7d84bdb46d9f70002d"
          },
          {
            "potential_name": "sweet italian sausage",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/raw-pork-sausage.png",
            "potential_id": "6623101b4651165a8f3f5cb5"
          },
          {
            "potential_name": "sweet chilli sauce",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/fish-sauce.jpg",
            "potential_id": "6626ff7aa6be53e4db0741f0"
          },
          {
            "potential_name": "sweet potatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sweet-potato.png",
            "potential_id": "66254e76de4729f9b4e65070"
          },
          {
            "potential_name": "gluten free all purpose baking flour",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/gluten-free-flour.jpg",
            "potential_id": "6629d8c9a4c95127604b288f"
          },
          {
            "potential_name": "devil's food cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-cake.jpg",
            "potential_id": "666d2f26b8ed437e5b352cc6"
          },
          {
            "potential_name": "allergy free chocolate chips",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-chips.jpg",
            "potential_id": "6656ddb784bdb46d9f70230e"
          },
          {
            "potential_name": "spring mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mixed-greens-or-mesclun.jpg",
            "potential_id": "666d2f0bb8ed437e5b2f1519"
          },
          {
            "potential_name": "chocolate cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chocolate-cake.jpg",
            "potential_id": "666bd42904a8f740be2dad0a"
          },
          {
            "potential_name": "instant hot cocoa",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cocoa-powder.png",
            "potential_id": "665a7233c646b1b0feb705c0"
          },
          {
            "potential_name": "candy coated chocolate pieces",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/candy-coated-chocolate-pieces-or-M&M's.jpg",
            "potential_id": "6656dac584bdb46d9f6f5964"
          },
          {
            "potential_name": "mix of brownies",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/brownie-isolated.png",
            "potential_id": "6656d6d7c70e5874845ad220"
          },
          {
            "potential_name": "cake mix",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/no.jpg",
            "potential_id": "665a7237c646b1b0feb83252"
          },
          {
            "potential_name": "regular chex cereal",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/regular-chex.png",
            "potential_id": "662854e2aa5852cf1cbd7f12"
          }
        ]
      },
      {
        "name": "GRAPES GREEN 1.174kg",
        "price": "$7.03",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "green seedless grapes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/white-grapes.jpg",
            "potential_id": "662877041672f75fb7c04e31"
          },
          {
            "potential_name": "green tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-tomato.png",
            "potential_id": "66254e71de4729f9b4e62dfb"
          },
          {
            "potential_name": "white grape juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/white-grape-juice.jpg",
            "potential_id": "666a95a26582319a8a252225"
          },
          {
            "potential_name": "green papayas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/papaya.png",
            "potential_id": "66287b121f3b4350727a14c0"
          },
          {
            "potential_name": "green apples",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/grannysmith-apple.png",
            "potential_id": "662876532b648b647ae21d75"
          },
          {
            "potential_name": "green mangos",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mango.jpg",
            "potential_id": "6628774b1672f75fb7c067ac"
          },
          {
            "potential_name": "green olive",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-olives---sliced.jpg",
            "potential_id": "66502aa21f0b300ad1ef9610"
          },
          {
            "potential_name": "white grapes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/white-grapes.jpg",
            "potential_id": "662877041672f75fb7c04c86"
          },
          {
            "potential_name": "grape",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/red-grapes.jpg",
            "potential_id": "662877041672f75fb7c04c3c"
          },
          {
            "potential_name": "black grapes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/black-grapes.jpg",
            "potential_id": "662877041672f75fb7c04ec2"
          },
          {
            "potential_name": "grape tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cherry-tomatoes.png",
            "potential_id": "66254e6fde4729f9b4e62875"
          },
          {
            "potential_name": "green shrimp",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-prawns.png",
            "potential_id": "66230c207ac4b51272baa045"
          },
          {
            "potential_name": "dandelion greens",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/dandelion-greens.jpg",
            "potential_id": "66879d4ae74918f2c9a219c8"
          },
          {
            "potential_name": "green tea",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-tea-leaves.jpg",
            "potential_id": "666e4633c853ec80ce6b6045"
          },
          {
            "potential_name": "grape fruit juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/grapefruit-juice.jpg",
            "potential_id": "6656dcba84bdb46d9f6fb6e7"
          },
          {
            "potential_name": "green peppercorns",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/capers.jpg",
            "potential_id": "66254f51de4729f9b4e6bbec"
          },
          {
            "potential_name": "mustard greens",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/chinese-mustard-green.jpg",
            "potential_id": "6626ff36a6be53e4db073278"
          },
          {
            "potential_name": "dried green peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/split-peas-green.jpg",
            "potential_id": "66254f91de4729f9b4e6bf87"
          },
          {
            "potential_name": "red wine",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/red-wine.jpg",
            "potential_id": "6650315a1f0b300ad1efb119"
          },
          {
            "potential_name": "red apples",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/red-delicious-apples.png",
            "potential_id": "662876522b648b647ae21980"
          }
        ]
      },
      {
        "name": "PEAS SNOW 0.218kg",
        "price": "$3.27",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "peas and carrots",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/peas-and-carrots.jpg",
            "potential_id": "6623139753a069c18baf3e10"
          },
          {
            "potential_name": "wasabi peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/wasabi-peas.jpg",
            "potential_id": "66254f92de4729f9b4e6c1a3"
          },
          {
            "potential_name": "baby peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/peas.jpg",
            "potential_id": "66254f52de4729f9b4e6bc7a"
          },
          {
            "potential_name": "snap peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sugar-snap-peas.jpg",
            "potential_id": "66254f52de4729f9b4e6bd4e"
          },
          {
            "potential_name": "cow pea pods",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cowpea.png",
            "potential_id": "66254f08de4729f9b4e696dc"
          },
          {
            "potential_name": "canned peas and carrots",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/peas-and-carrots.jpg",
            "potential_id": "6623139853a069c18baf4026"
          },
          {
            "potential_name": "canned peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/peas.jpg",
            "potential_id": "66254f92de4729f9b4e6c1ec"
          },
          {
            "potential_name": "split pigeon pea",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/yellow-split-peas.jpg",
            "potential_id": "66254f91de4729f9b4e6c094"
          },
          {
            "potential_name": "dried green peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/split-peas-green.jpg",
            "potential_id": "66254f91de4729f9b4e6bf87"
          },
          {
            "potential_name": "black eyed peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/black-eyed-peas.jpg",
            "potential_id": "66254f92de4729f9b4e6c275"
          },
          {
            "potential_name": "winter squash",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/butternut-squash.jpg",
            "potential_id": "66254f9ade4729f9b4e6ddc0"
          },
          {
            "potential_name": "dried black eyed peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/black-eyed-peas.jpg",
            "potential_id": "66254f92de4729f9b4e6c34d"
          },
          {
            "potential_name": "canned black eyed peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/black-eyed-peas.jpg",
            "potential_id": "66254f92de4729f9b4e6c2be"
          },
          {
            "potential_name": "potato flakes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/instant-potatoes.png",
            "potential_id": "66254e77de4729f9b4e652a9"
          },
          {
            "potential_name": "cream of potato soup",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cream-of-chicken-soup.jpg",
            "potential_id": "6626feaba6be53e4db06d4d2"
          },
          {
            "potential_name": "cooked split peas",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/split-peas-green.jpg",
            "potential_id": "66254f93de4729f9b4e6c4a9"
          },
          {
            "potential_name": "baby spinach leaves",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/spinach.jpg",
            "potential_id": "66254e31de4729f9b4e625ee"
          },
          {
            "potential_name": "frozen corn",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/corn.png",
            "potential_id": "66254f50de4729f9b4e6b8f1"
          },
          {
            "potential_name": "quinoa flakes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/quinoa-flakes.jpg",
            "potential_id": "6628549baa5852cf1cbd55f1"
          },
          {
            "potential_name": "white shoepeg corn",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/corn-white.png",
            "potential_id": "66254f49de4729f9b4e69f82"
          }
        ]
      },
      {
        "name": "TOMATOES GRAPE",
        "price": "$2.99",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "grape tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cherry-tomatoes.png",
            "potential_id": "66254e6fde4729f9b4e62875"
          },
          {
            "potential_name": "tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomato.png",
            "potential_id": "66254e6fde4729f9b4e6282b"
          },
          {
            "potential_name": "grape",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/red-grapes.jpg",
            "potential_id": "662877041672f75fb7c04c3c"
          },
          {
            "potential_name": "tomatoes with juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomatoes-canned.png",
            "potential_id": "66254e73de4729f9b4e63532"
          },
          {
            "potential_name": "tomato juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomato-juice.jpg",
            "potential_id": "6656dd9884bdb46d9f701155"
          },
          {
            "potential_name": "vine ripened tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/roma-tomatoes.png",
            "potential_id": "66254e6fde4729f9b4e62997"
          },
          {
            "potential_name": "plum tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/plum-tomatoes.png",
            "potential_id": "66254e71de4729f9b4e62d6a"
          },
          {
            "potential_name": "cherry tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cherry-tomatoes.png",
            "potential_id": "66254e70de4729f9b4e62c5a"
          },
          {
            "potential_name": "muscadine grapes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/black-grapes.jpg",
            "potential_id": "662877041672f75fb7c04f29"
          },
          {
            "potential_name": "grape fruit juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/grapefruit-juice.jpg",
            "potential_id": "6656dcba84bdb46d9f6fb6e7"
          },
          {
            "potential_name": "beefsteak tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/beefsteak-tomato.jpg",
            "potential_id": "66230a321001547f4041bdd1"
          },
          {
            "potential_name": "tomato puree",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomato-paste.jpg",
            "potential_id": "665032221f0b300ad1efbdd3"
          },
          {
            "potential_name": "green seedless grapes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/white-grapes.jpg",
            "potential_id": "662877041672f75fb7c04e31"
          },
          {
            "potential_name": "orange tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomato-orange.png",
            "potential_id": "66254e72de4729f9b4e63302"
          },
          {
            "potential_name": "heirloom tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomato.png",
            "potential_id": "66254e73de4729f9b4e63642"
          },
          {
            "potential_name": "sundried tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sundried-tomatoes.jpg",
            "potential_id": "66254e71de4729f9b4e62e8a"
          },
          {
            "potential_name": "white grape juice",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/white-grape-juice.jpg",
            "potential_id": "666a95a26582319a8a252225"
          },
          {
            "potential_name": "tomato & basil sauce",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomato-sauce-or-pasta-sauce.jpg",
            "potential_id": "6626ff2fa6be53e4db071db8"
          },
          {
            "potential_name": "yellow cherry tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/tomatoes-yellow.jpg",
            "potential_id": "66254e70de4729f9b4e62ce9"
          },
          {
            "potential_name": "green tomatoes",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/green-tomato.png",
            "potential_id": "66254e71de4729f9b4e62dfb"
          }
        ]
      },
      {
        "name": "LETTUCE ICEBERG",
        "price": "$2.49",
        "quantity": "1",
        "potential_matches": [
          {
            "potential_name": "iceberg lettuce leaves",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/iceberg-lettuce.jpg",
            "potential_id": "66254f00de4729f9b4e67b4c"
          },
          {
            "potential_name": "butterhead lettuce",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/Butter-or-Boston-Bibb-lettuce.jpg",
            "potential_id": "66254f01de4729f9b4e680df"
          },
          {
            "potential_name": "romaine lettuce leaves",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/romaine.jpg",
            "potential_id": "66254f01de4729f9b4e68006"
          },
          {
            "potential_name": "butterhead lettuce leaves",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/Butter-or-Boston-Bibb-lettuce.jpg",
            "potential_id": "66254f01de4729f9b4e67ea2"
          },
          {
            "potential_name": "lettuce leaves",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/iceberg-lettuce.jpg",
            "potential_id": "66254f00de4729f9b4e67abf"
          },
          {
            "potential_name": "curly lettuce",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/frisee.jpg",
            "potential_id": "66254f00de4729f9b4e67bdb"
          },
          {
            "potential_name": "red leaf lettuce",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/lollo-rosso.jpg",
            "potential_id": "66254f00de4729f9b4e67cf9"
          },
          {
            "potential_name": "babyleaf lettuce",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mixed-greens-or-mesclun.jpg",
            "potential_id": "66254f00de4729f9b4e67c6a"
          },
          {
            "potential_name": "curly lettuce leaves",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/frisee.jpg",
            "potential_id": "66254f01de4729f9b4e67f31"
          },
          {
            "potential_name": "red leaf lettuce leaves",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/lollo-rosso.jpg",
            "potential_id": "66254f00de4729f9b4e67e13"
          },
          {
            "potential_name": "broccoli slaw",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/slaw-mix.png",
            "potential_id": "66254e30de4729f9b4e62235"
          },
          {
            "potential_name": "cucumbers",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cucumber.jpg",
            "potential_id": "66254ec1de4729f9b4e674f3"
          },
          {
            "potential_name": "broccoli spears",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/broccoli.jpg",
            "potential_id": "6623139853a069c18baf41eb"
          },
          {
            "potential_name": "spinach leaves",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/spinach.jpg",
            "potential_id": "66254e30de4729f9b4e62516"
          },
          {
            "potential_name": "mesclun",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/mixed-greens-or-mesclun.jpg",
            "potential_id": "6656d9bec70e5874845b6c3b"
          },
          {
            "potential_name": "sea cucumber",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/sea-cucumber.png",
            "potential_id": "66254ec2de4729f9b4e67782"
          },
          {
            "potential_name": "cabbages",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/cabbage.jpg",
            "potential_id": "66254f02de4729f9b4e684f1"
          },
          {
            "potential_name": "spinach wraps",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/spinach-wraps.jpg",
            "potential_id": "66254e31de4729f9b4e6267e"
          },
          {
            "potential_name": "chinese celery cabbage",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/napa-cabbage.jpg",
            "potential_id": "66254f03de4729f9b4e68b37"
          },
          {
            "potential_name": "frozen spinach",
            "potential_image": "https://img.spoonacular.com/ingredients_250x250/spinach-frozen.jpg",
            "potential_id": "66254e31de4729f9b4e6255f"
          }
        ]
      }
    ],