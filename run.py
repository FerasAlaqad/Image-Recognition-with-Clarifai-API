from PIL import Image
import base64
import os

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = '27c0c62f3a494acfafb803112ae2627c'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'fcyehxqjklox'
APP_ID = 'test'
# Change these to whatever model you want to use
MODEL_ID = 'general-image-recognition'
MODEL_VERSION_ID = 'aa7f35c01e0642fda5cf400f543e7c40'
# Path to the folder containing images
IMAGE_FOLDER = "C:/Users/feras/Desktop/Mlops/APIs/clarifai/images/"

# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

# List all files in the image folder
image_files = os.listdir(IMAGE_FOLDER)

for image_file in image_files:
    # Create the full file path
    image_file_path = os.path.join(IMAGE_FOLDER, image_file)
    
    with open(image_file_path, "rb") as f:
        file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    output = post_model_outputs_response.outputs[0]
    first_concept = output.data.concepts[0]
    
    print("File: %s, Predicted Concept: %s %.2f" % (image_file, first_concept.name, first_concept.value))
