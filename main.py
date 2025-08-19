import pandas as pd
import google.generativeai as genai
import pickle
import csv

# maybe replaced by a offline model in the future
def gemini_response(prompt_text):
    response = model.generate_content(prompt_text)
    return response.text

f = open('gemini_api.pkl', 'rb')
my_api_key = pickle.load(f)
f.close()
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')


system_logs = pd.read_csv('system_event_logs.csv')
threats = pd.read_csv('threat_intelligence.csv')
network_traffic = pd.read_csv('network_traffic.csv')

def event_log_formatter(system_logs, current_log):
    prompt = f"""
        You are an expert cybersecurity analyst.
        Analyze the following system event log data and provide a summary of any suspicious activity.
        Identify potential threats and suggest a course of action.

        Your previous knowledge includes:
        ---
        {system_logs.to_string()}
        ---

        Your current log to analyze:
        {current_log}

        Your analysis:
        to answer in Yes or No, if the log is a threat.
        not a single other word is needed.
        In the second line, provide if this log is worth logging or if it already exist or not in just one word.
        """
    
    return prompt

def reload_data():
    global system_logs, threats, traffic
    traffic = pd.read_csv('network_traffic.csv')
    system_logs = pd.read_csv('system_event_logs.csv')
    threats = pd.read_csv('threat_intelligence.csv')

def action_logger(timestamp, action, user, success, is_threat):
    log_entry = {
        'timestamp': timestamp,
        'action': action,
        'user': user,
        'success': success,
        'is_threat': is_threat
    }
    # writing into csv file
    with open('system_event_logs.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        writer.writerow(log_entry)
    return log_entry
    
if __name__ == "__main__":
    log = "2024-05-04 23:00:00,Failed Login,user1,No"
    print(event_log_formatter(system_logs, log))