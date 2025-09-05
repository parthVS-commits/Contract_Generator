import os
import logging
import time
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logger = logging.getLogger("contract_generator.ai_assistant")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger.info("OpenAI client initialized")

def process_request(user_input, current_contract):
    """
    Process the user's modification request using GPT-4o-mini
    
    Args:
        user_input (str): The user's request for contract modifications
        current_contract (str): The current state of the contract
        
    Returns:
        tuple: (response_message, modified_contract)
    """
    start_time = time.time()
    logger.info(f"Processing contract modification request: {user_input[:50]}...")
    logger.debug(f"Current contract length: {len(current_contract)} characters")
    
    # Create a system prompt to guide the AI's behavior
    system_prompt = """You are a legal document assistant specialized in contract modifications. 
    You should help users modify their legal contracts according to their requests.
    Always maintain the legal integrity and structure of the document.
    
    IMPORTANT: Your response MUST use the following format:
    1. First, provide a brief explanation of the changes made
    2. Then add a line that says "---MODIFIED CONTRACT BEGINS---"
    3. Next, include the fully modified contract with NO explanatory text inside it
    4. End with a line that says "---MODIFIED CONTRACT ENDS---"
    
    Only modify the parts of the contract that the user has requested to change.
    Preserve all formatting, section numbering, and legal language in unmodified sections.
    Do not include any explanatory text, markers, or headers within the contract text itself.
    """
    
    # Create the user prompt with the contract and modification request
    user_prompt = f"""
    I need to modify the following contract according to this request:
    
    REQUEST: {user_input}
    
    CURRENT CONTRACT:
    {current_contract}
    """
    
    logger.debug("Sending request to OpenAI API")
    try:
        # Call the OpenAI API
        api_start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Lower temperature for more precise responses
            max_tokens=4000,  # Set an appropriate limit
        )
        api_duration = time.time() - api_start_time
        logger.info(f"OpenAI API call completed in {api_duration:.2f} seconds")
        
        # Extract the response content
        response_text = response.choices[0].message.content
        logger.debug(f"Raw API response length: {len(response_text)} characters")
        
        # Parse the response to separate explanation from the contract
        # Look for the contract between our markers
        contract_pattern = r"---MODIFIED CONTRACT BEGINS---\s*(.*?)\s*---MODIFIED CONTRACT ENDS---"
        contract_match = re.search(contract_pattern, response_text, re.DOTALL)
        
        if contract_match:
            logger.info("Successfully parsed response with expected format")
            # Extract everything before the start marker as the explanation
            explanation_parts = response_text.split("---MODIFIED CONTRACT BEGINS---", 1)
            explanation = explanation_parts[0].strip()
            
            # Extract the contract text from the match
            modified_contract = contract_match.group(1).strip()
            
            logger.debug(f"Explanation length: {len(explanation)} characters")
            logger.debug(f"Modified contract length: {len(modified_contract)} characters")
        else:
            # Try alternative parsing approaches if the markers aren't found
            logger.warning("Expected format markers not found, trying alternative parsing")
            
            # Check for "MODIFIED CONTRACT:" format
            parts = response_text.split("MODIFIED CONTRACT:", 1)
            if len(parts) > 1:
                logger.info("Found alternative 'MODIFIED CONTRACT:' format")
                explanation = parts[0].strip()
                modified_contract = parts[1].strip()
            else:
                # Last resort - look for common contract start phrases
                logger.warning("No clear markers found, trying to identify contract text")
                contract_starts = ["THIS AGREEMENT", "THIS DEED", "WHEREAS", "NOW THIS"]
                
                for start in contract_starts:
                    if start in response_text:
                        split_point = response_text.find(start)
                        explanation = response_text[:split_point].strip()
                        modified_contract = response_text[split_point:].strip()
                        logger.info(f"Identified contract starting with '{start}'")
                        break
                else:
                    # If we can't find any clear way to split it
                    logger.warning("Could not identify contract text, using original contract")
                    explanation = response_text.strip()
                    modified_contract = current_contract
        
        # Log character differences between original and modified contract
        if modified_contract != current_contract:
            char_diff = len(modified_contract) - len(current_contract)
            logger.info(f"Contract modified: {char_diff:+d} character change")
        else:
            logger.warning("No changes detected in contract content")
        
        total_duration = time.time() - start_time
        logger.info(f"Request processing completed in {total_duration:.2f} seconds")
        return explanation, modified_contract
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return f"Error processing request: {str(e)}", current_contract