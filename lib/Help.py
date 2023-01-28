
_body = """Theres only a Few Commands so far, but they are as follows:
**__Rolling__**
`$roll [#]` for a manual dice roll, ie. `$roll 2`

**__Searching__**
`$lookup [ability|power|skill]` to lookup details on a skill, power or ability

__**Characters**__
`$import [link]` to attach [gSheet (v1.05)](https://docs.google.com/spreadsheets/d/1ftFo8efEl7JoA6MNhj3X1gpxn3WymXErgasccqzXn4k/edit#gid=2109282530)
`$list` to show all attached sheets
`$char [name]` to select a pre-attached sheet
`$check [ability|power|skill]` to roll the dice
"""


def HelpCommand(message):
    #Content follows format of Heading, Body, Footer
    Heading = "You wanted Help?"
    Body = _body
    Footer = "$Help"
    return [Heading, Body, Footer]