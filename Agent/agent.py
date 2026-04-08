from google.adk.agents.llm_agent import Agent
import os
import dotenv
import google.auth
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams 
from .func import*




zapier=''
zmail=''
api_key=zapier
meet=MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://mcp.zapier.com/api/v1/connect",
                headers={
                   "Authorization": f"Bearer {api_key}"
                }
            )
        )
mail=MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://mcp.zapier.com/api/v1/connect",
                headers={
                   "Authorization": f"Bearer {zmail}"
                }
            )
        )
meet_agent= Agent(

    model='gemini-2.5-pro',
    name='meet_agent',
    instruction='Schedule interview using tool',
    tools=[meet]
)
# mail_agent= Agent(

#     model='gemini-2.5-pro',
#     name='meet_agent',
#     instruction='Your Job is to send an email to the user',
#     tools=[mail]
)
# interview_scheduler_agent = Agent(
#     model='gemini-2.5-pro',
#     name='interview_scheduler_agen',
#     description='You are an helpful AI assistant and your job is to schedule an interview with the user and send an email to the user.',
#     instruction='Your job is to schedule an interview with the user and send an email to the user.',
#     sub_agents=[meet_agent,mail_agent]
)
Recruiter = Agent(
    name="Recruiter",
    model="gemini-2.5-pro",
    description=('''This agent reads candidate emails and determines if they are interested in an interview.".

    '''),
    tools=[recived_emails]
)

interview_scheduler = Agent(
    name="InterviewScheduler",
    model="gemini-2.5-pro",
    description="This agent takes candidate details and sends an interview invitation email.",
    tools=[send_email]
)

sender_agent = Agent(
    name="InterviewScheduler",
    model="gemini-2.5-pro",
    description="This agent takes candidate details and sends an interview invitation email.",
    tools=[send_email]
)

root_agent = Agent(
    model='gemini-3.1-pro-preview',
    name='root_agent',
    description='A helpful assistant for scheduling interviews based on candidate emails.',
    instruction='''Use the Recruiter agent to read candidate emails and determine if they are interested in an interview. 
    If a candidate is interested, use the InterviewScheduler agent to send them an interview invitation email.
    Always ensure that your responses are based on the most relevant information available through the tools.
    You can send JD to candidate if they are interested in interview and also you can ask them about their availability for interview.''',
    sub_agents=[Recruiter, meet_agent,interview_scheduler],
   
)
