use dsc3037;

select s.course_title
from user_info
         join student_academic sa on sa.student_id = user_info.student_id
         join student_history sh on sa.student_id = sh.student_id
         join student_mandatory sm on sa.student_id = sm.student_id
         join student_preference sp on sa.student_id = sp.student_id
         join skku_subject s on sa.major = s.major
         join skku_subject s1 on sa.double_major = s1.major
         join skku_subject s2 on sa.triple_major = s2.major
where sa.student_id = 2018312342;

# 무슨 과목 들었는지 확인 할 수 있음
SELECT distinct(course_title)
FROM skku_subject
WHERE major is NULL
  AND course_title IN (SELECT course_title
                       FROM student_history
                                JOIN skku_subject ON student_history.course_id = skku_subject.course_id
                       WHERE student_history.student_id = 2018312342);

# 여기까지가 전공, 거르는 거없이 들은거 뺴줌
SELECT distinct(course_title)
FROM skku_subject
WHERE course_title IN (SELECT course_title
                       FROM student_history
                                JOIN skku_subject ON student_history.course_id = skku_subject.course_id
                                JOIN student_academic ON student_history.student_id = student_academic.student_id

                       WHERE student_history.student_id = 2018312342
                          OR skku_subject.major is NULL
                           AND (
                                         skku_subject.major = student_academic.major
                                     OR skku_subject.major = student_academic.double_major
                                     OR skku_subject.major = student_academic.triple_major
                                 )
                           AND skku_subject.semester = "2024학년도 2학기");

# 무슨 과목 들었는지 확인 할 수 있음
SELECT distinct (course_title)
FROM skku_subject
WHERE course_title IN (SELECT course_title
                       FROM student_history
                                JOIN skku_subject ON student_history.course_id = skku_subject.course_id
                                JOIN student_academic ON student_history.student_id = student_academic.student_id
                       WHERE student_history.student_id = 2020311111
                          OR skku_subject.major is NULL
                           AND (
                                         skku_subject.major = student_academic.major
                                     OR skku_subject.major = student_academic.double_major
                                     OR skku_subject.major = student_academic.triple_major
                                 )
                           AND skku_subject.semester = "2024학년도 2학기")
  AND (
            skku_subject.major = (SELECT major
                                  FROM student_academic
                                  WHERE student_id = 2020311111)
        OR skku_subject.major = (SELECT double_major
                                 FROM student_academic
                                 WHERE student_id = 2020311111)
        OR skku_subject.major is NULL
    );

SELECT *
FROM student_academic
         JOIN student_mandatory ON student_academic.student_id = student_mandatory.student_id
         JOIN student_preference ON student_preference.student_id = student_mandatory.student_id
WHERE student_academic.student_id = 2018312342;



SELECT distinct(course_title)
FROM skku_subject
WHERE course_title IN (SELECT course_title
                       FROM student_history
                                JOIN skku_subject ON student_history.course_id = skku_subject.course_id
                                JOIN student_academic ON student_history.student_id = student_academic.student_id
                       group by student_history.student_id, skku_subject.major, student_academic.major,
                                skku_subject.semester,
                                student_academic.double_major, student_academic.triple_major
                       having student_history.student_id = 2018312342
                           OR skku_subject.major is NULL
                           AND (
                                          skku_subject.major = student_academic.major
                                      OR skku_subject.major = student_academic.double_major
                                      OR skku_subject.major = student_academic.triple_major
                                  )
                           AND skku_subject.semester = "2024학년도 2학기");

SELECT *
FROM skku_subject
WHERE course_title NOT IN (SELECT course_title
                           FROM student_history
                                    JOIN skku_subject ON student_history.course_id = skku_subject.course_id
                                    JOIN student_academic ON student_history.student_id = student_academic.student_id
                           WHERE student_history.student_id = 2018312342
                              OR skku_subject.type_of_field = '교양'
                               AND (
                                             skku_subject.major = student_academic.major
                                         OR skku_subject.major = student_academic.double_major
                                         OR skku_subject.major = student_academic.triple_major
                                     ))
group by skku_subject.major, skku_subject.semester, skku_subject.course_code
having skku_subject.major = (SELECT major
                             FROM student_academic
                             WHERE student_id = 2018312342)
    OR skku_subject.major = (SELECT double_major
                             FROM student_academic
                             WHERE student_id = 2018312342)
    OR skku_subject.major is NULL
    AND skku_subject.semester = "2024학년도 2학기";

SELECT *
FROM skku_subject
WHERE course_title NOT IN (SELECT course_title
                           FROM student_history
                                    JOIN skku_subject ON student_history.course_id = skku_subject.course_id
                                    JOIN student_academic ON student_history.student_id = student_academic.student_id
                           WHERE student_history.student_id = 2018312342
                              OR skku_subject.type_of_field = '교양'
                               AND (
                                             skku_subject.major = student_academic.major
                                         OR skku_subject.major = student_academic.double_major
                                         OR skku_subject.major = student_academic.triple_major
                                     ))
  AND skku_subject.semester = "2024학년도 2학기"
  AND (
            skku_subject.major = (SELECT major
                                  FROM student_academic
                                  WHERE student_id = 2018312342)
        OR skku_subject.major = (SELECT double_major
                                 FROM student_academic
                                 WHERE student_id = 2018312342)
        OR skku_subject.type_of_field = '교양');
