(deftemplate decision
    (slot input)
    (slot priority (type STRING))
    (slot recommendation (type STRING))
)

(defrule high-priority-task
    (decision (input "critical"))
    =>
    (assert (decision (priority "High") (recommendation "Address immediately.")))
    (printout t "Task is HIGH PRIORITY. Address immediately." crlf)
)

(defrule medium-priority-task
    (decision (input "important"))
    =>
    (assert (decision (priority "Medium") (recommendation "Schedule for this week.")))
    (printout t "Task is MEDIUM PRIORITY. Schedule for this week." crlf)
)

(defrule low-priority-task
    (decision (input "optional"))
    =>
    (assert (decision (priority "Low") (recommendation "Defer if needed.")))
    (printout t "Task is LOW PRIORITY. Defer if needed." crlf)
)
