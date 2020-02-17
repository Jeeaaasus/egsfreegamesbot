from os import environ
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

egs_username = environ['egs_username']
egs_password = environ['egs_password']


class bot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)

    def main(self):
        self.goto_free_games_page()
        if self.page_load() is False:
            print(f'You are probably being rate limited or Epic Games could be experiencing issues..')
            sleep(60 * 10)
            self.driver.close()
            quit()
        self.login()
        self.goto_free_games_page()
        self.close_popup_cookies()
        self.find_free_games()
        self.driver.close()
        quit()

    def login(self):
        # go to the store page
        self.driver.get('https://www.epicgames.com/store/en-US')
        sleep(10)
        # click on 'sign in' button
        self.driver.find_element_by_xpath('//*[@id="user"]/ul/li/a/span').click()
        sleep(10)
        # write email/username
        self.driver.find_element_by_xpath('//*[@id="usernameOrEmail"]').send_keys(egs_username)
        # write password
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(egs_password)
        # click on 'login' button
        self.driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/div/form/div[4]/button/span').click()
        sleep(10)

    def goto_free_games_page(self):
        # go to the 'free games' page
        self.driver.get('https://www.epicgames.com/store/en-US/free-games')
        sleep(10)

    def find_free_games(self):
        # get number of 'Free Now' buttons
        free_now_buttons = len(self.driver.find_elements_by_xpath("//*[text()='Free Now']"))
        # for each button
        for n in range(free_now_buttons):
            # click button
            self.driver.find_elements_by_xpath("//*[text()='Free Now']")[n].click()
            sleep(10)
            while True:
                # make sure the game isn't already owned
                try:
                    self.driver.find_element_by_xpath("//*[text()='Owned']")
                    sleep(10)
                    break
                except NoSuchElementException:
                    # get the free game
                    try:
                        self.claim_game()
                        sleep(10)
                        break
                    # handle mature warning popup
                    except Exception:
                        self.close_popup_maturewarning()
                        sleep(10)
            self.goto_free_games_page()

    def claim_game(self):
        # click on 'Get'
        self.driver.find_element_by_xpath("//*[text()='Get']").click()
        sleep(10)
        # click on 'Place Order'
        self.driver.find_element_by_xpath("//*[text()='Place Order']").click()

    def close_popup_maturewarning(self):
        # click 'continue' on mature warning
        self.driver.find_element_by_xpath("//*[text()='Continue']").click()

    def close_popup_cookies(self):
        self.driver.find_element_by_xpath("//*[text()='Close']").click()

    def page_load(self):
        # make sure page loads correctly
        try:
            self.driver.find_element_by_xpath("//*[text()='Uh oh, something went wrong.']")
            return False
        except NoSuchElementException:
            return True
        except Exception:
            return False


start = bot()
start.main()
quit()
