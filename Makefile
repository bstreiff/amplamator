FONTFORGE=fontforge

OBJDIR=obj
OBJS=\
	AmplamatorMedium.otf \
	AmplamatorBold.otf \
	AmplamatorTimerMedium.otf \

all: $(OBJS)

$(OBJS): | $(OBJDIR)

$(OBJDIR):
	mkdir -p $(OBJDIR)

clean:
	rm -rf $(OBJDIR)/

$(OBJDIR)/%.ff: svg/%.svg
	tools/split_svg.py -s $< -o $(OBJDIR) -f $@

%.otf: $(OBJDIR)/%.ff
	fontforge $< $@
