from sys import exit

import checker

# Initial setup
directories_paths = ["./theme/sections",
                     "./theme/snippets"]
locale_path = "./theme/locales/en.default.json"
ch = checker.Checker(locale_path, directories_paths) #the GOD object... maybe it's better to split it into smaller objects: checker, parser, liquid part.. and pass data to methods?

ch.run()

if ch.has_unused_keys:
    exit("Found unused translation keys!")

#also: try to add tests. You'll see how it's hard to test this code because of the GOD object
#alse 2: think about error handling.
