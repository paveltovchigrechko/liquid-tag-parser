from sys import exit

import checker

# Initial setup
directories_paths = ["../optimum/theme/sections",
                     "../optimum/theme/snippets"]
locale_path = "../optimum/theme/locales/en.default.json"
ch = checker.Checker(locale_path, directories_paths)

ch.run()

if ch.has_unused_keys:
    exit("Found unused translation keys!")
