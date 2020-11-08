from RPA.Excel.Files import Files
from playwright import sync_playwright

excel = Files()
excel.open_workbook("challenge.xlsx")
sheet = excel.read_worksheet_as_table(header=True)


def myeval(page, xpath, elval):
    page.evaluate(
        """
        ([xpath, elval]) => {
        document.evaluate(xpath, document.body, null, 9, null).singleNodeValue.value = elval;}""",
        [xpath, elval],
    )


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
    page.screenshot(path="proof.png")
    browser.close()
