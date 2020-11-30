(deftemplate cell
(slot x)
(slot y)
(slot num) ;klo terdefinisi dia mine
(slot info) ;klo udh pernah didatengin otomatis tau oasti infonya
(slot know) ;klo ketauan bom dia 'bom'
(slot counted)
)

(deftemplate mine
    (slot x)
    (slot y)
)


(deftemplate tocheck
    (slot x)
    (slot y)
)

(deftemplate board
    (multislot cells)
    (slot n)
)

(deftemplate player
    (slot x)
    (slot y)
)

(deftemplate add
    (slot x)
    (slot y)
    (slot v)
)

(defglobal
    ?*countm* = 0
    ?*countu* = 0
    ?*countt* = 0
)

(deffacts global
    (countt 0)
    (countm 0)
    (countu 0)
)

; (deffacts
;     (state read)
; )

(defrule reading-input
    =>
    (assert (player (x 0) (y 0)))
    (printout t "n : ")
    (bind ?N (read))
    ; (assert (N(?N)))
    (assert (N ?N))
    (loop-for-count(?i 0 (- ?N 1))
        (loop-for-count (?j 0 (- ?N 1))
            (assert (cell (x ?i) (y ?j) (num 0) (info u) (counted non)))
        ))
    (printout t "mines : ")
    (assert (mineN (read)))
)

(defrule more-input
    (mineN ?mN)
    =>
    (loop-for-count (?i 0 (- ?mN 1))
        (printout t "x" ?i " : ")
        (bind ?x (read))
        (printout t "y" ?i " : ")
        (bind ?y (read))
        (assert (mine (x ?x) (y ?y))))
)

(defrule mined
    (declare (salience 300))
    ?m <- (mine (x ?x) (y ?y))
    ?c <- (cell (x ?x) (y ?y))
    =>
    (modify ?c (num 10))
    (retract ?m)
)

(defrule countValue
    (declare (salience 2))
    ?c <- (cell (x ?x1) (y ?y1) (num ?num) (counted non))
    ?v <- (cell (x ?x2) (y ?y2) (num 10))
    (test (<> ?num 10))
    (test
        (and
            (<= ?x2 (+ ?x1 1)) (>= ?x2 (- ?x1 1))
            (<= ?y2 (+ ?y1 1)) (>= ?y2 (- ?y1 1))
            (or (not (eq ?x1 ?x2)) (not (eq ?y1 ?y2)))
        )
    )
    =>
    (assert (add (x ?x1) (y ?y1) (v ?v)))
    (assert (gocheck fal))
)

(defrule addValue
    (declare (salience 1))
    ?c <- (cell (x ?x1) (y ?y1) (num ?num))
    ?a <- (add (x ?x1) (y ?y1) (v ?v))
    =>
    (modify ?c (counted yey) (num (+ ?num 1)))
    (retract ?a)
)   

; (defrule player
;     (declare (salience -999))
; )

(defrule visited 
    (player (x ?x) (y ?y))
    ?c <- (cell (x ?x) (y ?y) (know nil))
    =>
    (modify ?c (know yes))
)


(defrule reveal
    (player (x ?x) (y ?y))
    ?c <- (cell (x ?x) (y ?y) (info u) (num ?num))
    =>
    (modify ?c (info ?num))
)

(defrule chain-reveal
    (cell (x ?x1) (y ?y1) (info 0))
    ?c <- (cell (x ?x2) (y ?y2) (info u) (num ?n))
    (test
        (and
            (<= ?x2 (+ ?x1 1)) (>= ?x2 (- ?x1 1))
            (<= ?y2 (+ ?y1 1)) (>= ?y2 (- ?y1 1))
            (or (not (eq ?x1 ?x2)) (not (eq ?y1 ?y2)))
        )
    )
    ; ?c <- (cell (x ?x2) (y ?y2) (info u) (num ?n))
    =>
    (modify ?c (info ?n))
)

(defrule solveone
    (declare (salience -2))
    ; (test (eq ?*count* 0))
    ; (gocheck (not tru))
    ; (gocheck ?x)
    ; (test (not(eq ?x tru)))
    ?g <- (gocheck fal)
    (cell (x ?x) (y ?y) (info 1))
    ?p <- (player (x ?x2) (y ?y2))
    (test (or (<> ?x ?x2) (<> ?y ?y2)))
    =>
    (printout t ?x ?y " kesini" crlf)
    (modify ?p (x ?x) (y ?y))
    (retract ?g)
    (assert (gocheck tru))
)

(defrule solvetwo
    (declare (salience -3))
    ; (test (eq ?*count* 0))
    ; (gocheck (not tru))
    ; (gocheck ?x)
    ; (test (not(eq ?x tru))) 
    (cell (x ?x) (y ?y) (info 2))
    ?p <- (player (x ?x2) (y ?y2))
    (test (or (<> ?x ?x2) (<> ?y ?y2)))
    =>
    (modify ?p (x ?x) (y ?y))
    (assert (gocheck tru))
)



(defrule checkSurroundingU
    (gocheck tru)
    ?cm <- (countu ?x)
    ?c <- (countt ?x)
    (player (x ?x1) (y ?y1))
    (cell (x ?x1) (y ?y1) (num ?num))
    (cell (x ?x2) (y ?y2) (info ?u))
    (test (eq ?u u))
    (test
        (and
            (<= ?x2 (+ ?x1 1)) (>= ?x2 (- ?x1 1))
            (<= ?y2 (+ ?y1 1)) (>= ?y2 (- ?y1 1))
            (or (not (eq ?x1 ?x2)) (not (eq ?y1 ?y2)))
        )
    )
    =>    
    ; (retract ?cm)
    ; (retract ?c)
    (bind ?*countu* (+ ?*countu* 1))
    ; (assert (countu ?*countu*))
    (bind ?*countt* (+ ?*countt* 1))    
    ; (assert (countt ?*count*))
    (assert (tocheck (x ?x2) (y ?y2)))
    ;trus kalo nemu yang surrounding dan ga diketahui diapain
    (printout t "anjing" ?x1 ?y1 ?x2 ?y2 ?*countt* crlf)
)
(defrule checkSurroundingM
    (gocheck tru)
    ?cm <- (countm ?x)
    ?c <- (countt ?x)
    (player (x ?x1) (y ?y1))
    (cell (x ?x1) (y ?y1) (num ?num))
    (cell (x ?x2) (y ?y2) (info ?u))
    (test (eq ?u 10))
    (test
        (and
            (<= ?x2 (+ ?x1 1)) (>= ?x2 (- ?x1 1))
            (<= ?y2 (+ ?y1 1)) (>= ?y2 (- ?y1 1))
            (or (not (eq ?x1 ?x2)) (not (eq ?y1 ?y2)))
        )
    )
    =>   
    (retract ?cm)
    (retract ?c)
    (bind ?*countm* (+ ?*countm* 1))
    (assert (countm ?*countm*))
    (bind ?*countt* (+ ?*countt* 1))
    (assert (countt ?*countt*))
    (assert (tocheck (x ?x2) (y ?y2)))
    ;trus kalo nemu yang surrounding dan ga diketahui diapain
)

(defrule addt
    (declare (salience -1))
    ?x <- (countt 0)
    ?xu <- (countu 0)
    ?xm <- (countm 0)
    ?g <- (gocheck tru)
    =>
    (retract ?x)
    (retract ?xu)
    (retract ?xm)
    (assert (countt ?*countt*))
    (assert (countu ?*countu*))
    (assert (countm ?*countm*))
    (assert (gocheck true))
)


(defrule checkfail
    ; (declare (salience -6))
    (gocheck true)
    ?ct <- (countt ?x)
    (test (<> ?*countt* 0))
    (player (x ?x1) (y ?y1))
    (cell (x ?x1) (y ?y1) (num ?n))
    (test (> ?n (+ ?*countm* ?*countu*)))
    ?h <- (tocheck (x ?x2) (y ?y2))
    =>
    (printout t ?x1 ?y1 ?x2 ?y2 " cek fail" crlf)
    (retract ?h)
    (bind ?*countt* (- ?*countt* 1))
    (assert (countt (- ?x 1)))
    (retract ?ct)
    ; (retract ?g)
    ; (assert (gocheck fal))
)

(defrule checksuccess
    ; (declare (salience -7))
    (gocheck true)
    ?ct <- (countt ?x)
    (test (<> ?*countt* 0))
    (player (x ?x1) (y ?y1))
    (cell (x ?x1) (y ?y1) (num ?n))
    (test (> ?n ?*countt*))
    ?h <- (tocheck (x ?x2) (y ?y2))
    ?c <- (cell (x ?x2) (y ?y2))
    =>
    (printout t ?x1 ?y1 ?x2 ?y2 " cek suc \n")
    (retract ?h)
    (modify ?c (info 10))
    (bind ?*countt* (- ?*countt* 1))
    (assert (countt (- ?x 1)))
    (retract ?ct)
    ; (retract ?g)
    ; (assert (gocheck fal))
)


(defrule searchagain
    ?g <- (gocheck true)
    ; (test (eq ?*count* 0))
    ?cm <- (countm ?x)
    ?cu <- (countu ?x)
    (countt 0)
    =>
    (printout t "skrg " ?*countt* crlf)
    (bind ?*countu* 0)
    (bind ?*countm* 0)
    (retract ?g)
    (retract ?cm)
    (retract ?cu)
    (assert (countu 0))
    (assert (countm 0))
    (assert (gocheck fal))
)