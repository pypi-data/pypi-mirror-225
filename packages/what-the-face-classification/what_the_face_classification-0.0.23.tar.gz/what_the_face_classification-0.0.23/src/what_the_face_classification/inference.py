import numpy as np
import torch as th
import torchvision.transforms as transforms
import torch.nn.functional as F
from . import model
from PIL import Image, ImageOps
import cv2
import importlib.resources as pkg_resources
from pkg_resources import resource_stream, resource_filename

inp_file = resource_filename(__name__, 'active_model.pth')
xml_file = resource_filename(__name__, 'haarcascade_frontalface_default.xml')

class Image_classifier:
    def __init__(self, filter_layers = 3,
                  io_list = [[1, 28], [28, 56], [56, 112]],
                    kernals = [3, 3, 3],
                      padding = [0, 0, 0],
                        linear_filter_input = 305):


        self.filter_layers = filter_layers
        self.io_list = io_list
        self.kernals = kernals
        self.padding = padding
        self.linear_filter_input = linear_filter_input
        self.latent_dim = self.calc_latent_dim()
        self.classes = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
        self.transform = transforms.Compose([transforms.Resize(48),
                            transforms.CenterCrop(48),
                            transforms.Grayscale(),
                            transforms.ToTensor()
                            ])
        
        self.device = th.device("cpu")
        self.net = model.SimpleConvolutionalNetwork(self.filter_layers,
                                                     self.io_list, self.kernals,
                                                       self.padding, self.linear_filter_input,
                                                         self.latent_dim)
        
        self.net.to(self.device)
        self.net.load_state_dict(th.load(inp_file, map_location=self.device))

    def calc_latent_dim(self):
        if self.filter_layers >= 1:
            output_dim = (48 + (2 * self.padding[0]) - self.kernals[0]) + 1
            output_dim = output_dim // 2
        if self.filter_layers >= 2:
            output_dim = (output_dim + (2 * self.padding[1]) - self.kernals[1]) + 1
            output_dim = output_dim // 2
        if self.filter_layers >= 3:
            output_dim = (output_dim + (2 * self.padding[2]) - self.kernals[2]) + 1
            output_dim = output_dim // 2

        return pow(output_dim, 2) * self.io_list[-1][1]

    def face_crop(self, image):
        face_cascade = cv2.CascadeClassifier(xml_file)
        faces = face_cascade.detectMultiScale(np.array(image), 1.3, 5)
        if len(faces) > 0:
            x,y,w,h = faces[0]
            image = image.crop((x,y,x+w,y+h))
            return image, True
        else:
            return image, False

    
    def predict(self, image: Image) -> tuple[str, str]:
        #PIL image
        face_not_detected = False
        try:
            image = ImageOps.exif_transpose(image)
        except:
            pass
        
        image, face_detected = self.face_crop(image)        
        
        img_norm = self.transform(image).float()
        img_norm.unsqueeze(0)
        image = img_norm.to(self.device)
        self.net.eval()

        with th.no_grad():
            output = self.net(image)
            prob = F.softmax(output, 1)
            prob = prob.cpu()
            top_p, top_class = prob.topk(1, 1)
            label = self.classes[top_class]
            

            if top_p.numpy()[0][0] < .60 and not face_detected:
                return ("no face detected", "0")
            

            
            return (label, str(top_p.numpy()[0][0]))      

