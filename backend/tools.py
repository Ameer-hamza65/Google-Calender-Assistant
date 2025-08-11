from langchain_google_community.calendar.create_event import CalendarCreateEvent
from langchain_google_community.calendar.search_events import CalendarSearchEvents
from langchain_google_community.calendar.current_datetime import GetCurrentDatetime
from langchain_google_community.calendar.delete_event import CalendarDeleteEvent
from langchain_google_community.calendar.update_event import CalendarUpdateEvent
from langchain_google_community.calendar.get_calendars_info import GetCalendarsInfo
from langchain_core.tools import tool


tool1=CalendarDeleteEvent()
tool2=CalendarCreateEvent()
tool3=CalendarSearchEvents()
tool4=GetCalendarsInfo()
tool5=GetCurrentDatetime()
tool6=CalendarUpdateEvent()

tools=[tool1,tool2,tool3,tool4,tool5,tool6]