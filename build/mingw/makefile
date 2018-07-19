NAME := Notepad2
ROOT := ../..

CXX := g++
CC := gcc

INCLUDE_DIRS :=
SYMBOLS :=
WINLIBS :=

COMPILER_FLAGS :=
CFLAGS :=
CXXFLAGS :=
LDFLAGS :=

SILENCE_WARNINGS := 1
ESCALATE_WARNINGS := 0

INCLUDE_DIRS += $(ROOT)/src
INCLUDE_DIRS += $(ROOT)/scintilla/include
INCLUDE_DIRS += $(ROOT)/scintilla/lexlib
INCLUDE_DIRS += $(ROOT)/scintilla/src

SYMBOLS += MINGW_BUILD
SYMBOLS += STRICT
SYMBOLS += UNICODE _UNICODE WIN32 NDEBUG _WINDOWS
SYMBOLS += _CRT_SECURE_NO_WARNINGS
SYMBOLS += _CRT_SECURE_NO_DEPRECATE _SCL_SECURE_NO_WARNINGS
SYMBOLS += STATIC_BUILD SCI_LEXER BOOKMARK_EDITION USE_D2D
# SYMBOLS += __inline=__inline__
# SYMBOLS += __inline=inline
# SYMBOLS += __inline=

WINLIBS += gdi32 comctl32 comdlg32 imm32 shlwapi msimg32 uuid ole32 oleaut32

COMPILER_FLAGS += $(addprefix -I,$(INCLUDE_DIRS))
COMPILER_FLAGS += $(addprefix -D,$(SYMBOLS))
COMPILER_FLAGS += -imacros mingw_build_macros.h
COMPILER_FLAGS += -Xlinker --subsystem=windows
COMPILER_FLAGS += -msse2 -mthreads
COMPILER_FLAGS += -O3
COMPILER_FLAGS += -Wall -Wextra
ifeq ($(ESCALATE_WARNINGS),0)
else
COMPILER_FLAGS += -Werror
endif
ifeq ($(SILENCE_WARNINGS),0)
COMPILER_FLAGS += -Winline
else
# COMPILER_FLAGS += -pedantic
COMPILER_FLAGS += -finline-functions
COMPILER_FLAGS += -Wno-unused-parameter
COMPILER_FLAGS += -Wno-unused-variable
COMPILER_FLAGS += -Wno-unused-but-set-variable
COMPILER_FLAGS += -Wno-unused-value
COMPILER_FLAGS += -Wno-missing-braces
COMPILER_FLAGS += -Wno-parentheses
COMPILER_FLAGS += -Wno-implicit-fallthrough
COMPILER_FLAGS += -Wno-sign-compare
endif

CFLAGS += $(COMPILER_FLAGS)
CFLAGS += -std=c11
# CFLAGS += -Wno-incompatible-pointer-types

CXXFLAGS += $(COMPILER_FLAGS)
CXXFLAGS += -std=c++11

LDFLAGS += $(addprefix -l,$(WINLIBS))


COMPILE_CXX = $(CXX) -c -o $1 $(filter %.cpp %.cxx %.c,$2) $(CXXFLAGS)
COMPILE_CC = $(CC) -c -o $1 $(filter %.cpp %.cxx %.c,$2) $(CFLAGS)

LINK_CXX = $(CXX) -o $1 $(filter %.o %.a %.dll,$2) $(CXXFLAGS) $(LDFLAGS)
LINK_CC = $(CC) -o $1 $(filter %.o %.a %.dll,$2) $(CFLAGS) $(LDFLAGS)

.PHONY : all
all : $(ROOT)/src/VersionRev.h
all : $(ROOT)/res/Notepad2.exe.manifest
all : $(NAME).exe
$(ROOT)/res/Notepad2.exe.manifest : $(ROOT)/src/VersionRev.h
$(ROOT)/src/VersionRev.h : ; $(MAKE) -C $(ROOT) -f build/mingw/makefile versions

.PHONY : versions
versions : ; @python update_rev.py

SCI_MODS :=
SCI_OBJECTS :=

define sci_mod_target
SCI_$1_DIRPATH := $(ROOT)/scintilla/$1
SCI_$1_SOURCES := $$(wildcard $$(SCI_$1_DIRPATH)/*.$2)
SCI_$1_NAMEXTS := $$(notdir $$(SCI_$1_SOURCES))
SCI_$1_OBJECTS := $$(addprefix $1/,$$(SCI_$1_NAMEXTS:%.$2=%.o))

SCI_MODS += sci_$1
SCI_OBJECTS += $$(SCI_$1_OBJECTS)

sci_mods : sci_$1

.PHONY : sci_$1  sci_$1_folder
sci_$1 : $$(SCI_$1_OBJECTS) ;
sci_$1_folder : ; IF NOT EXIST $(subst /,\,$1) MKDIR $(subst /,\,$1)

$$(SCI_$1_OBJECTS) : $1/%.o : $$(SCI_$1_DIRPATH)/%.$2 | sci_$1_folder
	$$(call COMPILE_CC,$$@,$$^)
endef

.PHONY : sci_mods
sci_mods :
$(eval $(call sci_mod_target,lexers,cxx))
$(eval $(call sci_mod_target,lexlib,cxx))
$(eval $(call sci_mod_target,src,cxx))
$(eval $(call sci_mod_target,win32,cxx))
sci_mods : ; @echo $^


NOTEPAD_SOURCES := $(wildcard $(ROOT)/src/*.c)
NOTEPAD_OBJECTS := $(notdir $(NOTEPAD_SOURCES:%.c=%.o))

$(NAME).exe : Notepad2.rc.o EditPrint_dummy.o
$(NAME).exe : $(NOTEPAD_OBJECTS) $(SCI_OBJECTS)
Notepad2.rc.o : $(ROOT)/src/Notepad2.ansi.rc $(ROOT)/src/resource.h
EditPrint_dummy.o : EditPrint_dummy.c ; $(call COMPILE_CC,$@,$^)

$(NOTEPAD_OBJECTS) : %.o : $(ROOT)/src/%.c ; $(call COMPILE_CC,$@,$^)


%.exe : ; $(call LINK_CXX,$@,$^)
%.o : ; $(call COMPILE_CC,$@,$^)
%.rc.o : ; windres -o $@ -i $(filter %.rc,$^)

.PHONY : clean reset run

shell_delfile = DEL $(subst /,\,$1) 2>NUL
define shell_delfiles
	$(foreach file,$1,$(call shell_delfile,$(file))
)
endef
shell_deldir = @IF EXIST $(subst /,\,$1) RMDIR /S /Q $(subst /,\,$1)
define shell_deldirs
	$(foreach dir,$1,$(call shell_deldir,$(dir))
)
endef

clean :
	$(call shell_delfile,$(NAME).exe)
	$(call shell_delfiles,*.o *.a)
	$(call shell_delfile,$(ROOT)/res/Notepad2.exe.manifest)
	$(call shell_delfile,$(ROOT)/src/VersionRev.h)
	$(call shell_deldirs,lexers lexlib src win32)

reset : | clean ;

run : $(NAME).exe ; @.\$<
