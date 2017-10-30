SUBDIRS = countries fonts extensions keymaps skin_default rc_models hw_info weather_icons

dist_pkgdata_DATA = \
	encoding.conf \
	prev.png \
	radio.mvi \
	black.mvi \
	freesat.t1 \
	freesat.t2 \
	iso-639-3.pck \
        keymap.ntr \
EXTRA_DIST = *.xml

if HAVE_TEXTLCD
dist_pkgdata_DATA += skin_text.xml
else
dist_pkgdata_DATA += skin_display.xml
endif

skin_display.xml: $(srcdir)/skin_display_default.xml
	test -f $(srcdir)/skin_display_$(BOXTYPE).xml && cp $(srcdir)/skin_display_$(BOXTYPE).xml skin_display.xml || cp $(srcdir)/skin_display_default.xml skin_display.xml

skin_text.xml: $(srcdir)/skin_text_default.xml
	test -f $(srcdir)/skin_text_$(BOXTYPE).xml && cp $(srcdir)/skin_text_$(BOXTYPE).xml skin_text.xml || cp $(srcdir)/skin_text_$(TEXTSKIN).xml skin_text.xml

iso-639-3.pck: $(srcdir)/iso-639-3.tab
	python $(srcdir)/convert-iso-639-3.py $< $@
