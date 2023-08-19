from datetime import datetime
import random
from colorama import init, Fore, Back, Style
import keyring

init(autoreset=True)

GAIN_MESSAGES = [
            f"You've saved {Style.BRIGHT}{Fore.GREEN}{{gain}} minutes{Fore.RESET} using quip! If you found it valuable, show some love with a Bonusly bonus. Every point counts! ({Fore.BLUE}https://bonus.ly/app{Fore.RESET})",
            f"Awesome! You've saved {Style.BRIGHT}{Fore.GREEN}{{gain}} minutes{Fore.RESET} using quip. Consider sending a bonus on Bonusly! ({Fore.BLUE}https://bonus.ly/app{Fore.RESET})",
            f"Guess what? You've just gained back {Style.BRIGHT}{Fore.GREEN}{{gain}} minutes{Fore.RESET}! If you're feeling generous, a Bonusly bonus would make our day! ({Fore.BLUE}https://bonus.ly/app{Fore.RESET})",
            f"Time saved: {Style.BRIGHT}{Fore.GREEN}{{gain}} minutes{Fore.RESET}. Pleased with the time saved? Consider sending a bonus on Bonusly! ({Fore.BLUE}https://bonus.ly/app{Fore.RESET})",
            f"You've accelerated your project by {Style.BRIGHT}{Fore.GREEN}{{gain}} minutes{Fore.RESET}. That's efficiency in action! Show some love with a Bonusly bonus. ({Fore.BLUE}https://bonus.ly/app{Fore.RESET})",
            f"Thanks for using quip! You've saved {Style.BRIGHT}{Fore.GREEN}{{gain}} minutes{Fore.RESET} on this execution. A Bonusly bonus would be fantastic! ({Fore.BLUE}https://bonus.ly/app{Fore.RESET})"
        ]

def calculate_gain(action, template, args, duration=0):
    import quip.quip as q

    gain = 1
    if action == "new":
        if template:
            gain = 5
        else:
            gain = 9
    elif action in q.ICON_ACTION:
        gain = 14
    elif action in q.FIELD_ACTION:
        gain = 2
    elif action in q.UPDATE_ACTION:
        gain = 14
        if args.uuid:
            gain += 2
        if args.new_uuid:
            gain += 1
    elif action in q.DELETE_ACTION:
        gain = 0
    elif action in q.CLONE_ACTION:
        if template:
            gain = 5
        else:
            gain = 26
    elif action in q.BOOTSTRAP_ACTION:
        if template:
            gain = 5
        else:
            gain = 67
    elif action in q.UPLOAD_ACTION:
        if not template:
            gain = 2
        else:
            gain = 4
    elif action in q.DOWNLOAD_ACTION:
        if not template:
            gain = 2
        else:
            gain = 23
    elif action == "build":
        if template:
            gain = 3
        else:
            gain = 2
    elif action == "config":
        gain = 0
    elif action == "setup":
        gain = 157
    elif action in q.CLEAN_ACTION:
        gain = 1
    elif action == "version":
        if args.version_method is not None:
            gain = 3
        elif args.forced_version is not None:
            gain = 5
    
    if args.debug:
        gain -= 1
    


    if duration > 5: # if it is more than 5 seconds
        gain += (duration // 5)
    
    return gain

def print_greeting(_quip):
    action = _quip.args.action
    template = _quip.args.template
    try:
        duration = (datetime.now() - _quip.start_time).total_seconds()
    except:
        duration = 0
    gain = calculate_gain(action, template, args=_quip.args, duration=duration)
    
    if gain > 0:
        try:
            old_total_gain = keyring.get_password("quip", "total_gain")
            if old_total_gain is None:
                old_total_gain = 0
            else:
                old_total_gain = int(old_total_gain)
            
            total_gain = old_total_gain + gain
            keyring.set_password("quip", "total_gain", str(total_gain))
            message = random.choice(GAIN_MESSAGES)
            print(Style.BRIGHT + "\nTIP: " + message.format(gain=gain) + Style.RESET_ALL)
            if (old_total_gain % 500) > (total_gain % 500):
                if total_gain < 1000:
                    _message = f"{Back.YELLOW}{Fore.BLACK}Milestone Achieved!{Fore.RESET}{Back.RESET} You've saved more than {Fore.GREEN}500 minutes{Fore.RESET} in total! The total is {Fore.GREEN}{total_gain} minutes{Fore.RESET}. That's incredible efficiency. If you've found quip valuable, consider showing appreciation with a Bonus.ly bonus. Every point counts!"
                else:
                    _message = f"{Back.YELLOW}{Fore.BLACK}Milestone Achieved!{Fore.RESET}{Back.RESET} You've saved another {Fore.GREEN}500 minutes{Fore.RESET} in total! The total is {Fore.GREEN}{total_gain} minutes{Fore.RESET}. That's incredible efficiency. If you've found this tool valuable, consider showing appreciation with a Bonus.ly bonus. Every point counts!"
                print(f"TIP: {_message}")
        except:
            raise
    
    if _quip.args.debug:
        print_total_gain()

def print_total_gain():
    total_gain = keyring.get_password("quip", "total_gain")
    print(Style.BRIGHT + f"TIP: Your total gain for using quip is {Fore.GREEN}{total_gain} minutes{Fore.RESET}.")