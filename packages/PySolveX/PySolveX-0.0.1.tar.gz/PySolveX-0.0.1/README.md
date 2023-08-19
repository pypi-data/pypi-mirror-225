# PySolveX
Python library for solving reCaptcha using Selenium.

## Installation
To install the library, simply run the following command:
``` 
pip install PySolveX
```
Here's an example:
``` python
from selenium import webdriver
from PySolveX import reCAPTCHA_V2

driver = webdriver.Chrome()

driver.get("https://www.google.com/recaptcha/api2/demo")

v2 = reCAPTCHA_V2(driver, debug=True)

v2.solve()
```

### Channel
Telegram : [Channel](https://t.me/YDDCK)

### Support
Telegram : [Developer](https://t.me/V_IRUuS)
