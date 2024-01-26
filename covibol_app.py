# example/st_app_gsheets_using_service_account.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Add logos
st.image("Color_logo.png", width=305)

#Display the title and subtitle
st.title("Portail client")

#st.markdown("Enter your details as new customer below.")
st.markdown("Que vous soyez un hôtel, un restaurant, un service traiteur ou un particulier, si vous recherchez des jus d'ananas naturels, des aliments bio (plantain, pistache, huile rouge, legumes frais) avec la possibilité d'influencer le processus de production selon vos besoins, vous êtes au bon endroit. Laissez-nous vos coordonnées ci-dessous, nous vous contacterons pour préciser votre demande.")


# Establishing a Google sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing customers data
existing_data = conn.read(usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

# display dataframe
#st.dataframe(existing_data)

#List of Business Types and Products
BUSINESS_TYPES = [
    "Hôtel",
    "Restaurant",
    "Service traiteur",
    "Particulier",
]

PRODUCTS = [
    "Jus d'ananas Bio",
    "Jus de Kassi Bio",
    "Jus de Folere Bio",
    "Chips plantain Bio",
    "Regime de plantain",
    "Pistache cassé",
    "Huile de palme",
]

# Onboarding new customer Form
with st.form(key="customer_form"):
    company_name = st.text_input(label="Company Name")
    business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
    phone_number = st.text_input(label=" WhatsApp Number(+237)")
    products = st.multiselect("Products Offer", options=PRODUCTS)
    years_in_business = st.slider("Years in Business", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboarding Date")
    additional_info = st.text_area(label="Additional Notes")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Customer Details")

    #If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not company_name or not business_type or not phone_number:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        elif existing_data["CompanyName"].str.contains(company_name).any():
            st.warning("A customer with this company already exists.")
            st.stop()
        else:
            # Create a new row of customer data
            customer_data =pd.DataFrame(
                [
                    {
                        "CompanyName": company_name,
                        "BusinessType": business_type,
                        "PhoneNumber": phone_number,
                        "Products": ", ".join(products),
                        "YearsInBusiness": years_in_business,
                        "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                        "AdditionalInfo": additional_info,
                    }
                ]
            )

            # Add the new customer data to the existing data
            updated_df = pd.concat([existing_data, customer_data], ignore_index=True)


            # Update Google Sheets with the new customer data
            conn.update(data=updated_df)

            st.success("Customer details successfully submitted!")


