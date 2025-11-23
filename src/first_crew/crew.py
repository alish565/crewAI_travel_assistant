from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from first_crew.tools.custom_tool import search_flights, hotel_data, plan_tour
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class FirstCrew():
    """FirstCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    @agent
    def flight_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['flight_search_agent'],
            tools=[search_flights],
            verbose=True
        )
    

    @agent
    def hotel_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['hotel_search_agent'], 
            tools=[hotel_data],
            verbose=True
        )
    
    @agent
    def tourism_tour_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['tourism_tour_agent'], 
            tools=[plan_tour],
            verbose=True
        )

    @agent
    def advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['advisor_agent'], 
            verbose=True
        )

    @task
    def searchin_flights(self) -> Task:
        return Task(
            config=self.tasks_config['search_flights_task'],
            verbose=True
        )

    @task
    def searching_hotels(self) -> Task:
        return Task(
            config=self.tasks_config['search_hotels_task'],
            verbose=True
        )
    
    @task
    def planning_tours(self) -> Task:
        return Task(
            config=self.tasks_config['plan_tour_task'],
            verbose=True
        )
    
    @task
    def providing_advice(self) -> Task:
        return Task(
            config=self.tasks_config['provide_advice_task'],
            verbose=True
        )
    @crew
    def crew(self) -> Crew:
        """Creates the FirstCrew crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
                                   
        )
