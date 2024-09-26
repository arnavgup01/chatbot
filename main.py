import tkinter as tk
import threading
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

chatGUI = tk.Tk()
chatGUI.title("AI ChatBot")
chatGUI.geometry("800x800")
chatGUI["bg"] = "black"

#Defines how the conversation history and current question will be passed to model for generating an answer
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer: 
"""

#Doing all this allows me to invoke the model with inputs
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

context = ""

def format_text(text, max_line_length=80):
    lines = []
    while len(text) > max_line_length:
        split_index = text[:max_line_length].rfind(" ")
        if split_index == -1:  
            split_index = max_line_length
        lines.append(text[:split_index])
        text = text[split_index:].strip()
    lines.append(text)  
    return "\n".join(lines)

def button_clicked():
    def run_model():
        global context
        user_query = user_input.get()
        user_input.delete(0, tk.END)
        res = chain.invoke({"context": context, "question": user_query})
        res = format_text(str(res))  # Format the response text
        context += f"\nUser: {user_query}\nAI: {res}" 
        val["text"] = res
    
    thread = threading.Thread(target=run_model) #Using threading, it is a way for me to run multiple operations concurrently in my program
    thread.start() #The threading in my situation makes it so that AI Model's processing doesnt block my GUI

welcomeLabel = tk.Label(master=chatGUI, text="Welcome to AI ChatBot!\n" + "Please allow a few moments for a response.")
welcomeLabel.place(x=300, y=0)

val = tk.Label(chatGUI, bg="white", width=100, height=40, wraplength=700, justify="left")
val.place(x=50, y=100)

user_input = tk.Entry(master=chatGUI)
user_input.place(x=300, y=750)
confirmation_button = tk.Button(text="Send", command=button_clicked)
confirmation_button.place(x=450, y=750)

chatGUI.mainloop()
