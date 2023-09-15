from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from detection import Detection
from conf import USERNAME, PASSWORD
from datetime import datetime
from random import choice
import time


class Action:

    # properties
    main_x = 0
    main_y = 0
    x = 0
    y = 0

    def __init__(self, webdriver):
        self.webdriver = webdriver

    @staticmethod
    def get_time():
        # return current date and time
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    @staticmethod
    def enter(n):
        # press ENTER key N number of times
        for i in range(n):
            send_keys("{ENTER}")
            time.sleep(0.8)

    def click(self, cord):
        """
        Adding 85 to the y coordinate to compensate the firefox browser tabs and address bar at the top
        left mouse click with 4ms sleep timer
        """
        action = ActionBuilder(self.webdriver)
        print(f"x - {cord[0]}, y - {cord[1]}")
        action.pointer_action.move_to_location(cord[0], cord[1]).click()
        action.perform()
        time.sleep(0.4)

    def screenshot_and_match(self, image, threshold=0.90):
        # create screenshot and match(detect) image in entire window
        time.sleep(0.5)
        self.webdriver.save_screenshot(r'images\main_screen.png')
        return Detection(r'images\main_screen.png', fr'images\{image}.jpg', threshold)

    def do(self, current_image, custom_coordinates=None, previous_image=None, click=True, sleep_time=1.0):
        det = self.screenshot_and_match(current_image)
        while not det.check_if_available():
            time.sleep(sleep_time)
            if previous_image is not None:
                det = self.screenshot_and_match(previous_image)
                if det.check_if_available():
                    self.click(det.get_item_center())
            det = self.screenshot_and_match(current_image)
        if click:
            if det.check_if_available():
                if custom_coordinates is None:
                    self.click(det.get_item_center())
                else:
                    self.click(custom_coordinates)

    def login(self):
        self.do(r'login\title_screen', sleep_time=3)
        self.do(r'login\cookies_accept')
        self.do(r'login\play_now', previous_image=r'login\cookies_accept')
        self.do(r'login\before_first_login_button', (830, 680), previous_image=r'login\play_now')
        self.do(r'login\login_credentials', click=False)
        self.do(r'login\account_name', sleep_time=0.5)
        ActionChains(self.webdriver).send_keys(USERNAME).perform()
        self.do(r'login\password', sleep_time=0.5)
        ActionChains(self.webdriver).send_keys(PASSWORD).perform()
        self.do(r'login\stay_logged_in_false')
        self.do(r'login\stay_logged_in_true', previous_image=r'login\stay_logged_in_false')
        self.do(r'login\login_ready')
        self.do(r'login\character_selection', custom_coordinates=(780, 380))

    def abawuwu(self):
        # open the Dr. Abawuwu tab
        main_x, main_y = 150, 660
        self.click(main_x, main_y)

        # grab the daily bonus
        det = self.screenshot_and_match(r'abawuwu\daily_login')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'abawuwu\daily_login')
        if det.check_if_available():
            x, y = det.get_item_center()
            self.click(x, y)

        # spin the wheel
        det = self.screenshot_and_match(r'abawuwu\abawuwu_check')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'abawuwu\abawuwu_check')

        det = self.screenshot_and_match(r'abawuwu\dr_spin')
        if det.check_if_available():
            x, y = det.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: Dr. Abawuwu wheel has been spun')
        else:
            return print(f'{self.get_time()}: The wheel has already been spun today.')

    def arena(self):
        opponents = [(575, 300), (790, 300), (1000, 300)]
        # check if arena is available
        det = self.screenshot_and_match(r'arena\arena', 0.93)
        # get main center coordinates
        main_x, main_y = det.get_item_center()

        # check if available
        if det.check_if_available():
            self.click(main_x, main_y)
        else:
            return print(f'{self.get_time()}: Arena is currently on cooldown.')

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'arena\arena_boxes')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'arena\arena_boxes')

        # attack a random player
        x, y = choice(opponents)
        self.click(x, y)
        self.enter(3)
        print(f'{self.get_time()}: A player has been attacked in the Arena.')

    def pets(self):
        # check if pets are available
        det = self.screenshot_and_match(r'pets\pets_cooldown', 0.94)
        if det.check_if_available():
            return print(f'{self.get_time()}: Pets are under cooldown at the moment.')

        # set center coordinates and click
        main_x, main_y = 150, 365
        self.click(main_x, main_y)

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'pets\check_if_pet_screen')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'pets\check_if_pet_screen')

        det = self.screenshot_and_match(r'pets\pets_done', 0.97)
        if det.check_if_available():
            return print(f'{self.get_time()}: All pets have been attacked.')
        else:
            # iterate over all 5 pets
            pets = ['pet_shadow', 'pet_light', 'pet_earth', 'pet_fire', 'pet_water']
            count = 0
            for pet in pets:
                det = self.screenshot_and_match(r'pets\pets_cooldown', 0.94)
                if det.check_if_available():
                    return print(f'{self.get_time()}: Pets are under cooldown at the moment.')

                det = Detection('images/main_screen.jpg', f'images/pets/{pet}.jpg', 0.95)
                if not det.check_if_available():
                    count += 1
                    if count == 5:
                        return print(f'{self.get_time()}: All pets have been attacked.')
                    continue
                x, y = det.get_item_center()
                self.click(x, y)
                self.enter(3)
                print(f'{self.get_time()}: A pet has been attacked.')
                break

    # TODO implement image to text processing to choose quest based on gold, exp or duration
    def tavern(self):
        # check if tavern is free
        det = self.screenshot_and_match(r'tavern\tavern', 0.92)
        if not det.check_if_available():
            return print(f'{self.get_time()}: You are currently on a mission.')

        # get center coordinates and click
        main_x, main_y = det.get_item_center()
        self.click(main_x, main_y)

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'tavern\tavern_guard')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'tavern\tavern_guard')

        # start the first quest
        self.enter(1)
        det = self.screenshot_and_match(r'tavern\drink_beer', 0.9)
        if det.check_if_available():
            print(f'{self.get_time()}: No more adventure points in the tavern.')
        else:
            self.enter(1)
            print(f'{self.get_time()}: Mission started.')

    # TODO implement a way to choose a specific location in the Dungeon to be entered
    def dungeons(self):
        dungeons = {'The Twister': (370, 180), 'Hemorridor': (600, 200), 'Mount Olympus': (815, 115),
                    'Nordic Gods': (1100, 105), 'Continues Loop of Idols': (715, 280), 'The Tower': (370, 180),
                    'Time-honored School of Magic': (920, 200), 'Easteros': (1225, 180),
                    'Black Skull Fortress': (515, 360), 'Circus of Terror': (850, 345), 'Hell': (1000, 365),
                    'The 13th Floor': (1120, 270), 'The Pyramids of Madness': (345, 430),
                    'The Emerald Scale Altar': (1140, 425), 'Desecrated Catacombs': (410, 680),
                    'The Frost Blood Temple': (550, 540), 'The Mines of Gloria': (620, 630),
                    'The Magma Stream': (780, 515), 'The Ruins of Gnark': (910, 670), 'The Toxic Tree': (1030, 520),
                    'The Cutthroat Grotto': (1125, 620), 'Demon\'s Portal': (715, 280)}
        # check if dungeons are available
        det = self.screenshot_and_match(r'dungeons\dungeons', 0.92)
        if not det.check_if_available():
            return print(f'{self.get_time()}: The dungeons are currently on a cooldown.')

        # get center coordinates and click
        main_x, main_y = det.get_item_center()
        self.click(main_x, main_y)

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'dungeons\dungeons_twister')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'dungeons\dungeons_twister')

        # enter "The Twister"
        x, y = det.get_item_center()
        self.click(x, y)
        self.enter(3)

    def underground(self):
        # create a screenshot until we have the correct tab opened
        det = self.screenshot_and_match(r'underground\lure_hero', 0.95)
        det2 = self.screenshot_and_match(r'underground\lure_hero_done', 0.95)
        while not (det2.check_if_available() or det.check_if_available()):
            self.click(140, 450)
            det = self.screenshot_and_match(r'underground\lure_hero', 0.95)
            det2 = self.screenshot_and_match(r'underground\lure_hero_done', 0.95)

        # collect souls
        self.click(1080, 280)

        det_cancel = self.screenshot_and_match(r'underground\cancel_construction')
        det_close = self.screenshot_and_match(r'underground\close')
        if det_cancel.check_if_available():  # confirm that the Soul Extractor is not under construction
            x, y = det_cancel.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The Soul Extractor is under construction.')
        elif det_close.check_if_available():  # confirm that the storage is not full
            x, y = det_close.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The Soul storage is full.')
        else:
            print(f'{self.get_time()}: Underground souls collected.')

        # collect gold
        self.click(350, 380)

        det_cancel = self.screenshot_and_match(r'underground\cancel_construction')
        det_close = self.screenshot_and_match(r'underground\close')
        if det_cancel.check_if_available():  # confirm that the Gold Pit is not under construction
            x, y = det_cancel.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The Gold Pit is under construction.')
        elif det_close.check_if_available():  # confirm that the gold hasn't been collected already
            x, y = det_close.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The gold has already been collected.')
        else:
            print(f'{self.get_time()}: Underground gold collected.')

        # lure heroes underground
        det_lure = self.screenshot_and_match(r'underground\lure_hero', 0.95)
        x, y = det_lure.get_item_center()
        self.click(x, y)
        det_attack = self.screenshot_and_match(r'underground\attack_hero', 0.95)
        while True:
            if not det_attack.check_if_available():
                print(f'{self.get_time()}: Maximum heroes lured for the day.')
                break
            self.enter(3)
            print(f'{self.get_time()}: A hero has been lured in the underground.')

    def fortress(self):
        # create a screenshot until we have the correct tab opened
        self.click(140, 450)
        det = self.screenshot_and_match(r'fortress\attack', 0.94)
        while not det.check_if_available():
            self.click(140, 450)
            det = self.screenshot_and_match(r'fortress\attack', 0.94)

        # confirm that the Academy is not under construction and collect experience
        self.click(450, 200)
        det = self.screenshot_and_match(r'fortress\cancel_construction')
        if det.check_if_available():
            x, y = det.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The Academy is under construction.')
        else:
            print(f'{self.get_time()}: Experience from the Academy has been collected.')

        # collect stone
        self.click(450, 520)
        det_cancel = self.screenshot_and_match(r'fortress\cancel_construction')
        det_close = self.screenshot_and_match(r'fortress\close', 0.95)
        if det_cancel.check_if_available():  # confirm that the Quarry is not under construction
            x, y = det_cancel.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The Quarry is under construction.')
        elif det_close.check_if_available():  # confirm that the stone storage is not full
            x, y = det_close.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The Stone storage is full.')
        else:
            print(f'{self.get_time()}: Stone from the Quarry has been collected.')

        # collect wood
        self.click(600, 600)
        det_cancel = self.screenshot_and_match(r'fortress\cancel_construction')
        det_close = self.screenshot_and_match(r'fortress\close', 0.95)
        if det_cancel.check_if_available():  # confirm that the Woodcutter's Hut is not under construction
            x, y = det_cancel.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The Woodcutter\'s Hut is under construction.')
        elif det_close.check_if_available():  # confirm that the wood storage is not full
            x, y = det_close.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: The Wood storage is full.')
        else:
            print(f'{self.get_time()}: Wood from the Woodcutter\'s Hut has been collected.')