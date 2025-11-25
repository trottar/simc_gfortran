      MODULE F1F2IN21_MOD
      IMPLICIT NONE

C--  Runtime-selectable model flag (we will read it from the dbase file)
      INTEGER*4 F1F2_MODEL_ID
      PARAMETER (F1F2_MODEL_ID_DEFAULT = 21)

C--  Keep a separate variable so we can change it at runtime
      INTEGER*4 F1F2_MODEL_CURRENT

C--  Simple interface block so compiler knows the arguments of F1F2IN21
      INTERFACE
         SUBROUTINE F1F2IN21(Z, A, QSQ, WSQ, F1, F2)
         IMPLICIT NONE
         REAL*8 Z, A, QSQ, WSQ, F1, F2
         END SUBROUTINE F1F2IN21
      END INTERFACE

      CONTAINS

C===========================================================
C  Initialize / set the model flag
C===========================================================
      SUBROUTINE SET_F1F2_MODEL(ID)
      IMPLICIT NONE
      INTEGER*4 ID

         IF (ID .EQ. 0) THEN
C           0 means “use default” → F1F2IN21
            F1F2_MODEL_CURRENT = F1F2_MODEL_ID_DEFAULT
         ELSE
            F1F2_MODEL_CURRENT = ID
         ENDIF

      END SUBROUTINE SET_F1F2_MODEL

C===========================================================
C  Generic accessor: get F1,F2 given Z,A,Q2,W2
C  For now, we only support Christy/Bosted F1F2IN21,
C  but the SELECT CASE lets us plug more in later.
C===========================================================
      SUBROUTINE GET_F1F2(Z, A, QSQ, WSQ, F1, F2)
      IMPLICIT NONE
      REAL*8 Z, A, QSQ, WSQ, F1, F2

         IF (F1F2_MODEL_CURRENT .EQ. 0) THEN
            F1F2_MODEL_CURRENT = F1F2_MODEL_ID_DEFAULT
         ENDIF

         SELECT CASE (F1F2_MODEL_CURRENT)
         CASE (21)
C           Christy/Bosted inclusive A(e,e')X
            CALL F1F2IN21(Z, A, QSQ, WSQ, F1, F2)

         CASE DEFAULT
C           Fallback: still call F1F2IN21, but print a warning once if needed
            CALL F1F2IN21(Z, A, QSQ, WSQ, F1, F2)
         END SELECT

      END SUBROUTINE GET_F1F2

C===========================================================
C  Simple one-time initialization entry point
C===========================================================
      SUBROUTINE INIT_F1F2_MODEL
      IMPLICIT NONE

         F1F2_MODEL_CURRENT = F1F2_MODEL_ID_DEFAULT

      END SUBROUTINE INIT_F1F2_MODEL

      END MODULE F1F2IN21_MOD
