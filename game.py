import mss
import cv2
import pyscreenshot as ImageGrab
import numpy as np
import pytesseract as ocr


#pytesseract config
number_filter_config = '-c tessedit_char_whitelist=0123456789'

demo_screenshot = np.array(ImageGrab.grab())
h, w, _ = demo_screenshot.shape
rescaled_ss = cv2.resize(demo_screenshot, (1280, 800))
scale_factor = (w/1280, h / 800, w / 1280, h / 800)
threshold = 0.8
game_region =  cv2.selectROI(rescaled_ss)
game_ss = rescaled_ss[game_region[1]:game_region[1]+game_region[3], game_region[0]:game_region[0]+game_region[2]]
print("Select Minimap")
mini_map_roi = cv2.selectROI(game_ss)

print("Select Air Resistance Factor")
air_resistance_roi = cv2.selectROI(game_ss)

print("Select Angle Indicator")
angle_indicator_roi = cv2.selectROI(game_ss)






# scale back to normal res
mini_map_roi = [int(mini_map_roi[i] * scale_factor[i]) for i in range(len(mini_map_roi))]
game_region = [int(game_region[i] * scale_factor[i]) for i in range(len(game_region))]
angle_indicator_roi = [int(angle_indicator_roi[i] * scale_factor[i]) for i in range(len(angle_indicator_roi))]
air_resistance_roi  = [int(air_resistance_roi[i] * scale_factor[i]) for i in range(len(air_resistance_roi))]




while True:
    ss = np.array(ImageGrab.grab())
    game_ss = ss[game_region[1]:game_region[1]+game_region[3], game_region[0]:game_region[0]+game_region[2]]
    mini_map = game_ss[mini_map_roi[1]:mini_map_roi[1]+mini_map_roi[3], mini_map_roi[0]:mini_map_roi[0]+mini_map_roi[2]]
    air_resistance_img = cv2.cvtColor(game_ss[air_resistance_roi[1]:air_resistance_roi[1]+air_resistance_roi[3], air_resistance_roi[0]:air_resistance_roi[0]+air_resistance_roi[2]], cv2.COLOR_BGR2GRAY)
    angle_indicator_img = cv2.cvtColor(game_ss[angle_indicator_roi[1]:angle_indicator_roi[1]+angle_indicator_roi[3], angle_indicator_roi[0]:angle_indicator_roi[0]+angle_indicator_roi[2]], cv2.COLOR_BGR2GRAY)
    print("Wind: "+ocr.image_to_string(air_resistance_img, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789'))
    print("Angle: "+ocr.image_to_string(angle_indicator_img, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789'))
    cv2.imshow("aight", mini_map)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break