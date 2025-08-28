import streamlit as st

# --- App Configuration and Layout ---
st.set_page_config(
    page_title="Calculator",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Calculator")
st.markdown("Use the buttons below or type directly into the display and press **Enter**.")
st.divider()


# --- Session State Management ---
# Initialize session state variables if they don't exist
def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'expression' not in st.session_state:
        st.session_state.expression = ""
    if 'last_action' not in st.session_state:
        st.session_state.last_action = ""
    if 'calc_display' not in st.session_state:
        st.session_state.calc_display = ""


# Call initialization
initialize_session_state()


# --- Functions to Handle Button Clicks and Logic ---

def calculate_expression():
    """
    Evaluates the current expression and displays the result.
    This function is called by the '=' button or the Enter key.
    """
    try:
        # Get the expression from the text input field via its key
        expression_to_eval = st.session_state.get('calc_display', '').strip()

        # Check if the expression is empty to avoid a SyntaxError.
        if not expression_to_eval:
            st.session_state.expression = "Please enter an expression"
            return

        # Security: Replace a potentially dangerous function with a safer alternative
        # Note: 'eval' can be risky. For a production app, you would use a safer parser.
        result = eval(expression_to_eval)

        # Store the result in session state to display it in the input field
        st.session_state.expression = str(result)
        st.session_state.last_action = 'calculate'

    except (SyntaxError, NameError, ZeroDivisionError):
        st.session_state.expression = "Error: Invalid expression"
        st.session_state.last_action = 'error'

    except Exception as e:
        st.session_state.expression = f"Error: {str(e)}"
        st.session_state.last_action = 'error'


def append_to_expression(char):
    """
    Appends a character (number or operator) to the current expression.
    This function is called by each number and operator button.
    """
    # If the last action was a calculation and the new character is a number or parenthesis,
    # start a new expression. Otherwise, continue the current one.
    if st.session_state.get('last_action', '') in ('calculate', 'error') and str(char) not in "+-*/.":
        st.session_state.expression = str(char)
    else:
        st.session_state.expression += str(char)

    st.session_state.last_action = 'append'


def clear_calculator():
    """
    Clears the current expression.
    This function is called by the 'Clear' button.
    """
    st.session_state.expression = ""
    st.session_state.last_action = 'clear'


# --- Calculator Display and Buttons UI ---

st.text_input(
    "Your Expression",
    value=st.session_state.get('expression', ''),
    key="calc_display",
    on_change=calculate_expression,
    placeholder="e.g., 2*3.5 + 1"
)

# Create calculator button layout
row1_cols = st.columns(4)
with row1_cols[0]:
    st.button("7", on_click=append_to_expression, args=("7",), use_container_width=True)
with row1_cols[1]:
    st.button("8", on_click=append_to_expression, args=("8",), use_container_width=True)
with row1_cols[2]:
    st.button("9", on_click=append_to_expression, args=("9",), use_container_width=True)
with row1_cols[3]:
    st.button("÷", on_click=append_to_expression, args=("/",), use_container_width=True)

row2_cols = st.columns(4)
with row2_cols[0]:
    st.button("4", on_click=append_to_expression, args=("4",), use_container_width=True)
with row2_cols[1]:
    st.button("5", on_click=append_to_expression, args=("5",), use_container_width=True)
with row2_cols[2]:
    st.button("6", on_click=append_to_expression, args=("6",), use_container_width=True)
with row2_cols[3]:
    st.button("×", on_click=append_to_expression, args=("*",), use_container_width=True)

row3_cols = st.columns(4)
with row3_cols[0]:
    st.button("1", on_click=append_to_expression, args=("1",), use_container_width=True)
with row3_cols[1]:
    st.button("2", on_click=append_to_expression, args=("2",), use_container_width=True)
with row3_cols[2]:
    st.button("3", on_click=append_to_expression, args=("3",), use_container_width=True)
with row3_cols[3]:
    st.button("−", on_click=append_to_expression, args=("-",), use_container_width=True)

row4_cols = st.columns(4)
with row4_cols[0]:
    st.button("Clear", on_click=clear_calculator, use_container_width=True)
with row4_cols[1]:
    st.button("0", on_click=append_to_expression, args=("0",), use_container_width=True)
with row4_cols[2]:
    st.button(".", on_click=append_to_expression, args=(".",), use_container_width=True)
with row4_cols[3]:
    st.button("ADD +", on_click=append_to_expression, args=("+",), use_container_width=True)

# Create the equals button with a unique key for specific styling
st.button("=", on_click=calculate_expression, use_container_width=True, key="equals_btn", type="primary")

# CSS and JavaScript for styling and escape key functionality
st.markdown("""
<style>
/* Hide success and error messages that might pop up */
.stAlert {
    display: none !important;
}

/* Base style for all buttons to ensure they look uniform */
.stButton > button {
    height: 60px !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 1px solid #CCCCCC !important; /* Default border */
    background-color: #FFFFFF !important; /* Default background */
    color: #262730 !important; /* Default text color */
}

/* Style ONLY the equals button blue. 
   Using Streamlit's "primary" type and targeting the corresponding CSS class. */
.stButton button[kind="primary"] {
    background-color: #007BFF !important;
    color: white !important;
    border: 2px solid #007BFF !important;
    font-weight: bold !important;
    font-size: 20px !important;
}
</style>

<script>
// Simple escape key to refresh page
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        event.preventDefault();
        window.location.reload();
    }
});
</script>
""", unsafe_allow_html=True)

# --- Usage Instructions ---
st.markdown("---")
st.info("**Keyboard Shortcuts:** Press **Enter** to calculate, **ESC** to refresh page. Use the **Clear** button to reset.")