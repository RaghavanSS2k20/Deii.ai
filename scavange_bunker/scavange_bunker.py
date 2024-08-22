from flask import Blueprint, flash, jsonify, render_template, request
from .exceptions import *
from .scrape_ecampus import AttendanceWebScrapper


from .services import map_course_name_with_code, get_last_updated_date

template_page = Blueprint("template_app", __name__, template_folder="templates")

# For static
def get_data():
    
        username = "20pw26"
        pwd = "03mar02"

        try:
            awc = AttendanceWebScrapper(user_name=username, password=pwd)
            try:
                time_table = map_course_name_with_code(awc.fetch_time_table())
            except NoTimeTableDataException as error:
                time_table = None

            try:
                attendance = awc.fetch_attendance()
                last_date_updated = get_last_updated_date(attendance)
            except AttendanceUpdateInProcessException as error:
                attendance = None
            if attendance is not None:
                attendance_data = [value.dict() for value in attendance ]
                if time_table:
                    for i in attendance_data:
                        i["course_name"] = time_table[i['course_code']]
                attendance_dict = {

                    "attendance": attendance_data
                }  # Convert to dictionary
            else:
                attendance_dict = None
            # return render_template(
            #     "output.html",
            #     load=True,
            #     time_table=time_table,
            #     data=attendance,
            #     last_date_updated=last_date_updated,
            # )
            print(attendance)
            return{
                    "msg":"pass",
                    "data": attendance_dict,
                    "time_table": time_table,
                    "last_date_updated": last_date_updated,
                }
            

        except (ScrappingError, InvalidUsernameOrPasswordException) as error:
            return jsonify({
                "error":error
            }),400

    # return jsonify({
    #     "msg":"Falied"
    # }),500

import scavange_bunker.bunker_bot as bk


def send_attendance():
        username = "20pw26"
        pwd = "03mar02"
        try:
            try:
                table, session = bk.return_attendance(username, pwd)
            except:
                table = bk.return_attendance(username, pwd)

            if (
                table != "Invalid password"
                and table != "Try again after some time"
                and table != "Table is being updated"
            ):
                res = bk.data_json(table)

                return jsonify(res)
            else:
                res = {"error": "Invalid details try again"}
                return jsonify(res)

        except:
            response = {"error": "Given input details does not match up!!"}
            return jsonify(response)
