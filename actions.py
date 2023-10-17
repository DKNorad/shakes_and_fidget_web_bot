from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from detection import Detection
from conf import USERNAME, PASSWORD
from datetime import datetime
from random import choice
import time


class Action:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.actionBuilder = ActionBuilder(webdriver)
        self.actionChain = ActionChains(webdriver)
        self.cwd = Path.cwd()
        self.main_screenshot_png = str(self.cwd.joinpath('images/main_screen.png'))

    @staticmethod
    def get_time():
        # return current date and time
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def enter(self, n):
        # press ENTER key N number of times
        for i in range(n):
            self.actionChain.send_keys(Keys.RETURN)
            self.actionChain.perform()
            time.sleep(0.8)

    def click(self, coord):
        """
        left mouse click with half a second sleep time.
        """
        action = ActionBuilder(self.webdriver)
        print(f"x - {coord[0]}, y - {coord[1]}")
        action.pointer_action.move_to_location(coord[0], coord[1]).click()
        action.perform()
        self.actionBuilder.pointer_action.move_to_location(1, 1)
        self.actionBuilder.perform()
        time.sleep(0.5)

    def screenshot_and_match(self, image, threshold):
        """ create screenshot and match(detect) image in entire window """
        time.sleep(0.5)
        self.webdriver.save_screenshot(self.main_screenshot_png)
        return Detection(self.main_screenshot_png, image, threshold)

    def check_if_available(self, current_image, threshold=0.85):
        """ Check if we have a match. Sometimes we want to check without doing anything. """
        current_image = str(self.cwd.joinpath(f"images/{current_image}.jpg"))
        det = self.screenshot_and_match(current_image, threshold)
        return det.check_if_available()

    def do(self, current_image, custom_coordinates=None, previous_image=None, click=True, sleep_time=1.5,
           threshold=0.85, prev_threshold=0.85, retries=-1):
        """
        The main function where we use image comparison to make sure we are on the correct screen and click if needed.
        :param current_image: The image we will be checking on the screenshot.
        :param custom_coordinates: If we need to click somewhere, different from the center of the current_image.
        :param previous_image: If we don't match current_image, check the previous image/page again.
        :param click: Perform a click on the coordinates. (Boolean)
        :param sleep_time: Time between screenshots if we don't match the first time.
        :param threshold: For image match.
        :param prev_threshold: For previous image match.
        :param retries: Number of time it will try to perform the action until it considers that a logic error occurred.
        """
        current_image = str(self.cwd.joinpath(f"images/{current_image}.jpg"))
        det = self.screenshot_and_match(current_image, threshold)
        while retries > 0 or retries < 0:
            if det.check_if_available():
                break
            time.sleep(sleep_time)
            if previous_image is not None:
                det = self.screenshot_and_match(str(self.cwd.joinpath(f"images/{previous_image}.jpg")), prev_threshold)
                if det.check_if_available():
                    self.click(det.get_item_center())
            det = self.screenshot_and_match(current_image, threshold)
            retries -= 1

        if click:
            if det.check_if_available():
                if custom_coordinates is None:
                    self.click(det.get_item_center())
                else:
                    self.click(custom_coordinates)

    def login(self):
        """
        All actions required to completely log in to your account and tweak the settings so the script works.
        """
        self.do('login/title_screen', sleep_time=3, threshold=0.75)
        self.do('login/cookies_accept2')
        self.do('login/play_now', previous_image='login/cookies_accept', sleep_time=3)
        self.do('login/before_first_login_button', (830, 680), previous_image='login/play_now', sleep_time=3, threshold=0.9)
        self.do('login/login_credentials', click=False, sleep_time=2, previous_image='login/before_first_login_button')
        self.do('login/account_name', sleep_time=0.5)
        ActionChains(self.webdriver).send_keys(USERNAME).perform()
        self.do('login/password', sleep_time=0.5)
        ActionChains(self.webdriver).send_keys(PASSWORD).perform()
        self.do('login/stay_logged_in_false')
        self.do('login/stay_logged_in_true', previous_image='login/stay_logged_in_false')
        self.do('login/login_ready')
        self.do('login/character_selection', custom_coordinates=(900, 380))
        time.sleep(2.5)
        print(f'{self.get_time()}: Login was successful.')

        # Enable timers and other options.
        self.do('login/check_if_settings_screen', previous_image='login/settings', click=False)
        self.do('login/show_timer_true', previous_image='login/show_timer_false', click=False)
        self.do('login/tube_off_true', previous_image='login/tube_off_false', click=False)

        print(f'{self.get_time()}: Settings changes were successful.')
        return True

    def abawuwu(self):
        """
        Collect the daily bonus and do the free spin of the wheel of the day.
        """
        # open the Daily bonus tab and grab the daily bonus
        self.do('abawuwu/daily_bonus_check', previous_image='abawuwu/abawuwu', click=False)
        if self.check_if_available('abawuwu/claim_true', threshold=0.97):
            self.do('abawuwu/claim_true')
            print(f'{self.get_time()}: The daily bonus has been collected.')
        else:
            print(f'{self.get_time()}: The daily bonus has already been collected today.')

        # open the Dr. Abawuwu tab and spin the wheel
        self.do('abawuwu/abawuwu_check', previous_image='abawuwu/abawuwu', click=False)
        if self.check_if_available('abawuwu/dr_spin_true', threshold=0.95):
            self.do('abawuwu/dr_spin_true')
            print(f'{self.get_time()}: Dr. Abawuwu wheel has been spun.')
        else:
            print(f'{self.get_time()}: The wheel has already been spun today.')

    def arena(self):
        """
        Taking care of the arena attacks.
        TODO: Try to gather details about the opponents and simulate battles before attacking.
        TODO: Ex, simulate 1000 battles per opponent and attack the one with the greatest chance to win against.

        TODO: Add a counter for won/lost fights.
        """
        opponents = [(575, 300), (790, 300), (1000, 300)]
        if self.check_if_available('arena/arena', threshold=0.93):
            self.do('arena/arena', threshold=0.93)
            self.do('arena/arena_boxes', previous_image='arena/arena', threshold=0.93, prev_threshold=0.93)
            self.click(choice(opponents))
            self.enter(3)
            print(f'{self.get_time()}: A player has been attacked in the Arena.')
        else:
            print(f'{self.get_time()}: Arena is currently on cooldown.')

    def pets(self):
        """
        Check if pets are not under cooldown and attack all pets in order from "Shadow" to "Water".
        """
        if not self.check_if_available('pets/pets_cooldown', threshold=0.91):
            while True:
                self.do('pets/pets', threshold=0.94)
                if self.check_if_available('pets/check_if_pet_screen'):
                    break

            if self.check_if_available('pets/pets_done', threshold=0.94):
                print(f'{self.get_time()}: All pets have been attacked.')
                return

            pets = ['pet_shadow', 'pet_light', 'pet_earth', 'pet_fire', 'pet_water']
            for pet in pets:
                if self.check_if_available(f'pets/{pet}', threshold=0.9):
                    self.do(f'pets/{pet}', threshold=0.9)
                    self.enter(3)
                    print(f'{self.get_time()}: {pet.split("_")[1].upper()} pet has been attacked.')
                    break
                else:
                    continue
        else:
            print(f'{self.get_time()}: Pets are under cooldown at the moment.')

    def tavern(self):
        """
        Go on a random quest in the tavern.

        # TODO implement image to text processing to choose quest based on gold, exp or duration.
        """

        if self.check_if_available('tavern/tavern', threshold=0.89):
            self.do('tavern/tavern_keeper', previous_image='tavern/tavern', click=False)
            # Start the first quest
            self.enter(1)
            if self.check_if_available('tavern/drink_beer'):
                self.do('tavern/drink_beer')
                if self.check_if_available('tavern/can_drink_true', threshold=0.95):
                    self.do('tavern/can_drink_true')
                    print(f'{self.get_time()}: Adventure points exhausted. Drank the free beer.')
                    self.tavern()
                    return
                else:
                    print(f'{self.get_time()}: No more adventure points in the tavern.')
            else:
                self.enter(1)
                print(f'{self.get_time()}: Mission started.')

        else:
            print(f'{self.get_time()}: You are currently on a mission.')

    # TODO implement a way to choose a specific location in the Dungeon to be entered
    def dungeons(self):
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