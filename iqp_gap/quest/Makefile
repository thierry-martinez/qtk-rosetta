DEPS_DIR = $(shell pwd)/../../deps
DEPS_BUILD_DIR = $(DEPS_DIR)/_build
CHECK_DIR = $(DEPS_BUILD_DIR)/check
CHECK_LIBS = $(CHECK_DIR)/src/.libs
QUEST_DIR = $(DEPS_DIR)/QuEST/QuEST
QUEST_BUILD_DIR = $(DEPS_BUILD_DIR)/QuEST/QuEST

INCLUDE_DIRS = $(CHECK_DIR)/src $(CHECK_DIR) $(QUEST_DIR)/include $(QUEST_DIR)/src
CFLAGS = $(addprefix -I, $(INCLUDE_DIRS))
LDFLAGS = -Wl,-rpath,$(QUEST_BUILD_DIR):$(CHECK_LIBS)
LDLIBS = -L $(CHECK_LIBS) -L $(QUEST_BUILD_DIR) -lcheck -lQuEST -lgomp -lpthread -lm

TARGET_BIN = check_iqp_gap
OBJS = gap.o iqp_gap.o check_iqp_gap.o

.PHONY: all
all: check

.PHONY: check
check: $(TARGET_BIN)
	./$(TARGET_BIN)

$(TARGET_BIN): $(OBJS)

.PHONY: clean
clean:
	rm -f $(TARGET_BIN)
	rm -f $(OBJS)
