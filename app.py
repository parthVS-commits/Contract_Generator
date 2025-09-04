import streamlit as st
import os
import logging
import time
import uuid
from datetime import datetime
from dotenv import load_dotenv
from templates import templates_dict
from utils.ai_assistant import process_request
from utils.docx_converter import convert_to_docx

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"app_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("contract_generator")

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Generate session ID for tracking
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    logger.info(f"New session started with ID: {st.session_state.session_id}")

# Set page configuration
st.set_page_config(
    page_title="Legal Contract Generator",
    page_icon="📝",
    layout="wide"
)
logger.info("Streamlit page configured")

def main():
    """
    Main function for the Streamlit application.
    
    This function handles:
    1. User interface setup and layout
    2. Contract template selection and loading
    3. Chat interface for AI-assisted modifications
    4. DOCX conversion and download
    
    The application follows a flow where users first select a contract type,
    then can interact with the template via chat or direct editing.
    """
    start_time = time.time()
    logger.info(f"App main function called - Session: {st.session_state.session_id}")
    
    st.title("Legal Contract Generator")
    st.markdown("Select a contract template, customize it via chat, and download the final document.")
    
    # Initialize session states
    if "contract_text" not in st.session_state:
        st.session_state.contract_text = ""
        logger.debug("Initialized contract_text session state")
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        logger.debug("Initialized chat_history session state")
    
    if "contract_selected" not in st.session_state:
        st.session_state.contract_selected = False
        logger.debug("Initialized contract_selected session state")
    
    # Sidebar for contract selection
    with st.sidebar:
        st.header("Contract Options")
        
        contract_type = st.selectbox(
            "Select Contract Type",
            list(templates_dict.keys())
        )
        
        if contract_type and st.button("Load Template"):
            logger.info(f"User selected contract type: {contract_type}")
            st.session_state.contract_text = templates_dict[contract_type]
            st.session_state.previous_contract = contract_type
            st.session_state.contract_selected = True
            st.session_state.current_contract = contract_type
            logger.info(f"Template loaded for: {contract_type}")
            # Use rerun to refresh the UI
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Instructions")
        st.markdown("""
        1. Select a contract type and click 'Load Template'
        2. Review the template
        3. Use the chat to request modifications
        4. Download the final contract
        """)
    
    # Only display contract and chat UI after selection
    if st.session_state.contract_selected:
        logger.debug("Displaying contract UI as contract is selected")
        
        # Create two columns - one for contract display, one for chat
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"{st.session_state.current_contract} Template")
            
            # Text area for contract editing
            contract_text = st.text_area(
                "Review and edit your contract directly if needed",
                st.session_state.contract_text,
                height=600,
                key="contract_editor"
            )
            
            # Only update if text has changed
            if contract_text != st.session_state.contract_text:
                logger.info("User manually edited contract text")
                st.session_state.contract_text = contract_text
            
            # Download button
            if st.download_button(
                "Download as DOCX",
                convert_to_docx(st.session_state.contract_text),
                file_name=f"{st.session_state.current_contract.replace(' ', '_').lower()}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                logger.info(f"Contract downloaded as DOCX: {st.session_state.current_contract}")
        
        with col2:
            st.subheader("AI Assistant")
            st.markdown("Ask for specific changes to the contract:")
            
            # Display chat history
            chat_container = st.container()
            with chat_container:
                for i, message in enumerate(st.session_state.chat_history):
                    if message["role"] == "user":
                        st.markdown(f"**You:** {message['content']}")
                    else:
                        st.markdown(f"**Assistant:** {message['content']}")
            
            # Chat input
            user_input = st.text_area("Type your request here:", key="user_input", height=100)
            
            if st.button("Send", key="send_button"):
                if user_input:
                    logger.info(f"User sent modification request: {user_input[:50]}...")
                    
                    # Add user message to chat history
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    
                    # Process request with GPT-4o-mini
                    with st.spinner("Processing your request..."):
                        try:
                            logger.info("Calling AI assistant for contract modification")
                            ai_start_time = time.time()
                            response, modified_contract = process_request(
                                user_input, 
                                st.session_state.contract_text
                            )
                            ai_duration = time.time() - ai_start_time
                            logger.info(f"AI processing completed in {ai_duration:.2f} seconds")
                            
                            # Update contract text with modifications
                            st.session_state.contract_text = modified_contract
                            logger.info("Contract text updated with AI modifications")
                            
                            # Add assistant response to chat history
                            st.session_state.chat_history.append({"role": "assistant", "content": response})
                            
                            # Clear user input and refresh - using st.rerun() 
                            st.rerun()
                        except Exception as e:
                            error_msg = f"Error processing request: {str(e)}"
                            logger.error(error_msg, exc_info=True)
                            st.error(error_msg)
    else:
        # Display welcome message when no contract is selected
        st.info("👈 Please select a contract type from the sidebar and click 'Load Template' to begin")
        logger.debug("Displaying welcome message, waiting for contract selection")
    
    # Log execution time
    execution_time = time.time() - start_time
    logger.debug(f"Page render completed in {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()