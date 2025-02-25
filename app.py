# ui
import streamlit as st
import pickle
from streamlit_option_menu import option_menu

# Page Configuration
st.set_page_config(
    page_title="AI-Disease Prediction System",
    page_icon="⚕️",
    layout="wide"
)

# Hiding Streamlit default elements
hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Background image with overlay
background_image_url = "https://www.strategyand.pwc.com/m1/en/strategic-foresight/sector-strategies/healthcare/ai-powered-healthcare-solutions/img01-section1.jpg"
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url({background_image_url});
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
}}

[data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);
}}

.stApp {{
    color: white;
}}

.stButton>button {{
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    margin-top: 20px;
}}

.stButton>button:hover {{
    background-color: #45a049;
}}

.css-1n76uvr {{
    color: white;
}}

.stNumberInput>div>div>input {{
    color: black;
}}

.stTextInput>div>div>input {{
    color: black;
}}

.stSelectbox>div>div {{
    color: black;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load models
try:
    models = {
        'diabetes': pickle.load(open('Models/diabetes_model.sav', 'rb')),
        'heart_disease': pickle.load(open('Models/heart_disease_model.sav', 'rb')),
        'parkinsons': pickle.load(open('Models/parkinsons_model.sav', 'rb')),
        'lung_cancer': pickle.load(open('Models/lungs_disease_model.sav', 'rb')),
        'thyroid': pickle.load(open('Models/Thyroid_model.sav', 'rb'))
    }
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# App structure
def main():
    # Sidebar navigation
    with st.sidebar:
        st.title("AI - Disease Prediction System")
        
        selection = option_menu(
            menu_title="Main Menu",
            options=[
                "Home", 
                "Diabetes Prediction", 
                "Heart Disease Prediction", 
                "Parkinson's Prediction", 
                "Lung Cancer Prediction", 
                "Hypo-Thyroid Prediction",
                "About",
                "Creater"
            ],
            icons=["house", "activity", "heart", "person", "lungs", "thermometer", "info-circle"],
            menu_icon="hospital",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "rgba(0, 0, 0, 0.6)"},
                "icon": {"color": "white", "font-size": "25px"},
                "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#4CAF50"},
            }
        )
        
        st.markdown(" ")
        st.info("Created by Pranay Dhore")
    
    # Helper function for input fields - FIXED to use consistent types
    def display_input(label, tooltip, key, min_value=None, max_value=None, type="text"):
        col1, col2 = st.columns([3, 1])
        with col1:
            if type == "text":
                return st.text_input(label, key=key, help=tooltip)
            elif type == "number":
                # Convert all numeric values to float to avoid type mismatch
                if min_value is not None:
                    min_value = float(min_value)
                if max_value is not None:
                    max_value = float(max_value)
                return st.number_input(label, min_value=min_value, max_value=max_value, key=key, help=tooltip, step=float(1))
        
    # Home Page
    if selection == "Home":
        st.title("Welcome to Disease Prediction System")
        st.markdown("### AI-Powered Healthcare Assistance")
        
        st.write("""
        This application uses machine learning to predict the likelihood of various diseases based on user-provided data.
        
        ### Available Predictions:
        - **Diabetes**: Predicts diabetes risk based on health indicators
        - **Heart Disease**: Evaluates heart disease probability using clinical data
        - **Parkinson's Disease**: Analyzes voice data features to predict Parkinson's
        - **Lung Cancer**: Assesses lung cancer risk based on symptoms and habits
        - **Hypo-Thyroid**: Predicts thyroid condition based on thyroid function tests
        
        ### How to Use:
        1. Select a disease prediction from the sidebar menu
        2. Fill in all the required parameters
        3. Click on the test button to get your prediction result
        
        ⚠️ **Disclaimer**: This tool provides predictions based on statistical models and should not replace professional medical diagnosis. Always consult healthcare professionals for medical advice.
        """)
    
    # Diabetes Prediction Page
    elif selection == "Diabetes Prediction":
        st.title("Diabetes Prediction")
        st.markdown("### Enter patient health indicators:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            Pregnancies = display_input('Number of Pregnancies', 'Enter number of times pregnant', 'Pregnancies', 0.0, 20.0, 'number')
            Glucose = display_input('Glucose Level (mg/dL)', 'Enter glucose level', 'Glucose', 0.0, 500.0, 'number')
            BloodPressure = display_input('Blood Pressure (mmHg)', 'Enter blood pressure value', 'BloodPressure', 0.0, 200.0, 'number')
            SkinThickness = display_input('Skin Thickness (mm)', 'Enter skin thickness value', 'SkinThickness', 0.0, 100.0, 'number')
        
        with col2:
            Insulin = display_input('Insulin Level (μU/mL)', 'Enter insulin level', 'Insulin', 0.0, 1000.0, 'number')
            BMI = display_input('BMI (kg/m²)', 'Enter Body Mass Index value', 'BMI', 0.0, 70.0, 'number')
            DiabetesPedigreeFunction = display_input('Diabetes Pedigree Function', 'Enter diabetes pedigree function value', 'DiabetesPedigreeFunction', 0.0, 3.0, 'number')
            Age = display_input('Age (years)', 'Enter age of the person', 'Age', 0.0, 120.0, 'number')
        
        diab_diagnosis = ''
        if st.button('Predict Diabetes Status'):
            input_data = [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
            diab_prediction = models['diabetes'].predict(input_data)
            
            if diab_prediction[0] == 1:
                diab_diagnosis = "Result: The patient is likely to have diabetes."
                st.error(diab_diagnosis)
            else:
                diab_diagnosis = "Result: The patient is unlikely to have diabetes."
                st.success(diab_diagnosis)
            
            # Show input data summary
            st.subheader("Patient Data Summary:")
            data_df = {
                "Parameter": ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin", "BMI", "Diabetes Pedigree", "Age"],
                "Value": [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
            }
            st.dataframe(data_df)
    
    # Heart Disease Prediction Page
    elif selection == "Heart Disease Prediction":
        st.title("Heart Disease Prediction")
        st.markdown("### Enter cardiac assessment data:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = display_input('Age (years)', 'Enter age of the person', 'age', 0.0, 120.0, 'number')
            sex = display_input('Sex (1=male; 0=female)', 'Enter sex of the person', 'sex', 0.0, 1.0, 'number')
            cp = display_input('Chest Pain Type (0-3)', 'Enter chest pain type', 'cp', 0.0, 3.0, 'number')
            trestbps = display_input('Resting Blood Pressure (mmHg)', 'Enter resting blood pressure', 'trestbps', 0.0, 250.0, 'number')
            chol = display_input('Serum Cholesterol (mg/dL)', 'Enter serum cholesterol', 'chol', 0.0, 600.0, 'number')
        
        with col2:
            fbs = display_input('Fasting Blood Sugar > 120 mg/dL (1=true; 0=false)', 'Enter fasting blood sugar status', 'fbs', 0.0, 1.0, 'number')
            restecg = display_input('Resting ECG Results (0-2)', 'Enter resting ECG results', 'restecg', 0.0, 2.0, 'number')
            thalach = display_input('Maximum Heart Rate (bpm)', 'Enter maximum heart rate achieved', 'thalach', 0.0, 250.0, 'number')
            exang = display_input('Exercise Induced Angina (1=yes; 0=no)', 'Enter exercise induced angina status', 'exang', 0.0, 1.0, 'number')
        
        with col3:
            oldpeak = display_input('ST Depression by Exercise', 'Enter ST depression value', 'oldpeak', 0.0, 10.0, 'number')
            slope = display_input('Slope of Peak Exercise ST Segment (0-2)', 'Enter slope value', 'slope', 0.0, 2.0, 'number')
            ca = display_input('Number of Major Vessels (0-3)', 'Enter number of major vessels', 'ca', 0.0, 3.0, 'number')
            thal = display_input('Thalassemia (0-2)', 'Enter thal value', 'thal', 0.0, 2.0, 'number')
        
        heart_diagnosis = ''
        if st.button('Predict Heart Disease Status'):
            input_data = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
            heart_prediction = models['heart_disease'].predict(input_data)
            
            if heart_prediction[0] == 1:
                heart_diagnosis = "Result: The patient is likely to have heart disease."
                st.error(heart_diagnosis)
            else:
                heart_diagnosis = "Result: The patient is unlikely to have heart disease."
                st.success(heart_diagnosis)
    
    # Parkinson's Prediction Page
    elif selection == "Parkinson's Prediction":
        st.title("Parkinson's Disease Prediction")
        st.markdown("### Enter voice recording metrics:")
        
        tab1, tab2 = st.tabs(["Basic Metrics", "Advanced Metrics"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                fo = display_input('MDVP:Fo(Hz)', 'Average vocal fundamental frequency', 'fo', 0.0, 500.0, 'number')
                fhi = display_input('MDVP:Fhi(Hz)', 'Maximum vocal fundamental frequency', 'fhi', 0.0, 500.0, 'number')
                flo = display_input('MDVP:Flo(Hz)', 'Minimum vocal fundamental frequency', 'flo', 0.0, 500.0, 'number')
                Jitter_percent = display_input('MDVP:Jitter(%)', 'Percentage variation in fundamental frequency', 'Jitter_percent', 0.0, 5.0, 'number')
                Jitter_Abs = display_input('MDVP:Jitter(Abs)', 'Absolute jitter in microseconds', 'Jitter_Abs', 0.0, 1.0, 'number')
            
            with col2:
                RAP = display_input('MDVP:RAP', 'Relative amplitude perturbation', 'RAP', 0.0, 1.0, 'number')
                PPQ = display_input('MDVP:PPQ', 'Five-point period perturbation quotient', 'PPQ', 0.0, 1.0, 'number')
                DDP = display_input('Jitter:DDP', 'Average absolute difference of differences', 'DDP', 0.0, 1.0, 'number')
                Shimmer = display_input('MDVP:Shimmer', 'Local shimmer', 'Shimmer', 0.0, 1.0, 'number')
                Shimmer_dB = display_input('MDVP:Shimmer(dB)', 'Local shimmer in decibels', 'Shimmer_dB', 0.0, 5.0, 'number')
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                APQ3 = display_input('Shimmer:APQ3', 'Three-point amplitude perturbation quotient', 'APQ3', 0.0, 1.0, 'number')
                APQ5 = display_input('Shimmer:APQ5', 'Five-point amplitude perturbation quotient', 'APQ5', 0.0, 1.0, 'number')
                APQ = display_input('MDVP:APQ', 'Amplitude perturbation quotient', 'APQ', 0.0, 1.0, 'number')
                DDA = display_input('Shimmer:DDA', 'Average absolute differences between consecutive differences', 'DDA', 0.0, 1.0, 'number')
                NHR = display_input('NHR', 'Noise to harmonic ratio', 'NHR', 0.0, 1.0, 'number')
            
            with col2:
                HNR = display_input('HNR', 'Harmonic to noise ratio', 'HNR', 0.0, 50.0, 'number')
                RPDE = display_input('RPDE', 'Recurrence period density entropy', 'RPDE', 0.0, 1.0, 'number')
                DFA = display_input('DFA', 'Detrended fluctuation analysis', 'DFA', 0.0, 1.0, 'number')
                spread1 = display_input('Spread1', 'Nonlinear measure of fundamental frequency variation', 'spread1', -10.0, 10.0, 'number')
                spread2 = display_input('Spread2', 'Nonlinear measure of fundamental frequency variation', 'spread2', 0.0, 10.0, 'number')
                D2 = display_input('D2', 'Correlation dimension', 'D2', 0.0, 10.0, 'number')
                PPE = display_input('PPE', 'Pitch period entropy', 'PPE', 0.0, 1.0, 'number')
        
        parkinsons_diagnosis = ''
        if st.button("Predict Parkinson's Status"):
            input_data = [[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, 
                          Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, 
                          RPDE, DFA, spread1, spread2, D2, PPE]]
            parkinsons_prediction = models['parkinsons'].predict(input_data)
            
            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = "Result: The patient is likely to have Parkinson's disease."
                st.error(parkinsons_diagnosis)
            else:
                parkinsons_diagnosis = "Result: The patient is unlikely to have Parkinson's disease."
                st.success(parkinsons_diagnosis)
    
    # Lung Cancer Prediction Page
    elif selection == "Lung Cancer Prediction":
        st.title("Lung Cancer Prediction")
        st.markdown("### Enter patient symptoms and risk factors:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            GENDER = display_input('Gender (1=Male; 0=Female)', 'Enter gender of the person', 'GENDER', 0.0, 1.0, 'number')
            AGE = display_input('Age (years)', 'Enter age of the person', 'AGE', 0.0, 120.0, 'number')
            SMOKING = display_input('Smoking (1=Yes; 0=No)', 'Enter if the person smokes', 'SMOKING', 0.0, 1.0, 'number')
            YELLOW_FINGERS = display_input('Yellow Fingers (1=Yes; 0=No)', 'Enter if the person has yellow fingers', 'YELLOW_FINGERS', 0.0, 1.0, 'number')
            ANXIETY = display_input('Anxiety (1=Yes; 0=No)', 'Enter if the person has anxiety', 'ANXIETY', 0.0, 1.0, 'number')
        
        with col2:
            PEER_PRESSURE = display_input('Peer Pressure (1=Yes; 0=No)', 'Enter if the person is under peer pressure', 'PEER_PRESSURE', 0.0, 1.0, 'number')
            CHRONIC_DISEASE = display_input('Chronic Disease (1=Yes; 0=No)', 'Enter if the person has a chronic disease', 'CHRONIC_DISEASE', 0.0, 1.0, 'number')
            FATIGUE = display_input('Fatigue (1=Yes; 0=No)', 'Enter if the person experiences fatigue', 'FATIGUE', 0.0, 1.0, 'number')
            ALLERGY = display_input('Allergy (1=Yes; 0=No)', 'Enter if the person has allergies', 'ALLERGY', 0.0, 1.0, 'number')
            WHEEZING = display_input('Wheezing (1=Yes; 0=No)', 'Enter if the person experiences wheezing', 'WHEEZING', 0.0, 1.0, 'number')
        
        with col3:
            ALCOHOL_CONSUMING = display_input('Alcohol Consuming (1=Yes; 0=No)', 'Enter if the person consumes alcohol', 'ALCOHOL_CONSUMING', 0.0, 1.0, 'number')
            COUGHING = display_input('Coughing (1=Yes; 0=No)', 'Enter if the person experiences coughing', 'COUGHING', 0.0, 1.0, 'number')
            SHORTNESS_OF_BREATH = display_input('Shortness Of Breath (1=Yes; 0=No)', 'Enter if the person experiences shortness of breath', 'SHORTNESS_OF_BREATH', 0.0, 1.0, 'number')
            SWALLOWING_DIFFICULTY = display_input('Swallowing Difficulty (1=Yes; 0=No)', 'Enter if the person has difficulty swallowing', 'SWALLOWING_DIFFICULTY', 0.0, 1.0, 'number')
            CHEST_PAIN = display_input('Chest Pain (1=Yes; 0=No)', 'Enter if the person experiences chest pain', 'CHEST_PAIN', 0.0, 1.0, 'number')
        
        lungs_diagnosis = ''
        if st.button("Predict Lung Cancer Status"):
            input_data = [[GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, CHRONIC_DISEASE, 
                          FATIGUE, ALLERGY, WHEEZING, ALCOHOL_CONSUMING, COUGHING, SHORTNESS_OF_BREATH, 
                          SWALLOWING_DIFFICULTY, CHEST_PAIN]]
            lungs_prediction = models['lung_cancer'].predict(input_data)
            
            if lungs_prediction[0] == 1:
                lungs_diagnosis = "Result: The patient is likely to have lung cancer."
                st.error(lungs_diagnosis)
            else:
                lungs_diagnosis = "Result: The patient is unlikely to have lung cancer."
                st.success(lungs_diagnosis)
    
    # Hypo-Thyroid Prediction Page
    elif selection == "Hypo-Thyroid Prediction":
        st.title("Hypo-Thyroid Prediction")
        st.markdown("### Enter thyroid function test results:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = display_input('Age (years)', 'Enter age of the person', 'age', 0.0, 120.0, 'number')
            sex = display_input('Sex (1=Male; 0=Female)', 'Enter sex of the person', 'sex', 0.0, 1.0, 'number')
            on_thyroxine = display_input('On Thyroxine (1=Yes; 0=No)', 'Enter if the person is on thyroxine', 'on_thyroxine', 0.0, 1.0, 'number')
        
        with col2:
            tsh = display_input('TSH Level (mU/L)', 'Enter TSH level', 'tsh', 0.0, 100.0, 'number')
            t3_measured = display_input('T3 Measured (1=Yes; 0=No)', 'Enter if T3 was measured', 't3_measured', 0.0, 1.0, 'number')
            t3 = display_input('T3 Level (nmol/L)', 'Enter T3 level', 't3', 0.0, 10.0, 'number')
            tt4 = display_input('TT4 Level (nmol/L)', 'Enter TT4 level', 'tt4', 0.0, 300.0, 'number')
        
        thyroid_diagnosis = ''
        if st.button("Predict Thyroid Status"):
            input_data = [[age, sex, on_thyroxine, tsh, t3_measured, t3, tt4]]
            thyroid_prediction = models['thyroid'].predict(input_data)
            
            if thyroid_prediction[0] == 1:
                thyroid_diagnosis = "Result: The patient is likely to have Hypo-Thyroid disease."
                st.error(thyroid_diagnosis)
            else:
                thyroid_diagnosis = "Result: The patient is unlikely to have Hypo-Thyroid disease."
                st.success(thyroid_diagnosis)
    
    # About Page
    elif selection == "About":
        st.title("About Disease Prediction System")
        
        st.markdown("""
        ### Project Information
        
        This Disease Prediction System is an AI-powered application that uses machine learning algorithms to predict various diseases based on patient data. The system aims to assist healthcare professionals in early detection and diagnosis.
        
        ### Machine Learning Models
        
        The system uses supervised machine learning models trained on medical datasets to predict:
        
        - **Diabetes**: Using the Pima Indians Diabetes Database
        - **Heart Disease**: Using the UCI Heart Disease Dataset
        - **Parkinson's Disease**: Using voice recording data features
        - **Lung Cancer**: Using symptom-based indicators
        - **Hypo-Thyroid**: Using thyroid function test results
        
        ### Technology Stack
        
        - **Frontend**: Streamlit (Python web framework)
        - **Backend**: Python with scikit-learn machine learning models
        - **Model Storage**: Pickle serialization
        
        ### Disclaimer
        
        This application is intended for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.
        
        ### Creator
        
        This project was developed by **Pranay Dhore** as a demonstration of applying machine learning in healthcare.
        
        For more information or to report issues, please contact the developer.
        """)

    elif selection=="Creater":
        st.title("👤 About the Creator")
        st.subheader("Pranay Dhore")

        st.write("""
        I am a **Data Science & AI Enthusiast**, passionate about **Machine Learning, Data Analysis, and Web Development**.  
        This application is designed to predict multiple diseases using **Machine Learning models**.
        """)

        st.write("### 📲 Connect with me:")
        st.markdown("""
        - **GitHub**: [PranayDhore](https://github.com/)
        - **LinkedIn**: [Pranay Dhore](https://linkedin.com/in/)
        - **Instagram**: [@pranay_dhore](https://instagram.com/)
        - **Email**: pranay.dhore@example.com
        """, unsafe_allow_html=True)

        st.write("📌 Feel free to reach out for collaborations and projects! 🚀")

if __name__ == '__main__':
    main()