from django.db import connection


class SQL:
    # this function returns user's info when login_id is given
    def return_userinfo(self, login_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM swe3002.user_info WHERE login_id=%s ", [login_id]
            )
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    # this function stores user's info into the db when survey is done
    def insert_survey(
        self, login_id, credit, course, density, morning, professor, day_list, ratio
    ):
        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT student_id FROM swe3002.user_info WHERE login_id=%s ",
                [login_id],
            )
            student_id = cursor.fetchone()
            time = ""
            for day in day_list:
                time += day
            # If there exists student_id update it. If not, insert it.
            cursor.execute(
                "SELECT * FROM swe3002.student_mandatory WHERE student_id=%s ",
                [student_id],
            )
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE swe3002.student_mandatory SET course=%s, credit=%s, time=%s, five_days_a_week=%s WHERE student_id=%s ",
                    [course, credit, time, density, student_id],
                )
            else:
                cursor.execute(
                    "INSERT INTO swe3002.student_mandatory (student_id, course, credit, time, five_days_a_week) VALUES (%s, %s, %s, %s, %s) ",
                    [student_id, course, credit, time, density],
                )
            cursor.execute(
                "SELECT * FROM swe3002.student_preference WHERE student_id=%s ",
                [student_id],
            )
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE swe3002.student_preference SET instructor=%s, morningclass=%s, courseRatio=%s WHERE student_id=%s ",
                    [professor, morning, ratio, student_id],
                )
            else:
                cursor.execute(
                    "INSERT INTO swe3002.student_preference (student_id, instructor, morningclass, courseRatio) VALUES (%s, %s, %s, %s) ",
                    [student_id, professor, morning, ratio],
                )
            return True

    # this function returns all the courses that student can listen
    # student only can listen courses that match his/her major, double major
    # Students can take only subjects that they have not taken before.
    def subject_available(self, student_id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM skku_subject WHERE course_title NOT IN ( SELECT course_title FROM student_history JOIN skku_subject ON student_history.course_id = skku_subject.course_id JOIN student_academic ON student_history.student_id = student_academic.student_id WHERE student_history.student_id = CAST({student_id} AS UNSIGNED) OR (skku_subject.type_of_field = '교양' AND ( skku_subject.major = student_academic.major OR skku_subject.major = student_academic.double_major OR skku_subject.major = student_academic.triple_major )) ) AND skku_subject.semester = "2024학년도 2학기" AND ( skku_subject.major = (SELECT major FROM student_academic WHERE student_id = CAST({student_id} AS UNSIGNED)) OR skku_subject.major = (SELECT double_major FROM student_academic WHERE student_id = CAST({student_id} AS UNSIGNED)) OR skku_subject.type_of_field = '교양' );"""
            )
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    # This function joins all the information about student
    def student_info_join(self, student_id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT *
                    FROM student_academic
                        JOIN student_mandatory ON student_academic.student_id = student_mandatory.student_id
                        JOIN student_preference ON student_preference.student_id = student_mandatory.student_id
                    WHERE
                        student_academic.student_id ={student_id}"""
            )
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def register_user(
        self,
        login_id,
        login_password,
        student_name,
        student_id,
        major,
        double_major,
        triple_major,
        student_grade,
    ):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO student_academic (student_name, student_id, major, double_major, triple_major, student_grade)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [
                    student_name,
                    student_id,
                    major,
                    double_major,
                    triple_major,
                    student_grade,
                ],
            )
            cursor.execute(
                """
                INSERT INTO user_info (student_id, login_id, login_password)
                VALUES (%s, %s, %s)
                """,
                [student_id, login_id, login_password],
            )
            return True

    def register_subject(self, semester, course_id, student_id):
         with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO student_history (semester, course_id, student_id)
                VALUES (%s, %s, %s)
                """,
                [
                    semester,
                    course_id,
                    student_id,
                ],
            )
            return True
         
    def find_courseid_by_title(self, subject):
        print("in sql", subject)
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT course_id
                FROM skku_subject
                WHERE course_title = (%s)
                LIMIT 1;""",
                [ subject ],
            )
            results = cursor.fetchall()
            if results:
                course_id = results[0][0]  # 첫 번째 튜플의 첫 번째 값
                print("course_id: ", course_id)
                return course_id
            else:
                print("No results found.")
                return -1
        
    def get_history(self, student_id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT course_id
                FROM student_history
                WHERE student_id = {student_id};
                """
            )
            columns = [col[0] for col in cursor.fetchall()]
            return columns
        
    def find_title_by_courseid(self, course_id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT course_title
                FROM skku_subject
                WHERE course_id = {course_id}
                LIMIT 1;"""
            )
            columns = [col[0] for col in cursor.fetchall()]
            return columns[0]
        
    def delete_history(self, student_id, course_id):
        print(student_id, course_id)
        with connection.cursor() as cursor:
            cursor.execute(
                """DELETE FROM student_history
                WHERE course_id = %s
                AND student_id = %s;""",
                [course_id, student_id],
            )

            print("result: ", cursor.rowcount)
            if cursor.rowcount > 0:
                return 1
            else:
                return 0
