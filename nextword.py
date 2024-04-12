import cv2
import easyocr
from dataclasses import dataclass

reader = easyocr.Reader(['en'])

@dataclass
class BoundingBox:
    h : int
    w : int
    x : int
    y : int

detected_words_list:list[BoundingBox] = []


min_height_thresh = 5
min_width_thresh = 5
whitespace_width = 25

def check_if_detected(x, y, w, h):
    for bb in detected_words_list:
        if (bb.x <= x <= (bb.x+bb.w) and w <= bb.w) or (bb.y <= y <= (bb.y+bb.h) and h <= bb.y):
            return True
    return False

def detect_next_word_helper(page_image, detected_box: BoundingBox) -> BoundingBox:
    gray_image = cv2.cvtColor(page_image, cv2.COLOR_BGR2GRAY)

    blurred_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    edges = cv2.Canny(blurred_image, 30, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    lst = []
    min_x = page_image.shape[1]

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # if h > page_image.shape[0]//9 or w > page_image.shape[1]//8  or h < min_height_thresh or w < min_width_thresh:
        #     continue
        lst.append([x, y, w, h])
    lst = sorted(lst, key=lambda l: l[0])

    merged_lst = [lst[0]]
    for i in range(1, len(lst)):
        x, y, w, h = lst[i]  # new to check
        xf, yf, wf, hf = merged_lst[-1] # old
        if x <= xf+wf+whitespace_width:
            merged_lst[-1] = [min(xf, x), min(y, yf), max(xf+wf, x+w) - min(xf, x),
                             max(hf+yf, h+y) - min(yf, y)]
        else:
            merged_lst.append([x, y, w, h])
    
    for x, y, w, h in merged_lst:
        if check_if_detected(x, y, w, h):
            continue
        result = reader.readtext(page_image[y:y+h, x:x+w].copy())
        if not result:
            continue
        # Print the result
        for detection in result:
            detected_words_list.append(BoundingBox(
            h = h,
            w = w,
            x = x,
            y = y
        ))
    
def detect_next_word(page_image):
    detected_box = None
    if detected_words_list:
        detected_box = max(detected_words_list, key=lambda box:box.x)

    if detected_box is None:
        new_box = detect_next_word_helper(page_image, detected_box)
    else:
        page_image_cropped = page_image
        new_box = detect_next_word_helper(page_image_cropped, detected_box)

    if new_box is not None:
        detected_words_list.append(new_box)

def draw_bounding_boxes(page_image):
    for bb in detected_words_list:
        cv2.rectangle(page_image, (bb.x, bb.y), (bb.x + bb.w, bb.y + bb.h), (0, 0, 255), 3)
    

def main():
    writing_image = "writing.jpeg"
    while True:
        original_page_image = cv2.imread(writing_image)
        page_image = original_page_image.copy()
        detect_next_word(page_image)
        
        draw_bounding_boxes(page_image)
        cv2.imshow("", page_image)
        q = cv2.waitKey(0)
        if q == ord("q"):
            cv2.destroyAllWindows()
            break
        cv2.destroyAllWindows()

main()
