from crewai import Crew, Agent, Task, Process
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from textwrap import dedent
from dotenv import load_dotenv

load_dotenv()

class GetTranscript:
    @tool("Get Transcript Tool")
    def news(query: str) -> str:
        """Search Chroma DB for relevant news information based on a query."""
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=oembed)
        retriever = vectorstore.similarity_search(query)
        return retriever

note_compiler = Agent(
    role='Note Compiler',
    goal='Compile the transcripts into a organized format.',
    backstory="""You are a note compiler that is responsible for
    compiling the transcripts into an organized format.
    You like the method of organizing transcripts into 
    the main point, followed by sub points and then followed by
    sub sub points. You also have to make sure you are not repeating any 
    information in your notes.""",
    verbose=True,
    allow_delegation=False
)

note_checker = Agent(
    role='Note Checker',
    goal='Check the notes to see if any information from the transcript is missing',
    backstory="""You are a note checker that is responsible for 
    checking the notes to make sure that nothing from the transcript is missing from
    the notes. You always check every note throughly and you never miss a single note.""",
    verbose=True,
    allow_delegation=False,
    coworker=[note_compiler]
)

compile_task = Task(
    description='Compile {Transcript} into well organized notes.',
    expected_output="""The main point of the transcript is/are this/these
    - Main Point 1[Always at least one]
    - Main Point 2[If any other points exists]
    - Main Point 3[Maximum number of main points is 3]
    - Sub Point 1.1[Sub point 1 of Main Point 1]
    - Sub Point 1.2[If any other points exists]
    - Sub Point 1.3[Maximum number of sub points is 3]
    - Sub Point 2.1[Sub point 2 of Main Point 1]
  	- Sub Point 2.2[If any other points exists]
  	- Sub Point 2.3[Maximum number of sub points is 3]          
    - Sub Point 3.1[Sub point 1 of Main Point 1]
  	- Sub Point 3.2[If any other points exists]
  	- Sub Point 3.3[Maximum number of sub points is 3]
    """,
    agent=note_compiler
) 

check_task = Task(
    description='Check Notes to see if anything from the transcript is missing. Use Get Transcript Tool to get the transcript',
    expected_output="""These Informations are missing from the transcript
    -Information 1
    -Information 2
    
    or
    
    There is no information missing from the transcript, These are the notes: {context}""",
    agent=note_checker,
    context=[compile_task],
    coworker=[note_compiler],
    tool=[GetTranscript],
    #human_input=True
)


class NoteCrew:
 def __init__(self, Transcript):
    self.Transcript = Transcript

 def run(self):
    crew = Crew(
        agents=[note_compiler, note_checker],
        tasks=[compile_task, check_task],
        verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("Input Transcript")
  print('-------------------------------')
  Transcript = input()
  data = Document(page_content=Transcript)
  text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
  all_splits = text_splitter.split_documents([data])
  oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="mxbai-embed-large")
  vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)

note_crew = NoteCrew(Transcript)
results = note_crew.run()

print(results)