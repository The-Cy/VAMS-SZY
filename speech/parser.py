import re

from rapidfuzz import fuzz



# =====================================================
# NUMBER WORD MAPPING
# =====================================================

NUMBER_WORDS = {

    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"

}





# =====================================================
# CONVERT SPOKEN NUMBERS
#
# Example:
#
# two three zero zero
#
# becomes:
#
# 2 3 0 0
#
# =====================================================

def convert_spoken_numbers(text):


    words = text.split()


    converted = []



    for word in words:


        clean = word.lower().replace(
            "'",
            ""
        )



        if clean in NUMBER_WORDS:


            converted.append(
                NUMBER_WORDS[clean]
            )


        else:


            converted.append(
                word
            )



    return " ".join(converted)







# =====================================================
# JOIN SEPARATED DIGITS
#
# Example:
#
# 2 3 0 0 1 0 0 6 6 6
#
# becomes:
#
# 2300100666
#
# =====================================================

def join_spoken_digits(text):


    words = text.split()


    result = []


    buffer = ""



    for word in words:



        if word.isdigit() and len(word) == 1:


            buffer += word



        else:



            if buffer:


                result.append(
                    buffer
                )


                buffer = ""



            result.append(
                word
            )



    if buffer:


        result.append(
            buffer
        )



    return " ".join(result)







# =====================================================
# VOICE COMMAND CORRECTION
# =====================================================

def correct_command(text):


    commands = [

        "start attendance",

        "finish attendance",

        "end attendance",

        "close attendance"

    ]



    best_command = text

    highest_score = 0



    for command in commands:


        score = fuzz.partial_ratio(

            text,

            command

        )



        if score > highest_score:


            highest_score = score

            best_command = command





    # only correct strong matches

    if highest_score >= 75:


        return best_command



    return text







# =====================================================
# MAIN PARSER
# =====================================================

def parse_attendance_command(text):


    # normalize

    text = text.lower().strip()



    text = text.replace(
        ",",
        ""
    )



    # convert spoken numbers

    text = convert_spoken_numbers(
        text
    )



    # join digits

    text = join_spoken_digits(
        text
    )



    # correct command errors

    text = correct_command(
        text
    )



    print(
        "Normalized:",
        text
    )





    # =================================================
    # FINISH COMMAND
    # =================================================

    if (

        text == "finish attendance"

        or text == "end attendance"

        or text == "close attendance"

    ):


        return {

            "action": "finish"

        }







    # =================================================
    # START COMMAND
    # =================================================

    if text == "start attendance":


        return {

            "action": "start"

        }







    # =================================================
    # STUDENT ATTENDANCE
    #
    # Example:
    #
    # kims 2300100666 present
    #
    # =================================================


    number = re.search(

        r"\d{10}",

        text

    )



    if number:


        student_number = number.group()



        status = "Present"



        if "absent" in text:


            status = "Absent"



        elif "late" in text:


            status = "Late"





        name = text.replace(

            student_number,

            ""

        )



        name = (

            name

            .replace(
                "present",
                ""
            )

            .replace(
                "absent",
                ""
            )

            .replace(
                "late",
                ""
            )

            .strip()

        )



        return {


            "action": "attendance",


            "student_number": student_number,


            "name": name,


            "status": status

        }








    # =================================================
    # UNKNOWN
    # =================================================


    return {


        "action": "unknown",

        "text": text

    }