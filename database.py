import mysql.connector as db_connect
import traceback
import os

LIBRARY_VERSION = 64
INCLUDE_INCORRECT = False


class DB:
    def __init__(self, ltb_problems=False):

        # Let this fail if not present
        import db_cred

        # Set the DB connection details
        self.db_conn_details = db_cred.db_connection_details

        self.ltb_problems = ltb_problems
        self.include_incorrect = INCLUDE_INCORRECT

    def _fetch(self, query):
        try:
            conn = db_connect.connect(**self.db_conn_details)
            curs = conn.cursor()

            curs.execute(query)
            res = curs.fetchall()
            return res

        except Exception as err:
            print(err)
            print(traceback.format_exc())
        finally:
            if curs:
                curs.close()
            if conn:
                conn.close()

    def _base_query_solved_problemrun(self, select, exp_id, upper_time_bound, problem_set=None):
        sql_query = """
            {0}
            FROM ProblemRun PR
            """.format(
            select
        )

        # Join on appopriate tables to be able get status information
        sql_query += """
            JOIN ProblemVersion PV ON PV.ProblemVersionID = PR.Problem
            JOIN SZSStatus SL ON PV.Status = SL.SZSStatusID
            JOIN SZSStatus SR ON PR.Status = SR.SZSStatusID
            """

        # Join name information - TODO cannot make this work...
        sql_query += """
                     JOIN Problem P ON P.ProblemID = PV.Problem
                     """

        sql_query += """
                WHERE PR.Experiment={0}
                """.format(
            exp_id
        )

        if problem_set is not None:  # TODO can really only do this if Library ID is provided..
            sql_query += """
                         AND PR.Problem in
                         (
                            SELECT ProblemVersionID
                            FROM Problem P
                            INNER JOIN ProblemVersion PV ON P.ProblemID = PV.Problem
                            WHERE ProblemName IN ({0}) and PV.Version={1}
                         )
                        """.format(
                '"' + '", "'.join(problem_set) + '"', LIBRARY_VERSION
            )

        # Apply upper time bound if set
        if upper_time_bound is not None:
            sql_query += """
                    AND PR.Runtime <= {0}
                    """.format(
                upper_time_bound
            )

        if self.ltb_problems:
            sql_query += """
                 AND (PR.SZS_Status = 'Theorem'
                 OR PR.SZS_Status = 'Unsatisfiable')
                         """
        else:
            sql_query += """
                 AND SR.Solved = 1
                         """

        # Remove the incorrects by only including the correct
        if not self.include_incorrect:
            sql_query += """
                AND ((SL.Unsat AND SR.Sat)
                    OR (SL.Sat AND SR.Unsat)) = 0"""

        # Execute
        sql_query += ";"

        return self._fetch(sql_query)

    def get_solved_problem_name_time(self, exp_id, upper_time_bound=None, problem_set=None):

        select = "SELECT ProblemName, PR.Runtime"
        res = self._base_query_solved_problemrun(select, exp_id, upper_time_bound, problem_set)
        return res


def main():
    db = DB()
    r = db._fetch("SELECT * FROM Collection")
    print(r)
    r = db.get_solved_problem_name_time(117213)
    print(r)


if __name__ == "__main__":
    main()
