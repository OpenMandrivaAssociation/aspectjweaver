%{?_javapackages_macros:%_javapackages_macros}
Name:       aspectjweaver 
Version:    1.6.12
Release:    8.0%{?dist}
Summary:    Java byte-code weaving library

License:    EPL
URL:        http://eclipse.org/aspectj/

# wget -nd http://www.eclipse.org/downloads/download.php?file=/tools/aspectj/aspectj-1.6.12-src.jar
# jar xf aspectj-1.6.12-src.jar aspectjweaver1.6.12-src.jar
Source0:    aspectjweaver1.6.12-src.jar
# This build.xml file was adapted from the Ubuntu package. The src jar has no build scripts.
Source1:    aspectjweaver-build.xml
Source2:    http://repo1.maven.org/maven2/org/aspectj/aspectjweaver/1.6.12/aspectjweaver-1.6.12.pom
Patch0:     aspectjweaver-build-fixes.patch

BuildRequires:   java-devel
BuildRequires:   jpackage-utils
BuildRequires:   ant
BuildRequires:   objectweb-asm
BuildRequires:   apache-commons-logging
Requires:        java
Requires:        objectweb-asm
BuildArch:       noarch

%description
The AspectJ Weaver supports byte-code weaving for aspect-oriented
programming (AOP) in java.

%package javadoc
Summary:        Javadoc for %{name}

Requires:       jpackage-utils

%description javadoc
API documentation for %{summary}.


%prep
%setup -q -c
%patch0 -p1
cp %{SOURCE1} build.xml
# JRockit is not open source, so we cannot build against it
rm org/aspectj/weaver/loadtime/JRockitAgent.java

%build
%if 0%{?fedora}
LANG=en_US.ISO8859-1 CLASSPATH=$( build-classpath objectweb-asm/asm commons-logging ) ant
%else
LC_ALL=en_US CLASSPATH=$( build-classpath objectweb-asm/asm commons-logging ) ant
%endif
ant javadoc

%install
install -d -m 0755 ${RPM_BUILD_ROOT}/%{_javadir}
install -m 0644 build/%{name}.jar ${RPM_BUILD_ROOT}/%{_javadir}/%{name}.jar

install -d -m 0755 ${RPM_BUILD_ROOT}/%{_mavenpomdir}
install -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}/%{_mavenpomdir}/JPP-%{name}.pom

install -d -m 0755 ${RPM_BUILD_ROOT}/%{_javadocdir}
cp -rp javadoc ${RPM_BUILD_ROOT}/%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "org.aspectj:aspectjrt"

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%{_javadocdir}/*

%changelog
* Tue Oct 15 2013 Michal Srb <msrb@redhat.com> - 1.6.12-8
- Add alias org.aspectj:aspectjr

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Andy Grimm <agrimm@gmail.com> 1.6.12-4
- Add better comments, reference POM source URL

* Wed Feb 15 2012 Andy Grimm <agrimm@gmail.com> 1.6.12-3
- add commons-logging buildreq

* Tue Feb 14 2012 Andy Grimm <agrimm@gmail.com> 1.6.12-2
- Add javadoc
- Fix description

* Tue Dec 20 2011 Andy Grimm <agrimm@gmail.com> 1.6.12-1
- Initial Package
