from sys import exit

import checker

# First theme
directories_paths = ["/home/pavel/dev/python/templates/theme/sections",
                     "/home/pavel/dev/python/templates/theme/snippets"]
locale_path = "/home/pavel/dev/python/templates/theme/locales/en.default.json"
ch = checker.Checker(locale_path, directories_paths)

# Second theme
directories_paths2 = ["/home/pavel/dev/python/templates/theme2/sections",
                     "/home/pavel/dev/python/templates/theme2/snippets"]
locale_path2 = "/home/pavel/dev/python/templates/theme2/locales/en.default.json"
ch2 = checker.Checker(locale_path2, directories_paths2)

for checker in [ch, ch2]:
    checker.run()

if ch.has_unused_keys or ch2.has_unused_keys:
    exit("Found unused translation keys!")
