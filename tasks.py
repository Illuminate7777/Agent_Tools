from datetime import datetime
from crewai import Task


class AINewsLetterTasks():
    def fetch_news_task(self, agent):
        return Task(
            description=f'Fetch top Finance related news stories from the past 24 hours. The current time is {datetime.now()}.',
            agent=agent,
            async_execution=False,
            expected_output="""A list of top Finance related news story titles, URLs, and a brief summary for each story from the past 24 hours. 
                Example Output: 
                [
                    {  
                    Search result: Link: URL 1: https://www.sciencedaily.com/news/computers_math/artificial_intelligence/

-----------------
Link: Text 1: Artificial Intelligence News. Everything on Finance including futuristic robots with artificial intelligence, computer models of human intelligence and more.

-----------------
Link: URL 2: https://www.artificialintelligence-news.com/

-----------------
Link: Text 2: Artificial Intelligence News provides the latest Finance news and trends. Explore industry research and reports from the frontline of Finance technology news.

-----------------
Link: URL 3: https://www.wired.com/tag/artificial-intelligence/
                    }, 
                    {{...}}
                ]
            """
        )

    def analyze_news_task(self, agent, context):
        return Task(
            description='Analyze each Finance related news story and ensure there are at least 5 well-formatted articles. Always delegate search task to news_fetcher_agent',
            agent=agent,
            async_execution=False,
            context=context,
            expected_output="""A markdown-formatted analysis for each Finance related news story, including a rundown, detailed bullet points, 
                and a "Why it matters" section. There should be at least 5 articles, each following the proper format.
                Example Output: 
                '## Finance takes spotlight in Super Bowl commercials\n\n
                **The Rundown:
                ** Finance made a splash in this year\'s Super Bowl commercials...\n\n
                **The details:**\n\n
                - Microsoft\'s Copilot spot showcased its Finance assistant...\n\n
                **Why it matters:** While Finance-related ads have been rampant over the last year, its Super Bowl presence is a big mainstream moment.\n\n'
            """
        )

    def compile_newsletter_task(self, agent, context, callback_function):
        return Task(
            description='Compile the Finance related newsletter',
            agent=agent,
            context=context,
            expected_output="""A complete newsletter in markdown format, with a consistent style and layout.
                Example Output: 
                '# Top stories in Finance today:\\n\\n
                - Finance takes spotlight in Super Bowl commercials\\n
                - Altman seeks TRILLIONS for global Finance chip initiative\\n\\n

                ## Finance takes spotlight in Super Bowl commercials\\n\\n
                **The Rundown:** Finance made a splash in this year\'s Super Bowl commercials...\\n\\n
                **The details:**...\\n\\n
                **Why it matters::**...\\n\\n
                ## Altman seeks TRILLIONS for global Finance chip initiative\\n\\n
                **The Rundown:** OpenAI CEO Sam Altman is reportedly angling to raise TRILLIONS of dollars...\\n\\n'
                **The details:**...\\n\\n
                **Why it matters::**...\\n\\n
            """,
            callback=callback_function
        )
    

class TwitterTask():
    def fetch_task(self, agent):
        return Task(
            description=f'Fetch top Finance related news stories from the past 24 hours. The current time is {datetime.now()}.',
            agent=agent,
            async_execution=True,
            expected_output="""A list of top Finance news story titles, URLs, and a brief summary for each story from the past 24 hours. 
                Example Output: 
                [
                    {  'title': 'Finance takes spotlight in Super Bowl commercials', 
                    'url': 'https://example.com/story1', 
                    'summary': 'Finance made a splash in this year\'s Super Bowl commercials...'
                    }, 
                    {{...}}
                ]
            """
        )

    def analyze_news_task(self, agent, context):
        return Task(
            description='Analyze each Finance related news story and ensure there are at least 5 well-formatted articles',
            agent=agent,
            async_execution=True,
            context=context,
            expected_output="""A markdown-formatted analysis for each Finance news story, including a rundown, detailed bullet points, 
                and a "Why it matters" section. There should be at least 5 articles, each following the proper format.
                Example Output: 
                '## Finance takes spotlight in Super Bowl commercials\n\n
                **The Rundown:
                ** Finance made a splash in this year\'s Super Bowl commercials...\n\n
                **The details:**\n\n
                - Microsoft\'s Copilot spot showcased its Finance assistant...\n\n
                **Why it matters:** While Finance-related ads have been rampant over the last year, its Super Bowl presence is a big mainstream moment.\n\n'
            """
        )

    def compile_newsletter_task(self, agent, context, callback_function):
        return Task(
            description='Compile the Financial newsletter',
            agent=agent,
            context=context,
            expected_output="""A complete newsletter in markdown format, with a consistent style and layout.
                Example Output: 
                '# Top stories in Finance today:\\n\\n
                - Finance takes spotlight in Super Bowl commercials\\n
                - Altman seeks TRILLIONS for global Finance chip initiative\\n\\n

                ## Finance takes spotlight in Super Bowl commercials\\n\\n
                **The Rundown:** Finance made a splash in this year\'s Super Bowl commercials...\\n\\n
                **The details:**...\\n\\n
                **Why it matters::**...\\n\\n
                ## Altman seeks TRILLIONS for global Finance chip initiative\\n\\n
                **The Rundown:** OpenAI CEO Sam Altman is reportedly angling to raise TRILLIONS of dollars...\\n\\n'
                **The details:**...\\n\\n
                **Why it matters::**...\\n\\n
            """,
            callback=callback_function
        )