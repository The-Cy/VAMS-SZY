import re



# =====================================================
# PARSE VOICE ATTENDANCE COMMAND
# =====================================================

def parse_attendance_command(text):

    text = text.lower().strip()



    # ----------------------------
    # Finish command
    # ----------------------------

    if (
        "finish attendance" in text
        or "end attendance" in text
        or "close attendance" in text
    ):

        return {
            "action": "finish"
        }



    # ----------------------------
    # Start command
    # ----------------------------

    if "start attendance" in text:

        return {
            "action": "start"
        }





    # ----------------------------
    # Student attendance
    # Example:
    #
    # kims 2300100666 present
    #
    # ----------------------------


    number = re.search(
        r"\d{10}",
        text
    )



    if number:


        student_number = number.group()



        status = "Present"



        if "absent" in text:

            status = "Absent"


        if "late" in text:

            status = "Late"



        name = text.replace(
            student_number,
            ""
        )


        name = (
            name
            .replace("present", "")
            .replace("absent", "")
            .replace("late", "")
            .strip()
        )



        return {

            "action": "attendance",

            "student_number": student_number,

            "name": name,

            "status": status

        }



    return {

        "action": "unknown",

        "text": text

    }