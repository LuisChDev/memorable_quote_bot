# here we place all the config stuff

MEMORABLE_QUOTE_REGEX = '^"[^"]{50,140}\S"$'
source = 'https://github.com/Luischv/memorable_quote_bot'
start = 'start'
stop = 'stop'
msg_header = 'Send this message as it is'
bot_username = 'memorable_quote_bot'
delete_threshold = -2
numfigs = 60

startauto = ''.join(["https://reddit.com/message/compose?to=",
                     bot_username,
                     "&message=",
                     start,
                     "&subject=",
                     msg_header])

stopauto = ''.join(["https://reddit.com/message/compose?to=",
                    bot_username,
                    "&message=",
                    stop,
                    "&subject=",
                    msg_header])

PMme = "https://reddit.com/message/compose?to=LuisChDevOfficial"

already_stopped = 'I abstain from answering you already. If you want me to respond to your comments again, message me "' + start + '". (Without the quotes.)'
stopped = 'Done. I\'ll abstain from responding to your comments from now on. If you ever want me to start again, message me "' + start + '". (Without the quotes.)'
started = 'Okay. I\'ll start responding to your comments again. Remember you can always have me stop by messaging me "' + stop + '". (Without the quotes.)'

