from crewai import Crew, Agent, Process
from file_io import save_markdown
from tasks import AINewsLetterTasks
from agents import AINewsLetterAgents
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

tasks = AINewsLetterTasks()
agents = AINewsLetterAgents()

OpenAIGPT4 = ChatOpenAI( 
	model='L3I'  # Adjust based on available model
	)


# Instantiate the agents
editor = agents.editor_agent()
news_fetcher = agents.news_fetcher_agent()
news_analyzer = agents.news_analyzer_agent()
newsletter_compiler = agents.newsletter_compiler_agent()

# Instantiate the tasks
fetch_news_task = tasks.fetch_news_task(news_fetcher)
analyze_news_task = tasks.analyze_news_task(news_analyzer, [fetch_news_task])
compile_newsletter_task = tasks.compile_newsletter_task(
    newsletter_compiler, [analyze_news_task], save_markdown)

# Form the crew
crew = Crew(
    agents=[editor, news_fetcher, news_analyzer, newsletter_compiler],
    tasks=[fetch_news_task, analyze_news_task, compile_newsletter_task],
    coworker=[news_fetcher, news_analyzer, newsletter_compiler],
    context=[fetch_news_task],
    #process=Process.hierarchical,
    #manager_llm=OpenAIGPT4,
    verbose=2
)

# Kick off the crew's work
results = crew.kickoff()

# Print the results
print("Crew Work Results:")
print(results)