all: flash

KEYMAP_NAME = "romain_sabathe"
BUILD_DIR = $(abspath $(HOME)/qmk_firmware/keyboards/dz60/keymaps)/$(KEYMAP_NAME)

.python_is_ready: 
	pip3 install --user PyGObject qmk
	qmk setup -y
	touch .python_is_ready

keymap.c: app/render_keymap.py static/layers.json static/template_layout.j2 app/keycode_mapper.py .python_is_ready
	PYTHONPATH=. python $<

build: keymap.c rules.mk
	mkdir -p $(BUILD_DIR)
	cp keymap.c $(BUILD_DIR)
	cp rules.mk $(BUILD_DIR)
	qmk compile -kb dz60 -km $(KEYMAP_NAME)

flash: build
	qmk flash -kb dz60 -km $(KEYMAP_NAME)
