
_body = """Theres only a Few Commands so far, but they are as follows:
**__Rolling__**
`$roll [#]` for a manual dice roll, ie. `$roll 2`

**__Searching__**
`$lookup [group] [name]` to lookup details on a skill, power or ability

__**Sheet Control**__
`$import [link]` to attach a g-Sheet
`$list` to show all attached sheets
`$use [name]` to select a pre-attached sheet
`$check [ability|power|skill]` to use a skill from the sheet
"""


def HelpCommand(message):
    #Content follows format of Heading, Body, Footer
    Heading = "You wanted Help?"
    Body = _body
    Footer = "$Help"
    return [Heading, Body, Footer]