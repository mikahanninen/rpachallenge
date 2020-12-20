import Browser
from RPA.Excel.Files import Files
import RPA.Browser.Selenium
from pathlib import Path
from playwright import sync_playwright
import re
from datetime import date
from progress.bar import Bar
import time

js_filepath = str((Path(".") / "modify_dom.js").absolute())
rpachallenge_site = "http://www.rpachallenge.com"


class RecordHandler:
    REGEX_MATCHER = r".*in.(\d{1,4}).milliseconds"
    record_time = None
    engine = None

    def __init__(self):
        pass

    def set_engine(self, name):
        self.engine = name
        self.open_record_time()

    def open_record_time(self):
        with open(f"record_time_{self.engine}", "r") as rt:
            record = rt.read()
            self.record_time = int(record) if record else None
            if self.record_time:
                print(f"Current record time is {self.record_time} ms")

    def check_for_new_record(self, page, result):
        task_time = None
        match = re.match(self.REGEX_MATCHER, result)
        if match and len(match.groups()) > 0:
            task_time = int(match.group(1))
        print(f"Task execution time {task_time} ms")
        if not self.record_time or task_time and task_time < self.record_time:
            print(f"New record is {task_time} ms!")
            with open(f"record_time_{self.engine}", "w") as rt:
                rt.write(str(task_time))
            today = date.today()
            screenshot_filename = (
                f"record_{self.engine}_{today.strftime('%d%m%Y')}_time{task_time}ms.png"
            )
            if isinstance(page, RPA.Browser.Browser):
                page.screenshot(filename=screenshot_filename)
            elif isinstance(page, Browser.Browser):
                page.take_screenshot(filename=screenshot_filename)
            else:
                page.screenshot(path=screenshot_filename)


def myeval(browser_object, xpath, elval):
    eval_str_pw = """([xpath, elval]) => {
        document.evaluate(xpath, document.body, null, 9, null).singleNodeValue.value = elval;}"""
    eval_str_sel = f"document.evaluate('{xpath}', document.body, null, 9, null).singleNodeValue.value = '{elval}';"
    if isinstance(browser_object, RPA.Browser.Browser):
        browser_object.execute_javascript(eval_str_sel)
    else:
        browser_object.evaluate(
            eval_str_pw,
            [xpath, elval],
        )


def run_with_playwright(rh, sheet):
    print("Running RPA Challenge with Playwright")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.newPage()
        page.goto(rpachallenge_site)
        page.click('text="Start"')
        for row in sheet:
            myeval(
                page,
                '//input[@ng-reflect-name="labelFirstName"]',
                row["First Name"],
            )
            myeval(page, '//input[@ng-reflect-name="labelLastName"]', row["Last Name"])
            myeval(
                page,
                '//input[@ng-reflect-name="labelCompanyName"]',
                row["Company Name"],
            )
            myeval(
                page,
                '//input[@ng-reflect-name="labelRole"]',
                row["Role in Company"],
            )
            myeval(page, '//input[@ng-reflect-name="labelAddress"]', row["Address"])
            myeval(page, '//input[@ng-reflect-name="labelEmail"]', row["Email"])
            myeval(
                page,
                '//input[@ng-reflect-name="labelPhone"]',
                str(row["Phone Number"]),
            )
            page.evaluate("""document.querySelector('input[type="submit"]').click();""")
        result = page.evaluate(
            """() => {return document.querySelector('.message2').textContent;}"""
        )
        rh.check_for_new_record(page, result)
        browser.close()


def run_with_rfbrowser(rh, sheet):
    print("Running RPA Challenge with RFBrowser (RobotFramework Playwright)")
    browser = Browser.Browser()
    browser.new_context()
    browser.set_browser_timeout("30s")
    browser.new_page(rpachallenge_site)
    browser.click('"Start"')
    for row in sheet:
        browser.fill_text(
            '//input[@ng-reflect-name="labelFirstName"]', row["First Name"]
        )
        browser.fill_text('//input[@ng-reflect-name="labelLastName"]', row["Last Name"])
        browser.fill_text(
            '//input[@ng-reflect-name="labelCompanyName"]', row["Company Name"]
        )
        browser.fill_text(
            '//input[@ng-reflect-name="labelRole"]', row["Role in Company"]
        )
        browser.fill_text('//input[@ng-reflect-name="labelAddress"]', row["Address"])
        browser.fill_text('//input[@ng-reflect-name="labelEmail"]', row["Email"])
        browser.fill_text(
            '//input[@ng-reflect-name="labelPhone"]', str(row["Phone Number"])
        )
        browser.click('input[type="submit"]')

    result = browser.get_text(".message2")

    rh.check_for_new_record(browser, result)
    browser.close_browser()


def run_with_rpabrowser(rh, sheet, js=False):
    print(f"Running RPA Challenge with RPA Browser (Selenium) - JS: {js}")
    browser = RPA.Browser.Selenium.Selenium()
    browser.open_available_browser(
        rpachallenge_site, browser_selection="chrome,firefox", headless=True
    )
    if js:
        browser.execute_javascript(js_filepath)
    else:
        browser.click_button_when_visible("//button[text()='Start']")
        for row in sheet:
            myeval(
                browser, '//input[@ng-reflect-name="labelFirstName"]', row["First Name"]
            )
            myeval(
                browser, '//input[@ng-reflect-name="labelLastName"]', row["Last Name"]
            )
            myeval(
                browser,
                '//input[@ng-reflect-name="labelCompanyName"]',
                row["Company Name"],
            )
            myeval(
                browser, '//input[@ng-reflect-name="labelRole"]', row["Role in Company"]
            )
            myeval(browser, '//input[@ng-reflect-name="labelAddress"]', row["Address"])
            myeval(browser, '//input[@ng-reflect-name="labelEmail"]', row["Email"])
            myeval(
                browser,
                '//input[@ng-reflect-name="labelPhone"]',
                str(row["Phone Number"]),
            )
            browser.execute_javascript(
                """document.querySelector('input[type="submit"]').click();"""
            )
    result = browser.execute_javascript(
        """return document.querySelector('.message2').textContent;"""
    )
    rh.check_for_new_record(browser, result)
    browser.close_browser()


rh = RecordHandler()
excel = Files()
excel.open_workbook("challenge.xlsx")
sheet = excel.read_worksheet_as_table(header=True)


# rh.set_engine("robotframework-browser")
# run_with_rfbrowser(rh, sheet)
# rh.set_engine("playwright")
# run_with_playwright(rh, sheet)
# rh.set_engine("rpabrowser")
# run_with_rpabrowser(rh, sheet)
# rh.set_engine("playwright")
# run_with_playwright(rh, sheet)
# rh.set_engine("rpabrowser")
# run_with_rpabrowser(rh, sheet)

sleeptime = 300
while True:
    rh.set_engine("rpabrowser_js")
    run_with_rpabrowser(rh, sheet, True)
    bar = Bar("sleeping", max=sleeptime)
    for i in range(sleeptime):
        bar.next()
        time.sleep(1)
    bar.finish()
