ASPELL = /usr/local/bin/aspell
ASPELL_FLAGS = 
PREZIP = /usr/local/bin/prezip-bin
DESTDIR = 
dictdir = /usr/local/lib/aspell-0.60
datadir = /usr/local/lib/aspell-0.60

# Generated with Aspell Dicts "proc" script version 0.60.3

lang = ru
version = 0.99f7-1

cwl_files = ru-ye.cwl ru-yo.cwl
data_files = ru.dat ru_affix.dat
doc_files = README Copyright
extra_files = configure info Makefile.pre
multi_files = ru.multi ru-ye.multi ru-yeyo.multi ru-yo.multi
rws_files = ru-ye.rws ru-yo.rws

distdir=aspell6-${lang}-${version}

all: ${rws_files} ${data_files}

install: all
	mkdir -p ${DESTDIR}${dictdir}/
	cp ${rws_files} ${multi_files} ${DESTDIR}${dictdir}/
	cd ${DESTDIR}${dictdir}/ && chmod 644 ${rws_files} ${multi_files}
	mkdir -p ${DESTDIR}${datadir}/
	cp ${data_files} ${DESTDIR}${datadir}/
	cd ${DESTDIR}${datadir}/ && chmod 644 ${data_files}

clean:
	rm -f ${rws_files}

distclean: clean
	rm -f Makefile

maintainer-clean: distclean
	rm -f ${multi_files} configure Makefile.pre

uninstall:
	-cd ${DESTDIR}${dictdir}/ && rm ${rws_files} ${multi_files} ${link_files}
	-cd ${DESTDIR}${datadir}/ && rm ${data_files}

dist: ${cwl_files}
	perl proc
	./configure
	@make dist-nogen

dist-nogen:
	-rm -r ${distdir}.tar.bz2 ${distdir}
	mkdir ${distdir}
	cp -p ${extra_files} ${cwl_files} ${multi_files} ${doc_files} ${data_files} ${distdir}/
	-test -e doc  && mkdir ${distdir}/doc  && chmod 755 ${distdir}/doc  && cp -pr doc/* ${distdir}/doc/
	-test -e misc && mkdir ${distdir}/misc && chmod 755 ${distdir}/misc && cp -pr misc/* ${distdir}/misc/
	tar cf ${distdir}.tar ${distdir}/
	bzip2 -9 ${distdir}.tar
	rm -r ${distdir}/

distcheck:
	tar xfj ${distdir}.tar.bz2
	cd ${distdir} && ./configure && make

rel:
	mv ${distdir}.tar.bz2 ../rel


ru-ye.rws: ru-ye.cwl

ru-yo.rws: ru-yo.cwl


.SUFFIXES: .cwl .rws .wl

.cwl.rws:
	${PREZIP} -d < $< | ${ASPELL} ${ASPELL_FLAGS} --lang=ru create master ./$@

.wl.cwl:
	cat $< | LC_COLLATE=C sort -u | ${PREZIP} -z > $@

.pz:
	${PREZIP} -d < $< > $@

