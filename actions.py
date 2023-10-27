from selenium.webdriver import ActionChains
from selenium.webdriver import Firefox
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from detection import Detection
from conf import USERNAME, PASSWORD
from datetime import datetime
from random import choice
import time
from typing import Tuple


class Action:
    def __init__(self, webdriver: Firefox):
        self.webdriver = webdriver
        self.actionBuilder = ActionBuilder(webdriver)
        self.actionChain = ActionChains(webdriver)
        self.cwd = Path.cwd()
        self.main_screenshot_png = str(self.cwd.joinpath('images/main_screen.png'))

    @staticmethod
    def get_time() -> str:
        """
        :return: Current date and time. Ex: 27-10-2023 00:21:24
        """
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def press_key(self, key, n: int = 1) -> None:
        """
        press the given key N number of times
        """
        for i in range(n):
            self.actionChain.send_keys(key)
            self.actionChain.perform()
            time.sleep(0.8)

    def click(self, coord: Tuple[int, int]) -> None:
        """
        left mouse click with half a second sleep time.
        """
        action = ActionBuilder(self.webdriver)
        print(f"x - {coord[0]}, y - {coord[1]}")
        action.pointer_action.move_to_location(coord[0], coord[1]).click()
        action.perform()
        self.actionBuilder.pointer_action.move_to_location(1, 1)
        self.actionBuilder.perform()
        time.sleep(1)

    def screenshot_and_match(self, image: str, threshold: float) -> Detection:
        """ create screenshot and match(detect) image in entire window """
        time.sleep(0.5)
        self.webdriver.save_screenshot(self.main_screenshot_png)
        return Detection(self.main_screenshot_png, image, threshold)

    def check_if_available(self, current_image: str, threshold: float = 0.85) -> bool:
        """ Check if we have a match. Sometimes we want to check without doing anything. """
        current_image = str(self.cwd.joinpath(f"images/{current_image}.jpg"))
        det = self.screenshot_and_match(current_image, threshold)
        return det.check_if_available()

    def do(self, current_image: str, custom_coordinates: Tuple[int, int] = None, previous_image: str = None,
           click: bool = True, sleep_time: float = 1.5, threshold: float = 0.85, prev_threshold: float = 0.85,
           retries: int = -1) -> None:
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

    def login(self) -> bool:
        """
        All actions required to completely log in to your account and tweak the settings so the script works.
        """
        self.do('login/title_screen', sleep_time=3, threshold=0.75)
        if self.check_if_available('login/cookies_accept2', threshold=0.9):
            self.do('login/cookies_accept2')
            self.do('login/play_now', previous_image='login/cookies_accept', sleep_time=3)
            self.do('login/before_first_login_button', (830, 680), previous_image='login/play_now', sleep_time=3,
                    threshold=0.9)
            self.do('login/login_credentials', click=False, sleep_time=2, previous_image='login/before_first_login_button')
            self.do('login/account_name', sleep_time=0.5)
            ActionChains(self.webdriver).send_keys(USERNAME).perform()
            self.do('login/password', sleep_time=0.5)
            ActionChains(self.webdriver).send_keys(PASSWORD).perform()
            self.do('login/stay_logged_in_false')
            self.do('login/stay_logged_in_true', previous_image='login/stay_logged_in_false')
            self.do('login/login_ready')
            self.do('login/character_selection', custom_coordinates=(900, 380))

            # Enable timers and other options.
            self.do('login/check_if_settings_screen', previous_image='login/settings', click=False)
            self.do('login/show_timer_true', previous_image='login/show_timer_false', click=False)
            self.do('login/tube_off_true', previous_image='login/tube_off_false', click=False)

            print(f'{self.get_time()}: Settings changes were successful.')
        else:
            self.do('login/play_now', previous_image='login/cookies_accept', sleep_time=3)
            self.do('login/character_selection', custom_coordinates=(900, 380))
        time.sleep(2.5)

        if self.check_if_available('login/successful_login', threshold=0.93):
            print(f'{self.get_time()}: Login was successful.')
            return True
        else:
            return False

    def abawuwu(self) -> None:
        """
        Collect the daily bonus and do the free spin of the wheel of the day.
        """
        # open the Daily bonus tab and grab the daily bonus
        self.do('abawuwu/daily_bonus_check', previous_image='abawuwu/abawuwu', click=False, sleep_time=3)
        if self.check_if_available('abawuwu/claim_true', threshold=0.945):
            self.do('abawuwu/claim_true')
            print(f'{self.get_time()}: The daily bonus has been collected.')
        else:
            print(f'{self.get_time()}: The daily bonus has already been collected today.')

        # open the Dr. Abawuwu tab and spin the wheel
        self.do('abawuwu/abawuwu_check', previous_image='abawuwu/abawuwu', click=False, sleep_time=3)
        if self.check_if_available('abawuwu/dr_spin_true', threshold=0.933):
            self.do('abawuwu/dr_spin_true')
            if self.check_if_available('abawuwu/backpack_full', threshold=0.94):
                print(f'{self.get_time()}: Cannot spin the Dr. Abawuwu wheel, backpack is full.')
            else:
                print(f'{self.get_time()}: Dr. Abawuwu wheel has been spun.')
        else:
            print(f'{self.get_time()}: The wheel has already been spun today.')

    def arena(self) -> None:
        """
        Taking care of the arena attacks.
        TODO: Try to gather details about the opponents and simulate battles before attacking.
        TODO: Ex, simulate 1000 battles per opponent and attack the one with the greatest chance to win against.

        TODO: Add a counter for won/lost fights.
        """
        opponents = [(575, 300), (790, 300), (1000, 300)]
        if self.check_if_available('arena/arena', threshold=0.93):
            self.do('arena/arena', threshold=0.93, sleep_time=3)
            self.do('arena/arena_boxes', previous_image='arena/arena', threshold=0.93, prev_threshold=0.93)
            self.click(choice(opponents))
            self.press_key(Keys.RETURN, 3)
            print(f'{self.get_time()}: A player has been attacked in the Arena.')
        else:
            print(f'{self.get_time()}: Arena is currently on cooldown.')

    def pets(self) -> None:
        """
        Check if pets are not under cooldown and attack all pets in order from "Shadow" to "Water".
        """
        while True:
            self.do('pets/pets', threshold=0.922)
            if self.check_if_available('pets/check_if_pet_screen'):
                break

        if self.check_if_available('pets/pets_done', threshold=0.94):
            print(f'{self.get_time()}: All pets have been attacked.')
            return

        pets = ['pet_shadow', 'pet_light', 'pet_earth', 'pet_fire', 'pet_water']
        for pet in pets:
            if self.check_if_available(f'pets/{pet}', threshold=0.9):
                self.do(f'pets/{pet}', threshold=0.93)
                if self.check_if_available(f'pets/attack_ok', threshold=0.93):
                    self.press_key(Keys.RETURN, 3)
                    print(f'{self.get_time()}: {pet.split("_")[1].upper()} pet has been attacked.')
                    return
                else:
                    print(f'{self.get_time()}: Pets are under cooldown at the moment.')
                    self.press_key(Keys.ESCAPE)
                    return
            else:
                continue

    def tavern(self) -> None:
        """
        Go on a random quest in the tavern.

        # TODO implement image to text processing to choose quest based on gold, exp or duration.
        """

        if self.check_if_available('tavern/tavern', threshold=0.89):
            self.do('tavern/tavern_keeper', previous_image='tavern/tavern', click=False, sleep_time=3)
            # Start the first quest
            self.press_key(Keys.RETURN)
            if self.check_if_available('tavern/drink_beer', threshold=0.91):
                self.do('tavern/drink_beer')
                if self.check_if_available('tavern/can_drink_true', threshold=0.95):
                    self.do('tavern/can_drink_true')
                    print(f'{self.get_time()}: Adventure points exhausted. Drank the free beer.')
                    self.tavern()
                    return
                else:
                    print(f'{self.get_time()}: No more adventure points in the tavern.')
            elif self.check_if_available('tavern/select_quest'):
                self.press_key(Keys.RETURN)
                if self.check_if_available('tavern/inventory_full', threshold=0.95):
                    print(f'{self.get_time()}: Cannot start mission, inventory is full.')
                else:
                    print(f'{self.get_time()}: Mission started.')
            else:
                self.tavern()
        else:
            print(f'{self.get_time()}: You are currently on a mission.')

    def fortress(self) -> None:
        """
        Collect the resources generators in the Fortress.
        """
        self.do('fortress/attack', previous_image='fortress/fortress', click=False, sleep_time=3, threshold=0.92)

        # Collect experience from the Academy.
        self.click((450, 200))
        if self.check_if_available('fortress/cancel_construction'):
            self.press_key(Keys.ESCAPE)
            print(f'{self.get_time()}: The Academy is under construction.')
        else:
            print(f'{self.get_time()}: Experience from the Academy has been collected.')

        # Collect stone from the Quarry.
        self.click((450, 520))
        if self.check_if_available('fortress/cancel_construction'):
            self.press_key(Keys.ESCAPE)
            print(f'{self.get_time()}: The Quarry is under construction.')
        elif (self.check_if_available('fortress/close', threshold=0.95) or
              self.check_if_available('fortress/can_upgrade_false', threshold=0.95) or
              self.check_if_available('fortress/can_upgrade_true', threshold=0.95)):
            self.press_key(Keys.ESCAPE)
            print(f'{self.get_time()}: The Stone storage is full.')
        else:
            print(f'{self.get_time()}: Stone from the Quarry has been collected.')

        # Collect wood from the Woodcutter's Hut.
        self.click((600, 600))
        if self.check_if_available('fortress/cancel_construction'):
            self.press_key(Keys.ESCAPE)
            print(f'{self.get_time()}: The Woodcutter\'s Hut is under construction.')
        elif self.check_if_available('fortress/close', threshold=0.95):
            self.press_key(Keys.ESCAPE)
            print(f'{self.get_time()}: The Wood storage is full.')
        else:
            print(f'{self.get_time()}: Wood from the Woodcutter\'s Hut has been collected.')

    def underground(self) -> None:
        """
        Collect the resources in the Underground and lure all heroes for the day.
        """
        self.do('underground/soul_harvest', previous_image='fortress/fortress', click=False, sleep_time=3, threshold=0.92)

        # Collect souls.
        self.click((1080, 280))
        if self.check_if_available('underground/cancel_construction', threshold=0.92):
            self.press_key(Keys.ESCAPE)
            print(f'{self.get_time()}: The Soul Extractor is under construction.')
        elif self.check_if_available('underground/close', threshold=0.95):
            self.press_key(Keys.ESCAPE)
            print(f'{self.get_time()}: The Soul storage is full.')
        else:
            print(f'{self.get_time()}: Underground souls have been collected.')

        # Collect gold.
        self.click((350, 380))
        if (self.check_if_available('underground/close', threshold=0.95) or
                self.check_if_available('underground/cancel_construction', threshold=0.95)):
            self.press_key(Keys.ESCAPE)
            print(f'{self.get_time()}: The gold has already been collected.')
        else:
            print(f'{self.get_time()}: Underground gold has been collected.')

        # Lure heroes underground.
        if self.check_if_available('underground/lure_hero', threshold=0.95):
            self.do('underground/lure_hero')
            while True:
                if self.check_if_available('underground/attack_hero', threshold=0.95):
                    self.press_key(Keys.RETURN, 3)
                    print(f'{self.get_time()}: A hero has been lured in the underground.')
                else:
                    break

        print(f'{self.get_time()}: Maximum heroes lured for the day.')

    def dungeons(self):
        # TODO implement a way to choose a specific location in the Dungeon to be entered
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
        self.enter(Keys.RETURN, 3)