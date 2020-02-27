from os import environ
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as available
from selenium.webdriver.common.by import By


egs_debug = environ['egs_debug']
egs_username = environ['egs_username']
egs_password = environ['egs_password']


class bot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--whitelisted-ips')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('log-level=1')
        self.driver = webdriver.Chrome(options=options)

    def main(self):
        self.startup()
        self.goto_free_games_page()
        self.page_load()
        self.login()
        self.login_check()
        self.goto_free_games_page()
        self.close_popup_cookies()
        self.find_free_games()

        print(f'All done! Exiting.')
        self.driver.close()
        quit()

    def startup(self):
        print(f'------------------------------------------------------')
        print(f'Made By: Jeeaaasus')
        print(f'https://github.com/Jeeaaasus/egsfreegamesbot')
        print(f'https://hub.docker.com/r/jeeaaasustest/egsfreegamesbot')
        print(f'------------------------------------------------------')
        print(f'')
        print(f'Starting egsfreegamesbot')
        if egs_username == 'unset':
            print(f'Error: you need to set ENVs \'egs_username\' and \'egs_password\'')
            self.driver.close()
            quit()
        print(f'Login: \'{egs_username}\'')
        print(f'...')

    def login(self):
        print(f'Logging in..')
        # go to the store page
        self.driver.get('https://www.epicgames.com/id/login')
        sleep(10)
        if egs_debug: print(f'DEBUG:login @ {self.driver.current_url}')
        # write email/username
        self.driver.find_element_by_xpath('//*[@id="usernameOrEmail"]').send_keys(egs_username)
        # write password
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(egs_password)
        # wait for and click on 'login' button
        button = WebDriverWait(self.driver, 60).until(available((By.XPATH, '//*[@id="login"]')))
        button.click()
        sleep(10)

    def login_check(self):
        if self.driver.current_url == 'https://www.epicgames.com/account/personal':
            print(f'Login success.')
            if egs_debug: print(f'DEBUG:login_check @ {self.driver.current_url}')
        else:
            print(f'Error: login failed.')
            print(f'Expected: https://www.epicgames.com/account/personal')
            print(f'Got: {self.driver.current_url}')
            print(f'Exiting!')
            self.driver.close()
            quit()

    def find_free_games(self):
        print(f'Finding free games..')
        # get number of 'Free Now' buttons
        free_now_buttons = len(self.driver.find_elements_by_xpath("//*[text()='Free Now']"))
        print(f'Found \'{free_now_buttons}\' free game(s).')
        # for each button
        for n in range(free_now_buttons):
            # click button
           # self.driver.find_elements_by_xpath("//*[text()='Free Now']")[n].click()
           # sleep(10)
            button = WebDriverWait(self.driver, 60).until(available((By.XPATH, '//*[text()="Free Now"]')))
            button.click()
            sleep(10)
            print(f'#{1 + n}: {self.driver.current_url}')
            while True:
                # make sure the game isn't already owned
                try:
                    self.driver.find_element_by_xpath("//*[text()='Owned']")
                    print(f'#{1 + n}: You already own this game.')
                    break
                except NoSuchElementException:
                    # get the free game
                    try:
                        self.claim_game()
                        print(f'#{1 + n}: Claimed!')
                        break
                    # handle mature warning popup
                    except Exception:
                        self.close_popup_maturewarning()
            self.goto_free_games_page()

    def claim_game(self):
        # click on 'Get'
       # self.driver.find_element_by_xpath("//*[text()='Get']").click()
       # sleep(10)
        button = WebDriverWait(self.driver, 60).until(available((By.XPATH, '//*[text()="Get"]')))
        button.click()
        if egs_debug: print(f'DEBUG:claim_game Get @ {self.driver.current_url}')
        # click on 'Place Order'
       # self.driver.find_element_by_xpath("//*[text()='Place Order']").click()
       # sleep(10)
        button = WebDriverWait(self.driver, 60).until(available((By.XPATH, '//*[text()="Place Order"]')))
        button.click()
        if egs_debug: print(f'DEBUG:claim_game Place Order @ {self.driver.current_url}')
        try:
           # self.driver.find_element_by_xpath("//*[text()='I Agree']").click()
           # sleep(10)
            button = WebDriverWait(self.driver, 60).until(available((By.XPATH, '//*[text()="I Agree"]')))
            button.click()
            if egs_debug: print(f'DEBUG:claim_game I Agree @ {self.driver.current_url}')
        except NoSuchElementException:
            pass
        if egs_debug: print(f'DEBUG:claim_game End @ {self.driver.current_url}')

    def page_load(self):
        if self.page_load_test() is False:
            print(f'You are probably being rate limited or Epic Games could be experiencing issues.')
            print(f'Trying again in an hour..')
            sleep(3600)
            if self.page_load_test() is False:
                print(f'You are probably being rate limited or Epic Games could be experiencing issues.')
                print(f'Exiting!')
                self.driver.close()
                quit()

    def page_load_test(self):
        # make sure page loads correctly
        try:
            self.driver.find_element_by_xpath("//*[text()='Uh oh, something went wrong.']")
            return False
        except NoSuchElementException:
            return True
        except Exception:
            return False

    def goto_free_games_page(self):
        # go to the 'free games' page
        self.driver.get('https://www.epicgames.com/store/en-US/free-games')
        sleep(10)
        if egs_debug: print(f'DEBUG:goto_free_games_page @ {self.driver.current_url}')

    def close_popup_cookies(self):
        self.driver.find_element_by_xpath("//*[text()='Close']").click()
        if egs_debug: print(f'DEBUG:close_popup_cookies @ {self.driver.current_url}')

    def close_popup_maturewarning(self):
        # click 'continue' on mature warning
        self.driver.find_element_by_xpath("//*[text()='Continue']").click()
        if egs_debug: print(f'DEBUG:close_popup_maturewarning @ {self.driver.current_url}')


start = bot()
start.main()
quit()
