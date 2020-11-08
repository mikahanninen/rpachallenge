from RPA.Excel.Files import Files
from playwright import sync_playwright
import re
from datetime import date


class RecordHandler:
    REGEX_MATCHER = r".*in.(\d{1,4}).milliseconds"
    record_time = None

    def __init__(self):
        self.open_record_time()

    def open_record_time(self):
        with open("record_time", "r") as rt:
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
            with open("record_time", "w") as rt:
                rt.write(str(task_time))
            today = date.today()
            page.screenshot(
                path=f"record_{today.strftime('%d%m%Y')}_time{task_time}ms.png"
            )


def myeval(page, xpath, elval):
    page.evaluate(
        """
        ([xpath, elval]) => {
        document.evaluate(xpath, document.body, null, 9, null).singleNodeValue.value = elval;}""",
        [xpath, elval],
    )


rh = RecordHandler()
excel = Files()
excel.open_workbook("challenge.xlsx")
sheet = excel.read_worksheet_as_table(header=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.newPage()
    page.goto("http://www.rpachallenge.com")
    page.click('text="Start"')
    for row in sheet:
        myeval(page, '//input[@ng-reflect-name="labelFirstName"]', row["First Name"])
        myeval(page, '//input[@ng-reflect-name="labelLastName"]', row["Last Name"])
        myeval(
            page, '//input[@ng-reflect-name="labelCompanyName"]', row["Company Name"]
        )
        myeval(page, '//input[@ng-reflect-name="labelRole"]', row["Role in Company"])
        myeval(page, '//input[@ng-reflect-name="labelAddress"]', row["Address"])
        myeval(page, '//input[@ng-reflect-name="labelEmail"]', row["Email"])
        myeval(page, '//input[@ng-reflect-name="labelPhone"]', str(row["Phone Number"]))
        page.evaluate("""document.querySelector('input[type="submit"]').click();""")
    result = page.evaluate(
        """() => {return document.querySelector('.message2').textContent;}"""
    )
    rh.check_for_new_record(page, result)
    browser.close()
