from src.classes import *

def pixels_to_peaks(unet_output):
    unet_output = unet_output.squeeze()
    for dye in range(unet_output.shape[1]):
        current = unet_output[:,dye]
        for index in range(len(current)):
            if current[index] == current[index+1]:
                pass
    pass

def peak_oriented_loss():
    pass

def peak_metric():
    pass