from pyexpat.errors import messages

from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

URL = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "12345678"
DATABASE = "Health Data MVP"
AUTH = (USER, PASSWORD)

graph = Neo4jGraph(url=URL, username=USER, password=PASSWORD)

# test a query.
res = graph.query("match (d:Disease) return d;")
print(res)

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
# create a chain to QA
chain = GraphCypherQAChain.from_llm(llm=llm, graph=graph, verbose=True, top_k=1,
                                    allow_dangerous_requests=True)

query = "What is the youngest age of a patient with a disease and what is the disease and what is average age of a patient with that disease?"
res = chain.invoke({"query": query})

print(res)
