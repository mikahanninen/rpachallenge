const taskdata = [
    {'First Name': 'John', 'Last Name': 'Smith', 'Company Name': 'IT Solutions', 'Role in Company': 'Analyst', 'Address': '98 North Road', 'Email': 'jsmith@itsolutions.co.uk', 'Phone Number': 40716543298},
    {'First Name': 'Jane', 'Last Name': 'Dorsey', 'Company Name': 'MediCare', 'Role in Company': 'Medical Engineer', 'Address': '11 Crown Street', 'Email': 'jdorsey@mc.com', 'Phone Number': 40791345621},
    {'First Name': 'Albert', 'Last Name': 'Kipling', 'Company Name': 'Waterfront', 'Role in Company': 'Accountant', 'Address': '22 Guild Street', 'Email': 'kipling@waterfront.com', 'Phone Number': 40735416854},
    {'First Name': 'Michael', 'Last Name': 'Robertson', 'Company Name': 'MediCare', 'Role in Company': 'IT Specialist', 'Address': '17 Farburn Terrace', 'Email': 'mrobertson@mc.com', 'Phone Number': 40733652145},
    {'First Name': 'Doug', 'Last Name': 'Derrick', 'Company Name': 'Timepath Inc.', 'Role in Company': 'Analyst', 'Address': '99 Shire Oak Road', 'Email': 'dderrick@timepath.co.uk', 'Phone Number': 40799885412},
    {'First Name': 'Jessie', 'Last Name': 'Marlowe', 'Company Name': 'Aperture Inc.', 'Role in Company': 'Scientist', 'Address': '27 Cheshire Street', 'Email': 'jmarlowe@aperture.us', 'Phone Number': 40733154268},
    {'First Name': 'Stan', 'Last Name': 'Hamm', 'Company Name': 'Sugarwell', 'Role in Company': 'Advisor', 'Address': '10 Dam Road', 'Email': 'shamm@sugarwell.org', 'Phone Number': 40712462257},
    {'First Name': 'Michelle', 'Last Name': 'Norton', 'Company Name': 'Aperture Inc.', 'Role in Company': 'Scientist', 'Address': '13 White Rabbit Street', 'Email': 'mnorton@aperture.us', 'Phone Number': 40731254562},
    {'First Name': 'Stacy', 'Last Name': 'Shelby', 'Company Name': 'TechDev', 'Role in Company': 'HR Manager', 'Address': '19 Pineapple Boulevard', 'Email': 'sshelby@techdev.com', 'Phone Number': 40741785214},
    {'First Name': 'Lara', 'Last Name': 'Palmer', 'Company Name': 'Timepath Inc.', 'Role in Company': 'Programmer', 'Address': '87 Orange Street', 'Email': 'lpalmer@timepath.co.uk', 'Phone Number': 40731653845}
]

const labels = {
    'First Name': 'labelFirstName',
    'Last Name': 'labelLastName',
    'Role in Company': 'labelRole',
    'Address': 'labelAddress',
    'Phone Number': 'labelPhone',
    'Company Name': 'labelCompanyName',
    'Email': 'labelEmail'

}
var mapped = []
function convert(data) {
    var item = new Object()
    for(var key in data) {
        item[labels[key]] = data[key]
    }
    mapped.push(item)
}

taskdata.map(convert)

function setFormHTML(item) {
    var form = document.querySelectorAll("form")[0];
    form.querySelectorAll('input[ng-reflect-name="labelFirstName"]')[0].value = item['labelFirstName']
    form.querySelectorAll('input[ng-reflect-name="labelLastName"]')[0].value = item['labelLastName']
    form.querySelectorAll('input[ng-reflect-name="labelRole"]')[0].value = item['labelRole']
    form.querySelectorAll('input[ng-reflect-name="labelAddress"]')[0].value = item['labelAddress']
    form.querySelectorAll('input[ng-reflect-name="labelPhone"]')[0].value = item['labelPhone']
    form.querySelectorAll('input[ng-reflect-name="labelCompanyName"]')[0].value = item['labelCompanyName']
    form.querySelectorAll('input[ng-reflect-name="labelEmail"]')[0].value = item['labelEmail']
}

function loopItems() {
    var i = 0, len = mapped.length;
    document.querySelectorAll('button.uiColorButton')[0].click();
    while (i < len) {
        setFormHTML(mapped[i]);
        document.querySelectorAll('input[value="Submit"]')[0].click();
        i++
    }
}

loopItems()