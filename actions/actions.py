# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from rasa_sdk.types import DomainDict
from database import *
from finalphu import fetch_cov_cases, fetch_phu_data
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
import re
import json
import ast

# Covid Vaccine GREET MESSAGE/ INTRO------------------------------------------------------------------------------->
# ---------------------------------------------------------------------------------------------------------->

class ActionCovidVaccine(Action):

    def name(self) -> Text:
        return "action_covid_vaccine"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("virus")
        if name == None:
            dispatcher.utter_message(template="utter_greet_covid", virus='Covid-19')
        elif "covid" in name.lower():
            dispatcher.utter_message(template="utter_greet_covid", virus='Covid-19')
        elif "sars" in name.lower():
            dispatcher.utter_message(template="utter_greet_covid", virus='Sars cov 2')
        return []


# GREET MESSAGE END----------------------------------------------------------------------------------------->




# ------------------------------------------------------------------------------------------------------------
# COMPOSITE PATHWAY:
#--------------------------------------------------------------------------------------------------->
global currentIntent
class ActionSubmitAll(Action):
    def name(self) -> Text:
        return "action_submit_all"
    
    def utter_response(self, first, second, no_dose, currentIntent):
        if currentIntent == 'vaccine_side_effect':
            messages= "utter_vaccine_side_effect"
        elif currentIntent == 'covid_symptoms':
            messages ="utter_covid_symptoms"
        elif currentIntent == 'vaccine_infection':
            messages ="utter_infection"
        elif currentIntent == 'avoid_second_dose':
            messages ="utter_avoid_second_dose"
        elif currentIntent == 'long_term_implications':
            messages ="utter_long_term_implications"
        elif currentIntent == 'delay_vaccination_decision':
            messages ="utter_delay_vaccination_decision"
        elif currentIntent == 'vaccine_doses':
            messages ="utter_vaccine_doses"
        elif currentIntent == 'vaccine_work':
            messages ="utter_vaccine_work"
        elif currentIntent == 'vaccine_approval':
            messages ="utter_vaccine_approval"
        elif currentIntent == 'after_vaccine_precautions':
            messages="utter_after_vaccine_precautions"
        elif currentIntent == 'vaccine_efficacy':
            messages="utter_efficacy"
        elif currentIntent == 'vaccine_safety':
            messages ="utter_safety"
        elif currentIntent == 'side_effect_second_dose':
            messages="utter_side_effect_second_dose"
        elif currentIntent == 'serious_side_effect':
            messages="utter_serious_side_effect"
        elif currentIntent == 'call_the_doctor':
            messages="utter_call_the_doctor"
        elif currentIntent == 'vaccine_pregnancy':
            messages ="utter_vaccine_pregnancy"
        elif currentIntent == 'vaccine_breast_feeding':
            messages ="utter_vaccine_breast_feeding"
        elif currentIntent == 'vaccine_protection':
            messages ="utter_protection"
        elif currentIntent == 'vaccination_kids':
            messages ="utter_kids_vaccination"
        elif currentIntent == 'vaccine_death':
            messages ="utter_vaccine_deaths"
        elif currentIntent == 'covid_vs_flu_vac':
            messages ="utter_cov_vs_flu"
        elif currentIntent == 'vaccine_access':
            messages ="utter_vaccine_access"
        elif currentIntent == 'vaccine_cases':
            messages ="utter_vaccine_cases"
        elif currentIntent == "scared_second_dose":
            messages = "utter_side_effect_second_dose"
        elif currentIntent == "general_affirm":
            messages = "utter_general_affirm"
        return messages

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> List[Dict[Text, Any]]:
        required_slots = Select_Age(tracker.sender_id)
        gender = Select_Gender(tracker.sender_id)
        gender = gender[0]
        print(required_slots)
        print('gender is ', gender)
        first = Select_First_Dose(tracker.sender_id)[0][0]
        second = Select_Both_Dose(tracker.sender_id)[0][0]
        no_dose = Select_No_Dose(tracker.sender_id)[0][0]   
        print('first ', first)
        print('both ', second) 
        print('no_dose ', no_dose) 
        print(required_slots)
        print('gender is ', gender)
        event = tracker.events
        print(event)
        global currentIntent
        global second_last
        global third_last
        global fourth_last
        global fifth_last
        second_last = third_last = fourth_last = fifth_last = ' '
        temp = []
        for e in event:
            if e["event"] == 'user':
                temp.append(e)
        e = temp[-1]      
        currentIntent = e["parse_data"]["intent"]["name"]
        if len(temp) > 1:
            s_l = temp[-2]
            second_last = s_l["parse_data"]["intent"]["name"]
        if len(temp) > 2:  
            t_l = temp[-3]
            third_last =  t_l["parse_data"]["intent"]["name"]
        if len(temp) > 3: 
            f_l = temp[-4]
            fourth_last = f_l["parse_data"]["intent"]["name"]
        if len(temp) > 4:
            fif_l = temp[-5]
            fifth_last = fif_l["parse_data"]["intent"]["name"]
        print(tracker.events)
        print(currentIntent)
        if required_slots == ['There are no resources matching your query.']:
            dispatcher.utter_message(template="utter_vaccine_efficacy")
        elif gender == 'There are no resources matching your query.':
            buttons = [
            {"payload": '/gender{"gend":"Female"}', "title": "Female"},
            {"payload": '/gender{"gend":"Male"}', "title": "Male"},
            {"payload": '/gender{"gend":"Other"}', "title": "Other"},
            {"payload": '/gender{"gend":"Do not wish to disclose"}', "title": "Do not wish to disclose"}
        ]
            dispatcher.utter_message(text="To assist you better, Can we please know your gender?", buttons=buttons)    
        elif currentIntent == 'high_risk_vaccination':
            dispatcher.utter_message(template="utter_high_risk_vaccination")
            buttons = [
            {"payload": '/affirm_long_term{"affirm_l_t":"Yes"}', "title": "Yes"},
            {"payload": '/affirm_long_term{"affirm_l_t":"No"}', "title": "No"}
        ]
            dispatcher.utter_message(text="Would you like to know the long term implications of your decision of not getting vaccinated?", buttons=buttons)
        elif currentIntent == 'vaccine_ingredients':
            buttons = [
            {"payload": '/vaccine_kind{"vaccine_type":"Pfizer"}', "title": "Pfizer"},
            {"payload": '/vaccine_kind{"vaccine_type":"Moderna"}', "title": "Moderna"},
            {"payload": '/vaccine_kind{"vaccine_type":"Astrazeneca"}', "title": "Astrazeneca/ Covishield"},
            {"payload": '/vaccine_kind{"vaccine_type":"Johnson&Johnson"}', "title": "Johnson&Johnson"}
        ]
            dispatcher.utter_message(template="utter_vaccine_ingredients", buttons = buttons)
        elif (currentIntent == "vaccine_access" or currentIntent == "vaccine_cases"):
            messages = self.utter_response(first, second, no_dose, currentIntent)
            dispatcher.utter_message(template= messages)
        elif currentIntent == 'goodbye':
            buttons = [
            {"payload": '/general_affirm_feed{"g_affirm":"Yes"}', "title": "Yes"},
            {"payload": '/general_affirm_feed{"g_affirm":"No"}', "title": "No"}
        ]
            dispatcher.utter_message(template="utter_goodbye", buttons = buttons)
        elif currentIntent == "general_affirm_feed" or second_last == 'goodbye':
            affirm_state = tracker.get_slot("g_affirm")
            affirm_state = affirm_state.lower()
            msgs = list(tracker.latest_message.values())[2] 
            msgs = msgs.lower()
            if affirm_state != None:
                feedback_1 = affirm_state
            else:
                feedback_1 = msgs
            Update_Feedback_info1(tracker.sender_id, feedback_1)
            if "yes" in feedback_1 or "sure" in feedback_1:
                buttons = [
                {"payload": '/general_affirm_v1{"g_affirm_v1":"Yes"}', "title": "Yes"},
                {"payload": '/general_affirm_v1{"g_affirm_v1":"No"}', "title": "No"}
                ]
                dispatcher.utter_message(text= "Did we answer all your questions that you had on your mind today? Please choose one of the options or if you choose to type in your answer please type in 'Yes' or 'No' along with your feedback.", buttons= buttons)
            elif "no" in feedback_1:
                dispatcher.utter_message(text="Thank you for reaching out to us today. We are glad we were able to able to assist you today. Have a nice day.")            
        elif currentIntent == "general_affirm_v1" or second_last == "general_affirm_feed" or third_last == "goodbye":
            affirm_state = tracker.get_slot("g_affirm_v1")
            affirm_state = affirm_state.lower()
            msgs = list(tracker.latest_message.values())[2]
            msgs.lower()
            print('MSGS ', msgs)
            if affirm_state != None:
                feedback_2 = affirm_state 
            else:
                feedback_2 = msgs
            Update_Feedback_info2(tracker.sender_id, feedback_2) 
            if "yes" in feedback_2 or "sure" in feedback_2:
                buttons = [
                {"payload": '/general_affirm_v2{"g_affirm_v2":"Yes"}', "title": "Yes"},
                {"payload": '/general_affirm_v2{"g_affirm_v2":"No"}', "title": "No"}
            ]
                dispatcher.utter_message(text= "Was the vaccine assistant easy to use? Please choose one of the options or if you choose to type in your answer please type in 'Yes' or 'No' along with your feedback.", buttons = buttons)
            elif "no" in feedback_2:
                buttons = [
                {"payload": '/content_level{"discont":"Takes a long time, inefficient"}', "title": "Takes a long time, inefficient"},
                {"payload": '/content_level{"discont":"Did not understand my questions"}', "title": "Did not understand my questions"},
                {"payload": '/content_level{"discont":"Not friendly to use"}', "title": "Not friendly to use"},
                {"payload": '/content_level{"discont":"Prefer to speak with live agent"}', "title": "Prefer to speak with live agent"} 
            ]
                dispatcher.utter_message(text="Please choose one of the options to let us know why you were discontent with the chat service?", buttons = buttons)            
        elif currentIntent == "general_affirm_v2" or second_last == "general_affirm_v1" or third_last == "general_affirm_feed" or fourth_last == "goodbye":
            affirm_state = tracker.get_slot("g_affirm_v2")
            affirm_state = affirm_state.lower()
            msgs = list(tracker.latest_message.values())[2]
            msgs.lower()
            print('MSGS ', msgs)
            if affirm_state != None:
                feedback_3 = affirm_state 
            else:
                feedback_3 = msgs
            Update_Feedback_info3(tracker.sender_id, feedback_3) 
            if "yes" in feedback_3 or "sure" in feedback_3:
                buttons = [
                {"payload": '/content_level{"discont":"Takes a long time, inefficient"}', "title": "Takes a long time, inefficient"},
                {"payload": '/content_level{"discont":"Did not understand my questions"}', "title": "Did not understand my questions"},
                {"payload": '/content_level{"discont":"Not friendly to use"}', "title": "Not friendly to use"},
                {"payload": '/content_level{"discont":"Prefer to speak with live agent"}', "title": "Prefer to speak with live agent"},
                {"payload": '/content_level{"discont":"Friendly and helpful, answered all my questions"}', "title": "Friendly and helpful, answered all my questions"},
                {"payload": '/content_level{"discont":"Fast and convenient, answered my questions"}', "title": "Fast and convenient, answered my questions"},
                {"payload": '/content_level{"discont":"Answered my questions"}', "title": "Answered my questions"},
                {"payload": '/content_level{"discont":"Answered most of my questions"}', "title": "Answered most of my questions"}
            ]
                dispatcher.utter_message(text= "Kindly choose one of the options to let us know how your overall user experience was to use the assistant today?", buttons = buttons)
            elif "no" in feedback_3:
                buttons = [
                {"payload": '/content_level{"discont":"Takes a long time, inefficient"}', "title": "Takes a long time, inefficient"},
                {"payload": '/content_level{"discont":"Did not understand my questions"}', "title": "Did not understand my questions"},
                {"payload": '/content_level{"discont":"Not friendly to use"}', "title": "Not friendly to use"},
                {"payload": '/content_level{"discont":"Prefer to speak with live agent"}', "title": "Prefer to speak with live agent"},
            ]
                dispatcher.utter_message(text="Please choose one of the options to let us know why you were discontent with the chat service?", buttons = buttons)        
        elif currentIntent == "content_level" or second_last == "general_affirm_v2" or third_last == "general_affirm_v1" or fourth_last == "general_affirm_feed" or fifth_last == "goodbye":
            contentm = tracker.get_slot("discont")
            contentm = contentm.lower()
            msgs = list(tracker.latest_message.values())[2]
            print('MSGS ', msgs)
            if contentm != None:
                feedback_4 = contentm 
            else:
                feedback_4 = msgs
            Update_Feedback_info4(tracker.sender_id, feedback_4)
            dispatcher.utter_message(text="Thank you for taking the time to provide us your feedback to help us improve in our efforts to make our services better. Have a nice day.")            
        elif (first == None and second == None and no_dose == None):
            dispatcher.utter_message(text=f"Thank you for letting us know about yourself.")
            messages = self.utter_response(first, second, no_dose, currentIntent)
            dispatcher.utter_message(template=messages)
            dispatcher.utter_message(template= "utter_vaccine_taken")
        else:
            print('Current intent is ', currentIntent)
            messages = self.utter_response(first, second, no_dose, currentIntent)
            print('Messages is ,', messages)
            dispatcher.utter_message(template= messages)
        return []


# AGE PATH
# ----------------------------------------------------------------------------------------------------------
class ActionSubmitAge(Action):
    def name(self) -> Text:
        return "action_submit_age"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(currentIntent)
        global age_s
        age_s = tracker.get_slot("age")
        print(int(age_s))
        print(currentIntent)
        if int(age_s) < 12:
            dispatcher.utter_message(text="Vaccine is currently administered only in ages 12 and above. Those who are of age 12 and above are eligible to get Pfizer-BioNTech vaccine. Those who are of age 18 and above are eligible to get Moderna, Astrazeneca and Johnson&Johnson vaccines. So far, a vaccine has not been approved for children. Research is underway to determine when those under the authorized ages can receive the vaccine. We appreciate your patience and understanding in this matter.")
        else:
            buttons = [
            {"payload": '/gender{"gend":"Female"}', "title": "Female"},
            {"payload": '/gender{"gend":"Male"}', "title": "Male"},
            {"payload": '/gender{"gend":"Other"}', "title": "Other"},
            {"payload": '/gender{"gend":"Do not wish to disclose"}', "title": "Do not wish to disclose"}
        ]
            dispatcher.utter_message(text="To assist you better, Can we please know your gender?", buttons=buttons)
        DataUpdate(tracker.sender_id, int(tracker.get_slot('age')), currentIntent)
        return []
    # AGE PATH END----------------------------------------------------------------------------------------------


#GENDER ACTION PATH
#_______________________________________________________________________________________________________________

class ActionSubmitAllGender(Action):
    def name(self) -> Text:
        return "action_submit_all_gender"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(currentIntent)
        gender = tracker.get_slot("gend")
        first = Select_First_Dose(tracker.sender_id)[0][0]
        second = Select_Both_Dose(tracker.sender_id)[0][0]
        no_dose = Select_No_Dose(tracker.sender_id)[0][0] 
        print(currentIntent)
        print('both ', second) 
        print('first ', first)
        print('second ', second)
        print('no_dose ', no_dose)
        Update_Gender(tracker.sender_id, gender)
        if currentIntent == 'high_risk_vaccination':
            dispatcher.utter_message(template="utter_high_risk_vaccination")
            buttons = [
            {"payload": '/affirm_long_term{"affirm_l_t":"Yes"}', "title": "Yes"},
            {"payload": '/affirm_long_term{"affirm_l_t":"No"}', "title": "No"}
        ]
            dispatcher.utter_message(text="Would you like to know the long term implications of your decision of not getting vaccinated?", buttons=buttons)
        elif currentIntent == 'vaccine_ingredients':
            buttons = [
            {"payload": '/vaccine_kind{"vaccine_type":"Pfizer"}', "title": "Pfizer"},
            {"payload": '/vaccine_kind{"vaccine_type":"Moderna"}', "title": "Moderna"},
            {"payload": '/vaccine_kind{"vaccine_type":"Astrazeneca"}', "title": "Astrazeneca/ Covishield"},
            {"payload": '/vaccine_kind{"vaccine_type":"Johnson&Johnson"}', "title": "Johnson&Johnson"}
        ]
            dispatcher.utter_message(template="utter_vaccine_ingredients", buttons = buttons)
        elif (currentIntent == "vaccine_access" or currentIntent == "vaccine_cases"):
            messages = ActionSubmitAll.utter_response(self, first, second, no_dose, currentIntent)
            dispatcher.utter_message(template= messages)
        elif currentIntent == 'goodbye':
            buttons = [
            {"payload": '/general_affirm_feed{"g_affirm":"Yes"}', "title": "Yes"},
            {"payload": '/general_affirm_feed{"g_affirm":"No"}', "title": "No"}
        ]
            dispatcher.utter_message(template="utter_goodbye", buttons = buttons)
        elif currentIntent == "general_affirm_feed" or second_last == 'goodbye':
            affirm_state = tracker.get_slot("g_affirm")
            affirm_state = affirm_state.lower()
            msgs = list(tracker.latest_message.values())[2] 
            msgs = msgs.lower()
            if affirm_state != None:
                feedback_1 = affirm_state
            else:
                feedback_1 = msgs
            Update_Feedback_info1(tracker.sender_id, feedback_1)
            
            if "yes" in feedback_1 or "sure" in feedback_1:
                buttons = [
                {"payload": '/general_affirm_v1{"g_affirm_v1":"Yes"}', "title": "Yes"},
                {"payload": '/general_affirm_v1{"g_affirm_v1":"No"}', "title": "No"}
                ]
                dispatcher.utter_message(text= "Did we answer all your questions that you had on your mind today?", buttons= buttons)
            elif "no" in feedback_1:
                dispatcher.utter_message(text="Thank you for reaching out to us today. We are glad we were able to able to assist you today. Have a nice day.")            
        elif currentIntent == "general_affirm_v1" or second_last == "general_affirm_feed" or third_last == "goodbye":
            affirm_state = tracker.get_slot("g_affirm_v1")
            affirm_state = affirm_state.lower()
            msgs = list(tracker.latest_message.values())[2]
            msgs.lower()
            print('MSGS ', msgs)
            if affirm_state != None:
                feedback_2 = affirm_state 
            else:
                feedback_2 = msgs
            Update_Feedback_info2(tracker.sender_id, feedback_2) 
            if "yes" in feedback_2 or "sure" in feedback_2:
                buttons = [
                {"payload": '/general_affirm_v2{"g_affirm_v2":"Yes"}', "title": "Yes"},
                {"payload": '/general_affirm_v2{"g_affirm_v2":"No"}', "title": "No"}
            ]
                dispatcher.utter_message(text= "Was the vaccine assistant easy to use?", buttons = buttons)
            elif "no" in feedback_2:
                buttons = [
                {"payload": '/content_level{"discont":"Takes a long time, inefficient"}', "title": "Takes a long time, inefficient"},
                {"payload": '/content_level{"discont":"Did not understand my questions"}', "title": "Did not understand my questions"},
                {"payload": '/content_level{"discont":"Not friendly to use"}', "title": "Not friendly to use"},
                {"payload": '/content_level{"discont":"Prefer to speak with live agent"}', "title": "Prefer to speak with live agent"} 
            ]
                dispatcher.utter_message(text="Please choose one of the options to let us know why you were discontent with the chat service?", buttons = buttons)            
        elif currentIntent == "general_affirm_v2" or second_last == "general_affirm_v1" or third_last == "general_affirm_feed" or fourth_last == "goodbye":
            affirm_state = tracker.get_slot("g_affirm_v2")
            affirm_state = affirm_state.lower()
            msgs = list(tracker.latest_message.values())[2]
            msgs.lower()
            print('MSGS ', msgs)
            if affirm_state != None:
                feedback_3 = affirm_state 
            else:
                feedback_3 = msgs
            Update_Feedback_info3(tracker.sender_id, feedback_3) 
            if "yes" in feedback_3 or "sure" in feedback_3:
                buttons = [
                {"payload": '/content_level{"discont":"Takes a long time, inefficient"}', "title": "Takes a long time, inefficient"},
                {"payload": '/content_level{"discont":"Did not understand my questions"}', "title": "Did not understand my questions"},
                {"payload": '/content_level{"discont":"Not friendly to use"}', "title": "Not friendly to use"},
                {"payload": '/content_level{"discont":"Prefer to speak with live agent"}', "title": "Prefer to speak with live agent"},
                {"payload": '/content_level{"discont":"Friendly and helpful, answered all my questions"}', "title": "Friendly and helpful, answered all my questions"},
                {"payload": '/content_level{"discont":"Fast and convenient, answered my questions"}', "title": "Fast and convenient, answered my questions"},
                {"payload": '/content_level{"discont":"Answered my questions"}', "title": "Answered my questions"},
                {"payload": '/content_level{"discont":"Answered most of my questions"}', "title": "Answered most of my questions"}
            ]
                dispatcher.utter_message(text= "Kindly choose one of the options to let us know how your overall user experience was to use the assistant today?", buttons = buttons)
            elif "no" in feedback_3:
                buttons = [
                {"payload": '/content_level{"discont":"Takes a long time, inefficient"}', "title": "Takes a long time, inefficient"},
                {"payload": '/content_level{"discont":"Did not understand my questions"}', "title": "Did not understand my questions"},
                {"payload": '/content_level{"discont":"Not friendly to use"}', "title": "Not friendly to use"},
                {"payload": '/content_level{"discont":"Prefer to speak with live agent"}', "title": "Prefer to speak with live agent"},
            ]
                dispatcher.utter_message(text="Please choose one of the options to let us know why you were discontent with the chat service?", buttons = buttons)        
        elif currentIntent == "content_level" or second_last == "general_affirm_v2" or third_last == "general_affirm_v1" or fourth_last == "general_affirm_feed" or fifth_last == "goodbye":
            contentm = tracker.get_slot("discont")
            contentm = contentm.lower()
            msgs = list(tracker.latest_message.values())[2]
            print('MSGS ', msgs)
            if contentm != None:
                feedback_4 = contentm 
            else:
                feedback_4 = msgs
            Update_Feedback_info4(tracker.sender_id, feedback_4)
            dispatcher.utter_message(text="Thank you for taking the time to provide us your feedback to help us improve in our efforts to make our services better. Have a nice day.")                       
        elif (first == None and second == None and no_dose == None):
            dispatcher.utter_message(text=f"Thank you for letting us know about yourself.")
            messages = ActionSubmitAll.utter_response(self, first, second, no_dose, currentIntent)
            dispatcher.utter_message(template=messages)
            dispatcher.utter_message(template= "utter_vaccine_taken")
        else:
            print('CurrentIntent is', currentIntent)
            messages = ActionSubmitAll.utter_response(self, first, second, no_dose, currentIntent)
            dispatcher.utter_message(template= messages)
        return []
        
#LONG TERM CHILD PATH
#-------------------------------------------------------------------------------------------------------->
class ActionSubmitLongTermChildPath(Action):
    def name(self) -> Text:
        return "action_submit_long_term_child_path"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(currentIntent)
        affirm_long = tracker.get_slot("affirm_l_t")
        first = Select_First_Dose(tracker.sender_id)[0][0]
        second = Select_Both_Dose(tracker.sender_id)[0][0]
        no_dose = Select_No_Dose(tracker.sender_id)[0][0]   
        print('both ', second)  
        print('first ', first)
        print('second ', second)
        print('no_dose ', no_dose)
        print('affirm long', affirm_long)
        if affirm_long == "Yes" and (first == [None] and second == [None] and no_dose == [None]):
            dispatcher.utter_message(template="utter_long_term_implications")
            dispatcher.utter_message(template="utter_vaccine_taken")
        elif affirm_long == "Yes":
            dispatcher.utter_message(template="utter_long_term_implications")
        elif (first == [None] and second == [None] and no_dose == [None]):
            dispatcher.utter_message(template="utter_vaccine_taken")
            dispatcher.utter_message(text="Is there anything else we can assist you with today regarding any concerns you may have regarding the Covid vaccine?")
        else:
            dispatcher.utter_message(text="Is there anything else we can assist you with today regarding any concerns you may have regarding the Covid vaccine?")

        return []

#LONG TERM CHILD PATH ENDS________________________________________________________________________________>
#-------------------------------------------------------------------------------------------------------->
# HIGH RISK PATHWAY END
#-------------------------------------------------------------------------------------------------------->


# Vaccine Information: First Dose, Second Dose, Vaccine Taken (Pfizer, Moderna, Johnson&Johnson)
# --------------------------------------------------------------------------------------------------------->

class ActionSubmitVaccineInfo_v1(Action):
    def name(self) -> Text:
        return "action_first_dose"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"payload": '/vaccine_received{"vac_rec":"Pfizer"}', "title": "Pfizer"},
            {"payload": '/vaccine_received{"vac_rec":"Moderna"}', "title": "Moderna"},
            {"payload": '/vaccine_received{"vac_rec":"Astrazenca"}', "title": "Astrazeneca/ Covishield"},
            {"payload": '/vaccine_received{"vac_rec":"Johnson&Johnson"}', "title": "Johnson&Johnson"}
        ]
        # print(currentIntent)
        dispatcher.utter_message(text= "Which vaccine did you get?", buttons = buttons)
        Update_first_dose_info(tracker.sender_id)
        return []


class ActionSubmitVaccineInfo_v2(Action):
    def name(self) -> Text:
        return "action_both_dose"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(currentIntent)
        buttons = [
            {"payload": '/vaccine_received{"vac_rec":"Pfizer"}', "title": "Pfizer"},
            {"payload": '/vaccine_received{"vac_rec":"Moderna"}', "title": "Moderna"},
            {"payload": '/vaccine_received{"vac_rec":"Astrazenca"}', "title": "Astrazeneca/ Covishield"},
            {"payload": '/vaccine_received{"vac_rec":"Johnson&Johnson"}', "title": "Johnson&Johnson"}
        ]
        # print(currentIntent)
        dispatcher.utter_message(text= "That's great! Do you have any questions about the vaccine and precautions to taken after your vaccination? Also will you please let us know which vaccine did you get so we can better assist you with any other concerns you may have.", buttons = buttons)
        Update_both_dose_info(tracker.sender_id)
        return []

class ActionSubmitVaccineInfo_v3(Action):
    def name(self) -> Text:
        return "action_no_dose"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(currentIntent)
        dispatcher.utter_message(template="utter_deny_dose")
        Update_no_dose_info(tracker.sender_id)
        return []


class ActionSubmitVaccineInfo_v4(Action):
    def name(self) -> Text:
        return "action_vac_info"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(currentIntent)
        vaccine_name = tracker.get_slot("vac_rec")
        vaccine_name = str(vaccine_name)
        print('vaccine name is: ', vaccine_name)
        Update_vaccine_info(tracker.sender_id, vaccine_name)
        first = Select_First_Dose(tracker.sender_id)[0][0]
        second = Select_Both_Dose(tracker.sender_id)[0][0]
        no_dose = Select_No_Dose(tracker.sender_id)[0][0]   
        print('both ', second)  
        print('first ', first)
        print('second ', second)
        print('no_dose ', no_dose)
        if "pfizer" in vaccine_name.lower() or "moder" in vaccine_name.lower() or "astra" in vaccine_name.lower() or "covish" in vaccine_name.lower():
            if first != None:
                dispatcher.utter_message(template="utter_vaccine_pfizer_moderna")
            elif second != None:
                dispatcher.utter_message(text= "Thank you for providing us the information. Please let us know your question or concerns about the vaccine and we will be happy to assist you.")
        elif "john" in vaccine_name.lower():
            dispatcher.utter_message(template="utter_vaccine_j&j")
        return []


# Vaccine Information: END
# ---------------------------------------------------------------------------------------------------------->

# Region & Vaccine Access Info
# ----------------------------------------------------------------------------------------------------------->

class ActionSubmitRegion(Action):
    def name(self) -> Text:
        return "action_submit_region"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(currentIntent)
        global regions
        regions = tracker.get_slot("phu")
        last_message = tracker.latest_message.get("text", "")
        print('LAST MESSAGE ', last_message)
        print('regions is ', regions)
        print(currentIntent)
        #regions = last_message
        if currentIntent == 'vaccine_access':
            region_inf = fetch_phu_data(regions)
            print(region_inf)
            phu = region_inf[0][0]
            web_inf = region_inf[0][1]
            print(phu, web_inf)
            first = Select_First_Dose(tracker.sender_id)[0][0]
            second = Select_Both_Dose(tracker.sender_id)[0][0]
            no_dose = Select_No_Dose(tracker.sender_id)[0][0] 
            print('first ', first)
            print('both ', second) 
            print('no_dose ', no_dose)
            if phu and (first == None and second == None and no_dose == None):
                dispatcher.utter_message(text=f"Thank you for contacting us today. You have requested information for {phu} and you can access the website for your Public health unit by going on the particular link {web_inf} to gain further information about the vaccination clinics in your area.")
                dispatcher.utter_message(template="utter_vaccine_taken")
            elif phu:
                dispatcher.utter_message(text=f"You have requested information for {phu} and you can access the website for your Public health unit by going on the particular link {web_inf} to gain further information about the vaccination clinics in your area.")
            else: 
                dispatcher.utter_message(text= f"Sorry that Public health unit is not found. Please enter the correct name of the Public health unit to allow us to help you find the nearest Public health unit close to your region.")
            Update_region_info_Access(tracker.sender_id, regions)

            return []
        elif currentIntent == 'vaccine_cases':
            region_inf = fetch_cov_cases(regions)
            print(region_inf)
            phu = region_inf[0][0]
            active = region_inf[0][1]
            resolved = region_inf[0][2]
            deaths = region_inf[0][3]
            print(phu, active, resolved, deaths)
            first = Select_First_Dose(tracker.sender_id)[0][0]
            second = Select_Both_Dose(tracker.sender_id)[0][0]
            no_dose = Select_No_Dose(tracker.sender_id)[0][0]   
            print('both ', second) 
            if phu and (first == None and second == None and no_dose == None):
                dispatcher.utter_message(text=f"Thank you for contacting us today. You have requested information for {phu} and the total number of active cases in your area are {active}, the number of resolved cases are {resolved} and total number of deaths in your region due to Covid are {deaths}.")
                dispatcher.utter_message(template="utter_vaccine_taken")
            elif phu:
                dispatcher.utter_message(text=f"You have requested information for {phu} and the total number of active cases in your area are {active}, the number of resolved cases are {resolved} and total number of deaths in your region due to Covid are {deaths}.")
            else: 
                dispatcher.utter_message(text= f"Sorry that Public health unit is not found. Please enter the correct name to allow us to help you find the nearest Public health unit close to your region.")
            Update_region_info_Cases(tracker.sender_id, regions)

            return []

# Region and Vaccine Access Info END----------------------------------------------------------------------->
# --------------------------------------------------------

# INGREDIENTS AND VACCINE TYPE
#_________________________________________________________________________________________________________
class ActionSubmitIngredientsType(Action):
    def name(self) -> Text:
        return "action_submit_ingredients_type"

    async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(currentIntent)
        vac_type = tracker.get_slot("vaccine_type")
        first = Select_First_Dose(tracker.sender_id)[0][0]
        second = Select_Both_Dose(tracker.sender_id)[0][0]
        no_dose = Select_No_Dose(tracker.sender_id)[0][0] 
        print('both ', second) 
        print('first ', first)
        print('second ', second)
        print('no_dose ', no_dose)
        print('VAC Type', vac_type)
        if vac_type == 'Pfizer' and (first == None and second == None and no_dose == None):
            dispatcher.utter_message(text=f"Thank you for providing the information.")
            dispatcher.utter_message(template="utter_pfizer_ingredients")
            dispatcher.utter_message(template="utter_vaccine_taken")
        elif vac_type == 'Moderna' and (first == None and second == None and no_dose == None):
            dispatcher.utter_message(text=f"Thank you for providing the information.")
            dispatcher.utter_message(template="utter_moderna_ingredients")
            dispatcher.utter_message(template="utter_vaccine_taken")
        elif vac_type == 'Johnson&Johnson' and (first == None and second == None and no_dose == None):
            dispatcher.utter_message(text=f"Thank you for providing the information.")
            dispatcher.utter_message(template="utter_j&j_ingredients")
            dispatcher.utter_message(template="utter_vaccine_taken")
        elif vac_type == 'Astrazeneca' and (first == None and second == None and no_dose == None):
            dispatcher.utter_message(text=f"Thank you for providing the information.")
            dispatcher.utter_message(template="utter_astrazeneca_ingredients")
            dispatcher.utter_message(template="utter_vaccine_taken")
        elif vac_type == 'Pfizer':
            dispatcher.utter_message(template="utter_pfizer_ingredients")
        elif vac_type == 'Moderna':
            dispatcher.utter_message(template="utter_moderna_ingredients")
        elif vac_type == 'Johnson&Johnson':
            dispatcher.utter_message(template="utter_j&j_ingredients")
        elif vac_type == 'Astrazeneca':
            dispatcher.utter_message(template="utter_astrazeneca_ingredients")
        else:
            dispatcher.utter_message(text=f"Sorry, I can not understand your response. Please enter the correct vaccine name.")
            dispatcher.utter_message(template="utter_vaccine_ingredients")

        return []





