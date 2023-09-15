import cv2 as cv
from pathlib import Path


class Detection:
    def __init__(self, screenshot, image, threshold=0.85):
        self.cwd = Path.cwd()
        self.threshold = threshold
        self.main_screenshot_jpg = str(self.cwd.joinpath('images/main_screen.jpg'))
        self.debug_image = image
        cv.imwrite(self.main_screenshot_jpg, cv.imread(screenshot, cv.IMREAD_UNCHANGED), [int(cv.IMWRITE_JPEG_QUALITY), 100])
        self.main_screen = cv.imread(self.main_screenshot_jpg, cv.IMREAD_UNCHANGED)
        self.image_to_search = cv.imread(image, cv.IMREAD_UNCHANGED)
        self.image_found = cv.matchTemplate(self.main_screen, self.image_to_search, cv.TM_CCORR_NORMED)

    def check_if_available(self):
        # check if image match is above the threshold
        max_val = cv.minMaxLoc(self.image_found)[1]
        print(self.debug_image)
        print(max_val)
        print(self.threshold)
        if max_val >= self.threshold:
            return True
        return False

    def get_item_center(self):
        # https://stackoverflow.com/questions/61687427/python-opencv-append-matches-center-x-y-coordinates-in-tuples
        # get image size and position
        image_h, image_w = self.image_to_search.shape[:2]
        max_loc = cv.minMaxLoc(self.image_found)[3]
        # top_left = max_loc
        # bottom_right = (top_left[0] + image_w, top_left[1] + image_h)

        center = (max_loc[0] + image_w//2, max_loc[1] + image_h//2)
        return center
