from groq import Groq
from dotenv import load_dotenv
import os 
load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])

class TaskOutput:
  def __init__(self,raw_output,agent_name,task_description,task_context=None):
    self.raw_output = raw_output; 
    self.agent_name = agent_name
    self.task_descripton = task_description
    self.task_context = task_context
    
  def __str__(self):
    return(
      f"Agent: {self.agent_name}\n"
            f"Task: {self.task_descripton}\n"
            f"Output: {self.raw_output}"
    )
    

class LLM:
  def __init__(self,model_name):
    self.model_name = model_name

  def call(self,system_prompt,user_prompt):
    
    chat_completion = client.chat.completions.create(
       messages=[
         {
           "role":"system",
           "content": system_prompt
         },{
           "role":"user",
           "content": user_prompt
         }
       ],
       model=self.model_name

     )
    raw_output = chat_completion.choices[0].message.content
    return raw_output 

    
class Agents:
  def __init__(self,name,role,goal,description,tools=None):
    self.name = name  
    self.role = role
    self.goal = goal  
    self.tools = tools if tools is not None else []
    self.description = description
  
  def build_prompt(self,context=None,task=None):
    if task is not None:
      return f'''
                  Context:
                   {context}

              Task:
              {task.description}
              '''
    return  f'''
           You are a {self.role}

             Goal:
             {self.goal}

            Description:
             {self.description}           
            '''
  


  def execute(self,task): 
     if task.context:
      context = task.context.raw_output
     else:
       context = "No context"
     system_prompt = self.build_prompt()
     user_prompt = self.build_prompt(context,task)
     llm = LLM('llama-3.3-70b-versatile')
     output = llm.call(system_prompt,user_prompt)
     if task.context: 
         return TaskOutput(
           output,
           self.name,
           task.description,
           task.context
         ) 
     else:
      return TaskOutput(
         output,
         self.name,
         task.description
     )
  
class Task: 
  def __init__(self,topic,description,agent:Agents):
    self.topic = topic ; 
    self.description = description
    self.agent = agent
    self.context = None



class ExecutionEngine:
  def __init__(self):
    self.outputs=[]

  def execute_task(self,tasks:list):
     for task in tasks: 
        if self.outputs : 
            task.context = self.outputs[-1]      
        output = task.agent.execute(task)
        self.outputs.append(output)
     print(len(self.outputs))
     return self.outputs[-1]