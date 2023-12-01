import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langsmith import Client
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory


st.set_page_config(page_title="Mathematics - Grade 8 - 1st Semester Test", page_icon="🦜")
st.title("🦜 Mathmatics Test")
button_css = """.stButton>button {
    color: #4F8BF9;
    border-radius: 50%;
    height: 2em;
    width: 2em;
    font-size: 4px;
}"""
st.markdown(f'<style>{button_css}</style>', unsafe_allow_html=True)

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)



def load_prompt(topic):

	template = """
        As a Cambridge grade 8 Math Teacher, you need to provide homework for the grade 8 students.
        You will use the given math topic to generate the question and wait for user to provide answer.
        Once got the answer from the user, you will check the result and always reply first with 'Correct' or 'Wrong' 
        follow with the explanation.
        If they ask questions not related to this getting started guide,you should politely decline to answer and remind them to stay on topic.
        Here is the maths topic: {topic}
        """.format(topic = topic)

	prompt_template = ChatPromptTemplate(messages = [
		SystemMessage(content=template), 
		MessagesPlaceholder(variable_name="chat_history"), 
		HumanMessagePromptTemplate.from_template("{input}")
		]) # type: ignore
	return prompt_template



# Initialize LangSmith client
client = Client()

Math_Lesson = [
    "3.1 Multiplying and dividing by 0.1 and 0.01",
    "3.2 Rounding",
    "1.1 Factors, multiples and primes",
    "1.2 Multiplying and dividing integers",
    "1.3 Square roots and cube roots",
    "1.4 Indices",
    "4.1 Ordering decimals",
    "4.2 Multiplying decimals",
    "4.3 Dividing by decimals",
    "4.4 Making decimal calculations easier",
    "2.1 Constructing expressions",
    "2.2 Using expressions and formulae",
    "2.3 Expanding brackets",
    "2.4 Factorising",
    "2.5 Constructing and solving equations",
    "2.6 Inequalities",
    "8.1 Quadrilaterals and polygons",
    "8.2 The circumference of a circle",
    "8.3 3D shapes",
    "15.1 Converting between miles and kilometres",
    "15.2 The area of a parallelogram and a trapezium",
    "15.3 Calculating the volume of triangular prisms",
    "15.4 Calculating the surface area of triangular prisms and pyramids",
    "7.1 Fractions and recurring decimals",
    "7.2 Ordering fractions",
    "7.3 Subtracting mixed numbers",
    "7.4 Multiplying an integer by a mixed number",
    "7.5 Dividing an integer by a fraction",
    "7.6 Making fraction calculations easier",
    "13.1 Calculating probabilities",
    "13.2 Experimental and theoretical probabilities"
]

# Lesson selection sidebar
lesson_selection = st.sidebar.selectbox("Select Lesson", Math_Lesson)


#prompt_template = ""

prompt_template = load_prompt(lesson_selection)

# Clear chat session if dropdown option or radio button changes
if st.session_state.get("lesson_selection") != lesson_selection:
    st.session_state["lesson_selection"] = lesson_selection
    st.session_state["messages"] = [
        AIMessage(content="Welcome! This is the 1st Semester Grade 8 Cambridge Math Review. Say Okie once you ready")
    ]

# Display lesson name and description
st.title(f"**{lesson_selection}**")


# Message handling and interaction
def send_feedback(run_id, score):
    client.create_feedback(run_id, "user_score", score=score)

for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        model = ChatOpenAI(streaming=True, callbacks=[stream_handler], model="gpt-3.5-turbo-16k")

        chain = LLMChain(prompt=prompt_template, llm=model)

        response = chain(
            {"input": prompt, 
             "chat_history": st.session_state.messages[-2:]  # No need Chat History
            },
            include_run_info=True
        )
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.session_state.messages.append(AIMessage(content=response[chain.output_key]))
        run_id = response["__run"].run_id

        col_blank, col_text, col1, col2 = st.columns([10, 2, 1, 1])
        with col_text:
            st.text("Feedback:")

        with col1:
            st.button("👍", on_click=send_feedback, args=(run_id, 1))

        with col2:
            st.button("👎", on_click=send_feedback, args=(run_id, 0))
