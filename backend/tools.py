from langchain_google_community.calendar.create_event import CalendarCreateEvent
from langchain_google_community.calendar.search_events import CalendarSearchEvents
from langchain_google_community.calendar.current_datetime import CurrentDatetimeSchema
from langchain_google_community.calendar.delete_event import CalendarDeleteEvent
from langchain_google_community.calendar.update_event import CalendarUpdateEvent
from langchain_google_community.calendar.get_calendars_info import GetCalendarsInfo
from langchain_core.tools import tool


@tool
def create_event():
    """
    Create a new event in Google Calendar.
    Use this tool when the user requests to add or schedule a meeting, reminder, or appointment.
    Requires event details such as title, date, time, and optional description/location.
    """
    return CalendarCreateEvent()


@tool
def delete_event():
    """
    Delete an existing event from Google Calendar.
    Use this tool when the user requests to cancel or remove a specific event.
    Requires the event ID or details to identify the correct event.
    """
    return CalendarDeleteEvent()


@tool
def update_event():
    """
    Update an existing event in Google Calendar.
    Use this tool when the user wants to change event details such as date, time, title, location, or description.
    Requires the event ID or identifiable details of the event.
    """
    return CalendarUpdateEvent()


@tool
def search_event():
    """
    Search for events in Google Calendar.
    Use this tool when the user asks to check upcoming events, find a specific meeting, or see events on a particular date.
    """
    return CalendarSearchEvents()


@tool
def get_current_event():
    """
    Get the current date and time.
    Use this tool when event scheduling requires knowing the current date/time for context or default values.
    """
    return CurrentDatetimeSchema()


@tool
def get_info_event():
    """
    Retrieve information about available Google Calendars in the account.
    Use this tool when the user wants to see calendar lists, IDs, or details before creating, updating, or deleting events.
    """
    return GetCalendarsInfo()
