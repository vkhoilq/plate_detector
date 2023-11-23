import streamlit as st
from pathlib import Path
from typing import Union
from pydantic_class.plate_class import PlateInfo,Box
from io import BytesIO
from typing_extensions import Final, Literal, TypeAlias


# from streamlit_back_camera_input import back_camera_input
# st.write('Hello 1')
# image1 = st.camera_input('Test Cam') 
# if image1:
#     st.image(image1)
# st.write('Hello 2')
# image2 = back_camera_input()
# if image2:
#     st.image(image2)
# st.write('Hello 2')

# reader = easyocr.Reader(['en'], gpu=False)


# def read_license_plate(license_plate_crop):
#     """
#     Read the license plate text from the given cropped image.

#     Args:
#         license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

#     Returns:
#         tuple: Tuple containing the formatted license plate text and its confidence score.
#     """

#     detections = reader.readtext(license_plate_crop)

#     for detection in detections:
#         bbox, text, score = detection
#         print(text)

#     return None

AtomicImage: TypeAlias = Union[str,Path,BytesIO]

def read_license_plate_3rd_party(img:AtomicImage) ->PlateInfo:
    import requests
    import pprint

    if "plate_api_key" in st.secrets:
        api_key = st.secrets.plate_api_key
    else:
        api_key = 'FILL IN'


    regions = ["vn"] # Change to your country
    if isinstance(img, BytesIO):
        files = {'upload':('image.jpg',img.getvalue(), 'image/jpeg')}
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  #Optional
            files=files,
            headers={'Authorization': f'Token {api_key}'})
    else:
        with open(img, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),  #Optional
                files=dict(upload=fp),
                headers={'Authorization': f'Token {api_key}'})

    pprint.pprint(response.json())
    results = []
    results = response.json()['results']
    if len(results) > 0:
        result = results[0]
        plate = PlateInfo(**result)
        print(plate.plate)
        return plate
    
    return None
        


def image_input():
    # Camera input
    camera_image = st.camera_input("Take a picture")

    # Image upload
    uploaded_file = st.file_uploader("...or upload an image", type=['png', 'jpg', 'jpeg'])

    # Display the image
    if camera_image:
        st.image(camera_image, caption='Captured Image')
        return camera_image
    elif uploaded_file:
        st.image(uploaded_file, caption='Uploaded Image')
        return uploaded_file
    return None

image = image_input()
if image:
    if st.button('Send To Server'):
        plate = read_license_plate_3rd_party(image)
        if plate:
            st.write(f'Plate Number: {plate.plate}')
        else:
            st.write(f'No Plate Found')
#filepath = Path('images/plate.jpg')



#plate = read_license_plate_3rd_party(filepath)










# img = cv2.imread(filepath)
# st.image(img,caption='Detected Image')

# # load models
# coco_model = YOLO('yolov8n.pt')


# license_plate_detector = YOLO(Path('models/license_plate_detector.pt'))


# # detect license plates
# license_plates = license_plate_detector(img)[0]
# for license_plate in license_plates.boxes.data.tolist():
#     x1, y1, x2, y2, score, class_id = license_plate
#     if (score > 0.2):
#         st.write(f'{x1}, {y1} , {x2} , {y2}')
#         license_plate_crop = img[int(y1):int(y2), int(x1): int(x2), :]
#         license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
#         _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
#         st.image(license_plate_crop_thresh)
#         abc = read_license_plate(license_plate_crop_thresh)
#         st.write(abc)