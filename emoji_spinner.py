import itertools
import os
import sys
import time


def make_bouncer(spin_set):
    return itertools.cycle(spin_set + spin_set[-2:0:-1])


skin_tones = make_bouncer([
    "{}🏻",
    "{}🏼",
    "{}🏽",
    "{}🏾",
    "{}🏿",
])


skin_tone_emoji = (
    "👋🤚🖐✋🖖👌🤏✌🤞🤟🤘🤙👈👉👆🖕👇☝👍👎✊👊🤛🤜👏🙌👐🤲🤝🙏✍💅🤳💪🦵🦶👂🦻👃👶🧒👦👧"
    "🧑👱👨🧔👩🧓👴👵🙍🙎🙅🙆💁🙋🧏🙇🤦🤷🧟👮🕵💂👷🤴👸👳👲🧕🤵👰🤰🤱👼🎅🤶🦸🦹🧙🧚🧛🧜"
    "🧝💆💇🚶🧍🧎🏃💃🕺🕴👯🧖🧗🏇🏂🏌🏄🚣🏊⛹🏋🚴🚵🤸🤽🤼🤾🤹🧘🛀🛌👭👫👬💏💑👪☞🖒🖓🖑☟☛"
    "🖔☜🖎☚"
)

arrows = ["⬆️", "↗️", "➡️", "↘️", "⬇️", "↙️", "⬅️", "↖️"]
clocks_00 = "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛"
clocks_30 = "🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧"
moons = "🌕🌖🌗🌘🌑🌒🌓🌔"
hearts = "🧡💛💚💙💜"  # ❤️ formats weird sometimes

spinner_lookup = {
    **{emoji: skin_tones for emoji in skin_tone_emoji},
    **{arrow: itertools.cycle(arrows) for arrow in arrows},
    **{clock: itertools.cycle(clocks_00) for clock in clocks_00},
    **{clock: itertools.cycle(clocks_30) for clock in clocks_30},
    **{moon: itertools.cycle(moons) for moon in moons},
    **{heart: itertools.cycle(hearts) for heart in hearts},
}

def spinner(emoji):
    emoji = emoji.strip()
    if emoji not in spinner_lookup:
        raise Exception(f"No spinner registered for {emoji!r}")
    os.system("tput civis")  # disable cursor
    try:
        for template in spinner_lookup[emoji]:
            print("\r" + template.format(emoji), end="")
            time.sleep(0.1)
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        os.system("tput cvvis")
        print()


if __name__ == '__main__':
    spinner(sys.argv[1])
