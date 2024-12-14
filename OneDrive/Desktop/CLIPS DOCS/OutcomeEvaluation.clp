;; Define a template for the contribution facts
(deftemplate contribution
   (slot id)
   (slot impact (type INTEGER))
   (slot quality (type INTEGER))
   (slot collaboration (type INTEGER))
)

;; Define global weights for scoring
(defglobal ?*impact-weight* = 0.4)
(defglobal ?*quality-weight* = 0.3)
(defglobal ?*collaboration-weight* = 0.3)

;; Define initial facts
(deffacts contributions
   (contribution (id 1) (impact 80) (quality 70) (collaboration 90))
   (contribution (id 2) (impact 60) (quality 80) (collaboration 70))
   (contribution (id 3) (impact 70) (quality 90) (collaboration 60))
)

;; Rule to calculate scores
(defrule calculate-scores
   ?f <- (contribution (id ?id) (impact ?impact) (quality ?quality) (collaboration ?collaboration))
   =>
   (bind ?score (+ (* ?impact ?*impact-weight*)
                   (* ?quality ?*quality-weight*)
                   (* ?collaboration ?*collaboration-weight*)))
   (printout t "Contributor " ?id " Score: " ?score crlf)
)

;; Rule to recommend top contributors
(defrule recommend-top-contributor
   ?f <- (contribution (id ?id) (impact ?impact) (quality ?quality) (collaboration ?collaboration))
   (test (> (+ (* ?impact ?*impact-weight*)
               (* ?quality ?*quality-weight*)
               (* ?collaboration ?*collaboration-weight*)) 40.0))
   =>
   (printout t "Contributor " ?id " is a top performer!" crlf)
)

;; Reset and run commands
(reset)
(run)
