import os
from textwrap import dedent
from crewai import Agent
from tools.search_tools import SearchTools
from crewai_tools import ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import load_tools

load_dotenv()
human_tools = load_tools(["human"])

class AINewsLetterAgents():

	def editor_agent(self):
		return Agent(
            role='Editor',
            goal='Oversee the creation of the Finance Newsletter',
            backstory="""With a keen eye for detail and a passion for storytelling, you ensure that the newsletter
            not only informs but also engages and inspires the readers. """,
            #allow_delegation=True,
            verbose=True,
            max_iter=15,
			
        )

	def news_fetcher_agent(self):
		return Agent(
            role='NewsFetcher',
            goal='Fetch the top Finance news stories for the day',
            backstory="""As a digital sleuth, you scour the internet for the latest and most impactful developments
            in the world of Finance, ensuring that our readers are always in the know.""",
            tools=[SearchTools.search_internet],
            verbose=True,
            #allow_delegation=True,
			
        )

	def news_analyzer_agent(self):
		return Agent(
            role='NewsAnalyzer',
            goal='Analyze each Finance news story and generate a detailed markdown summary',
            backstory="""With a critical eye and a knack for distilling complex information, you provide insightful
            analyses of Finance news stories, making them accessible and engaging for our audience.""",
            tools=[SearchTools.search_internet],
            verbose=True,
            #allow_delegation=True,
			
        )

	def newsletter_compiler_agent(self):
		return Agent(
            role='NewsletterCompiler',
            goal='Compile the analyzed Finance news stories into a final newsletter format',
            backstory="""As the final architect of the newsletter, you meticulously arrange and format the content,
            ensuring a coherent and visually appealing presentation that captivates our readers. Make sure to follow
            newsletter format guidelines and maintain consistency throughout.""",
            verbose=True,
			
        )
	
class NoteCompilers():

	def Head_Compiler(self):
		return Agent(
            role='Editor',
            goal='Oversee the creation of the Notes for students',
            backstory="""With an amazing ability to summarize and organize transcripts, ensures the notes to be as 
			 clear as possible for each student""",
            allow_delegation=True,
            verbose=True,
            max_iter=15,
			
        )

	def news_fetcher_agent(self):
		return Agent(
            role='NewsFetcher',
            goal='Fetch the top Finance news stories for the day',
            backstory="""As a digital sleuth, you scour the internet for the latest and most impactful developments
            in the world of Finance, ensuring that our readers are always in the know.""",
            tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=True,
			
        )

	def news_analyzer_agent(self):
		return Agent(
            role='NewsAnalyzer',
            goal='Analyze each Finance news story and generate a detailed markdown summary',
            backstory="""With a critical eye and a knack for distilling complex information, you provide insightful
            analyses of Finance news stories, making them accessible and engaging for our audience.""",
            tools=[
				SearchTools.search_internet 
				   
				   ],
            verbose=True,
            allow_delegation=True,
			
        )

	def newsletter_compiler_agent(self):
		return Agent(
            role='NewsletterCompiler',
            goal='Compile the analyzed Finance news stories into a final newsletter format',
            backstory="""As the final architect of the newsletter, you meticulously arrange and format the content,
            ensuring a coherent and visually appealing presentation that captivates our readers. Make sure to follow
            newsletter format guidelines and maintain consistency throughout.""",
            verbose=True,
			
        )