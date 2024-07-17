def format_message(data_by_drug):
    message_parts = []
    for drug, entries in data_by_drug.items():
        message = f"🌻  {drug}  🌻 \n\n{'⬇️🔽⏬⏬🔽⬇️'*2}\n\n"
        for entry in entries:
            status_icon = get_status_icon(entry[2])
            part = (
                f"⚕️  {entry[0]}\n"
                f"🗺️  {entry[1]}\n"
                f"⛽  {status_icon} {entry[2]} {status_icon}\n"
                f"🎍  {entry[3]}\n"
                f"📉  {entry[5]}\n\n"
            )
            message += part
        if len(message) > 2000:
            message_parts.append(message)
            message = ""
        else:
            message_parts.append(message)
    return message_parts

def get_status_icon(status):
    if "wiele sztuk" in status:
        return "🟢"
    elif "kilka sztuk" in status:
        return "🟡"
    elif "niepełne opakowanie" in status:
        return "🟠"
    elif "ostatnia sztuka" in status:
        return "🔴"
    return "🔴"
