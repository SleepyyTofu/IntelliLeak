import mysql.connector


# Save analysis log
def save_analysis(

    entered_text,
    uploaded_filename,
    findings,
    total_score,
    overall_risk

):

    try:

        db = mysql.connector.connect(

            host="localhost",
            user="root",
            password="",
            database="fyp_leakage_system"

        )

        cursor = db.cursor()

        sql = """
        INSERT INTO analysis_logs
        (
            entered_text,
            uploaded_filename,
            findings,
            total_score,
            overall_risk
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            entered_text,
            uploaded_filename,
            str(findings),
            total_score,
            overall_risk
        )

        cursor.execute(sql, values)

        db.commit()

        cursor.close()
        db.close()

    except Exception as e:

        print("Database Error:", e)