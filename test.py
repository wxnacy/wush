#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import os

from wapi.common.decorates import env_functions
from wapi.common.config_value import ConfigValue

if __name__ == "__main__":
    #  print(env_functions)
    #  func_str = "test(1, 'ww')"
    #  name, args_str = func_str.split("(")
    #  print(name, args_str)
    #  args = eval('(' + args_str)
    #  print(args)

    #  for name, func in env_functions.items():
        #  print(name, func(1))
    os.system('vim')

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter
from wapi.common.loggers import logger

class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        logger.info(document)
        logger.info(dir(document))
        logger.info(document.text)
        logger.info(document.text_after_cursor)
        logger.info(complete_event)
        # Display this completion, black on yellow.
        yield Completion('completion1',
                         style='bg:ansiyellow fg:ansiblack')

        # Underline completion.
        yield Completion('completion2', start_position=0,
                         style='underline')

        # Specify class name, which will be looked up in the style sheet.
        yield Completion('completion3', start_position=0,
                         style='class:special-completion')

from prompt_toolkit import PromptSession

def main():
    session = PromptSession(completer = MyCustomCompleter(),
        complete_in_thread=True)

    while True:
        try:
            text = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            print('You entered:', text)
    print('GoodBye!')

if __name__ == '__main__':
    main()
