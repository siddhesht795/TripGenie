# activity_utils.py
import os
import json
import re
import random
from datetime import datetime, timedelta
from config import GOOGLE_API_KEY
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def clean_and_parse_json(json_string):
    """Helper function to clean and parse JSON strings from Gemini responses"""
    try:
        # Remove markdown code blocks if present
        json_string = re.sub(r'^```json|```$', '', json_string, flags=re.MULTILINE).strip()
        
        # Sometimes Gemini adds explanatory text before/after the JSON
        # Try to extract the first valid JSON object/array
        json_match = re.search(r'(\[.*\]|\{.*\})', json_string, re.DOTALL)
        if json_match:
            json_string = json_match.group(1)
        
        return json.loads(json_string)
    except (json.JSONDecodeError, AttributeError) as e:
        raise ValueError(f"Failed to parse JSON: {str(e)}. Original text: {json_string[:200]}...")

def get_daywise_activities(destination, start_date, end_date):
    """
    Fetch day-wise activities for the given destination using Google's Generative AI.
    Includes rest days (1 rest day per 5 days) and ensures unique activities each day.
    Randomly assigns 2 or 3 activities per day, ensuring no duplicate times of day.
    Generates unique descriptions for each activity.
    Ensures rest days are spread across the trip and not consecutive.
    """
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end - start).days + 1

    if total_days <= 0:
        print("❌ No valid days for activities.")
        return [{"date": "No valid days for activities", "activities": ["Travel days only."]}]

    # Calculate rest days (1 per 5 days, rounded down)
    rest_days = total_days // 5
    rest_days = min(rest_days, total_days - 1)  # Ensure at least one activity day remains

    # Generate rest days spread across the trip
    rest_day_indices = []
    if rest_days > 0:
        interval = total_days // (rest_days + 1)  # Spread rest days evenly
        for i in range(1, rest_days + 1):
            rest_day_indices.append(i * interval)
    rest_day_indices = sorted(set(rest_day_indices))  # Ensure no duplicates

    activities_by_day = []
    used_activities = set()  # Track used activities to avoid duplicates
    all_activity_types = set()  # Track types of activities for variety

    # First get a master list of all possible activities for the destination
    master_prompt = f"""Generate a comprehensive list of 30-40 unique attractions and activities in {destination}, 
    categorized by type (landmark, museum, park, cultural experience, etc.). 
    Include a mix of well-known and off-the-beaten-path options.
    Format as JSON with fields: 'name', 'description', 'type', 'best_time_to_visit'."""

    try:
        print("Fetching master list of activities...")
        master_response = model.generate_content(
            master_prompt,
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 2000,
            }
        )
        
        if master_response.candidates and master_response.candidates[0].content.parts:
            master_text = master_response.candidates[0].content.parts[0].text
            try:
                master_activities = clean_and_parse_json(master_text)
                if not isinstance(master_activities, list):
                    raise ValueError("Master list is not a JSON array")
            except ValueError as e:
                print(f"❌ Error parsing master list: {str(e)}")
                master_activities = []
        else:
            print("❌ No valid response for master list")
            master_activities = []
    except Exception as e:
        print(f"❌ Error fetching master list: {str(e)}")
        master_activities = []

    # Process each day
    for day in range(total_days):
        current_date = start + timedelta(days=day)
        formatted_date = current_date.strftime("%B %d, %Y")

        # Handle rest days
        if day in rest_day_indices:
            print(f"🛌 Adding rest day for {formatted_date}")
            activities_by_day.append({
                "date": formatted_date,
                "activities": ["🛌 Rest Day: Take time to relax and recharge."],
                "is_rest_day": True
            })
            continue

        # Randomly decide the number of activities for the day (2 or 3)
        num_activities = random.choice([2, 3])

        # Select activities for this day
        print(f"Fetching activities for {formatted_date}...")
        day_activities = []
        used_times_of_day = set()  # Track times of day to avoid duplicates (morning, afternoon, evening)
        attempts = 0
        max_attempts = 3
        
        while len(day_activities) < num_activities and attempts < max_attempts:
            attempts += 1
            
            # Try to get activities from our master list first
            if master_activities:
                random.shuffle(master_activities)
                for activity in master_activities:
                    time_of_day = activity.get("best_time_to_visit", "Anytime").lower()
                    if (activity.get("name") not in used_activities and 
                        activity.get("type") not in all_activity_types and
                        time_of_day not in used_times_of_day):
                        
                        # Generate a unique description for the activity
                        unique_description = f"{activity.get('description', 'No description')} This is a must-visit spot in {destination} for its {activity.get('type', 'unique features')}."
                        
                        day_activities.append({
                            "name": activity.get("name", "Unknown"),
                            "description": unique_description,
                            "reason_to_visit": activity.get("reason_to_visit", "Unique experience"),
                            "best_time_to_visit": activity.get("best_time_to_visit", "Anytime"),
                            "rest_period": "1-2 hours between activities"
                        })
                        used_activities.add(activity.get("name"))
                        all_activity_types.add(activity.get("type"))
                        used_times_of_day.add(time_of_day)
                        
                        if len(day_activities) >= num_activities:
                            break
            
            # If we still need more activities, query Gemini
            if len(day_activities) < num_activities:
                activity_types_needed = num_activities - len(day_activities)
                prompt = f"""Suggest {activity_types_needed} unique activities in {destination} that haven't been mentioned yet.
                Focus on {["landmarks", "cultural experiences", "local hidden gems"][day % 3]} today.
                Each should include name, description, reason_to_visit, best_time_to_visit, and rest_period.
                Ensure no duplicate times of day (morning, afternoon, evening).
                Format as JSON array. Do not repeat any activities."""
                
                try:
                    response = model.generate_content(
                        prompt,
                        generation_config={
                            "temperature": 0.7,
                            "max_output_tokens": 800,
                        }
                    )
                    
                    if response.candidates and response.candidates[0].content.parts:
                        activities_text = response.candidates[0].content.parts[0].text
                        try:
                            new_activities = clean_and_parse_json(activities_text)
                            if isinstance(new_activities, list):
                                for activity in new_activities:
                                    name = activity.get("name", "").strip()
                                    time_of_day = activity.get("best_time_to_visit", "Anytime").lower()
                                    if name and name not in used_activities and time_of_day not in used_times_of_day:
                                        # Generate a unique description for the activity
                                        unique_description = f"{activity.get('description', 'No description')} This is a must-visit spot in {destination} for its {activity.get('type', 'unique features')}."
                                        
                                        day_activities.append({
                                            "name": name,
                                            "description": unique_description,
                                            "reason_to_visit": activity.get("reason_to_visit", ""),
                                            "best_time_to_visit": activity.get("best_time_to_visit", "Anytime"),
                                            "rest_period": activity.get("rest_period", "1-2 hours between activities")
                                        })
                                        used_activities.add(name)
                                        used_times_of_day.add(time_of_day)
                                        if len(day_activities) >= num_activities:
                                            break
                        except ValueError as e:
                            print(f"❌ JSON parse error: {str(e)}")
                except Exception as e:
                    print(f"❌ Gemini query failed: {str(e)}")

        # Add the day's activities
        if day_activities:
            activities_by_day.append({
                "date": formatted_date,
                "activities": day_activities,
                "is_rest_day": False
            })
        else:
            activities_by_day.append({
                "date": formatted_date,
                "activities": ["No activities found for this day."],
                "is_rest_day": False
            })

    return activities_by_day