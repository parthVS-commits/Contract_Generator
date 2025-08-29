import streamlit as st
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("contract_generator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
logger.info("Loading environment variables")
load_dotenv()

# Initialize OpenAI client with the latest syntax
logger.info("Initializing OpenAI client")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY not found in environment variables")

# Set page configuration
logger.info("Setting up Streamlit page configuration")
st.set_page_config(
    page_title="Contract Generator",
    page_icon="📝",
    layout="wide"
)

# Initialize session state variables
if 'contract_type' not in st.session_state:
    st.session_state.contract_type = None
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = False
if 'contract_generated' not in st.session_state:
    st.session_state.contract_generated = False
if 'contract_text' not in st.session_state:
    st.session_state.contract_text = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'answers' not in st.session_state:
    st.session_state.answers = {}

logger.info("Session state initialized")

# Define document types and their associated questions/suggestions
document_info = {
    "Insurance": {
        "questions": [
            {"question": "What type of insurance is this contract for?", 
             "suggestions": ["Health", "Auto", "Home", "Life", "Business"]},
            {"question": "Who is the insurer?", 
             "suggestions": ["Enter company name"]},
            {"question": "Who is the insured party?", 
             "suggestions": ["Individual name", "Company name"]},
            {"question": "What is the coverage amount?", 
             "suggestions": ["$100,000", "$250,000", "$500,000", "$1,000,000"]},
            {"question": "What is the premium amount?", 
             "suggestions": ["Monthly: $XX", "Annually: $XX"]},
            {"question": "What is the effective date of this policy?", 
             "suggestions": ["MM/DD/YYYY"]},
            {"question": "What is the expiration date of this policy?", 
             "suggestions": ["MM/DD/YYYY (1 year from effective)"]}
        ]
    },
    "MoU": {
        "questions": [
            {"question": "Who are the parties entering this MoU?", 
             "suggestions": ["Party A: [Name]", "Party B: [Name]"]},
            {"question": "What is the purpose of this MoU?", 
             "suggestions": ["Collaboration on project", "Exploration of business relationship"]},
            {"question": "What is the scope of this MoU?", 
             "suggestions": ["Define specific activities", "Define geographical boundaries"]},
            {"question": "What are the responsibilities of each party?", 
             "suggestions": ["Party A: [Responsibilities]", "Party B: [Responsibilities]"]},
            {"question": "What is the duration of this MoU?", 
             "suggestions": ["6 months", "1 year", "2 years"]},
            {"question": "Are there any financial commitments?", 
             "suggestions": ["Yes - specify", "No financial obligations"]}
        ]
    },
    "NDA": {
        "questions": [
            {"question": "Is this a unilateral or mutual NDA?", 
             "suggestions": ["Unilateral (one-way)", "Mutual (two-way)"]},
            {"question": "Who is the disclosing party?", 
             "suggestions": ["Company name", "Individual name"]},
            {"question": "Who is the receiving party?", 
             "suggestions": ["Company name", "Individual name"]},
            {"question": "What is the purpose of disclosure?", 
             "suggestions": ["Business evaluation", "Potential partnership", "Project collaboration"]},
            {"question": "What information is considered confidential?", 
             "suggestions": ["All shared information", "Only marked confidential", "Specific categories"]},
            {"question": "How long will the confidentiality obligation last?", 
             "suggestions": ["1 year", "2 years", "5 years", "Indefinitely"]},
            {"question": "What are the exclusions to confidential information?", 
             "suggestions": ["Public information", "Independently developed"]}
        ]
    },
    "MSA": {
        "questions": [
            {"question": "Who is the service provider?", 
             "suggestions": ["Company name"]},
            {"question": "Who is the client?", 
             "suggestions": ["Company name"]},
            {"question": "What services will be provided?", 
             "suggestions": ["General description", "Reference to Statement of Work"]},
            {"question": "What is the term of this agreement?", 
             "suggestions": ["1 year", "2 years", "3 years"]},
            {"question": "What are the payment terms?", 
             "suggestions": ["Net 30", "Net 45", "Net 60"]},
            {"question": "What is the fee structure?", 
             "suggestions": ["Fixed fee", "Hourly rate", "Milestone-based"]},
            {"question": "Are there any service level agreements (SLAs)?", 
             "suggestions": ["Yes - specify details", "No SLAs"]},
            {"question": "What are the termination conditions?", 
             "suggestions": ["30 days written notice", "Material breach", "Convenience"]}
        ]
    },
    "Rental Agreement": {
        "questions": [
            {"question": "Who is the landlord?", 
             "suggestions": ["Individual name", "Company name"]},
            {"question": "Who is the tenant?", 
             "suggestions": ["Individual name(s)", "Company name"]},
            {"question": "What is the property address?", 
             "suggestions": ["Full address with zip code"]},
            {"question": "What is the monthly rent amount?", 
             "suggestions": ["$XXX.XX"]},
            {"question": "What is the security deposit amount?", 
             "suggestions": ["Equal to one month's rent", "Equal to two months' rent"]},
            {"question": "What is the lease term?", 
             "suggestions": ["Month-to-month", "6 months", "1 year"]},
            {"question": "What is the lease start date?", 
             "suggestions": ["MM/DD/YYYY"]},
            {"question": "What utilities are included?", 
             "suggestions": ["Water", "Electricity", "Gas", "Internet", "None"]}
        ]
    }
}

# Common contract modification suggestions for each document type
modification_suggestions = {
    "Insurance": [
        "Change coverage amount", 
        "Modify premium payment schedule", 
        "Add additional insured", 
        "Update policy dates"
    ],
    "MoU": [
        "Extend agreement duration", 
        "Modify scope of cooperation", 
        "Add new responsibilities", 
        "Change termination clause"
    ],
    "NDA": [
        "Change confidentiality period", 
        "Modify definition of confidential information", 
        "Add permitted disclosure clause", 
        "Change jurisdiction"
    ],
    "MSA": [
        "Update payment terms", 
        "Modify service description", 
        "Change termination notice period", 
        "Add new service levels"
    ],
    "Rental Agreement": [
        "Change lease duration", 
        "Modify rent amount", 
        "Update utilities included", 
        "Add/remove pet clause"
    ]
}

# Function to generate contract using OpenAI
def generate_contract(contract_type, answers):
    try:
        logger.info(f"Generating {contract_type} contract")
        # Create a prompt based on contract type and answers
        prompt = f"Generate a detailed {contract_type} contract with the following details:\n\n"
        
        for q_and_a in answers:
            prompt += f"- {q_and_a['question']}: {q_and_a['answer']}\n"
            logger.debug(f"Added question: {q_and_a['question']}, answer: {q_and_a['answer']}")
        
        prompt += "\nCreate a professional, legally-sound contract that includes all standard clauses for this type of agreement."
        
        logger.info("Calling OpenAI API to generate contract")
        # Call OpenAI API with latest syntax
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a legal document assistant that creates professional, comprehensive contracts. Format the contract with clear sections, numbered clauses, and proper legal terminology."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        # Extract the generated contract
        contract = response.choices[0].message.content
        logger.info("Contract generation successful")
        return contract
    
    except Exception as e:
        error_msg = f"Error generating contract: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)
        return None

# Function to modify contract using OpenAI
def modify_contract(original_contract, modification_request):
    try:
        logger.info(f"Modifying contract with request: {modification_request}")
        prompt = f"Original contract:\n\n{original_contract}\n\nModification request: {modification_request}\n\nPlease provide the updated contract with these changes."
        
        logger.info("Calling OpenAI API to modify contract")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a legal document assistant. Modify the provided contract according to the user's request while maintaining the document's structure and legal integrity. Return the COMPLETE modified contract, not just the changes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        modified_contract = response.choices[0].message.content
        logger.info("Contract modification successful")
        return modified_contract
    
    except Exception as e:
        error_msg = f"Error modifying contract: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)
        return original_contract

# Main app interface
def main():
    logger.info("Starting main application")
    
    # App header
    st.title("🧾 Smart Contract Generator")
    st.write("Generate professional legal documents tailored to your needs")
    
    # Document selection step
    if 'contract_type' not in st.session_state or not st.session_state.contract_type:
        logger.info("Displaying document selection step")
        st.header("Step 1: Select Document Type")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            contract_type = st.radio(
                "What type of contract do you need?",
                list(document_info.keys()),
                index=None
            )
            
        with col2:
            if contract_type:
                if st.button("Proceed", type="primary"):
                    logger.info(f"User selected contract type: {contract_type}")
                    st.session_state.contract_type = contract_type
                    st.session_state.answers = {}
                    st.rerun()
    
    # Question collection step
    elif 'questions_answered' not in st.session_state or not st.session_state.questions_answered:
        logger.info(f"Displaying questions for {st.session_state.contract_type}")
        st.header(f"Step 2: Complete {st.session_state.contract_type} Details")
        st.write("Please answer the following questions to customize your contract")
        
        # Initialize answers in session state if not already present
        if 'answers' not in st.session_state:
            st.session_state.answers = {}
            
        # Display all questions for the selected document type
        with st.form(key="contract_form"):
            for item in document_info[st.session_state.contract_type]["questions"]:
                question = item["question"]
                suggestions = item["suggestions"]
                
                # Display the question
                st.subheader(question)
                
                # Create suggestion options as selectable buttons (not with callbacks)
                suggestion_cols = st.columns(min(4, len(suggestions)))
                for i, suggestion in enumerate(suggestions):
                    with suggestion_cols[i % 4]:
                        st.write(f"**Suggestion:** {suggestion}")
                
                # Text input for the answer
                answer_key = f"answer_{question}"
                answer = st.text_input(
                    "Your answer:",
                    key=answer_key,
                    value=st.session_state.answers.get(question, "")
                )
                st.session_state.answers[question] = answer
                st.divider()
            
            # Submit button for the form
            submit = st.form_submit_button("Generate Contract", type="primary")
            
            if submit:
                logger.info("Contract form submitted")
                # Process all the answers
                all_answers = []
                all_answered = True
                
                for item in document_info[st.session_state.contract_type]["questions"]:
                    question = item["question"]
                    answer = st.session_state.answers.get(question, "")
                    
                    if not answer:
                        all_answered = False
                        logger.warning(f"Missing answer for question: {question}")
                    
                    all_answers.append({"question": question, "answer": answer})
                
                if all_answered:
                    logger.info("All questions answered, generating contract")
                    with st.spinner("Generating your contract..."):
                        contract = generate_contract(st.session_state.contract_type, all_answers)
                        
                        if contract:
                            logger.info("Contract generated successfully")
                            st.session_state.contract_text = contract
                            st.session_state.questions_answered = True
                            st.session_state.contract_generated = True
                            st.rerun()
                else:
                    logger.warning("Form submission incomplete")
                    st.error("Please answer all questions before generating the contract.")
        
        # Back button outside the form
        if st.button("Back to Selection", key="back_to_selection"):
            logger.info("User navigated back to document selection")
            st.session_state.contract_type = None
            st.rerun()
    
    # Contract display and modification step
    elif 'contract_generated' in st.session_state and st.session_state.contract_generated:
        logger.info("Displaying generated contract and modification interface")
        st.header(f"Your {st.session_state.contract_type} Contract")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display the generated contract
            st.subheader("Generated Contract")
            st.text_area(
                "Contract Text",
                st.session_state.contract_text,
                height=500,
                key="contract_display",
                disabled=True
            )
            
            # Download button
            current_date = datetime.now().strftime("%Y-%m-%d")
            contract_filename = f"{st.session_state.contract_type}_Contract_{current_date}.txt"
            
            download_button = st.download_button(
                label="Download Contract",
                data=st.session_state.contract_text,
                file_name=contract_filename,
                mime="text/plain",
                type="primary"
            )
            if download_button:
                logger.info(f"Contract downloaded as {contract_filename}")
            
            # Start over button
            if st.button("Create New Contract", key="start_over"):
                logger.info("User chose to create a new contract")
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            # Contract modification chat interface
            st.subheader("Need Changes?")
            st.write("Describe what you'd like to modify or select a common change:")
            
            # Common modification suggestions
            if st.session_state.contract_type in modification_suggestions:
                # Display suggestions outside of any form
                for suggestion in modification_suggestions[st.session_state.contract_type]:
                    if st.button(suggestion, key=f"mod_{suggestion}"):
                        logger.info(f"User selected modification: {suggestion}")
                        st.session_state.chat_history.append({"role": "user", "content": f"Please {suggestion.lower()}"})
                        
                        # Process modification with OpenAI
                        with st.spinner("Updating contract..."):
                            modified_contract = modify_contract(
                                st.session_state.contract_text,
                                f"Please {suggestion.lower()}"
                            )
                            
                            if modified_contract:
                                st.session_state.contract_text = modified_contract
                                st.session_state.chat_history.append({"role": "assistant", "content": "Contract has been updated with your requested changes."})
                                logger.info("Contract successfully modified")
                        
                        st.rerun()
            
            # Custom modification request
            with st.form(key="modification_form"):
                modification_request = st.text_area(
                    "Describe your requested changes:",
                    placeholder="Example: Please increase the contract duration to 2 years",
                    height=100
                )
                
                if st.form_submit_button("Apply Changes"):
                    if modification_request:
                        logger.info(f"Custom modification requested: {modification_request}")
                        st.session_state.chat_history.append({"role": "user", "content": modification_request})
                        
                        # Process modification with OpenAI
                        with st.spinner("Updating contract..."):
                            modified_contract = modify_contract(
                                st.session_state.contract_text,
                                modification_request
                            )
                            
                            if modified_contract:
                                st.session_state.contract_text = modified_contract
                                st.session_state.chat_history.append({"role": "assistant", "content": "Contract has been updated with your requested changes."})
                                logger.info("Contract successfully modified with custom request")
                        
                        st.rerun()
            
            # Display chat history
            st.subheader("Modification History")
            chat_container = st.container(height=200)
            with chat_container:
                if 'chat_history' in st.session_state:
                    for message in st.session_state.chat_history:
                        if message["role"] == "user":
                            st.info(message["content"])
                        else:
                            st.success(message["content"])
            
            # Add personal information section
            st.subheader("Add Personal Information")
            with st.form(key="personal_info_form"):
                personal_info = st.text_area(
                    "Enter additional personal information for the notice section:",
                    placeholder="Example: Contact email: john@example.com, Phone: (555) 123-4567",
                    height=100
                )
                
                if st.form_submit_button("Add to Contract"):
                    if personal_info:
                        logger.info("Adding personal information to contract")
                        # Update contract with personal info
                        with st.spinner("Adding personal information..."):
                            modified_contract = modify_contract(
                                st.session_state.contract_text,
                                f"Add the following personal information to the notice section: {personal_info}"
                            )
                            
                            if modified_contract:
                                st.session_state.contract_text = modified_contract
                                st.session_state.chat_history.append({
                                    "role": "user", 
                                    "content": f"Added personal information: {personal_info}"
                                })
                                st.session_state.chat_history.append({
                                    "role": "assistant", 
                                    "content": "Personal information has been added to the contract."
                                })
                                logger.info("Personal information successfully added")
                        
                        st.rerun()

# Run the app
if __name__ == "__main__":
    try:
        logger.info("Starting contract generator application")
        main()
        logger.info("Application execution completed")
    except Exception as e:
        error_msg = f"Unhandled exception in application: {str(e)}"
        logger.critical(error_msg, exc_info=True)
        st.error(f"An unexpected error occurred: {str(e)}")