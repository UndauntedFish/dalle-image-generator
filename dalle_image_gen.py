# Imports for encoding/decoding API key to keep it secure
import configparser
from base64 import b64decode
# Imports for openai and openai error handling
import openai
from openai.error import InvalidRequestError
# Imports for recieving and displaying generated images
import datetime
import webbrowser

#===============================================================================================
# Connect to the Open AI API
#===============================================================================================
# Create an instance of the ConfigParser class and store it in config
config = configparser.ConfigParser()

# Read the credentials.ini file and store the API key into API_KEY
config.read("credentials.ini")
API_KEY = config["openai"]["APIKEY"]

# Set the openai api key property to my API key
openai.api_key = API_KEY
#===============================================================================================


#===============================================================================================
# Generate an image using DALL-E
# Params:
#  prompt        (str): The prompt, which is a description of what image you want to create.
#  num_image     (int): Number of images to be generated in the completion. Default is 1.
#  size          (str): The size of the image to be generated in the completion. Default is 256x256.
#  output_format (str): The medium through which the generated image will be returned. Default is URL.
#===============================================================================================
def generate_image(prompt, num_image=1, size="256x256", output_format="url"):
   
    # Tries to send the prompt to openai and get a completion
    # If it gets a completion, execute the code in "try." If no completion is recieved, execute the code in "except."
    try:
       
        # This list will store all the images generated by the openai api
        images = []

        # Calls the openai Image class's create function to send the prompt to DALL-E and generate an image based on our input requirements
        response = openai.Image.create(prompt=prompt, n=num_image, size=size, response_format=output_format)

        # If the output format is set to URL, get all the image URLS and store them in images.
        # Otherwise, if the output format is b64json, get all the image's json data and store them in images.
        if output_format == "url":
            # response["data"] passes in "data" as a key into the response object, and returns a list of images generated
            for image in response["data"]:
                images.append(image.url)
        elif output_format == "b64_json":
            for image in response["data"]:  
                images.append(image.b64_json)
        
        # Return a dictionary which contains the timestap and url/json of each image generated
        return {"created": datetime.datetime.fromtimestamp(response["created"]), "images": images}
    
    except InvalidRequestError as e:
        # Print the error
        print(e)
#===============================================================================================


#===============================================================================================
# Takes in a prompt, and generates a completion using DALL-E by using the helper function above
#===============================================================================================
# Call the generate_image() method to submit a prompt and get a completion
completion = generate_image("AI clipart no background", num_image=2, size="512x512")

# Get the list of image URLs generated
images = completion["images"]

# Prints each URL to the console, and also opens them in the web browser.
for i in range(0, len(images)):
    print("URL ", i, ": ", images[i])
    webbrowser.open(images[i])

# image 1: https://oaidalleapiprodscus.blob.core.windows.net/private/org-97ONNWmoDAih9S6t7h9gliBr/user-5fswk11tVZKt43hfIhQRel8l/img-U5rhWCPnnHgGYjLxV2yH6YFj.png?st=2023-05-02T20%3A44%3A10Z&se=2023-05-02T22%3A44%3A10Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-05-02T19%3A53%3A01Z&ske=2023-05-03T19%3A53%3A01Z&sks=b&skv=2021-08-06&sig=VrjeFK3YVquJHm63VdnRrVHITPqyeQN45%2BBDXabnqcE%3D
# image 2: https://oaidalleapiprodscus.blob.core.windows.net/private/org-97ONNWmoDAih9S6t7h9gliBr/user-5fswk11tVZKt43hfIhQRel8l/img-cre5UWSkMQatnTAueWbfXlUo.png?st=2023-05-02T20%3A44%3A10Z&se=2023-05-02T22%3A44%3A10Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-05-02T19%3A53%3A01Z&ske=2023-05-03T19%3A53%3A01Z&sks=b&skv=2021-08-06&sig=dFQle0EfbGB63GvWbKU6lyU0KYsyx3T/XqZjHgC0N6A%3D 
#===============================================================================================