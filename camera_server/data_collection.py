import cv2
import numpy as np
import IPython
import os

def binarize_hand_shadow(img):
    _,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    return thresh

def smooth_hand_shadow(img):
    blur = cv2.GaussianBlur(img,(3,3),0)
    return blur

def edge_detection(img, sigma=0.33):
    v = np.median(img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(img, upper, lower)
    return edges

def make_thick_edges(edges):
    new_edges = np.zeros(edges.shape)
    height, width = edges.shape
    edge_line = np.argwhere(edges==255)
    for i,j in edge_line:
        new_edges[i][j] = 255
        if i-1 >= 0:
            new_edges[i-1][j] = 255
        if i+1 < height:
            new_edges[i+1][j] = 255
        if j-1 >= 0:
            new_edges[i][j-1] = 255
        if j+1 < width:
            new_edges[i][j+1] = 255
    return new_edges

def collect_images(dir_path, filename_list):
    hand_shadow_list = []
    edges_list = []
    for filename in filename_list:
        binary_shadow_filename = os.path.join(dir_path,
                filename+'_binary.png')
        edges_filename = os.path.join(dir_path,
                filename+'_edges.png')
        binary_shadow = cv2.imread(binary_shadow_filename,
                cv2.IMREAD_GRAYSCALE)
        edges = cv2.imread(edges_filename,
                cv2.IMREAD_GRAYSCALE)

        hand_shadow_list.append(binary_shadow)
        edges_list.append(edges)

    return hand_shadow_list, edges_list

def main():
    # Some constants.
    in_hand_shadow_filename = './spock.png'
    out_shadow_filename = 'spock_binary.png'
    out_edges_filename = 'spock_edges.png'

    # Read image.
    hand_shadow = cv2.imread(in_hand_shadow_filename,
            cv2.IMREAD_GRAYSCALE)
    assert hand_shadow.shape == (480, 640)
    cv2.imshow("Original image", hand_shadow)
    cv2.waitKey(0)

    # Convert to binary image.
    hand_shadow = smooth_hand_shadow(hand_shadow)
    hand_shadow = binarize_hand_shadow(hand_shadow)
    cv2.imshow("Hand Shadow", hand_shadow)
    cv2.waitKey(0)
    cv2.imwrite(out_shadow_filename, hand_shadow)

    # Detect contour.
    edges = edge_detection(cv2.resize(hand_shadow, (80,60)))
    edges = make_thick_edges(edges)
    # To add the edges to an image, use the following line.
    # img[edges != 0] = \
    #        np.minimum(img[edges != 0] + np.array([255,0,0]),
    #        255)
    cv2.imshow("Edges", edges)
    cv2.waitKey(0)
    cv2.imwrite(out_edges_filename, edges)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

