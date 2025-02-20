# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of Obama?</title>
    <h1>Upload a picture and see if it's a picture of Obama!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    known_face_encoding = [-0.09634063,  0.12095481, -0.00436332, -0.07643753,  0.0080383,
                            0.01902981, -0.07184699, -0.09383309,  0.18518871, -0.09588896,
                            0.23951106,  0.0986533 , -0.22114635, -0.1363683 ,  0.04405268,
                            0.11574756, -0.19899382, -0.09597053, -0.11969153, -0.12277931,
                            0.03416885, -0.00267565,  0.09203379,  0.04713435, -0.12731361,
                           -0.35371891, -0.0503444 , -0.17841317, -0.00310897, -0.09844551,
                           -0.06910533, -0.00503746, -0.18466514, -0.09851682,  0.02903969,
                           -0.02174894,  0.02261871,  0.0032102 ,  0.20312519,  0.02999607,
                           -0.11646006,  0.09432904,  0.02774341,  0.22102901,  0.26725179,
                            0.06896867, -0.00490024, -0.09441824,  0.11115381, -0.22592428,
                            0.06230862,  0.16559327,  0.06232892,  0.03458837,  0.09459756,
                           -0.18777156,  0.00654241,  0.08582542, -0.13578284,  0.0150229 ,
                            0.00670836, -0.08195844, -0.04346499,  0.03347827,  0.20310158,
                            0.09987706, -0.12370517, -0.06683611,  0.12704916, -0.02160804,
                            0.00984683,  0.00766284, -0.18980607, -0.19641446, -0.22800779,
                            0.09010898,  0.39178532,  0.18818057, -0.20875394,  0.03097027,
                           -0.21300618,  0.02532415,  0.07938635,  0.01000703, -0.07719778,
                           -0.12651891, -0.04318593,  0.06219772,  0.09163868,  0.05039065,
                           -0.04922386,  0.21839413, -0.02394437,  0.06173781,  0.0292527 ,
                            0.06160797, -0.15553983, -0.02440624, -0.17509389, -0.0630486 ,
                            0.01428208, -0.03637431,  0.03971229,  0.13983178, -0.23006812,
                            0.04999552,  0.0108454 , -0.03970895,  0.02501768,  0.08157793,
                           -0.03224047, -0.04502571,  0.0556995 , -0.24374914,  0.25514284,
                            0.24795187,  0.04060191,  0.17597422,  0.07966681,  0.01920104,
                           -0.01194376, -0.02300822, -0.17204897, -0.0596558 ,  0.05307484,
                            0.07417042,  0.07126575,  0.00209804]
    
    luisfer_face_encoding = [-0.11231618,  0.06299703,  0.0217769 ,  0.01927234, -0.04071514,
        0.03533049, -0.0383848 , -0.07037434,  0.10443643, -0.05706102,
        0.24297197,  0.00503374, -0.21630484,  0.08044215, -0.04702449,
        0.07706863, -0.16646177, -0.06996191, -0.10635699,  0.03861973,
        0.09823027, -0.01719735, -0.02002988,  0.08047897, -0.1438365 ,
       -0.29509965, -0.1077523 , -0.05563687,  0.0121289 , -0.07039692,
       -0.01993041,  0.0258231 , -0.14561135,  0.04682582,  0.03943215,
        0.01961103, -0.02454426, -0.06458037,  0.24199829,  0.02496972,
       -0.15349707,  0.03146677,  0.04711599,  0.25314671,  0.17052855,
        0.02646449, -0.00721924, -0.10350284,  0.12816332, -0.36851797,
        0.12360322,  0.14111054,  0.154084  ,  0.10596898,  0.05406531,
       -0.16662532,  0.03272658,  0.11826867, -0.15726542,  0.10663216,
        0.01626732, -0.07271046,  0.01734689, -0.07086322,  0.16381745,
        0.14920668, -0.14363301, -0.09353517,  0.06189087, -0.1551321 ,
       -0.01406012,  0.07499465, -0.08156656, -0.26478568, -0.29156995,
        0.09120265,  0.44834954,  0.19342156, -0.21763594, -0.00793736,
       -0.07441463, -0.08307736,  0.05755723,  0.04034131, -0.14868076,
       -0.06941402, -0.10071489,  0.05415241,  0.28371254,  0.00420167,
        0.00134942,  0.2846278 ,  0.02121732,  0.00925194,  0.03962364,
        0.06552636, -0.06095132, -0.08143448, -0.10792952,  0.01982656,
       -0.04558356, -0.08806515, -0.02397634,  0.11074951, -0.24787802,
        0.12550431, -0.033372  , -0.08832453,  0.03410845, -0.01334313,
       -0.17694934, -0.0411241 ,  0.14848432, -0.2737419 ,  0.10477202,
        0.13191062,  0.11237685,  0.13715413,  0.05446596,  0.07082986,
       -0.01219781,  0.00656867, -0.14484563, -0.01692682,  0.11385472,
       -0.0099913 , -0.02014174, -0.01784595]

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    print(unknown_face_encodings)

    face_found = False
    is_obama = False
    is_luisfer = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_obama = True
        match_results = face_recognition.compare_faces([luisfer_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_luisfer = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": is_obama,
        "is_picture_of_luisfer": is_luisfer

    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
