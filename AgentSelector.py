# You are given the following data for agents 
# agent
# is_available
# available_since (the time since the agent is available)
# roles (a list of roles the user has, e.g. spanish speaker, sales, support etc.) 

# When an issue comes in we need to present the issue to 1 or many agents based on an agent selection mode.
# An agent selection mode can be all available, least busy or random.
#  In “all available mode” the issue is presented to all agents so they pick the issue if they want.
# In least busy the issue is presented to the agent that has been available for the longest.
# In random mode we randomly pick an agent. An issue also has one or many roles (sales/support e.g.).
# Issues are presented to agents only with matching roles.

# Please write a function that takes an input the list of agents with their data, agent selection mode and returns a list of agents the
# issue should be presented to.  

from datetime import datetime
from random import choice
import pickle


class Agent:

    def __init__(self, name, role, is_available, available_since):
        self.name = name
        self.role = role
        self.is_available = is_available
        self.available_since = available_since

    @classmethod
    def add_agents(cls):
        agent_name = str(input("Agent Name : "))
        agent_role = str(input("Agent Role : "))

        agent_is_available = int(input(
            "Select Agent is Available : \n\tPress 1 for Agent is  available, \n\tPress 2 for Agent is not available\n"))
        if agent_is_available == 1:
            agent_is_available = True
        elif agent_is_available == 2:
            agent_is_available = False
        else:
            print("please choose correct option")

        if agent_is_available == True:
            agent_available_since = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif agent_is_available == False:
            agent_available_since = "Agent is not available"

        agent = Agent(name=agent_name, role=agent_role,
                      is_available=agent_is_available, available_since=agent_available_since)

        return agent


class Issue:

    def __init__(self, selection_mode, role, is_selected, selected_by):
        self.selection_mode = selection_mode
        self.role = role
        self.is_selected = is_selected
        self.selected_by = selected_by

    @classmethod
    def add_issue(cls):
        agent_selection_mode = int(input(
            "Agent Selection mode : \n\tPress 1 for 'All available', \n\tPress 2 for 'Least busy', \n\tPress 3 for 'Random mode'\n"))

        if agent_selection_mode == 1:
            agent_selection_mode = 'All available'
        elif agent_selection_mode == 2:
            agent_selection_mode = 'Least busy'
        elif agent_selection_mode == 3:
            agent_selection_mode = 'Random mode'
        else:
            print("please choose correct option")

        issue_role = str(input("Issue Role : "))

        issue = Issue(selection_mode=agent_selection_mode,
                      role=issue_role, is_selected=False, selected_by=None)

        return issue

    @staticmethod
    def present_issue(issue):
        if issue.selection_mode == 'All available':
            for agent in agents:
                if agent.role == issue.role and agent.is_available:
                    print(
                        f"Issue of role {issue.role} is presented to {agent.name} and it's selection mode is {issue.selection_mode}")
        elif issue.selection_mode == 'Least busy':
            for i in range(len(agents) - 1):
                if agents[i].role == issue.role and agents[i].is_available:
                    longets_available = agents[0]
                    try:
                        if longets_available.available_since > agents[i+1].available_since:
                            longets_available = agents[i+1]
                    except:
                        pass
            else:
                print(
                    f"Issue of role {longets_available.role} is presented to {longets_available.name} and it's selection mode is {longets_available.selection_mode}")
        elif issue.selection_mode == 'Random mode':
            for agent in agents:
                available_agents = list()
                if agent.role == issue.role and agent.is_available:
                    available_agents.append(agent)
            else:
                try:
                    agent = choice(available_agents)
                    print(
                    f"Issue of role {issue.role}, The selected agent is {agent.name} and it's selection mode is {issue.selection_mode}")

                except:
                    pass
                


if __name__ == "__main__":
    issues = list()
    agents = list()

    try:
        with open('issue_data.pkl', 'rb') as issue_file:
            while True:
                try:
                    issues.append(pickle.load(issue_file))
                except:
                    break
    except:
        pass

    try:
        with open('agent_data.pkl', 'rb') as agent_file:
            while True:
                try:
                    agents.append(pickle.load(agent_file))
                except:
                    break
    except:
        pass

    while True:
        if len(issues) > 0:
            for issue in issues:
                if issue.is_selected == False:
                    Issue.present_issue(issue)
        try:
            selection = int(input(
                "\nPress 1 for Add agent, \nPress 2 for add issue, \nPress 3 to terminate programe\n"))
            if selection == 1:
                agent = Agent.add_agents()
                agents.append(agent)

            if selection == 2:
                issue = Issue.add_issue()
                issues.append(issue)

            if selection == 3:
                with open('agent_data.pkl', 'wb') as agent_data:
                    for agent in agents:
                        pickle.dump(agent, agent_data, pickle.HIGHEST_PROTOCOL)

                with open('issue_data.pkl', 'wb') as issue_data:
                    for issue in issues:
                        pickle.dump(issue, issue_data, pickle.HIGHEST_PROTOCOL)
                break
        except:
            print("\nPlease choose wisely!")
