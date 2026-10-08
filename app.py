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
    page_title="EL Rera Certificate Verification",
    page_icon="🔐",
    layout="centered"
)

create_tables()


# =====================================================
# 🔒 FIXED COMPANY DETAILS
# =====================================================

COMPANY_NAME = "RPAC CONSULTANTS & ADVISORS LLP"
COMPANY_LLPIN = ""
COMPANY_ADDRESS = "shok Nagar,Raj.)"
COMPANY_CONTACT = " "
COMPANY_EMAIL_ADDRESS = "ail.com"
MANAGER_NAME = "M"


# =====================================================
# PROFESSIONAL PAGE DESIGN
# =====================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    opacity: 0.75;
    margin-bottom: 25px;
}

.verified-box {
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    margin: 15px 0 25px 0;
    border: 2px solid #2e7d32;
}

.verified-title {
    font-size: 25px;
    font-weight: 700;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
}

.info-box {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(128,128,128,0.35);
    margin-bottom: 12px;
}

.footer {
    text-align: center;
    margin-top: 30px;
    font-size: 13px;
    opacity: 0.7;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# CERTIFICATE VERIFICATION
# =====================================================

certificate_id_from_url = st.query_params.get("certificate_id")


if certificate_id_from_url:

    st.markdown(
        '<div class="main-title">🔐 Internship Certificate</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Certificate Verification Portal</div>',
        unsafe_allow_html=True
    )

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


    # =================================================
    # VERIFIED CERTIFICATE
    # =================================================

    if result:

        st.markdown("""
        <div class="verified-box">
            <div class="verified-title">🟢 CERTIFICATE VERIFIED</div>
            <div>This certificate has been successfully verified.</div>
        </div>
        """, unsafe_allow_html=True)


        # -------------------------------------------------
        # CERTIFICATE INFORMATION
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">📄 Certificate Information</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="info-box">
                <b>Certificate ID:</b> {result[0]}<br><br>
                <b>Verification Status:</b> 🟢 Verified<br><br>
                <b>Internship Status:</b> Internship Completed
            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # INTERN INFORMATION
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">👩‍🎓 Intern Information</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="info-box">
                <b>Intern Name:</b> {result[1]}<br><br>
                <b>College Name:</b> {result[2]}<br><br>
                <b>Internship Role / Work:</b> {result[3]}<br><br>
                <b>Internship Start Date:</b> {result[4]}<br><br>
                <b>Internship Completion Date:</b> {result[5]}<br><br>
                <b>Total Internship Hours:</b> {result[6]} Hours
            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # COMPANY INFORMATION
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">🏢 Company Information</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="info-box">
                <b>Company Name:</b> {COMPANY_NAME}<br><br>
                <b>LLPIN:</b> {COMPANY_LLPIN}<br><br>
                <b>Address:</b> {COMPANY_ADDRESS}<br><br>
                <b>Contact:</b> {COMPANY_CONTACT}<br><br>
                <b>Email Address:</b> {COMPANY_EMAIL_ADDRESS}<br><br>
                <b>Managing Partner:</b> {MANAGER_NAME}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.success(
            "This internship certificate is valid and has been successfully verified."
        )


        st.markdown(
            '<div class="footer">EL Rera Certificate Verification System</div>',
            unsafe_allow_html=True
        )


    # =================================================
    # INVALID CERTIFICATE
    # =================================================

    else:

        st.error("🔴 Certificate Not Found")

        st.markdown(
            """
            <div class="info-box">
                <b>Verification Failed</b><br><br>
                The Certificate ID entered or scanned could not be
                found in the verification database.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "Please check the QR code or Certificate ID and try again."
        )

    st.stop()


# =====================================================
# QR GENERATOR PAGE
# =====================================================

st.markdown(
    '<div class="main-title">🔐 EL Rera QR Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Generate a verification QR code for an internship certificate.</div>',
    unsafe_allow_html=True
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
        # SAVE INTERN DETAILS
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


        # =================================================
        # 🌐 PUBLIC VERIFICATION URL
        # =================================================

        verification_url = (
            "https://el-rera-qr-app-a5zrmgmtj4ghjvurbz9ssx.streamlit.app/"
            "?certificate_id="
            + certificate_id
        )


        # =================================================
        # CREATE QR
        # =================================================

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )

        qr.add_data(verification_url)
        qr.make(fit=True)

        qr_image = qr.make_image()


        # =================================================
        # CONVERT TO PNG
        # =================================================

        img_bytes = BytesIO()

        qr_image.save(
            img_bytes,
            format="PNG"
        )

        qr_bytes = img_bytes.getvalue()


        # =================================================
        # SHOW RESULT
        # =================================================

        st.success("✅ QR Code Generated Successfully!")

        st.markdown(
            f"### Certificate ID: `{certificate_id}`"
        )

        st.image(
            qr_bytes,
            width=300
        )


        # =================================================
        # DOWNLOAD QR
        # =================================================

        st.download_button(
            label="⬇️ Download QR Code",
            data=qr_bytes,
            file_name=f"{certificate_id}.png",
            mime="image/png",
            use_container_width=True
        )

        st.info(
            "Place this QR code on the internship certificate. "
            "Scanning the QR code will open the online verification page."
        )
