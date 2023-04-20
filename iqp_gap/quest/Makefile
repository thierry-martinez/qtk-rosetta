QUEST_DIR = deps/QuEST/QuEST

CFLAGS = -I deps/check/src -I deps/check -I $(QUEST_DIR)/include -I $(QUEST_DIR)/src
LDLIBS = -L deps/check/src/.libs -lcheck -lcheckinternal -lm

QUEST_OBJS = QuEST.o QuEST_validation.o QuEST_common.o QuEST_qasm.o mt19937ar.o CPU/QuEST_cpu.o CPU/QuEST_cpu_local.o

.PHONY: all
all: check

.PHONY: check
check: check_iqp_gap
	LD_LIBRARY_PATH=deps/check/src/.libs ./check_iqp_gap

check_iqp_gap: gap.o iqp_gap.o check_iqp_gap.o $(addprefix $(QUEST_DIR)/src/, $(QUEST_OBJS))
