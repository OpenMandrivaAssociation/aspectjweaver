%{?_javapackages_macros:%_javapackages_macros}
Name:          aspectjweaver 
Version:       1.8.4
Release:       1.2
Summary:       Java byte-code weaving library
Group:		Development/Java
License:       EPL
URL:           http://eclipse.org/aspectj/
Source0:       http://repo1.maven.org/maven2/org/aspectj/%{name}/%{version}/%{name}-%{version}-sources.jar
# This build.xml file was adapted from the Ubuntu package. The src jar has no build scripts.
Source1:       aspectjweaver-build.xml
Source2:       http://repo1.maven.org/maven2/org/aspectj/%{name}/%{version}/%{name}-%{version}.pom
Source3:       epl-v10.txt

BuildRequires: ant
BuildRequires: apache-commons-logging
BuildRequires: javapackages-local
BuildRequires: objectweb-asm
#Requires:      objectweb-asm
BuildArch:     noarch

%description
The AspectJ Weaver supports byte-code weaving for aspect-oriented
programming (AOP) in java.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{summary}.

%prep
%setup -q -c
sed -i.objectweb-asm "s|import aj.|import |" \
 org/aspectj/weaver/bcel/asm/StackMapAdder.java

cp %{SOURCE1} build.xml

# JRockit is not open source, so we cannot build against it
rm org/aspectj/weaver/loadtime/JRockitAgent.java

cp %{SOURCE2} pom.xml
%pom_xpath_inject "pom:project" "
  <dependencies>
    <dependency>
      <groupId>org.ow2.asm</groupId>
      <artifactId>asm</artifactId>
      <version>5.0.3</version>
    </dependency>
  </dependencies>"

cp %{SOURCE3} .
  
%build
export LC_ALL=en_US.ISO8859-1

%mvn_file org.aspectj:%{name} %{name}
%mvn_alias org.aspectj:%{name} "org.aspectj:aspectjrt" "aspectj:aspectjrt"
LANG=en_US.ISO8859-1 CLASSPATH=$( build-classpath objectweb-asm/asm commons-logging ) ant
LANG=en_US.ISO8859-1 CLASSPATH=$( build-classpath objectweb-asm/asm commons-logging ) ant javadoc
%mvn_artifact pom.xml build/%{name}.jar

%install
%mvn_install -J javadoc

%files -f .mfiles
%doc epl-v10.txt

%files javadoc -f .mfiles-javadoc
%doc epl-v10.txt

%changelog
* Tue Dec 09 2014 gil cattaneo <puntogil@libero.it> 1.8.4-1
- update to 1.8.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.6.12-11
- Use Requires: java-headless rebuild (#1067528)

* Mon Mar 24 2014 Michal Srb <msrb@redhat.com> - 1.6.12-10
- Add alias aspectj:aspectjrt

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 1.6.12-9
- use objectweb-asm3

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

