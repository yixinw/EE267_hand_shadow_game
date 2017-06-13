import cv2
import numpy as np
import IPython

'''
Takes in RGB and depth image as numpy arrays, and outputs
hand image as numpy array.
'''
def detect_hand(colour, depth):
    height, width, n_channels = colour.shape
    hand_image = np.zeros((height, width, n_channels))
    # Depth thresholding for hand detection.
    hand_region = np.where(
            np.all(
                np.stack([depth >= 100, depth <= 400], axis=2),
                axis=2)
            )
    # print hand_region
    hand_image[hand_region] = colour[hand_region]
    return hand_image

'''
Input: hand_shadow is ground truth shadow, 480x600 binary (255 or 0). hand_image is the user hand state, 480x600x3 BGR channels.
Output: a boolean, True if they look the same, else False.
'''
def compare_hand_shadow(hand_image, hand_shadow, threshold = 0.85):
    height, width = hand_shadow.shape
    hand_image_binary = np.sum(hand_image, 2)
    hand_image_binary = (hand_image_binary > 0).astype(float)
    hand_shadow_binary = (hand_shadow == 0).astype(float)
    diff_image = hand_image_binary - hand_shadow_binary
    # add baseline for blind guess
    baseline = np.sum(hand_shadow_binary) / (height * width)
    lowerbound = max(baseline, 1-baseline)
    upperbound = threshold
    diff = np.sum(diff_image != 0)
    raw_score = 1 - float(diff) / (height * width)
    # rescale the raw_score to new scale
    score = (raw_score - lowerbound) / (upperbound - lowerbound)
    print float(diff) / (height * width)
    score = int(score * 100)
    return diff < (height * width * (1-threshold)), score

def detect_hand_sample(colour, depth):
    height, width, n_channels = colour.shape
    hand_image = np.zeros((height, width, n_channels))

    # Depth thresholding for hand detection.
    hsv = cv2.cvtColor(colour, cv2.COLOR_BGR2HSV)
    hand_region = np.where(
            np.all(
                np.stack([depth >= 150, depth <= 400], axis=2),
                axis=2)
            )
    # print hand_region
    samples = hsv[hand_region][:,0]
    samples_mean = samples.mean()
    samples_std = samples.std()
    lower_bound = np.array([samples_mean - 2*samples_std, 50, 50])
    upper_bound = np.array([samples_mean + 2*samples_std, 255, 255])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    blurred_mask = cv2.medianBlur(mask, 9)
    blurred_mask = blurred_mask > 0

    extended_mask = np.zeros((height, width))
    extended_mask[hand_region] = 1
    new_extended_mask = extended_mask.copy()
    for _ in xrange(5):
        new_extended_mask[:, :width-1] += extended_mask[:, 1:]
        new_extended_mask[:, 1:] += extended_mask[:, :width-1]
        new_extended_mask[:height-1] += extended_mask[1:]
        new_extended_mask[1:] += extended_mask[:height-1]
        extended_mask = new_extended_mask.copy()
    blurred_mask *= (new_extended_mask > 0)

    hand_image[blurred_mask] = colour[blurred_mask]

    return hand_image
