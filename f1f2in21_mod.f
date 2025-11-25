      MODULE F1F2IN21_MOD
C======================================================================
C  Simple wrapper around F1F2IN21_v1.0.f for SIMC
C  - Holds a runtime-selectable model ID (integer)
C  - Provides GET_F1F2(Z,A,Q2,W2,F1,F2)
C  - Uses F1F2IN21 for model ID 21 (Christy/Bosted)
C======================================================================
      IMPLICIT NONE

C-- Default model ID for F1F2IN21
      INTEGER*4 F1F2_MODEL_ID_DEFAULT
      PARAMETER (F1F2_MODEL_ID_DEFAULT = 21)

C-- Current model in use (set from dbase.f)
      INTEGER*4 F1F2_MODEL_CURRENT

C-- Explicit interface to F1F2IN21 from F1F2IN21_v1.0.f
      INTERFACE
         SUBROUTINE F1F2IN21(Z, A, QSQ, WSQ, F1, F2)
         IMPLICIT NONE
         REAL*8 Z, A, QSQ, WSQ, F1, F2
         END SUBROUTINE F1F2IN21
      END INTERFACE

      CONTAINS

C======================================================================
C  SET_F1F2_MODEL(ID)
C  - If ID = 0 → use default (21)
C  - Otherwise use whatever ID is passed
C======================================================================
      SUBROUTINE SET_F1F2_MODEL(ID)
      IMPLICIT NONE
      INTEGER*4 ID

         IF (ID .EQ. 0) THEN
            F1F2_MODEL_CURRENT = F1F2_MODEL_ID_DEFAULT
         ELSE
            F1F2_MODEL_CURRENT = ID
         ENDIF

      END SUBROUTINE SET_F1F2_MODEL

C======================================================================
C  INIT_F1F2_MODEL
C  - One-time initialization to default model
C======================================================================
      SUBROUTINE INIT_F1F2_MODEL
      IMPLICIT NONE

         F1F2_MODEL_CURRENT = F1F2_MODEL_ID_DEFAULT

      END SUBROUTINE INIT_F1F2_MODEL

C======================================================================
C  GET_F1F2(Z,A,Q2,W2,F1,F2)
C  - Generic accessor used by the physics code
C  - For now, only model 21 is implemented and both
C    DEFAULT and unknown IDs fall back to F1F2IN21.
C======================================================================
      SUBROUTINE GET_F1F2(Z, A, QSQ, WSQ, F1, F2)
      IMPLICIT NONE
      REAL*8 Z, A, QSQ, WSQ, F1, F2

C        If nobody initialized, use default
         IF (F1F2_MODEL_CURRENT .EQ. 0) THEN
            F1F2_MODEL_CURRENT = F1F2_MODEL_ID_DEFAULT
         ENDIF

         SELECT CASE (F1F2_MODEL_CURRENT)

         CASE (21)
C           Christy/Bosted inclusive A(e,e')X
            CALL F1F2IN21(Z, A, QSQ, WSQ, F1, F2)

         CASE DEFAULT
C           Fallback: still call F1F2IN21 but you can add
C           warning/diagnostic here if you want.
            CALL F1F2IN21(Z, A, QSQ, WSQ, F1, F2)

         END SELECT

      END SUBROUTINE GET_F1F2

      END MODULE F1F2IN21_MOD
