from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts.prompt import PromptTemplate

load_dotenv()

URL = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "PASSWORD"
DATABASE = "Health Data MVP"
AUTH = (USER, PASSWORD)

SAMPLE_QUESTIONS = [
    "How many hospitals are there in the graph?",
    "What is the most common disease in the graph?",
    "How many women are there in the graph?",
    "What is the average age of the patients in the graph?"
    ]

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Graph node names are capitalized. Relationship names are in all caps. For example gender is "Male" or "Female". 
Here are the relationships in the graph:

NODES:
    1. Patient
        - name
        - age
        - gender
        - blood Type
    2. Disease
    3. Doctor
    4. Hospital
    5. InsuranceProvider
    6. Medication

RELATIONSHIPS between NODES:

    1. Patient - [:HAS_CONDITION] -> Disease
    2. Patient - [:ADMITTED_TO] -> Hospital
        - Properties:
            - dateOfAdmission
            - dischargeDate
            - billingAmount
            - roomNumber
            - admissionType
            - testResults
    3. Patient - [:INSURED_BY] -> InsuranceProvider
    4. Patient - [:TAKES] -> Medication
    5. Patient - [:TREATED_BY] -> Doctor

For example if user asks something like "What is the admission type of Kyle Fuller?"
You should use relationship properties between Patient and Hospital to answer the question.
For example:
MATCH (p:Patient where name: "Kyle Fuller")-[rel:ADMITTED_TO]->(h:Hospital)
RETURN rel.admissionType

The question is:
{question}"""

graph = Neo4jGraph(url=URL, username=USER, password=PASSWORD)
LLM = ChatOpenAI(temperature=0, model="gpt-4o-mini")
# create a chain to QA
CHAIN = GraphCypherQAChain.from_llm(llm=LLM, graph=graph, verbose=True, top_k=5, allow_dangerous_requests=True,
                                    cypher_prompt=PromptTemplate(input_variables=["question"],
                                                                 template=CYPHER_GENERATION_TEMPLATE),
                                    )


def create_sample_sentences() -> None:
    st.markdown("🚀 *Hello! Here are some sample questions you can ask:*")

    follow_up_container = st.container()

    with follow_up_container.container():
        cols = st.columns(3)
        with cols[0]:
            st.success(SAMPLE_QUESTIONS[0], icon="👉")
        with cols[1]:
            st.warning(SAMPLE_QUESTIONS[1], icon="👉")
        with cols[2]:
            st.error(SAMPLE_QUESTIONS[2], icon="👉")


def run_app():
    title = "GSU Data Science Final Project"
    st.set_page_config(page_title=title, page_icon="🤖")
    #st.image("../asset/gsu_logo.png", width=40)

    st.title(title)
    st.caption("Final project of the program.")

    create_sample_sentences()
    query = st.text_input("Enter your query here:")

    submit_button = st.button("Ask")
    if submit_button:
        response = CHAIN.invoke(query)
        st.info(response['result'])

if __name__ == '__main__':
    run_app()
