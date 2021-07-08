CHROME_LINUX = {
    'isMobile': False,
    'platformName': 'LINUX',
    'browserName': 'Chrome',
    'deviceName': 'Ubuntu 18.04 LTS'
}

CHROME_ANDROID_GALAXY_S9 = {
    'isMobile': True,
    'platformName': 'Android',
    'browserName': 'Chrome',
    'deviceName': 'Samsung Galaxy S9*'
}

SAFARI_IPHONE_X = {
    'isMobile': True,
    'platformName': 'iOS',
    'browserName': 'safari',
    'deviceName': 'iPhone X.*'
}

SAUCE_LABS_RDC_CHROME_EMULATION_MAPPING = {
    'Samsung Galaxy S9*': 'Pixel 2 XL',
    'iPhone X.*': 'iPhone X',
    'Ubuntu 18.04 LTS': 'Laptop with HiDPI screen'
}
