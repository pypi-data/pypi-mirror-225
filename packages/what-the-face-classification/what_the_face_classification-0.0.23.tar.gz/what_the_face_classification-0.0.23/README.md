This package was created as a part of Talentsprint and Techwise program by James Rodgers of team "What The Face". It uses a pytorch CNN network trained on FER2013 and CK+ images to classify an image passed into it. 

Initialize class and pass a jpg PIL image to the predict() method.

classes:
    Image_classifier()
        returns self

functions:
    predict(image)
        returns [classified_name: str, probability: double]

Example:

from PIL import Image
from what_the_face_classification.inference import Image_classifier

classifier = Image_classifier()
image = Image.open(test.jpg)

prediction = classifier(image)

print(prediction)


<!-- haarcascade_frontalface_default.xml
    Stump-based 24x24 discrete(?) adaboost frontal face detector.
    Created by Rainer Lienhart.

////////////////////////////////////////////////////////////////////////////////////////

  IMPORTANT: READ BEFORE DOWNLOADING, COPYING, INSTALLING OR USING.

  By downloading, copying, installing or using the software you agree to this license.
  If you do not agree to this license, do not download, install,
  copy or use the software.


                        Intel License Agreement
                For Open Source Computer Vision Library

 Copyright (C) 2000, Intel Corporation, all rights reserved.
 Third party copyrights are property of their respective owners.-->
