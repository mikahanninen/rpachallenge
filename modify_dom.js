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