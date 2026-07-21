from speech.parser import parse_attendance_command



tests = [

    "Kims 2300100666 present",

    "John 2300100667 absent",

    "finish attendance",

    "start attendance"

]


for text in tests:


    print(
        text
    )


    print(
        parse_attendance_command(text)
    )

    print("----------------")