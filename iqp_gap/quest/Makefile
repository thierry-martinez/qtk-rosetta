DEPS_DIR = ../../deps
CHECK_DIR = $(DEPS_DIR)/check
CHECK_LIBS = $(CHECK_DIR)/src/.libs
QUEST_DIR = $(DEPS_DIR)/QuEST/QuEST

INCLUDE_DIRS = $(CHECK_DIR)/src $(CHECK_DIR) $(QUEST_DIR)/include $(QUEST_DIR)/src
CFLAGS = $(addprefix -I, $(INCLUDE_DIRS))
LDLIBS = -L $(CHECK_LIBS) -lcheck -lcheckinternal -lm

QUEST_OBJS = QuEST.o QuEST_validation.o QuEST_common.o QuEST_qasm.o mt19937ar.o CPU/QuEST_cpu.o CPU/QuEST_cpu_local.o

.PHONY: all
all: check

.PHONY: check
check: check_iqp_gap
	LD_LIBRARY_PATH=$(CHECK_LIBS) ./check_iqp_gap

check_iqp_gap: gap.o iqp_gap.o check_iqp_gap.o $(addprefix $(QUEST_DIR)/src/, $(QUEST_OBJS))
