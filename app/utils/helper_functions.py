from flask import current_app
import requests


# helper for pagination purpose
def pagination(query_db, page):
    return query_db.paginate(page, current_app.config['ITEMS_PER_PAGE'], False)


# helper to format the link based on the med name (if more than one word, the space -> '+')
def med_verify_link(link: list):
    response = requests.get("".join(link))
    data = response.json()
    return data


# helper to fetch info from med label
def med_label(data: dict):
    if data:
        last_updated = data["meta"]["last_updated"]
        results = data["results"]
        adv_reactions = results[0].get("adverse_reactions")
        boxed_warnings = results[0].get("boxed_warning")
        warnings = results[0].get("warnings")
        return {'last_updated_label': last_updated,
                'reactions': adv_reactions,
                'boxed_warnings': boxed_warnings,
                'warnings': warnings}
    else:
        return False

# helper to fetch info from patients' experience
def med_event(data: dict):
    if data:
        last_updated = data["meta"]["last_updated"]
        events = data["results"]
        return {'last_updated_events': last_updated, 'events': events}
    else:
        return False
