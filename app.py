import streamlit as st
import qrcode
from io import BytesIO
from datetime import date
import uuid

from database import create_tables, get_connection


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="EL Rera Internship QR Verification",
    page_icon="🔐",
    layout="centered"
)

# Create database tables
create_tables()


# =====================================================
# 🔒 FIXED COMPANY DETAILS
# =====================================================
# APNI ACTUAL COMPANY DETAILS YAHAN BHARO.
# YE DETAILS APP KE USERS CHANGE NAHI KAR SAKTE.

COMPANY_NAME = "RPAC CONSULTANTS & ADVISORS LLP"
COMPANY_LLPIN = "ACW-3008"
COMPANY_ADDRESS = "C- 39, First Floor, Lajpat Marg, Next to Crazy Coffee, Ashok Nagar, C- Scheme, Jaipur - 302001(Raj.)"
COMPANY_CONTACT = "+91 9772933041 "
COMPANY_EMAIL_ADDRESS = "rpacadvisorsllp2606@gmail.com"
MANAGER_NAME = "Mr. Kaushal Jangid"


# =====================================================
# CERTIFICATE VERIFICATION
# =====================================================

certificate_id_from_url = st.query_params.get("certificate_id")

if certificate_id_from_url:

    st.title("🔐 Certificate Verification")
    st.write("Verify an internship certificate using its Certificate ID.")
    st.divider()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            certificate_id,
            intern_name,
            college_name,
            internship_role,
            start_date,
            end_date,
            total_hours
        FROM interns
        WHERE certificate_id = ?
    """, (certificate_id_from_url,))

    result = cursor.fetchone()
    connection.close()

    if result:
        st.success("✅ Certificate Verified Successfully!")

        st.subheader("📄 Internship Details")

        st.write("**Certificate ID:**", result[0])
        st.write("**Intern Name:**", result[1])
        st.write("**College Name:**", result[2])
        st.write("**Internship Role / Work:**", result[3])
        st.write("**Internship Start Date:**", result[4])
        st.write("**Internship Completion Date:**", result[5])
        st.write("**Total Internship Hours:**", f"{result[6]} Hours")

        st.subheader("🏢 Company Details")

        st.write("**Company Name:**", COMPANY_NAME)
        st.write("**LLPIN:**", COMPANY_LLPIN)
        st.write("**Address:**", COMPANY_ADDRESS)
        st.write("**Contact:**", COMPANY_CONTACT)
        st.write("**Email Address:**", COMPANY_EMAIL_ADDRESS)
        st.write("**Managing Partner:**", MANAGER_NAME)

        st.info("✅ Verification Status: Internship Completed")

    else:
        st.error("❌ Certificate Not Found or Invalid Certificate ID.")
        st.warning(
            "Please check the Certificate ID and scan the correct QR code."
        )

    st.stop()


# =====================================================
# APP TITLE
# =====================================================

st.title("🔐 EL Rera Internship QR Generator")

st.write(
    "Generate a secure verification QR code for an internship certificate."
)

st.divider()


# =====================================================
# INTERN DETAILS
# =====================================================

st.subheader("👩‍🎓 Intern Details")

intern_name = st.text_input(
    "Intern Name",
    placeholder="Enter intern name"
)

college_name = st.text_input(
    "College Name",
    placeholder="Enter college name"
)

internship_role = st.text_input(
    "Internship Role / Work",
    placeholder="Example: Python Developer Intern"
)

start_date = st.date_input(
    "Internship Start Date",
    value=date.today()
)

end_date = st.date_input(
    "Internship Completion Date",
    value=date.today()
)

total_hours = st.number_input(
    "Total Internship Hours",
    min_value=1,
    max_value=5000,
    value=120,
    step=1
)


# =====================================================
# GENERATE QR CODE
# =====================================================

if st.button("🔐 Generate QR Code", use_container_width=True):

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    if not intern_name.strip():
        st.warning("Please enter Intern Name.")

    elif not college_name.strip():
        st.warning("Please enter College Name.")

    elif not internship_role.strip():
        st.warning("Please enter Internship Role / Work.")

    elif end_date < start_date:
        st.error(
            "Internship Completion Date cannot be before Start Date."
        )

    else:

        # -------------------------------------------------
        # UNIQUE CERTIFICATE ID
        # -------------------------------------------------

        unique_id = uuid.uuid4().hex[:8].upper()

        certificate_id = (
            f"ELR-{start_date.strftime('%Y')}-{unique_id}"
        )

        # -------------------------------------------------
        # SAVE INTERN DETAILS IN DATABASE
        # -------------------------------------------------

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO interns (
                certificate_id,
                intern_name,
                college_name,
                internship_role,
                start_date,
                end_date,
                total_hours
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            certificate_id,
            intern_name.strip(),
            college_name.strip(),
            internship_role.strip(),
            str(start_date),
            str(end_date),
            int(total_hours)
        ))

        connection.commit()
        connection.close()

        # -------------------------------------------------
        # VERIFICATION URL
        # -------------------------------------------------
        # IMPORTANT:
        # localhost sirf testing ke liye hai.
        # Online deployment ke baad is URL ko apni
        # deployed Streamlit URL se replace karna hoga.

        verification_url = (
            "http://localhost:8501/?certificate_id="
            + certificate_id
        )

        # QR contains ONLY the verification URL.
        # Actual intern/company information remains in
        # the database/application.

        qr_data = verification_url

        # -------------------------------------------------
        # CREATE QR CODE
        # -------------------------------------------------

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )

        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_image = qr.make_image()

        # -------------------------------------------------
        # CONVERT QR TO PNG
        # -------------------------------------------------

        img_bytes = BytesIO()

        qr_image.save(
            img_bytes,
            format="PNG"
        )

        qr_bytes = img_bytes.getvalue()

        # -------------------------------------------------
        # SHOW RESULT
        # -------------------------------------------------

        st.success("✅ QR Code Generated Successfully!")

        st.write(
            "**Certificate ID:**",
            certificate_id
        )

        st.image(
            qr_bytes,
            width=300
        )

        # -------------------------------------------------
        # DOWNLOAD QR
        # -------------------------------------------------

        st.download_button(
            label="⬇️ Download QR Code",
            data=qr_bytes,
            file_name=f"{certificate_id}.png",
            mime="image/png",
            use_container_width=True
        )

        # -------------------------------------------------
        # INFORMATION
        # -------------------------------------------------

        st.info(
            "This QR code contains a verification link. "
            "Place the QR code on the internship certificate."
        )